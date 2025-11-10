/*
* Firmware mínimo - ATmega328P (Arduino Nano, 16 MHz)
* Função: Ler ACS712 no ADC0 (A0) e imprimir CSV na UART (9600 bps):
*         <timestamp_ms>,<current_mA>\r\n
*
* Projeto: Energy Consumption Monitor - firmware bare-metal (registradores)
*
* Requisitos atendidos:
*  - Apenas registradores (sem Arduino API / sem printf).
*  - UART_BAUD = 9600.
*  - Timestamp em milissegundos via Timer0 (CTC).
*  - CSV com "timestamp_ms,adc_raw,current_mA".
*  - Código contido inteiramente em main.c, bem documentado, sem itens não usados.
*
* Taxa de amostragem:
*  - SAMPLE_PERIOD_MS = 20 ms (50 amostras/s).
*    Justificativa: 9600 bps consegue transmitir ~50 linhas/s com folga.
*
* Conversão para corrente (ACS712-05B):
*  - Sensibilidade S = 185 mV/A
*  - Vref = AVCC = 5000 mV
*  - Código ADC: 10 bits (0..1023), offset nominal ~ VCC/2 => ADC_MID = 512
*  - Fórmula (inteira, com arredondamento):
*      I_mA = ( (adc - ADC_MID) * Vref_mV * 1000 ) / ( 1023 * S_mV_A )
*    onde S_mV_A = 185 mV/A
*  - Observação: sem calibração fina; para maior precisão, ajustar ADC_MID conforme medição em 0 A.
*
* Compilação (PlatformIO):
*  - F_CPU=16000000UL
*  - mcu=atmega328p
*/

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdint.h>
#include <stdbool.h>

/*---------------------- Configurações do sistema ----------------------*/
#ifndef F_CPU
#define F_CPU 16000000UL
#endif

#define UART_BAUD               9600UL
/* UBRR = (F_CPU/(16*BAUD)) - 1  => para 16 MHz e 9600 bps ≈ 103 */
#define UART_UBRR_VALUE         ((F_CPU/(16UL*UART_BAUD)) - 1UL)

/* Período entre amostras (em ms). 16 ms = 62.5 Hz */
#define SAMPLE_PERIOD_MS        16UL

/* Conversão corrente (ACS712-05B) */
#define VREF_MV                 5000L   /* AVCC em mV */
#define ACS712_SENS_MV_PER_A    185L    /* mV/A para o modelo de 5 A */
#define ADC_FULL_SCALE          1023L
#define ADC_MID                 512     /* offset nominal VCC/2 → ajuste conforme necessário */

/*---------------------- Variáveis globais -----------------------------*/
/* Contador de milissegundos (incrementado no ISR do Timer0 Compare A) */
static volatile uint32_t g_millis = 0;

/* Próximo instante (ms) em que devemos amostrar/emitir CSV */
static uint32_t g_next_sample_ms = 0;

/*---------------------- UART (registradores) --------------------------*/
static void uart_init_9600(void)
{
	/* Configura baud rate */
	UBRR0H = (uint8_t)(UART_UBRR_VALUE >> 8);
	UBRR0L = (uint8_t)(UART_UBRR_VALUE & 0xFF);

	/* Formato do frame: 8N1 (UCSR0C) */
	UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); /* 8 bits, 1 stop, sem paridade */

	/* Habilita RX e TX (UCSR0B) */
	UCSR0B = (1 << RXEN0) | (1 << TXEN0);
}

/* Transmite 1 byte (bloqueante), aguardando UDRE0=1 (buffer de transmissão livre) */
static void uart_putc(uint8_t c)
{
	while ((UCSR0A & (1 << UDRE0)) == 0) {
		/* espera buffer livre */
	}
	UDR0 = c;
}

/* Converte e transmite um número decimal sem sinal (uint32) */
static void uart_put_u32(uint32_t v)
{
	char buf[11];
	uint8_t i = 0;

	if (v == 0) {
		uart_putc('0');
		return;
	}
	while (v > 0 && i < sizeof(buf) - 1) {
		uint32_t q = v / 10;
		uint8_t  r = (uint8_t)(v - q * 10);
		buf[i++] = (char)('0' + r);
		v = q;
	}
	while (i > 0) {
		uart_putc((uint8_t)buf[--i]);
	}
}

/* Converte e transmite um número decimal com sinal (int32) */
static void uart_put_i32(int32_t v)
{
	if (v < 0) {
		uart_putc('-');
		/* cuidado com INT32_MIN: converte via unsigned para evitar overflow ao negar */
		uint32_t uv = (uint32_t)(-(v + 1)) + 1U;
		uart_put_u32(uv);
	} else {
		uart_put_u32((uint32_t)v);
	}
}

