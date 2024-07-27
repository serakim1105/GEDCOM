import pytest
from datetime import datetime
from ProjectAgile import us15, parse_gedcom_file

def create_fam(id = "NA", children = ["NA"], line = "NA"):
    return {
        "ID": id,
        "Children": children,
        "line": line
    }
# def create_indi(id = "NA", name = "NA", age = "NA", child = ["NA"], birthday = "NA", death = "NA"):
#     return {
#         "Name": name,
#         "Child": child
#     }



# birth and death 
def test_1_us15():
    # Test case 1: Family that has 15 siblings
    fam1 = create_fam("F05", ["I01", "I02", "I03", "I04", "I05", "I06", "I07", "I08", 
                            "I09", "I10", "I11", "I12", "I13", "I14", "I15"], 1)
    assert us15([fam1]) == [f'Line {fam1["line"]} - US15: FAMILY: {fam1["ID"]} has 15 siblings or more.']
    
def test_2_us15():
    # Test case 1: Family that has 15 siblings
    fam2 = create_fam("F06", ["I16", "I17", "I18", "I19", "I20", "I21", "I22", 
                            "I23", "I24", "I25", "I26", "I27", "I28", "I29", "I30", "I31"], 2)
    assert us15([fam2]) == [f'Line {fam2["line"]} - US15: FAMILY: {fam2["ID"]} has 15 siblings or more.']
    
def test_3_us15():
    # Test case 1: Family that has 15 siblings
    fam3 = create_fam("F06", ["I26", "I27", "I28", "I29", "I30", 
                            "I31", "I32", "I33", "I34", "I35", "I36", "I37", "I38", "I39", "I40", "I41"], 3)
    assert us15([fam3]) == [f'Line {fam3["line"]} - US15: FAMILY: {fam3["ID"]} has 15 siblings or more.']
    
