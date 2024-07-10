import pytest
from ProjectAgile import us06
from datetime import datetime

def create_individual(id, birth_date, name="NA", death_date="NA"):
    return {
        "ID": id,
        "Name": name,
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": ["NA"]
    }

def create_family(id, husband_id, wife_id, children_ids, divorced_date="NA"):
    return {
        "ID": id,
        "Husband": husband_id,
        "Wife": wife_id,
        "Children": children_ids,
        "Divorced": divorced_date
    }

def test_1_us06():
    # Test case 1: Divorce before death of both spouses
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe", "10 JUN 1980")
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe", "10 JUN 1990")
    family1 = create_family("F01", "I01", "I02", [], "10 JUN 1970")
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = []

    assert us06(individuals, families) == expected_output

def test_2_us06():
    # Test case 2: Divorce after death of one spouse
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe", "10 JUN 1980")
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe")
    family1 = create_family("F01", "I01", "I02", [], "10 JUN 1985")
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = [
        'Error: US06: Family F01: Divorce can only occur before death of spouses'
    ]

    assert us06(individuals, families) == expected_output

def test_3_us06():
    # Test case 3: Divorce after death of both spouses
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe", "10 JUN 1980")
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe", "10 JUN 1985")
    family1 = create_family("F01", "I01", "I02", [], "10 JUN 1990")
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = [
        'Error: US06: Family F01: Divorce can only occur before death of spouses'
    ]

    assert us06(individuals, families) == expected_output

def test_4_us06():
    # Test case 4: No divorce
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe")
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe")
    family1 = create_family("F01", "I01", "I02", [])
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = []

    assert us06(individuals, families) == expected_output

if __name__ == "__main__":
    pytest.main()
