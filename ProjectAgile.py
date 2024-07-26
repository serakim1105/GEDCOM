from datetime import date, datetime, timedelta
import sys
from prettytable import PrettyTable
from parseDate import parse_date, safe_parse_date

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
    line_num = 0

    for line in lines:
        line = line.strip()
        line_num += 1
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
                current_indi = {"line": line_num, "ID": args, "Name": "NA", "Gender": "NA", "Birthday": "NA", "Death": "NA", "Child": "NA", "Spouse": []}
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
                current_indi["line"] = line_num
                indi_id = line.split()[1]
                current_indi["ID"] = indi_id

        if current_fam:
            if tag == "DATE":
                if date_type == "MARR":
                    current_fam["Married"] = args
                elif date_type == "DIV":
                    current_fam["Divorced"] = args
            elif tag == "MARR":
                date_type = "MARR"
            elif tag == "DIV":
                date_type = "DIV"
            # if tag == "DATE":
            #     date_type = tag
            #     current_fam["Married"] = args
            # elif tag == "DATE":
            #     date_type = tag
            #     current_fam["Divorced"] = args
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
                    current_fam["line"] = line_num
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

    for fam in families:
        if not fam["Children"]:
            fam["Children"] = ["none"]

    #US41: Accept and use dates without days or without days and months
    for indi in individuals:
        indi['Birthday'] = safe_parse_date(indi['Birthday'])
        indi['Death'] = safe_parse_date(indi['Death'])

    for fam in families:
        fam['Married'] = safe_parse_date(fam['Married'])
        fam['Divorced'] = safe_parse_date(fam['Divorced'])

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

    # print(individuals)
    # print(families)

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
                errors.append(f'Line {fam["line"]} - {fam["ID"]}: {fam["HusbandName"]} married before his birthday.')
            if wife_birthday > fam['Married']:
                errors.append(f'Line {fam["line"]} - {fam["ID"]}: {fam["WifeName"]} married before her birthday.')
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
                anomalies.append(f'Line {fam["line"]} - {fam["ID"]}: {fam["HusbandName"]} married before age of 10.')
            if wdob_plus10 > fam['Married']:
                anomalies.append(f'Line {fam["line"]} - {fam["ID"]}: {fam["WifeName"]} married before age of 10.')
    return anomalies

#US03 - Birth before Death
def us03(individuals):
    errors = []
    for indi in individuals:
        birth_date_str = indi["Birthday"]
        death_date_str = indi["Death"]
        indi_name = indi["Name"] != "NA"
        #birth info
        if birth_date_str != "NA":
            birthDate = datetime.strptime(birth_date_str, "%d %b %Y").toordinal()
        #death info
        if death_date_str != "NA":
            deathDate = datetime.strptime(death_date_str, "%d %b %Y").toordinal()
        if (birthDate > deathDate):
                errors.append(f'Line {indi["line"]} - INDIVIDUAL: US03: {indi["ID"]}:{indi["Name"]}:{indi["Birthday"]}:{indi["Death"]} - Birth date not before death date.')
    return errors

#US05 - Marriage before Death
def us05(individuals, families):
    errors = []
    for fam in families:
        wedding_date_str = fam['Married']
        husbandName = fam['HusbandName']
        wifeName = fam['WifeName']
        #wedding info
        weddingDate = datetime.strptime(wedding_date_str, "%d %b %Y").toordinal()
        line = fam['line']
        for indi in individuals:
            if(husbandName == indi["Name"]):
                husband_death_str = indi['Death']
                if husband_death_str != "NA":
                    #husband death info
                    husbandDeathDate = datetime.strptime(husband_death_str, "%d %b %Y").toordinal()
            if(wifeName == indi["Name"] ):
                wife_death_str = indi['Death']
                if wife_death_str != "NA":
                    # wife death info
                    wifeDeathDate = datetime.strptime(wife_death_str, "%d %b %Y").toordinal()
                    if weddingDate > husbandDeathDate or weddingDate > wifeDeathDate:
                        errors.append(f'Line {line} - US05: Marriage date not listed before either spouse death.')
        return errors

