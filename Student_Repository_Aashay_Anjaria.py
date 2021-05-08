#!/usr/bin/env python

#------------------------------------------------
# this code group will automatically install python modules if they do not exists
try:
  from typing import Dict, List, DefaultDict, Set
  from collections import defaultdict
  from HW08_Aashay_Anjaria import file_reader
  from prettytable import PrettyTable
  import os
  import sys
  import statistics
except ImportError:
  import subprocess
  install = ["pip", "install", "-U", "PrettyTable"]
  result = subprocess.call(install)
  if result != 0 and result != 23:
    install[0] = "pip3"
    subprocess.call(install)
finally:
  from typing import Dict, List, DefaultDict, Set
  from collections import defaultdict
  from HW08_Aashay_Anjaria import file_reader
  from prettytable import PrettyTable
  import os
  import sys
  import statistics
#------------------------------------------------
#------------------------------------------------
class Student:
  """Student class"""
  
  __titles__ = ['_cwid', '_name', '_courses']
  field_name: List[str] = ["Cwid", "Name", "Completed Courses"]

  def __init__(
    self, cwid: str, name: str) -> None:

    self._cwid: str = cwid
    self._name: str = name
    self._courses: Dict[str, str] = dict()

  def courses_add(self, course: str, grade: str) -> None:
    """Add courses for students"""

    self._courses[course] = grade

  def info(self) -> List[str]:
    return [self._cwid, self._name, sorted(self._courses.keys())]

#------------------------------------------------
class Instructor:
  """Instructor class"""
  
  __titles__ = ['_cwid', '_name', '_dept', '_courses']
  field_name: List[str] = ["Cwid", "Name", "Department", "Course", "Count"]

  def __init__(self, cwid: str, name: str, dept: str) -> None:
    """Initializing all fields"""
   
    self._cwid: str = cwid
    self._name: str = name
    self._dept: str = dept
    self._courses: DefaultDict[str, int] = defaultdict(int)

  def inst_courses_add(self, course: str) -> None:
    """Adding courses"""
     
    self._courses[course] += 1

  def info(self) -> List[str]:
    for course, count in self._courses.items():
      yield[self._cwid, self._name, self._dept, course, count]

#------------------------------------------------
class Repository:
  """Repository of students and instructors"""

  __titles__ = ['_path', '_students', '_instructors']

  def __init__(self, path: str, ptables: bool = True) -> None:
    """Initializing all fields"""
   
    self._path: str = path
    self._students: Dict[str, Student] = dict()
    self._instructors: Dict[str, Instructor] = dict()
     

    self._read_students()
    self._read_instructors()
    self._read_grades()

  def _read_students(self) -> None:
    try:
      for cwid, name, course in file_reader(os.path.join(self._path,"students.txt"),3, sep='\t', header=False):
     
        if cwid in self._students:
          print("Student with CWID is already in the file")
     
        self._students[cwid] = Student(cwid, name)
   
    except FileNotFoundError:
      print(f"Error! Cannot locate file here {self._path}")
   
  #except ValueError:
  # print("Incorrect input")

  def _read_instructors(self) -> None:
   
    try:
    
      for cwid, name, dept in file_reader(os.path.join (self._path,"instructors.txt"), 3, sep='\t', header=False):
     
        if cwid in self._instructors:
          print("Instructor with that CWID already exists!")
     
        self._instructors[cwid] = Instructor(cwid, name, dept)
   
    except (FileNotFoundError, ValueError) as e:
      print(f"Error! Cannot locate file here {self._path}")
   
  #except ValueError:
  # print("Incorrect input")

  def _read_grades(self) -> None:
    """Reading the grades for the students"""
   
    try:
    
      for stud_cwid, course, grade, prof_cwid in file_reader(os.path.join(self._path, "grades.txt"), 4, sep='\t', header=False):
     
        if stud_cwid in self._students:
          s: Student = self._students[stud_cwid]
          s.courses_add(course, grade)
     
        else:
          print(f"No such Student with {stud_cwid}")
     
        if prof_cwid in self._instructors:
          p: Instructor = self._instructors[prof_cwid]
          p.inst_courses_add(course)
     
        else:
          print(f"Cannot find Instructor with {prof_cwid}")

    except FileNotFoundError:
      print(f"Error! Cannot locate file here {self._path}")
   
  #except ValueError:
  # print("Incorrect input")

  def student_pretty_table(self) -> PrettyTable:
    """Prettytable for Student"""
   
    pt: PrettyTable = PrettyTable()
    pt.field_names = Student.field_name
     
    for s in self._students.values(): pt.add_row(s.info())
   
    print("\nStudent Summary")
    print(pt)
   
    return pt

  def instructor_pretty_table(self) -> PrettyTable:
    """Prettytable for Instructor"""
   
    pt: PrettyTable = PrettyTable()
    pt.field_names = Instructor.field_name
   
    for instval in self._instructors.values():
    
      for row in instval.info():
        pt.add_row(row)
   
    print("\nInstructor Summary")
    print(pt)
   
    return pt
#------------------------------------------------
#------------------------------------------------
def main():
  student_repo = Repository(".\\students_directory")
  student_repo.student_pretty_table()
  student_repo.instructor_pretty_table()

#------------------------------------------------
# let's begin :)
if __name__ == '__main__':
  main()