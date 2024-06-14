import pytest
from Pro3_2 import us29, parse_gedcom_line, parse_gedcom_file
#import Pro3_2
from datetime import datetime

# Helper function to create a mock individual
def create_indi(id, name, death_date="NA"):
    return {
        "ID": id,
        "Name": name,
        "Death": death_date,
    }
indi01 = create_indi("I01", "Christine /Anthony/", "20 OCT 1942") #deceased
indi02 = create_indi("I01", "Sriya /Bhamidipati/", "01 NOV 2024") #deceased
indi03 = create_indi("I02", "Sera /Kim/")                         #not deceased
indi03 = create_indi("I02", "Navya /Pai/", "NA")                  #not deceased

individuals = []
individuals.append(indi01)
individuals.append(indi02)
individuals.append(indi03)

def test_1_us29(): 
    assert us29(individuals) == ["Christine /Anthony/", "Sriya /Bhamidipati/"] #should pass
    #print(individuals)

def test_2_us29():
    #num_deceased = len(us29(individuals))
    assert len(us29(individuals)) == 2
    #print(f"Number of deceased = {num_deceased}")

if __name__ == "__main__":
    pytest.main()