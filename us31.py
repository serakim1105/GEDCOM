import pytest
from Pro3_2 import parse_gedcom_line, parse_gedcom_file
from datetime import datetime

#list all living single individuals above age 30
def us31(individuals, families):
    living_individuals = []
    living_married_individuals = []
    errors = []
    print("\nAll living single individuals over the age of 30:")

    for indi in individuals:
        alive = indi['Death'] == "NA"
        age = calculate_age(indi["Birthday"], None if alive else indi["Death"]) if indi["Birthday"] != "NA" else "NA"
        if indi[age] > 30:
            living_individuals.append(indi["Name"])
    return living_individuals