#US06 Divorce can only occur before death of both spouses
def str_to_date(date_str):
        return datetime.strptime(date_str, '%d %b %Y')
def us06(individuals, families):
    familyId =[]
    errors = []
    idDeath ={}
    def countDays(member, divorceDate, famId):
        if member in idDeath:
            diff = str_to_date(idDeath[member]) - str_to_date(divorceDate)
            diff = str(diff).split(' ')[0]
            if int(diff) < 0 :
                if famId not in familyId:
                    familyId.append(famId)
                return True   
        return False
    
    for indi in individuals:
        if indi['Death'] != 'NA':
            idDeath[indi['ID']] = indi['Death']
    # print("US06",familyId)
    for fam in families:
        if fam['Divorced'] != 'NA':
            husbandResult = countDays(fam['Husband'], fam['Divorced'], fam['ID'])
            wifeResult = countDays(fam['Wife'], fam['Divorced'], fam['ID'])
            if husbandResult or wifeResult:
                errors.append(f'Line {fam["line"]} - US06: Family {fam["ID"]}: Divorce can only occur before death of spouses')
    return errors

#US07: Death should be less than 150 years after birth for dead people, 
#and current date should be less than 150 years after birth for all living people
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
                errors.append(f'Line {indi["line"]} - INDIVIDUAL: {indi["ID"]}: More than 150 years old at death: {age_at_death} years')
        else:
            age = calculate_age(birth_date_str)
            if age >= 150:
                errors.append(f'Line {indi["line"]} - INDIVIDUAL: {indi["ID"]}: More than 150 years old and still alive: {age} years')
    return errors

#US08: Birth before marriage of parents: Children should be born after marriage of parents (and not more than 9 months after their divorce)
def us08(individuals, families):
    errors =[]
    
    def is_valid_birth(marriage_date, birth_date, divorce_date=None):
        if birth_date < marriage_date:
            return False
        if divorce_date and birth_date > divorce_date + timedelta(days=274):
                return False
        return True

    for fam in families:
        if fam['Married'] != 'NA':
            marriage_date = str_to_date(fam['Married'])
            divorce_date = str_to_date(fam['Divorced']) if fam['Divorced'] != 'NA' else None
            for child_id in fam['Children']:
                for indi in individuals:
                    if indi['ID'] == child_id:
                        if indi['Birthday'] != 'NA':
                            birth_date = str_to_date(indi['Birthday'])
                            if not is_valid_birth(marriage_date, birth_date, divorce_date):
                                errors.append(f'Line {fam["line"]} - US08: Family {fam["ID"]}: Child {child_id} born before marriage or more than 9 months after divorce.')
    return errors

#Helper function for us09 and us10
def date_to_number(date_str):
    if date_str == 'NA':
        return 999999999999
    date_object = datetime.strptime(date_str, '%d %b %Y')
    timestamp = date_object.timestamp() 
    
    return timestamp   

#US09: Child should be born before death of mother and before 9 months after death of father
def us09(individuals, families):
    errors = []

    def str_to_date(date_str):
        return datetime.strptime(date_str, '%d %b %Y')

    for fam in families:
        husband_id = fam["Husband"]
        wife_id = fam["Wife"]
        children_ids = fam["Children"]
        husband_death = next((indi["Death"] for indi in individuals if indi["ID"] == husband_id), None)
        wife_death = next((indi["Death"] for indi in individuals if indi["ID"] == wife_id), None)

        if husband_death and husband_death != "NA" and husband_death is not None:
            husband_death_new = str_to_date(husband_death)
            # print(husband_death_new)
            husband_death_plus9 = husband_death_new + timedelta(days = 274)
            # print(husband_death_plus9)

            for child_id in children_ids:
                child_birth = next((indi["Birthday"] for indi in individuals if indi["ID"] == child_id), None)
                if child_birth:
                    child_bir = date_to_number(child_birth)
                    if child_bir > husband_death_plus9.timestamp():
                        errors.append(f'Line {fam["line"]} - Family {fam["ID"]}: Child {child_id} born more than 9 months after fathers death.')

        if wife_death:
            for child_id in children_ids:
                child_birth = next((indi["Birthday"] for indi in individuals if indi["ID"] == child_id), None)
                if child_birth:
                    child_bir = date_to_number(child_birth)
                    if child_bir > date_to_number(wife_death):
                        errors.append(f'Line {fam["line"]} - Family {fam["ID"]}: Child {child_id} born after mothers death.')
    return errors

