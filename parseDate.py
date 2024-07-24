from datetime import datetime

# Function to safely parse dates, allowing for 'NA' values
def safe_parse_date(date_str):
    if date_str == 'NA':
        return "NA"  # Or set to a default value if preferred
    else:
        parsed_date, _ = parse_date(date_str)
        return parsed_date
    
def parse_date(input_str):
    # Split the input string into components
    components = input_str.split()
    
    # Initialize defaults
    day = '01'
    month = 'JAN'
    year = None
    
    # Determine the number of components and assign values accordingly
    if len(components) == 3:
        day, month, year = components
    elif len(components) == 2:
        month, year = components
    elif len(components) == 1:
        year = components[0]
    else:
        raise ValueError("Invalid input format")
    
    # Reconstruct the date string
    reconstructed_date_str = f"{day} {month} {year}"
    
    # Optionally convert to datetime object
    try:
        reconstructed_date_obj = datetime.strptime(reconstructed_date_str, "%d %b %Y").date()
    except ValueError as e:
        print(f"Error converting date: {e}")
        return None
    
    return reconstructed_date_str, reconstructed_date_obj

# Example usage
# input_formats = ['10 JAN 2000', 'JAN 2000', '2000']
# for fmt in input_formats:
#     result = parse_date(fmt)
#     if result:
#         print(f"Input: '{fmt}' -> Reconstructed Date: {result[0]}, Date Object: {result[1]}")
