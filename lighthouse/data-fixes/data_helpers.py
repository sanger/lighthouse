def remove_everything_after_first_underscore(string: str):
    substrings_to_skip = [
        '...',
        'Lysis',
        'LYSIS',
        'Accuplex',
        'ACCUPLEX',
        'chris',
        'ACC',
        '_'
    ]
    split_string = string.split('_')[0]
    if any(x in split_string for x in substrings_to_skip):
        return string
    else:
        return split_string
