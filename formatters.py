import csv

def to_csv(items, header_fields, data_fields, num_channels):
    # Returns a CSV-formatted string
    # Expects `items` to have a structure as defined by the long_energy api endpoint
    fields = header_fields.copy()
    for field in data_fields:
        for i in range(num_channels):
            fields += ['{field_name}_{index}'.format(field_name=field, index=str(i))]

    buffer = ','.join(fields)
    buffer += '\r\n'

    for row in items:
        for field_name in header_fields + data_fields:
            if field_name in row:
                element = row[field_name]
                if isinstance(element, list):
                    buffer += ','.join(map(str, element))
                else:
                    buffer += str(element)
            buffer += ','
        buffer += '\r\n'
    return buffer
