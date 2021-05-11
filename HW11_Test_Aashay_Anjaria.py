#!/usr/bin/env python

#------------------------------------------------
# import test lib
import unittest

# import HW11_Aashay_Anjaria.py -> this is the name of file that we are testing
import HW11_Aashay_Anjaria
#------------------------------------------------
#------------------------------------------------
# test for student module
class TestStudent(unittest.TestCase):

  #-----------------------------#
  def test_repository(self):
    """ Unit Test for Repository class """

    # set expected Student details
    expected_student_details = {
      '10001': ['10001', 'One, O', 'SFEN', ['ELE 003', 'REQ 001'], ['REQ 002'], [], '3.88'],
      '10002': ['10002', 'Two, T', 'SYEN', ['REQ 005', 'REQ 006'], [], ['ELE 007', 'ELE 008'], '2.88']
    }

    # set expected Major details
    expected_major_details = {
      'SFEN': ['SFEN', ['REQ 001', 'REQ 002'], ['ELE 003', 'ELE 004']],
      'SYEN': ['SYEN', ['REQ 005', 'REQ 006'], ['ELE 007', 'ELE 008']]
    }

    # set expected Instructor details
    expected_instructor_details = {
      '98765': [
        ['98765', 'Einstein, A', 'SFEN', 'REQ 001', 1]
      ],
      '98764': [
        ['98764', 'Feynman, R', 'SFEN', 'ELE 003', 1]
      ],
      '98763': [
        ['98763', 'Newton, I', 'SYEN', 'REQ 005', 1],
        ['98763', 'Newton, I', 'SYEN', 'REQ 006', 1]
      ],
      '98762': [
        "."
      ]
    }

    # get repository
    actual_repo = HW11_Aashay_Anjaria.Repository(".\\test")

    # test Student info
    # loop all students
    for cwid in actual_repo._students:
      # get student details
      actual_details = actual_repo._students[cwid].info()
      # compare actual vs expected
      self.assertEqual(actual_details, expected_student_details[cwid])

    # test Major info
    # loop all majors
    for major in actual_repo._majors:
      # get major details
      actual_details = actual_repo._majors[major].info()
      # compare actual vs expected
      self.assertEqual(actual_details, expected_major_details[major])

    # test Instructor info
    # loop all instructors
    for instructor in actual_repo._instructors:
      # get instructor details
      actual_details = actual_repo._instructors[instructor].info()
      # enumerate() -->  adds a counter to an iterable and returns it in a form of enumerate object (tuple)
      # loop all instructor details
      for index, actual_row in enumerate(actual_details):
        # compare actual vs expected
        self.assertEqual(actual_row, expected_instructor_details[instructor][index])
  #-----------------------------#

#------------------------------------------------

if __name__ == '__main__':
  unittest.main()