# #Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
def us10(individuals, families):
    errors = []
    for fam in families:
        husband_id = fam["Husband"]
        wife_id = fam["Wife"]
        husband_birth = next((indi["Birthday"] for indi in individuals if indi["ID"] == husband_id), None)
        wife_birth = next((indi["Birthday"] for indi in individuals if indi["ID"] == wife_id), None)
        married_date = fam["Married"]

        def str_to_date(date_str):
            return datetime.strptime(date_str, '%d %b %Y')
        
        husb_dob = str_to_date(husband_birth)
        wife_dob = str_to_date(wife_birth)
        married = str_to_date(married_date)

        if husb_dob and married and married < husb_dob + timedelta(days=5110):
            errors.append(f'Line {fam["line"]} - Family {fam["ID"]}: {fam["HusbandName"]} married before age 14.')
        if wife_dob and married and married < wife_dob + timedelta(days=5110):
            errors.append(f'Line {fam["line"]} - Family {fam["ID"]}: {fam["WifeName"]} married before age 14.')

    return errors

#Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
def us12(individuals, families):
    too_old_parents = []
    
    for individual in individuals:
        #individual['Birthday'] = datetime.strptime(individual['Birthday'], '%d %b %Y')
        alive = individual['Death'] == "NA"

    for family in families:
        husband_id = family['Husband']
        wife_id = family['Wife']
        children_ids = family['Children']
        
        husband = next((i for i in individuals if i['ID'] == husband_id), None)
        wife = next((i for i in individuals if i['ID'] == wife_id), None)
        
        if husband and wife:

            #age = calculate_age(indi["Birthday"], None if alive else indi["Death"]) if indi["Birthday"] != "NA" else "NA"
            husband_age = calculate_age(husband['Birthday'], None if alive else husband['Death']) if husband['Birthday'] != 'NA' else 'NA'
            wife_age = calculate_age(wife['Birthday'], None if alive else wife["Death"]) if wife["Birthday"] != "NA" else "NA"
            
            for child_id in children_ids:
                child = next((i for i in individuals if i['ID'] == child_id), None)
                if child:
                    child_age = calculate_age(child['Birthday'], None if alive else child["Death"]) if child["Birthday"] != "NA" else "NA"
                    
                    if (wife_age - child_age > 60):
                        too_old_parents.append(f'Line {wife["line"]} - Individual {wife["ID"]}, family {family["ID"]}: {family["WifeName"]}, DOB {wife["Birthday"]} is more than 60 yrs older than her child {child["Name"]}, DOB {child["Birthday"]}')
                    if (husband_age - child_age > 80):
                        too_old_parents.append(f'Line {husband["line"]} -Individual {husband["ID"]}, family {family["ID"]}: {family["HusbandName"]}, DOB {husband["Birthday"]} is more than 80 yrs older than his child {child["Name"]}, DOB {child["Birthday"]}')

    return list(set(too_old_parents))  # Remove duplicates

#US13: Sibling Spacing
# def us13():

#US15: Fewer Than 15 Siblings
# def us15():

#US16: All male members of a family should have the same last name
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
                        errors.append(f'Line {indi["line"]} - Family {fam["ID"]}: Male child ({child_last_name}) has a different last name than the father ({husband_last_name})')
    return errors
    
# US22: All individual IDs should be unique and all family IDs should be unique
def us22(individuals, families):
    errors = []
    uids = [] 
    
    for indi in individuals:
        id = indi['ID']
        if id not in uids:
            uids.append(id)
        else:
            errors.append(f'Line {indi["line"]} - Duplicate individual ID, {id}, for {indi["Name"]}')
    
    for fam in families:
        id = fam['ID']
        marr = fam['Married']
        #print(marr)
        if id not in uids:
            uids.append(id)
        else:
            errors.append(f'Line {fam["line"]} - Duplicate family ID, {id}, with marriage date {marr}')
    return errors

