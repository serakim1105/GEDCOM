import pytest
from ProjectAgile import us37
from datetime import datetime, timedelta

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

def create_family(id, husband_id, wife_id, children_ids):
    return {
        "ID": id,
        "Husband": husband_id,
        "Wife": wife_id,
        "Children": children_ids
    }
def test_1_us37():
    # Test case 1: Individual died in the last 30 days with living spouse and children
    past_death_date = (datetime.today() - timedelta(days=10)).strftime("%d %b %Y")
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe", past_death_date)
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe")
    indi3 = create_individual("I03", "3 JAN 1900", "Michael Doe")
    family1 = create_family("F01", "I01", "I02", ["I03"])
    individuals = [indi1, indi2, indi3]
    families = [family1]

    expected_output = [[
        'INDIVIDUAL: I01 Name: John Doe died in the last 30 days',
        'Thier family:',
        '\tSpouse: I02 Name: Jane Doe',
        '\tChild: I03 Name: Michael Doe']
    ]

    assert us37(individuals, families) == expected_output

def test_2_us37():
    # Test case 2: Individual died in the last 30 days with no living spouse or children
    past_death_date = (datetime.today() - timedelta(days=5)).strftime("%d %b %Y")
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe", past_death_date)
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe", '10 SEP 1996')
    family1 = create_family("F01", "I01", "I02", [])
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = [[
        'INDIVIDUAL: I01 Name: John Doe died in the last 30 days',
        'Thier family:',
        'They do not have living spouse or desendants']
    ]

    assert us37(individuals, families) == expected_output

def test_3_us37():
    # Test case 3: Individual did not die in the last 30 days
    indi1 = create_individual("I01", "1 JAN 1900", "John Doe")
    indi2 = create_individual("I02", "2 JAN 1900", "Jane Doe")
    family1 = create_family("F01", "I01", "I02", [])
    individuals = [indi1, indi2]
    families = [family1]

    expected_output = []

    assert us37(individuals, families) == expected_output

if __name__ == "__main__":
    pytest.main()