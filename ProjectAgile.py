from datetime import datetime, timedelta
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
            elif tag == "DATE":
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

    print("\nIndividuals:")
    print(indi_table)

    print("\nFamilies:")
    print(fam_table)

    return individuals, families 

# User Story 02 - Check for Error: Birth should occur before marriage
def us02_err(individuals, families):
    def str_to_date(date_str):
        return datetime.strptime(date_str, '%d %b %Y')

    # convert birthdates and married to datestring objects
    individuals_new = [{**i, 'Birthday': str_to_date(i['Birthday'])} for i in individuals]
    familes_new = [{**f, 'Married': str_to_date(f['Married'])} for f in families]

    # find errors
    errors = []
    for fam in familes_new:
        husband_birthday = next((i for i in individuals_new if i['ID'] == fam['Husband']), None)['Birthday']
        wife_birthday = next((i for i in individuals_new if i['ID'] == fam['Wife']), None)['Birthday']
        if husband_birthday and wife_birthday:
            if husband_birthday > fam['Married']:
                errors.append(f"US02: {fam['ID']}: {fam['HusbandName']} married before his birthday.")
            if wife_birthday > fam['Married']:
                errors.append(f"US02: {fam['ID']}: {fam['WifeName']} married before her birthday.")
    return errors

# User Story 02 - Check for Anomoly: Marriage should occur 10 years after birth
def us02_anom(individuals, families):
    def str_to_date(date_str):
        return datetime.strptime(date_str, '%d %b %Y')

    # convert birthdates and married to datestring objects
    individuals_new = [{**i, 'Birthday': str_to_date(i['Birthday'])} for i in individuals]
    familes_new = [{**f, 'Married': str_to_date(f['Married'])} for f in families]

    # find anomalies
    anomalies = []
    for fam in familes_new:
        husband_birthday = next((i for i in individuals_new if i['ID'] == fam['Husband']), None)['Birthday']
        wife_birthday = next((i for i in individuals_new if i['ID'] == fam['Wife']), None)['Birthday']
        if husband_birthday and wife_birthday:
            hdob_plus10 = husband_birthday + timedelta(days = 3650)
            wdob_plus10 = wife_birthday + timedelta(days = 3650)
            #print(f"husband birthday + 10 yrs: {hdob_plus10}")
            if hdob_plus10 > fam['Married']:
                anomalies.append(f"US02: {fam['ID']}: {fam['HusbandName']} married before age of 10.")
            if wdob_plus10 > fam['Married']:
                anomalies.append(f"US02: {fam['ID']}: {fam['WifeName']} married before age of 10.")
    return anomalies

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
                errors.append(f"US07: INDIVIDUAL: {indi['ID']}: More than 150 years old at death: {age_at_death} years")
        else:
            age = calculate_age(birth_date_str)
            if age >= 150:
                errors.append(f"US07: INDIVIDUAL: {indi['ID']}: More than 150 years old and still alive: {age} years")
    return errors

def us16(individuals, families):
    errors = []
    individual_last_names = {indi["ID"]: indi["Name"].split('/')[-2] for indi in individuals}

    for fam in families:
        husband_id = fam["Husband"]
        husband_last_name = individual_last_names[husband_id]
        
        child_id = fam["Children"]
        for child_id in fam["Children"]:
            for indi in individuals:
                if indi["ID"] == child_id and indi["Gender"] == "M":
                    child_last_name = individual_last_names[child_id]
                    if husband_last_name and child_last_name != husband_last_name:
                        errors.append(f'US16: Family {fam["ID"]}: Male child ({child_last_name}) has a different last name than the father ({husband_last_name})')
    return errors
    
# list all deceased individuals
def us29(individuals):
    deceased_individuals = []
    for indi in individuals:
        if indi["Death"] != "NA":
            # id = indi["ID"]
            name = indi["Name"].replace("/", "")
            deceased_individuals.append(f'\tIndividual: {indi["ID"]}: {name}\n')
    return deceased_individuals       


