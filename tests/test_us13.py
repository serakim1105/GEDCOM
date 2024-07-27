import pytest
from datetime import datetime
from ProjectAgile import us13, parse_gedcom_file

def create_indi(children = ["NA"], id = "NA", name = "NA", birth_date = "NA"):
    return {
        "Child": child,
        "ID": id,
        "Name": name,
        "Birthday": birth_date
    }
def create_fam(id = "NA", children = ["NA"], line = "NA"):
    return {
        "ID": id,
        "Children": children,
        "line": line
    }

#contains two sibling birthDates that don't match requirements
def test_1_us13(): 
    sibling1 = create_indi("F01", "I06", "Taylor /Smith/", "12 MAR 2006") #siblings
    sibling2 = create_indi("F01", "I07", "Tyler /Smith/", "1 MAR 2006") #siblings
    fam1 = create_fam("F01", ["I06", "I07"], 1)
    assert us13([sibling1, sibling2], [fam1]) == [f'Line {fam1["line"]} - US13: FAMILY: {fam1["ID"]} contains siblings that have birthdays less than 8 months and greater than 2 days apart.']
    
#contains two sibling birthDates that don't match requirements (sibling birthdays less than 8 months)
def test_2_us13(): 
    sibling3 = create_indi("F02", "I08", "Trisha /Smith/", "12 APR 2006") #siblings
    sibling4 = create_indi("F02", "I09", "Terran /Smith/", "1 MAR 2006") #siblings
    fam2 = create_fam("F02", ["I08", "I09"], 2)
    assert us13([sibling3, sibling4], [fam2]) == [f'Line {fam2["line"]} - US13: FAMILY: {fam2["ID"]} contains siblings that have birthdays less than 8 months and greater than 2 days apart.']

#contains two sibling birthDates that don't match requirements (sibling birthdays less than 8 months)
def test_3_us13(): 
    sibling5 = create_indi("F03", "I10", "Tiana /Smith/", "15 APR 2016") #siblings
    sibling6 = create_indi("F03", "I11", "Tenzing/Smith/", "12 MAR 2016") #siblings
    fam3 = create_fam("F03", ["I10", "I11"], 3)
    assert us13([sibling5, sibling6], [fam3]) == [f'Line {fam3["line"]} - US13: FAMILY: {fam3["ID"]} contains siblings that have birthdays less than 8 months and greater than 2 days apart.']

#contains two sibling birthDates that don't match requirements (twin birthdays more than two days apart)
def test_4_us13(): 
    sibling7 = create_indi("F04", "I12", "Trina /Smith/", "12 APR 2020") #siblings
    sibling8 = create_indi("F04", "I13", "Ttrxie /Smith/", "15 APR 2020") #siblings
    fam4 = create_fam("F04", ["I12", "I13"], 4)
    assert us13([sibling7, sibling8], [fam4]) == [f'Line {fam4["line"]} - US13: FAMILY: {fam4["ID"]} contains siblings that have birthdays less than 8 months and greater than 2 days apart.']
 
#contains two sibling birthDates that don't match requirements
def test_5_us13(): 
    sibling9 = create_indi("F05", "I14", "Tiffany /Smith/", "12 NOV 2020") #siblings
    sibling10 = create_indi("F05", "I15", "Trent /Smith/", "16 DEC 2020") #siblings
    fam5 = create_fam("F05", ["I14", "I15"], 5)
    assert us13([sibling9, sibling10], [fam5]) == [f'Line {fam5["line"]} - US13: FAMILY: {fam5["ID"]} contains siblings that have birthdays less than 8 months and greater than 2 days apart.']