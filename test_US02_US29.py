import Pro3_2


# def test_answer():
#     assert Pro3_2.func(3) == 5

def test_check_birth_before_marriage(indi):
  assert Pro3_2.check_birth_before_marriage(indi) == True