# US23: Check for individuals who have the same name and birth date
def us23(individuals):
    names_birthdays = []
    errors = []
    
    for individual in individuals:
        # format the name and birthday for easy comparison
        formatted_name_birthday = f"{individual['Name']} {individual['Birthday']}"
        id = individual['ID']

        if formatted_name_birthday not in names_birthdays:
            names_birthdays.append(formatted_name_birthday)
        else:
            errors.append((f'Line {individual["line"]} - Individual {id} has the same name and birth date - {formatted_name_birthday} - with at least one other individual in this GEDCOM.'))

    return errors

#US:25 No more than one child with the same name and birth date should appear in a family
def us25(individuals, families):
    names_birthdays = []
    errors = []

    for family in families:
        family_id = family['ID']
        children = family['Children']
        
        for child_id in children:
            child = next((i for i in individuals if i['ID'] == child_id), None)

            # Skip if its not a child
            if not child:
                continue

            formatted_name_birthday = f"{child['Name']} {child['Birthday']}"
            id = child['ID']

            if formatted_name_birthday not in names_birthdays:
                names_birthdays.append(formatted_name_birthday)
            else:
                errors.append((f'Line {child["line"]} - Child with ID {id} in family {family_id} has the same name and birth date - {formatted_name_birthday} - as another child in family {family_id}'))

    return errors

def us27():
    errors = []
    filename = "sera.ged"  
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
        if alive:
            age = calculate_age(indi["Birthday"])
        else: 
            age = -1
            errors.append(f'No age listed for {indi["ID"]}')
        indi_table.add_row([indi['ID'], indi['Name'], indi['Gender'], indi['Birthday'], age, alive, indi['Death'], indi['Child'], ','.join(indi['Spouse'])])
            
    return errors

#US28: Order siblings by age in decreasing order (oldest to youngest)
def us28(individuals, families):
    sibling = []
    print(" ")
    print("US28: Order siblings by age in decreasing order (oldest to youngest)")
    for fam in families:
        childrenFam = fam["ID"]
        for indi in individuals:  
            if(childrenFam == indi["Child"]):
                id = indi['ID']
                birthday = indi['Birthday']
                death_date = indi['Death']
                if(death_date != "NA"):
                    age = calculate_age(birthday, death_date)
                    name = indi["Name"]
                    sibling.append(f'{age}:{name}')
                if(death_date == "NA"):
                    age = calculate_age(birthday)
                    name = indi["Name"]
                    sibling.append(f'{age}:{name}')
    def extractAge(sibling):
        ageStr = sibling.split(':')[0]
        ageInt = int(ageStr)
        return ageInt      
    sibling.sort(key = extractAge,reverse=True)

    return sibling

#US29: List all deceased individuals
def us29(individuals):
    deceased_individuals = []
    for indi in individuals:
        if indi["Death"] != "NA":
            # id = indi["ID"]
            name = indi["Name"].replace("/", "")
            deceased_individuals.append(f'Individual: {indi["ID"]}: {name}')
    return deceased_individuals       

#US30: List all living married individuals
def us30(individuals):
    errors = []
    living_married_individuals = []
    print("\nUS30: All living married individuals:\n")
    for indi in individuals:
        dead = indi["Death"] != "NA" 
        notMarried = indi["Spouse"] == ["NA"]
        married = indi["Spouse"] != ["NA"]
        if not dead and married:
            living_married_individuals.append(f'{indi["ID"]}:{indi["Name"]}\n')
        return living_married_individuals

#US31:List all individuals who are 30 and have never been married
def us31(individuals):
    errors = []
    living_single_individuals = []
    print("\n\nUS31: All living single individuals over the age of 30:")
    for indi in individuals:
        alive = indi['Death'] == "NA" 
        age = calculate_age(indi["Birthday"]) 
        noSpouse = indi['Spouse'] == ["NA"]
        #Living individuals over 30 and have never been married
        if age > 30 and noSpouse:
            living_single_individuals.append(f'{indi["ID"]}:{indi["Name"]}')
        #Living individuals not over 30 or not single
        if age < 30 or not noSpouse or (not alive):
            errors.append(f'Individual {indi["ID"]}: Is not alive or single above 30.')
    if len(living_single_individuals) == 0:
        print("No results")
    return living_single_individuals


