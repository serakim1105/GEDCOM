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
                        #name = indi["Name"].replace("/", "")
                        too_old_parents.append(f"Individual {wife['ID']}, family {family['ID']}: {family['WifeName'].replace('/', '')}, DOB {wife['Birthday']} is more than 60 yrs older than her child {child['Name'].replace('/', '')}, DOB {child['Birthday']}")
                        #break  # Stop checking once a parent doesn't meet the criteria
                    if (husband_age - child_age > 80):
                        too_old_parents.append(f"Individual {husband['ID']}, family {family['ID']}: {family['HusbandName'].replace('/', '')}, DOB {husband['Birthday']} is more than 80 yrs older than his child {child['Name'].replace('/', '')}, DOB {child['Birthday']}")

    return list(set(too_old_parents))  # Remove duplicates

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
    
# Test unique IDs
def us22(individuals, families):
    errors = []
    uids = [] 
    
    for indi in individuals:
        id = indi['ID']
        if id not in uids:
            uids.append(id)
        else:
            errors.append(f"Duplicate individual ID, {id}, for {indi['Name']}")
    
    for fam in families:
        id = fam['ID']
        marr = fam['Married']
        print(marr)
        if id not in uids:
            uids.append(id)
        else:
            errors.append(f"Duplicate family ID, {id}, with marriage date {marr}")
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
    sibling1 = []
    sibling2 = []
    sibling3 = []
    sibling4 = []
    sibling5 = []
    print(" ")
    print("US28: Order siblings by age in decreasing order (oldest to youngest)")
    for fam in families:
        childrenFam = fam["ID"]
        for indi in individuals:  
                if(fam["ID"] == indi["Child"]):
                        if '1' in indi["Child"]:
                            birthday = indi['Birthday']
                            age = calculate_age(indi["Birthday"])
                            name = indi["Name"]
                            sibling1.append(f'{age}:{name}')
                            sibling1.sort(reverse = True) 
                        if '2' in indi["Child"]:
                            birthday = indi['Birthday']
                            age = calculate_age(indi["Birthday"])
                            name = indi["Name"]
                            sibling2.append(f'{age}:{name}')
                            sibling2.sort(reverse = True)
                        if '3' in indi["Child"]:
                            birthday = indi['Birthday']
                            age = calculate_age(indi["Birthday"])
                            name = indi["Name"]
                            sibling3.append(f'{age}:{name}')
                            sibling3.sort(reverse = True)      
                        if '4' in indi["Child"]:
                            birthday = indi['Birthday']
                            age = calculate_age(indi["Birthday"])
                            name = indi["Name"]
                            sibling4.append(f'{age}:{name}')
                            sibling4.sort(reverse = True) 
                        if '5' in indi["Child"]:
                            birthday = indi['Birthday']
                            age = calculate_age(indi["Birthday"])
                            name = indi["Name"]
                            sibling5.append(f'{age}:{name}')
                            sibling5.sort(reverse = True) 
    return sibling1,sibling2,sibling3,sibling4,sibling5

#Check for US29: List all deceased individuals
def us29(individuals):
    deceased_individuals = []
    for indi in individuals:
        if indi["Death"] != "NA":
            # id = indi["ID"]
            name = indi["Name"].replace("/", "")
            deceased_individuals.append(f'Individual: {indi["ID"]}: {name}\n')
    return deceased_individuals       

##Check for US30: List all living married individuals
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
        if dead or notMarried:
            errors.append(f'ERROR: INDIVIDUAL: US30: {indi["ID"]}: Not living and married.')  
    print ("\n".join(living_married_individuals)) 
    return errors

#Check for US31: List all individuals who are 30 and have never been married
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
            errors.append(f'ERROR: INDIVIDUAL: US31: {indi["ID"]}: Is not alive or single above 30.')
    if len(living_single_individuals) == 0:
        print("No results")
    print ("\n".join(living_single_individuals))
    return errors

# US33: List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
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
                listName.append(f'INDIVIDUAL: US35: ID: {indi["ID"]} Name {indi["Name"]} Birthday {birthday}')
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
                listName.append(f'INDIVIDUAL: US36: ID: {indi["ID"]} Name {indi["Name"]} Death {deathday}')
    return listName


#US37: List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days
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
    
    for family in families:
        curFam =[]
        if family['Husband'] in diedId:
            curFam.append(family['Husband'])
            if family['Wife'] in alive:
                curFam.append(family['Wife'])
            else:
                curFam.append('NA')
            for child in family['Children']:
                if child in alive:
                    curFam.append(child)
        if family['Wife'] in diedId:
            curFam.append(family['Wife'])
            if family['Husband'] in alive:
                curFam.append(family['Husband'])
            else:
                curFam.append('NA')
            for child in family['Children']:
                if child in alive:
                    curFam.append(child)
        if len(curFam) > 1:
            theirFam.append(curFam)

    for val in theirFam:
        indi_id = val[0]
        indi_name = idName.get(indi_id, "Unknown")

        listName.append(f'INDIVIDUAL: {indi_id} Name: {indi_name} died in the last 30 days')
        if len(val) > 1:
            listName.append(f'Thier family:')
        else:
            listName.append('They do not have living spouse or desendants')

        if len(val) > 1 and val[1] != 'NA':
            spouse_id = val[1]
            spouse_name = idName.get(spouse_id, "Unknown")
            listName.append(f'\tSpouse: {spouse_id} Name: {spouse_name}')

        for child_id in val[2:]:
            child_name = idName.get(child_id, "Unknown")
            listName.append(f'\tChild: {child_id} Name: {child_name}')         
    # print(theirFam)
    return listName

