import pytest
from datetime import datetime, timedelta
from ProjectAgile import us18, us17

def create_individual(id, name="NA"):
    return {
        "ID": id,
        "Name": name,
        "Gender": "NA",
        "Birthday": "NA",
        "Death": "NA",
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
def test_1_us17():
    # Test case 1: Parent married to a child
    
    family1 = create_family("F1", "I1", "I2", ["I3"])
    family2 = create_family("F2", "I1", "I3", [])

    families = [family1, family2]

    expected_output = ["Error US17: Parent I1 should not marry descendant I3 in family F2."]

    assert us17(families) == expected_output

def test_2_us17():
    # Test case 2: No parent married to a child

    family1 = create_family("F1", "I1", "I2", ["I3"])
    family2 = create_family("F2", "I3", "I4", [])

    families = [family1, family2]

    expected_output = []

    assert us17(families) == expected_output

def test_3_us17():
    # Test case 3: Parent married to a child 
    family1 = create_family("F1", "I1", "I2", ["I3", "I4"])
    family2 = create_family("F2", "I2", "I4", [])

    
    families = [family1, family2]

    expected_output = ["Error US17: Parent I2 should not marry descendant I4 in family F2."]

    assert us17(families) == expected_output

def test_1_us18():
    # Test case 1: Siblings are married
    
    family1 = create_family("F1", "I1", "I2", ["I3", "I4"])
    family2 = create_family("F2", "I3", "I4", [])

    
    families = [family1, family2]

    expected_output = ["Error US18: Siblings I3 and I4 should not marry one another in family F2."]

    assert us18(families) == expected_output

def test_2_us18():
    # Test case 2: No siblings are married
    
    family1 = create_family("F1", "I1", "I2", ["I3", "I4"])
    family2 = create_family("F2", "I3", "I5", [])

    
    families = [family1, family2]

    expected_output = []

    assert us18(families) == expected_output


def test_3_us18():
    # Test case 3: siblings are married
    

    family1 = create_family("F1", "I1", "I2", ["I3", "I4"])
    family2 = create_family("F2", "I3", "I4", [])
    family3 = create_family("F3", "I5", "I6", ["I7", "I8"])
    family4 = create_family("F4", "I7", "I8", [])

    
    families = [family1, family2, family3, family4]

    expected_output = [
        "Error US18: Siblings I3 and I4 should not marry one another in family F2.",
        "Error US18: Siblings I7 and I8 should not marry one another in family F4."
    ]

    assert us18(families) == expected_output

if __name__ == "__main__":
    pytest.main()