# List all multiple births in a GEDCOM file
def us32(families):
    errors = []

    for fam in families:
        if len(fam["Children"]) > 1:
            error_msg = (
                f"Family ID {fam['ID']} has multiple ( {len(fam['Children'])} ) children."
            )
            errors.append(error_msg)

    return errors

#US33:List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
def us33(individuals,families):
    errors = []
    
    def find_individual_by_id(individuals, indi_id):
        for indi in individuals:
            if indi["ID"] == indi_id:
                return indi
        return None

    for family in families:
        husband = find_individual_by_id(individuals, family["Husband"])
        wife = find_individual_by_id(individuals, family["Wife"])
        husband_dead = False
        wife_dead = False

        if husband and wife:
            if husband["Death"] != "NA":

                husband_dead = True

            if wife["Death"] != "NA":
                wife_dead = True
            
            if husband_dead and wife_dead:
                for child_id in family["Children"]:
                    child = find_individual_by_id(individuals, child_id)
                    if child:
                        birth_date = child["Birthday"]
                        age = calculate_age(birth_date)
                        if age < 18:
                            errors.append(f'US33: INDIVIDUAL: Orphaned child: {child["Name"]} (ID: {child["ID"]}), Age: {age}')

    return errors


# List all couples who were married when the older spouse was more than twice as old as the younger spouse
def us34(individuals, families):
    errors = []

    def find_individual_by_id(indi_id):
        for indi in individuals:
            if indi["ID"] == indi_id:
                return indi
        return None

    for fam in families:
        marriage_date = fam.get("Married")
        if not marriage_date:
            continue
        
        husband_id = fam.get("Husband")
        wife_id = fam.get("Wife")

        husband = find_individual_by_id(husband_id)
        wife = find_individual_by_id(wife_id)

        if husband and wife:
            husband_birth_date = husband.get("Birthday")
            wife_birth_date = wife.get("Birthday")

            if husband_birth_date and wife_birth_date:
                husband_age_at_marriage = calculate_age(husband_birth_date, marriage_date)
                wife_age_at_marriage = calculate_age(wife_birth_date, marriage_date)

                older_age = max(husband_age_at_marriage, wife_age_at_marriage)
                younger_age = min(husband_age_at_marriage, wife_age_at_marriage)

                if older_age > 2 * younger_age:
                    error_msg = (
                        f"Family ID {fam['ID']} married on {marriage_date}: "
                        f"Older spouse ({'Husband' if older_age == husband_age_at_marriage else 'Wife'}) "
                        f"was more than twice as old as the younger spouse."
                    )
                    errors.append(error_msg)
    return errors

#US35:List all people in a GEDCOM file who were born in the last 30 days
def us35(individuals):
    listName = []
    today = datetime.now().date()
    for indi in individuals:
        birthday = indi['Birthday']
        if birthday != 'NA':
            birthdate_format = datetime.strptime(birthday, "%d %b %Y").date()
            diff = abs((today - birthdate_format).days)
            if diff <= 30:
                listName.append(f'INDIVIDUAL: US35: ID: {indi["ID"]} Name {indi["Name"]} Birthday {birthday}')
    return listName

#US36:List all people in a GEDCOM file who died in the last 30 days
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
                listName.append(f'US36: INDIVIDUAL: ID: {indi["ID"]} Name {indi["Name"]} Death {deathday}')
    return listName