#US38: List all living people in a GEDCOM file whose birthdays occur in the next 30 days
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
                listName.append(f'INDIVIDUAL: US38: ID: {indi["ID"]} Name {indi["Name"]} Birthday {birth}')
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
        # str(weddingDate)
        # print(weddingDate)
        if weddingDate != 'NA':
            AnniversaryMonth = (datetime.strptime(weddingDate, "%d %b %Y").date().month) * 31
            AnniversaryDay =  (datetime.strptime(weddingDate, "%d %b %Y").date().day)
            AnniversaryYear =  (datetime.strptime(weddingDate, "%d %b %Y").date().year)
            AnniversaryDate = abs((AnniversaryDay + AnniversaryMonth))
            if (today < AnniversaryDate) :
                anniversaries.append(weddingDate)
            if (todayYear < AnniversaryYear) :
                print("Wedding did not happen yet")
            if (today > AnniversaryDate) :
                print("AnniversaryDate before today")
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

    # Check for US07 errors
    errors_us07 = us07(individuals)
    if errors_us07:
        print(f"\nErrors in US07:")
        for error in errors_us07:
            print(error)
    else:
        print(f"\nNo errors in us07")

    #Check for US12 errors
    too_old = us12(individuals, families)
    if too_old:
        print(f"\nErrors in US12: List of miracle parents that are way too old to have kids:")
        for parent in too_old:
            print(parent)
    else:
        print(f"\nNone of the parents are too old to have kids in US12")

    # Check for US16 errors
    errors_us16 = us16(individuals, families)
    if errors_us16:
        print(f"\nErrors in US16:")
        for error in errors_us16:
            print(error)
    else:
        print(f"\nNo errors in US16")

    #Check for US22 errors
    errors = us22(individuals, families)
    if errors:
        print(f"\nErrors in US22:")
        for error in errors:
            print(error)
    else:
        print('\nNo Errors in US22')

    # Check for US02 anomalies
    anomalies_us02 = us02_anom(individuals, families)    
    if anomalies_us02:
        print(f"\nAnomalies in US02:")
        for anomaly in anomalies_us02:
            print(anomaly)
    else:
        print(f"\nNo anomalies in US02")

    # Check for US12: Parents are Not Too Old
    too_old = us12(individuals, families)
    if too_old:
        print(f"\nErrors in US12: List of miracle parents that are way too old to have kids:")
        for parent in too_old:
            print(parent)
    else:
        print(f"\nNone of the parents are too old to have kids in US12")

    # Check for US27: Include individual ages
    errors_us27 = us27()
    if errors_us27:
        print(f"\nErrors in US27:")
        for error in errors_us27:
            print(error)
    else:
        print('\nNo Errors in US27')


    #Check for US28: Order Siblings By Age
    sibling1,sibling2,sibling3,sibling4,sibling5 = us28(individuals, families)
    if sibling1:
        print("F01 siblings")
        for value in sibling1:
            print(value)
        print(" ")
    if sibling2:
        print("F02 siblings")
        for value in sibling2:
            print(value)
        print(" ")
    if sibling3:
        print("F03 siblings")
        for value in sibling3:
            print(value)
        print(" ")
    if sibling4:
        print("F04 siblings")
        for value in sibling4:
            print(value)
        print(" ")
    if sibling5:
        print("F05 siblings")
        for value in sibling5:
            print(value)


    #US29: List all deceased individuals
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

    # Check for US33 error
    errors_us33 = us33(individuals,families)
    if errors_us33:
        for error in errors_us33:
            print("\n",error)
    else:
        print("US33: No orphans under 18 years old")

    list_us35 = us35(individuals)
    if list_us35:
        print('\n US35: List of all people in a GEDCOM file who were born in the last 30 days. ')
        for val in list_us35:
            print("\n",val)
    else:
        print('\nUS35: No one was born in the last 30 days.')

    list_us36 = us36(individuals)
    if list_us36:
        print('\nUS36: List of all people in a GEDCOM file who died in the last 30 days')
        for val in list_us36:
            print("\n",val)
    else:
        print('\nUS36: No one died in the last 30 days.')

    list_us37 = us37(individuals,families)
    if list_us37:
        print('\nUS37: List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days')
        for val in list_us37:
            print("\n",val)
    else:
        print('\nUS37: No one died in the last 30 days.')

    list_us38 = us38(individuals)
    if list_us38:
        print('\nUS38: List all living people in a GEDCOM file whose birthdays occur in the next 30 days')
        for val in list_us38:
            print("\n",val)
    else:
        print('\nUS38: No one has birthyday in the next 30 days.')

    #Check for US39: List Upcoming Anniversaries
    print(" ")
    print("US39")
    weddingDate = us39(families)
    if weddingDate:
        for wedding in weddingDate:
            print(wedding)
    else:
        print('No anniversaries/Anniversary date is not after today')

        
if __name__ == "__main__":
    main()
