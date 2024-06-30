import pytest
from ProjectAgile import us28, parse_gedcom_file
from datetime import datetime

# Helper function to create a mock individual
def create_indi(id = "NA", name = "NA", age = "NA", child = ["NA"], birthday = "NA", death = "NA"):
    return {
        "ID": id,
        "Name": name,
        "Age": age,
        "Child": child,
        "Birthday": birthday,
        "Death": death
    }
def create_fam(id, child):
    return {
        "ID": id,
        "Child": child
    }

def test_1_us28(): 
    indi1 = create_indi("I06","18","Taylor /Smith/", "F01", "1 MAR 2006", "NA") #siblings
    indi2 = create_indi("I07","18","Tyler /Smith/", "F01", "1 MAR 2006", "NA") #siblings
    fam01 = create_fam("F01", ["I06", "I07"])
    assert us28([indi1, indi2], [fam01])

def test_2_us28(): 
    indi3 = create_indi("I08","6","Anjali /Pai/", "F02", "1 APR 2018", "NA") #siblings
    indi4 = create_indi("I09","8", "Akaash /Pai/", "F02", "21 MAR 2016", "NA") #siblings
    fam02 = create_fam("F02", ["I08", "I09"])
    assert us28([indi3, indi4], [fam02])

def test_3_us28(): 
    indi5 = create_indi("I10","11","Trisha /Smith/", "F03", "12 SEP 2013","NA") #siblings
    indi6 = create_indi("I11","15","Terrance /Smith/", "F03", "1 JUN 2009","NA") #siblings
    fam03 = create_fam("F03", ["I10", "I11"])
    assert us28([indi5, indi6], [fam03])

def test_4_us28(): 
    indi1 = create_indi("I02","6","Paulina /Ash/", "F04", "1 MAR 2014", "2 MAR 2020") #siblings
    indi2 = create_indi("I01","10","Paul /Ash/", "F04", "1 MAR 2014") #siblings
    fam04 = create_fam("F04", ["I06", "I07"])
    assert us28([indi1, indi2], [fam04])

def test_5_us28(): 
    indi1 = create_indi("I05","13","Sarah /Smith/", "F05", "1 SEP 1987", "12 SEP 2000") #siblings
    indi2 = create_indi("I04","30","Sam /Smith/", "F05", "12 SEP 1974") #siblings
    fam05 = create_fam("F05", ["I06", "I07"])
    assert us28([indi1, indi2], [fam05])


if __name__ == "__main__":
    pytest.main()