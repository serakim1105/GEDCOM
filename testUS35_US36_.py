import pytest
from datetime import datetime, timedelta
from Pro3_2 import us35, us36, parse_gedcom_file

# Helper function to create a mock individual
def create_individual(id, birth_date, death_date="NA"):
    return {
        "ID": id,
        "Name": "Individual Name",
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": ["NA"]
    }

def test_1_us35():
    # Test case 1: Individual with birth date not in the past 30 days
    indi1 = create_individual("I01", "1 JAN 1900")
    assert us35([indi1]) == []

def test_2_us35():
    # Test case 2: Indidvidual with birth date exactly today
    today = datetime.today().strftime("%d %b %Y")
    indi2 = create_individual("I02", today)
    assert us35([indi2]) == [f'ERROR: INDIVIDUAL: US35: I02: Birthday {today}, born in the last 30 days']

def test_3_us35():
    # Test case 3: Indidvidual with birth date in past 30days
    past_date = (datetime.today() - timedelta(days=15)).strftime("%d %b %Y")
    # print(past_date)
    indi3 = create_individual("I03", past_date)
    assert us35([indi3]) == [f'ERROR: INDIVIDUAL: US35: I03: Birthday {past_date}, born in the last 30 days']

def test_4_us36():
    # Test case 4: Indidvidual with death date in past 30days
    past_death_date = (datetime.today() - timedelta(days=10)).strftime("%d %b %Y")
    indi4= create_individual("I04", "2 JAN 2000", past_death_date)
    assert us36([indi4]) == [f'ERROR: INDIVIDUAL: US36: I04: Death {past_death_date}, died in the last 30 days']

def test_5_us36():
    # Test case 5: Individual with no death date specified
    indi5= create_individual("I05", "15 FEB 2015","NA")
    assert us36([indi5]) == []

def test_6_us35():
    # Test case 6: Check if expected 1 error come out of navya.ged from Pro3_2.py for US35
    individuals, _ = parse_gedcom_file("navya.ged")
    errors = us35(individuals)
    print(errors) 
    expected_num_errors = 1
    assert len(errors) == expected_num_errors

def test_7_us36():
    # Test case 7: Check if expected 1 error come out of navya.ged for US36
    individuals, _ = parse_gedcom_file("navya.ged")
    errors = us36(individuals)
    print(errors)
    expected_num_errors = 1
    assert len(errors) == expected_num_errors

if __name__ == "__main__":
    pytest.main()