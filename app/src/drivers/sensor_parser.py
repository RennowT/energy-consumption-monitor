def parse_csv_line(line: str):
    """
    Recebe uma linha CSV no formato: "<timestamp_ms>,<current_mA>"
    Retorna tupla (timestamp: int, current_mA: float) ou None se inválido.
    """
    try:
        parts = line.split(",")
        if len(parts) != 2:
            return None
        timestamp = int(parts[0].strip())
        current_mA = float(parts[1].strip())
        return timestamp, current_mA
    except ValueError:
        return None
