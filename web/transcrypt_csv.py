def parse_csv(csv_string):
    data = []
    row = []
    current_value = ''
    in_quotes = False
    for char in csv_string:
        if char == ',' and not in_quotes:
            row.append(current_value)
            current_value = ''
        elif char == '\n' and not in_quotes:
            if current_value:
                row.append(current_value)
                current_value = ''
            data.append(row)
            row = []
        elif char == '"':
            in_quotes = not in_quotes
        else:
            current_value += char
    if current_value:
        row.append(current_value)
    if row:
        data.append(row)
    return data
