import pytest
from datetime import datetime
from Pro3_2 import us30, us31, parse_gedcom_file

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

def test_1():
    # Test case 1: Individual who is alive and less than 150 years old
    indi1 = create_individual()
    assert us30([indi1]) == []

def test_2():
    # Test case 2: Individual who is alive and exactly 150 years old
    indi2 = create_individual()
    assert us30([indi2]) == []

def test_3():
    # Test case 3: Individual who died and was less than 150 years old
    indi3 = create_individual()
    assert us30([indi3]) == []

def test_4():
    # Test case 4: Individual who died and was exactly 150 years old
    indi4= create_individual()
    assert us30([indi4]) == []

def test_5():
    # Test case 5: Individual with no birth date specified
    indi5= create_individual()
    assert us30([indi5]) == []

if __name__ == "__main__":
    pytest.main()
