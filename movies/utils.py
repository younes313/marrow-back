
def number_converter(rate_count_string):
    if rate_count_string[-1] == 'K':
        return float(rate_count_string[:-1]) * 10 ** 3
    if rate_count_string[-1] == 'M':
        return float(rate_count_string[:-1]) * 10 ** 6
    return float(rate_count_string)
