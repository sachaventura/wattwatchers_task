import csv

def to_csv(items, header_fields, data_fields, num_channels, delim = ','):
    """Returns a CSV-formatted string
    Expects `items` to be structured as defined by the long_energy api endpoint
    """

    # Create the column headers, duplicating the data fields for each channel
    # e.g. with 3 channels, the field name 'eReal' generates 'eReal_0', 'eReal_1', eReal_2'
    fields = header_fields.copy()
    if num_channels:
        for field in data_fields:
            for i in range(num_channels):
                fields += ['{field_name}_{index}'.format(field_name=field, index=str(i))]
    else:
        fields += data_fields

    buffer = delim.join(fields)
    buffer += '\r\n'

    for row in items:
        # Ensure the values are added under their respective column
        for field_name in header_fields + data_fields:
            if field_name in row:
                element = row[field_name]
                if isinstance(element, list):
                    buffer += delim.join(map(str, element))
                else:
                    buffer += str(element)
            buffer += delim
        # remove trailing delimiter
        buffer = buffer.rstrip(delim)
        buffer += '\r\n'
    return buffer
