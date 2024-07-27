from datetime import datetime

# allow for 'NA' date values
def safe_parse_date(date_str):
    if date_str == 'NA':
        return "NA" 
    else:
        parsed_date = parse_date(date_str)
        return parsed_date
    
def parse_date(input_str):
    components = input_str.split()
    
    # initialize default day = 1 and month = JAN 
    # to estimate unknown day and/or month
    day = '1'
    month = 'JAN'
    year = ''
    
    if len(components) == 3:
        day, month, year = components
    elif len(components) == 2:
        month, year = components
    elif len(components) == 1:
        year = components[0]
    else:
        raise ValueError("Invalid date input format")
    
    reconstructed_date_str = f"{day} {month} {year}"
    
    return reconstructed_date_str