#US37:List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days
def us37(individuals,families):
    listName=[]
    diedId =[]
    theirFam=[]
    alive = set()
    idName ={}
    diedLast = us36(individuals)
    for val in diedLast:
        id = val.split('ID: ')[1]
        id = id.split(' ')[0]
        diedId.append(id)
    # print(diedId)
    for indi in individuals:
        if indi['Death'] == 'NA':
            alive.add(indi['ID']) 
        idName[indi['ID']] = indi['Name']
    # check if people died in last 30days have spose and descendants and append it to theirFam list
    for person in diedId:
        for family in families:
            curFam =[]
            if family['Husband'] == person:
                curFam.append(family['Husband'])
                if family['Wife'] in alive:
                    curFam.append(family['Wife'])
                else:
                    curFam.append('NA')
                if len(family['Children']) > 0:
                    for child in family['Children']:
                        if child in alive:
                            curFam.append(child)
            elif family['Wife'] == person:
                curFam.append(family['Wife'])
                if family['Husband'] in alive:
                    curFam.append(family['Husband'])
                else:
                    curFam.append('NA')
                if len(family['Children']) > 0:
                    for child in family['Children']:
                        if child in alive:
                            curFam.append(child)
            if curFam not in theirFam and len(curFam) >0 :
                theirFam.append(curFam)

        for val in theirFam:
            indi_id = val[0]
            indi_name = idName.get(indi_id, "NA")
            curFamName =[]
            curFamName.append(f'INDIVIDUAL: {indi_id} Name: {indi_name} died in the last 30 days')
            
            if len(val) > 1:
                curFamName.append(f'Thier family:')
                if val[1] != 'NA':
                    spouse_id = val[1]
                    spouse_name = idName.get(spouse_id, "NA")
                    curFamName.append(f'\tSpouse: {spouse_id} Name: {spouse_name}')
                
                for child_id in val[2:]:
                    child_name = idName.get(child_id, "NA")
                    curFamName.append(f'\tChild: {child_id} Name: {child_name}') 
                if len(curFamName) < 3:
                    curFamName.append('They do not have living spouse or desendants')

            else:
                curFamName.append('They do not have living spouse or desendants')

            listName.append(curFamName)
            # print(curFamName)
            # print(listName)
    return listName

#US38:List all living people in a GEDCOM file whose birthdays occur in the next 30 days
def us38(individuals):
    listName = []
    today = datetime.now().date()
    for indi in individuals:
        birth = indi['Birthday']
        if indi['Death'] == 'NA' and birth != 'NA':
            birthdate = datetime.strptime(birth, "%d %b %Y").date()
            birthday = birthdate.replace(year=today.year)
            if 0 <= (birthday - today).days <= 30:
                # print(birthday-today)
                listName.append(f'US38: INDIVIDUAL: ID: {indi["ID"]} Name {indi["Name"]} Birthday {birth}')
    return listName

#US39: List upcoming anniversaries
def us39(families):
    anniversaries = []
    todayMonth = (datetime.now().date().month) * 31
    todayDay = (datetime.now().date().day) 
    todayYear = (datetime.now().date().year)
    today = abs((todayMonth + todayDay))
    for fam in families:
        weddingDate = fam["Married"]
        if weddingDate != 'NA':
            AnniversaryMonth = (datetime.strptime(weddingDate, "%d %b %Y").date().month) * 31
            AnniversaryDay =  (datetime.strptime(weddingDate, "%d %b %Y").date().day)
            AnniversaryYear =  (datetime.strptime(weddingDate, "%d %b %Y").date().year)
            AnniversaryDate = abs((AnniversaryDay + AnniversaryMonth))
            if (today < AnniversaryDate) :
                anniversaries.append(weddingDate)
            if (todayYear < AnniversaryYear) :
                print("Wedding did not happen yet")
    return anniversaries

