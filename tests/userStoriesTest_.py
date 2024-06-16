import pytest
from datetime import datetime
from ProjectAgile import us02, us07, us16, us29, parse_gedcom_file
import tests.test_us29 as test_us29

# Helper function to create a mock individual
def create_individual(id, birth_date, death_date="NA"):
    return {
        "ID": id,
        "Name": "Test Name",
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": ["NA"]
    }

def test_1_us07():
    # Test case 1: Individual who is alive and less than 150 years old
    indi1 = create_individual("I01", "1 JAN 1900")
    assert us07([indi1]) == []

def test_2_us07():
    # Test case 2: Individual who is alive and exactly 150 years old
    today = datetime.today()
    today_str = today.strftime("%d %b %Y")
    indi2 = create_individual("I02", today_str)
    assert us07([indi2]) == []

def test_3_us07():
    # Test case 3: Individual who died and was less than 150 years old
    indi3 = create_individual("I03", "1 JAN 1900", "1 JAN 2000")
    assert us07([indi3]) == []

def test_4_us07():
    # Test case 4: Individual who died and was exactly 150 years old
    indi4= create_individual("I04", "2 JAN 1800", "1 JAN 1950")
    assert us07([indi4]) == []

def test_5_us07():
    # Test case 5: Individual with no birth date specified
    indi5= create_individual("I05", "NA")
    assert us07([indi5]) == []

def test_6_us07():
    # Test case 6: Check if expected 2 errors come out of sera.ged as tested from Pro3_2.py
    individuals, _ = parse_gedcom_file("sera.ged")
    errors = us07(individuals)
    print(errors) 
    expected_num_errors = 2
    assert len(errors) == expected_num_errors

def test_7_us16():
    # Test case 7: 
    individuals, families = parse_gedcom_file("sera.ged")
    errors = us16(individuals, families)
    print(errors)
    expected_num_errors = 1
    assert len(errors) == expected_num_errors


if __name__ == "__main__":
    pytest.main()
