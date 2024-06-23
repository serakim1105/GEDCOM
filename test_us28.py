import pytest
from ProjectAgile import us28, parse_gedcom_file
from datetime import datetime

# Helper function to create a mock individual
def create_indi(id, name, death_date="NA"):
    return {
        "ID": id,
        "Name": name,
        "MarriageAge": calculate_age(fam["Marriage"]),
    }

indi01 = create_indi("I01", "Christine /Anthony/", "20 OCT 1942") #siblings
indi02 = create_indi("I02", "Christine /Anthony/", "18 OCT 1942") #siblings
indi02 = create_indi("I02", "Christine /Anthony/", "18 OCT 1942") #siblings
indi02 = create_indi("I02", "Christine /Anthony/", "18 OCT 1942") #siblings
indi03 = create_indi("I04", "Navya /Pai/", "NA")                  #not deceased

individuals = []
individuals.append(indi01)
individuals.append(indi02)
individuals.append(indi03)

def test_1_us28(): 
    assert us28(individuals) == ["Individual: I01: Christine Anthony\n", "Individual: I02: Sriya Bhamidipati\n"] #should pass

def test_2_us28():
    assert len(us28(individuals)) == 2


if __name__ == "__main__":
    pytest.main()