## List all living married individuals
def us30(individuals):
    errors = []
    print("\nAll living married individuals:")
    for indi in individuals:
        dead = indi["Death"] != "NA" 
        notMarried = indi["Spouse"] == ["NA"]
        if dead or notMarried:
            errors.append(f'ERROR: INDIVIDUAL: US30: {indi["ID"]}: Not living and married.')
    return errors

#List all individuals who are 30 and have never been married
def us31(individuals):
    errors = []
    print("\nAll living single individuals over the age of 30:")

    for indi in individuals:
        alive = indi['Death'] == "NA" 
        age = calculate_age(indi["Birthday"]) 
        Spouse = indi['Spouse'] == ["NA"]
        if age < 30 or Spouse or not alive:
            errors.append(f'ERROR: INDIVIDUAL: US31: {indi["ID"]}: Is not alive or married above 30.')
    return errors

#US35: List all people in a GEDCOM file who were born in the last 30 days
def us35(individuals):
    listName = []
    today = datetime.now().date()
    for indi in individuals:
        birthday = indi['Birthday']
        if birthday != 'NA':
            birthdate_format = datetime.strptime(birthday, "%d %b %Y").date()
            diff = abs((today - birthdate_format).days)
            if diff <= 30:
                listName.append(f'ID {indi["ID"]} Name {indi["Name"]} Birthday {birthday}')
    return listName

#US36: List all people in a GEDCOM file who died in the last 30 days
def us36(individuals):
    listName = []
    today = datetime.now().date()
    # print(today)
    for indi in individuals:
        deathday = indi['Death']
        if deathday != 'NA':
            deathdate_format = datetime.strptime(deathday, "%d %b %Y").date()
            diff = abs((today - deathdate_format).days)
            if diff <= 30:
                listName.append(f'ID {indi["ID"]} Name {indi["Name"]} Death {deathday}')
    return listName

def main():
    # To read file from command line
    if len(sys.argv) != 2:
        print("Please enter an input file name when running the command")
        return
    filename = sys.argv[1]

    # Pull out individuals and families list from parse_gedcom_file()
    individuals, families = parse_gedcom_file(filename)
    #print("\n".join(us02(individuals, families)))

    # Check for US07 errors
    errors_us07 = us07(individuals)
    if errors_us07:
        print(f"\nErrors in US07:")
        for error in errors_us07:
            print(error)
    else:
        print(f"\nNo errors in us07")
    
    # Check for US16 errors
    errors_us16 = us16(individuals, families)
    if errors_us16:
        print(f"\nErrors in US16:")
        for error in errors_us16:
            print(error)
    else:
        print(f"\nNo errors in US16")

    # Check for US02 errors
    errors_us02 = us02_err(individuals, families)
    if errors_us02:
        print(f"\nErrors in US02:")
        for error in errors_us02:
            print(error)
    else:
        print(f"\nNo errors in US02")

    # Check for US02 anomalies
    anomalies_us02 = us02_anom(individuals, families)    
    if anomalies_us02:
        print(f"\nAnomalies in US02:")
        for anomaly in anomalies_us02:
            print(anomaly)
    else:
        print(f"\nNo anomalies in US02")

    # US29: List all deceased individuals
    deceased = us29(individuals)
    if deceased:
        print("\nUS29: List of all deceased individuals:\n")
        print("\n".join(us29(individuals)))    
    else:
        print(f"\nUS29: No deceased individuals")

    #Check for US30 errors
    errors_us30 = us30(individuals)
    if errors_us30:
        for error in errors_us30:
            print("\n",error)
    else:
        print('No Error in US30')

    #Check for US31 errors
    errors_us31 = us31(individuals)
    if errors_us31:
        for error in errors_us31:
            print("\n",error)
    else:
        print('No Error in US31')

    list_us35 = us35(individuals)
    if list_us35:
        print('\n US35: List of all people in a GEDCOM file who were born in the last 30 days. ')
        for val in list_us35:
            print("\n",val)
    else:
        print('\n US35: No one was born in the last 30 days.')

    list_us36 = us36(individuals)
    if list_us36:
        print('\n US36: List of all people in a GEDCOM file who died in the last 30 days')
        for val in list_us36:
            print("\n",val)
    else:
        print('US36: No one died in the last 30 days.')
        
if __name__ == "__main__":
    main()
