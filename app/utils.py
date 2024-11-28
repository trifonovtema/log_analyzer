def count_lines_buffered(filepath: str, buffer_size: int = 1024 * 1024) -> int:
    with open(filepath, "r", encoding="utf-8") as file:
        buffer = file.read(buffer_size)
        lines = 0
        while buffer:
            lines += buffer.count("\n")
            buffer = file.read(buffer_size)
        return lines