def main():
    # To read file from command line
    if len(sys.argv) != 2:
        print("Please enter an input file name when running the command")
        return
    filename = sys.argv[1]

    # Pull out individuals and families list from parse_gedcom_file()
    individuals, families = parse_gedcom_file(filename)
    #print("\n".join(us02(individuals, families)))

    # Function to print out list of errors or anomalies for a user story
    # Parameters: variable storing result of user story function,
    # 'user story number', 'Errors' (default) or 'Anomalies'
    def print_errors(us_result, us_num, errs_or_anoms = 'Errors'):
        if us_result:
            #print(f"\n\x1B[4m{us_num} {errs_or_anoms}\x1B[0m")
            print(f"\n__{us_num} {errs_or_anoms}__")

            for r in us_result:
                #l = get_line()
                print(r)
        else:
            print(f"\n__No {errs_or_anoms} in {us_num}__.")

    def print_list(us_result, us_num, list_description):
        if us_result:
            print(f"\n__{us_num}__")
            print(f"{list_description}:")
            for r in us_result:
                print(r)
        else:
            print(f"\n__{us_num}__")
            print(f"No {list_description}.")

    # The following section validates the data in the GEDCOM file
    # and prints out any discrepancies

    # Check for US02: Birth before marriage
    errors_us02 = us02_err(individuals, families)
    print_errors(errors_us02, 'US02')

    # Check for US02: Birth before marriage
    anomalies_us02 = us02_anom(individuals, families)    
    print_errors(anomalies_us02, 'US02', 'Anomalies')

    #Check for US03: Birth before death
    birthDates = us03(individuals)    
    print_errors(birthDates, 'US03')

    #Check for US05: Marriage Before Either Spouse Death
    errors_us05 = us05(individuals, families)
    print_errors(errors_us05, 'US05')

    # Check for US06: Divorce before death
    errors_us06 = us06(individuals, families)
    print_errors(errors_us06, 'US06')


    # Check for US07: Less then 150 years old
    errors_us07 = us07(individuals)
    print_errors(errors_us07, 'US07')

    # Check for US08: Birth before marriage of parents
    errors_us08 = us08(individuals, families)
    print_errors(errors_us08, 'US08')

    # Check for US09
    errors_us09 = us09(individuals, families)
    print_errors(errors_us09, 'US09')

    # Check for US10
    errors_us10 = us10(individuals, families)
    print_errors(errors_us10, 'US10')

    # # Check for US12: Parents not too old
    too_old = us12(individuals, families)
    print_errors(too_old, 'US12: Parents that are way too old to have kids')

    # Check for US16: Male last names
    errors_us16 = us16(individuals, families)
    print_errors(errors_us16, 'US16')

    # Check for US22: Unique IDs
    errors_us22 = us22(individuals, families)
    print_errors(errors_us22, 'US22')

    # Check for US23: Unique name & birth date
    errors_us23 = us23(individuals)
    print_errors(errors_us23, 'US23')

    # Check for US25: Unique first names in families
    errors_us25 = us25(individuals, families)
    print_errors(errors_us25, 'US25')

    # Check for US27: Include individual ages
    errors_us27 = us27()
    print_errors(errors_us27, 'US27')

    #Check for US28: Order Siblings By Age
    sibling = us28(individuals, families)
    print_list(sibling, 'US28', 'Siblings')

    # Check for US29: List deceased
    deceased = us29(individuals)
    print_list(deceased, 'US29', 'Deceased individuals')

    # Check for US30: List living married
    list_us30 = us30(individuals)
    print_list(list_us30, 'US30', 'All living married individuals')

    # Check for US31: List living single
    list_us31 = us31(individuals)
    print_list(list_us31, 'US31', 'All living single individuals over age 30')

    # Check for US32
    errors_us32 = us32(families)
    print_errors(errors_us32, 'US32')

    # Check for US33: List orphans
    errors_us33 = us33(individuals,families)
    print_list(errors_us33, 'US33', 'Orphans under 18 years old')

    # Check for US34
    errors_us34 = us34(individuals, families)
    print_errors(errors_us34, 'US34')

    # Check for US35: List recent births
    list_us35 = us35(individuals)
    print_list(list_us35, 'US35', 'Indivuduals who were born in the last 30 days')

    # Check for US36: List recent deaths
    list_us36 = us36(individuals)
    print_list(list_us36, 'US36', 'Individuals who died in the last 30 days')
        
    # Check for US37: List recent survivors
    list_us37 = us37(individuals,families)
    #print_list(list_us37, 'US37', 'Living spouses and descendants who died in the last 30 days')
    if list_us37:
        print('\n__US37: List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days__')
        for val in list_us37:
            for output in val:
                print("\n",output)
    else:
        print('\nUS37: No one died in the last 30 days.')

   #Check for US38: List upcoming birthdays
    list_us38 = us38(individuals)
    print_list(list_us38, 'US38', 'Living people whose birthdays occur in the next 30 days')

    #Check for US39: List Upcoming Anniversaries
    weddingDate = us39(families)
    print_list(weddingDate, 'US39', 'Upcoming Anniversaries')


if __name__ == "__main__":
    main()