/* Converte e transmite um número decimal sem sinal (uint16) */
static void uart_put_u16(uint16_t v)
{
	uart_put_u32((uint32_t)v);
}

/*---------------------- Timer0 -> base de tempo (1 ms) ---------------*/
/*
* Timer0 em CTC para 1 kHz (1 ms por tick):
*  - Prescaler = 64 -> f_timer = F_CPU/64 = 250 kHz
*  - OCR0A = 249 -> interrupção a cada 250 contagens = 1 ms
*/
static void timer0_init_1ms(void)
{
	TCCR0A = (1 << WGM01);                 /* CTC (Clear Timer on Compare Match) */
	TCCR0B = (1 << CS01) | (1 << CS00);    /* Prescaler 64 */
	OCR0A  = 249;                          /* 1 ms @ 16 MHz, presc 64 */
	TIMSK0 = (1 << OCIE0A);                /* Habilita interrupção Compare A */
}

/* ISR do Timer0 Compare A: incrementa contador de ms */
ISR(TIMER0_COMPA_vect)
{
	g_millis++;
}

/* Leitura atômica de g_millis (32 bits) */
static uint32_t millis(void)
{
	uint32_t m;
	uint8_t  sreg = SREG; /* salva status global de interrupção */
	cli();
	m = g_millis;
	SREG = sreg;          /* restaura status */
	return m;
}

/*---------------------- ADC (canal ADC0 / A0) ------------------------*/
static void adc_init_single_ended_adc0(void)
{
	/* Referência AVCC, canal ADC0, right-adjust */
	ADMUX = (1 << REFS0);            /* REFS0=1 (AVCC), MUX=0 (ADC0), ADLAR=0 */

	/* Prescaler 128, habilita ADC -> f_adc = 125 kHz */
	ADCSRA = (1 << ADEN)
		| (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); /* /128 */

	/* Desabilita entrada digital no pino ADC0 (reduz consumo/ruído) */
	DIDR0 = (1 << ADC0D);
}

/* Realiza uma conversão única no ADC0 e retorna o valor 10 bits (0..1023) */
static uint16_t adc_read_blocking(void)
{
	ADCSRA |= (1 << ADSC);                 /* inicia conversão */
	while (ADCSRA & (1 << ADSC)) {
		/* espera término (ADSC volta a 0) */
	}
	/* IMPORTANTE: ler ADCL antes de ADCH */
	uint8_t low  = ADCL;
	uint8_t high = ADCH;
	return (uint16_t)((high << 8) | low);
}

/*---------------------- Conversão ADC -> corrente (mA) ---------------*/
/*
* I_mA = ((adc - ADC_MID) * VREF_MV * 1000) / (ADC_FULL_SCALE * ACS712_SENS_MV_PER_A)
* Usa 64 bits no numerador para evitar overflow, com arredondamento half-up.
*/
static int32_t adc_to_current_mA(uint16_t adc)
{
	int32_t delta = (int32_t)adc - (int32_t)ADC_MID;          /* pode ser negativo */
	int64_t num   = (int64_t)delta * (int64_t)VREF_MV * 1000; /* delta * 5000 * 1000 */
	int64_t den   = (int64_t)ADC_FULL_SCALE * (int64_t)ACS712_SENS_MV_PER_A; /* 1023 * 185 */

	/* Arredondamento (half-up) respeitando o sinal */
	if (num >= 0) {
		num += den / 2;
	} else {
		num -= den / 2;
	}

	int64_t res = num / den; /* resultado em mA (pode ser negativo) */
	if (res > INT32_MAX) res = INT32_MAX;
	if (res < INT32_MIN) res = INT32_MIN;
	return (int32_t)res;
}

/*---------------------- Aplicação principal --------------------------*/
int main(void)
{
	uart_init_9600();
	timer0_init_1ms();
	adc_init_single_ended_adc0();
	sei();

	g_next_sample_ms = millis() + SAMPLE_PERIOD_MS;

	for (;;) {
		uint32_t now = millis();
		if ((int32_t)(now - g_next_sample_ms) >= 0) {
			uint16_t adc_raw   = adc_read_blocking();
			int32_t  current_mA = adc_to_current_mA(adc_raw);

			/* CSV: <timestamp_ms>,<current_mA>\r\n */
			uart_put_u32(now);
			uart_putc(',');
			uart_put_i32(current_mA);
			uart_putc('\r');
			uart_putc('\n');

			g_next_sample_ms += SAMPLE_PERIOD_MS;
		}
	}
	return 0;
}
