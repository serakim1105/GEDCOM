from datetime import datetime
import sys
from prettytable import PrettyTable

valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

def print_result(level, tag, is_valid, args):
    print("<-- " + level + "|" + tag + "|" + is_valid + "|" + args)

def calculate_age(birth_date, death_date=None):
    birth_date = datetime.strptime(birth_date, "%d %b %Y")
    if death_date:
        death_date = datetime.strptime(death_date, "%d %b %Y")
        age = death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
    else:
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def parse_gedcom_line(line):
    tokens = line.split()
    if len(tokens) < 3:
        tokens.append("")  # avoid TypeError & Overflow

    level = tokens[0]
    if tokens[1] in valid_tags:
        tag = tokens[1]
        args = ' '.join(tokens[2:])
        is_valid = "T"
        # print_result(level, tag, is_valid, args + "\n")
    elif tokens[2] in valid_tags:
        tag = tokens[2]
        args = ' '.join(tokens[3:])
        is_valid = "T"
        # print_result(level, tag, is_valid, args + "\n")
    else:
        tag = tokens[1]
        args = ' '.join(tokens[2:])
        is_valid = "F"
        # print_result(level, tag, is_valid, args + "\n")
    
    return level, tag, is_valid, args

def parse_gedcom_file(filename):    
    # if len(sys.argv) != 2:
    #     print("Please enter an input file name when running the command")
    #     return
    # filename = sys.argv[1]
    # filename = 'sample.ged'
    file = open(filename, 'r')
    lines = file.readlines()
    
    individuals = []
    families = []
    current_indi = None
    current_fam = None
    date_type = None

    for line in lines:
        line = line.strip()
        # print("--> " + line)#.strip()) #remove return char for easier reading
        
        level, tag, is_valid, args = parse_gedcom_line(line)

        if level == '0':
            if current_indi:
                individuals.append(current_indi)
                current_indi = None
            if current_fam:
                families.append(current_fam)
                current_fam = None

            if tag == "INDI":
                current_indi = {"ID": args, "Name": "NA", "Gender": "NA", "Birthday": "NA", "Death": "NA", "Child": "NA", "Spouse": []}
            elif tag == "FAM":
                current_fam = {"ID": args, "Married": "NA", "Divorced": "NA", "Husband": "NA", "HusbandName": "Unknown", "Wife": "NA", "WifeName": "Unknown", "Children": []}

        if current_indi:
            if tag == "NAME":
                current_indi["Name"] = args
            elif tag == "SEX":
                current_indi["Gender"] = args
            elif tag in ["BIRT", "DEAT"]:
                date_type = tag
            elif tag == "DATE" and date_type:
                if date_type == "BIRT":
                    current_indi["Birthday"] = args
                elif date_type == "DEAT":
                    current_indi["Death"] = args
                date_type = None
            elif tag == "FAMC":
                current_indi["Child"] = args
            elif tag == "FAMS":
                current_indi["Spouse"].append(args)
            elif level == "0":
                indi_id = line.split()[1]
                current_indi["ID"] = indi_id

        if current_fam:
            if tag == "DATE":
                date_type = tag
                current_fam["Married"] = args
            elif tag == "DIV":
                date_type = tag
                current_fam["Divorced"] = args
            elif tag == "HUSB":
                current_fam["Husband"] = args
                for indi in individuals:
                    if indi["ID"] == args:
                        current_fam["HusbandName"] = indi["Name"]
            elif tag == "WIFE":
                current_fam["Wife"] = args
                for indi in individuals:
                    if indi["ID"] == args:
                        current_fam["WifeName"] = indi["Name"]
            elif tag == "CHIL":
                current_fam["Children"].append(args)
            else: 
                if level == "0":
                    tokens = line.split()
                    current_fam["ID"] = tokens[1]

    if current_indi:
        # print(f'{current_indi["ID"]}')
        individuals.append(current_indi)
    if current_fam:
        families.append(current_fam)

    for indi in individuals:
        if not indi["Spouse"]:
            indi["Spouse"] = ["NA"]

    # Print the individuals and families
    
    indi_table = PrettyTable()
    indi_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    
    for indi in individuals:
        alive = indi['Death'] == "NA"
        age = calculate_age(indi["Birthday"], None if alive else indi["Death"]) if indi["Birthday"] != "NA" else "NA"
        indi_table.add_row([indi['ID'], indi['Name'], indi['Gender'], indi['Birthday'], age, alive, indi['Death'], indi['Child'], ','.join(indi['Spouse'])])
    
    
    fam_table = PrettyTable()
    fam_table.field_names = ["ID", "Married", "Divorced", "HusbandID", "HusbandName", "WifeID", "WifeName", "Children"]
    
    for fam in families:
        fam_table.add_row([fam['ID'], fam['Married'], fam['Divorced'], fam['Husband'], fam['HusbandName'], fam['Wife'], fam['WifeName'], ','.join(fam['Children'])])

    print("Individuals:")
    print(indi_table)

    print("\nFamilies:")
    print(fam_table)

    return individuals, families 

def us07(individuals):
    errors = []
    for indi in individuals:
        birth_date_str = indi['Birthday']
        death_date_str = indi['Death']
        
        if birth_date_str == "NA":
            continue
        
        if death_date_str != "NA":
            age_at_death = calculate_age(birth_date_str, death_date_str)
            if age_at_death >= 150:
                errors.append(f"US07: {indi['ID']}: More than 150 years old at death: {age_at_death} years")
        else:
            age = calculate_age(birth_date_str)
            if age >= 150:
                errors.append(f"US07: {indi['ID']}: More than 150 years old and still alive: {age} years")
    return errors

def us16(individuals, families):
    errors = []
    family_last_names = {}

    return errors

def main():
    # To read file from command line
    if len(sys.argv) != 2:
        print("Please enter an input file name when running the command")
        return
    filename = sys.argv[1]

    # Pull out individuals and families list from parse_gedcom_file()
    individuals, families = parse_gedcom_file(filename)
    
    # Check for US07 errors
    errors_us07 = us07(individuals)
    if errors_us07:
        print(f"\nError in US07:")
        for error in errors_us07:
            print(error)
    else:
        print(f"\nNo errors in us07")
    
    # Check for US16 errors
    errors_us16 = us16(individuals, families)
    if errors_us16:
        print(f"\nError in US16:")
        for error in errors_us16:
            print(error)
    else:
        print(f"\nNo errors in US16")



if __name__ == "__main__":
    main()
