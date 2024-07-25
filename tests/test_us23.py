import pytest
from ProjectAgile import us23

individuals = [
    {'line': 1, 'ID': 'I01', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 2, 'ID': 'I05', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 3, 'ID': 'I02', 'Name': 'Jane /Jones/', 'Gender': 'F', 'Birthday': '10 APR 1810', 'Death': '25 JUN 1890', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 4, 'ID': 'I03', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']}, 
    {'line': 5, 'ID': 'I04', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']}]


def test_1_us23(): # 2 dup individuals
    assert len(us23(individuals)) == 2

def test_2_us23(): # 1 dup individuals
    individuals.pop()
    assert len(us23(individuals)) == 1

