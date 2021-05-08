#!/usr/bin/env python

#------------------------------------------------
# this code group will automatically install python modules if they do not exist
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
class Major:
  """Major instance created"""
   
  __titles__ = ['_major', '_required', '_electives']
   
  field_name: List[str] = ["Major", "Required Courses", "Elective Courses"]

  def __init__(self, major: str) -> None:
    """Initializing Variables"""
     
    self._major: str = major
    self._required: List[str] = list()
    self._electives: List[str] = list()

  def add_course(self, type: str, course: str) -> None:
    """Adding courses based on type"""
     
    if type == "R":
      self._required.append(course)
    
    elif type == "E":
      self._electives.append(course)
     
    else:
      raise ValueError("Course not found")

  def get_required(self) -> List[str]:
    """Return required courses"""
    return list(self._required)

  def get_electives(self) -> List[str]:
    """Return the electives"""
    return list(self._electives)

  def info(self) -> List[str]:
    """Return the outputs"""
    return [self._major, self._required, self._electives]

#------------------------------------------------
class Student:
  """Student class"""
   
  __titles__ = ['_cwid', '_name', '_major', '_courses', '_remaining_required', '_remaining_electives', '_fail', '_grade']
  field_name: List[str] = ["Cwid", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Elective", "GPA"]

  def __init__(
      self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:

    self._cwid: str = cwid
    self._name: str = name
    self._major: str = major
    self._courses: Dict[str, str] = dict()
    self._remaining_required: List[str] = required
    self._remaining_electives: List[str] = electives
    self._fail: List[str] = ["C-", "D+", "D", "D-", "F"]
    self._grade: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25,
                     "B": 3.0, "B-": 2.75, "C+": 2.25,
                     "C": 2.0, "C-": 0.0, "D+": 0.0,
                     "D": 0.0, "D-": 0.0, "F": 0.0}

  def courses_add(self, course: str, grade: str) -> None:
    """Add courses for students"""
     
    if grade not in self._fail:
      self._courses[course] = grade
    
    if course in self._remaining_required:
      self._remaining_required.remove(course)
     
    if course in self._remaining_electives:
      self._remaining_electives.clear()

  def compute_gpa(self) -> float:
    """Compute GPA"""
     
    Gpa1: List[float] = list()
     
    for i in self._courses.values():
       
      if i in self._grade:
        Gpa1.append(self._grade[i])
       
      else:
        print("Invalid grade")
    
    if len(Gpa1) == 0:
      return 0.0
    
    else:
      gpa: float = statistics.mean(Gpa1)
    
    return format(gpa, '.2f')

  def info(self) -> List[str]:
    
    return [self._cwid, self._name, self._major, sorted(self._courses.keys()), sorted(self._remaining_required), sorted(self._remaining_electives), self.compute_gpa()]

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
  
  __titles__ = ['_path', '_students', '_instructors', '_majors']

  def __init__(self, path: str, ptables: bool = True) -> None:
    """Initializing all fields"""
     
    self._path: str = path
    self._students: Dict[str, Student] = dict()
    self._instructors: Dict[str, Instructor] = dict()
    self._majors: Dict[str, Major] = dict()
    self._read_majors()
    self._read_students()
    self._read_instructors()
    self._read_grades()
        

  def _read_majors(self) -> None:
    """Reading each major"""
     
    try:
      for major, type, course in file_reader(os.path.join(self._path,"majors.txt"),3, sep='\t', header=True):
         
        if major not in self._majors:
          self._majors[major] = Major(major)
         
        self._majors[major].add_course(type, course)
     
    except FileNotFoundError:
      print(f"Incorrect input {self._path}")

  def _read_students(self) -> None:
     
    try:
       
      for cwid, name, major in file_reader(os.path.join(self._path,"students.txt"),3, sep=';', header=True):
         
        if cwid in self._students:
          print("Student with CWID is already in the file")
         
        required: List[str] = self._majors[major].get_required()
        electives: List[str] = self._majors[major].get_electives()
        self._students[cwid] = Student(cwid, name, major, required, electives)
     
    except FileNotFoundError:
      print(f"Error! Cannot locate file here {self._path}")
     
    except ValueError:
      print("Incorrect input")

  def _read_instructors(self) -> None:
    
    try:
       
      for cwid, name, dept in file_reader(os.path.join (self._path,"instructors.txt"), 3, sep='|', header=True):
         
        if cwid in self._instructors:
           
          print("Instructor with that CWID already exists!")
         
        self._instructors[cwid] = Instructor(cwid, name, dept)
     
    except (FileNotFoundError, ValueError) as e:
      print(f"Error! Cannot locate file here {self._path}")
     
    except ValueError:
      print("Incorrect input")

  def _read_grades(self) -> None:
    """Reading the grades for the students"""
     
    try:
       
      for stud_cwid, course, grade, prof_cwid in file_reader(os.path.join(self._path, "grades.txt"), 4, sep='|', header=True):
         
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
     
    except ValueError:
      print("Incorrect input")

  def major_pretty_table(self) -> PrettyTable:
    """Prettytable for major"""
     
    pt: PrettyTable = PrettyTable()
    pt.field_names = Major.field_name
     
    for s in self._majors.values():
      pt.add_row(s.info())
     
    print("\nMajors Summary")
    print(pt)
     
    return pt

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
  student_repo = Repository("D:\\Documents\\School\\Stevens\\810\\HW10")
  student_repo.student_pretty_table()
  student_repo.major_pretty_table()
  student_repo.instructor_pretty_table()

#------------------------------------------------
if __name__ == '__main__':
  main()