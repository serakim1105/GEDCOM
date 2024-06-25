import pytest
from ProjectAgile import us39, parse_gedcom_file

def create_date(marriage_date="NA"):
    return {
        "WeddingDate": fam["Marriage"],
    }

def test_1_us39(): 
    assert us39(create_date("20 OCT 1942")) #weddingDate

def test_2_us39():
    assert us39(create_date("25 DEC 1962")) #weddingDate
    
def test_3_us39():
   assert us39(create_date("4 MAY 1990")) #weddingDate

def test_4_us39():
   assert us39(create_date("1 JAN 2025")) #weddingDate

def test_4_us39():
   assert us39(create_date("11 NOV 2000")) #weddingDate