"""Author: Aashay Anjaria SSW-810-A 4/14/2021"""
"""Homework 09"""

import os

from HW08_Aashay_Anjaria_2 import file_reader

from typing import List, Iterator, Tuple, DefaultDict, Dict
from collections import defaultdict
from prettytable import PrettyTable

class Student:
    """holds all of the details of a student, including a dict to 
    store the classes taken and the grade where the course is the key and the grade is the value."""

    student_field_names: List[str] = ["CWID", "Name", "Completed Courses"]

    def __init__(self, cwid: int, name: str, major: str) -> None:
        
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def course_grade(self, course: str, grade: str) -> None:
        
        self._courses[course] = grade

    def student_information(self) -> Tuple[str, str, List[str]]:
        
        return [self._cwid, self._name, sorted(self._courses.keys())]

class Instructor:
    """holds all of the details of an instructor, including a defaultdict(int) to 
    store the names of the courses taught along with the number of students who have taken the course.
    """

    instructor_field_names: List[str] = ["CWID", "Name", "Dept", "Courses", "Students"]

    def __init__(self, cwid: int, name: str, department: str) -> None:
        
        self._cwid: str = cwid
        self._name: str = name
        self._department: str = department
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_students(self, course: str) -> None:
        
        self._courses[course] += 1

    def instructor_information(self) -> Iterator[Tuple[str, str, str, str, int]]:
        
        for course, students in self._courses.items():
            
            yield [self._cwid, self._name, self._department, course, students]

class Repository:
    """Includes a container for all students, Includes a container for all instructors
    __init__(self, dir_path) specifies a directory path where to find the students.txt, instructors.txt, and grades.txt files.  
    """

    def __init__(self, dir_path: str, tables: bool = True) -> None:
        
        self._dir_path: str = dir_path
        self._students_dict: Dict[str, Student] = dict()
        self._instructors_dict: Dict[str, Instructor] = dict()

        try:
            
            self._get_students(os.path.join(dir_path, "students.txt"))
            self._get_instructors(os.path.join(dir_path, "instructors.txt"))
            self._get_grades(os.path.join(dir_path, "grades.txt"))
        
        except FileNotFoundError:
            
            raise FileNotFoundError("Error, cannot find file")
        
        except ValueError as e:
            
            print(e)
        
        else:
            
            if tables:
                
                print("Student Information")
                print(self.student_pt())
                print("Instructor Information")
                print(self.instructor_pt())

    def _get_students(self, path: str) -> None:
        
        try:
            students_information: Iterator(Tuple[str]) = file_reader(path, 3, sep = "\t", header = False)
            
            for cwid, name, major in students_information:
                
                self._students_dict[cwid] = Student(cwid, name, major)
        
        except ValueError as e:
            
            raise ValueError(e)

    def _get_instructors(self, path: str) -> None:
    
        try:
            instructors_information: Iterator(Tuple[str]) = file_reader(path, 3, sep = "\t", header = False)
            
            for cwid, name, department in instructors_information:
                
                self._instructors_dict[cwid] = Instructor(cwid, name, department)
        
        except ValueError as e:
            
            raise ValueError(e)

    def _get_grades(self, path: str) -> None:
       
        grades: Iterator(Tuple[str]) = file_reader(path, 4, sep="\t", header = False)
        
        for st_cwid, course, grade, inst_cwid in grades:
            
            if st_cwid in self._students_dict:
                
    
                self._students_dict[st_cwid].course_grade(course, grade) 
            
            else:
               
                print(f"student grade {st_cwid}")
            
            if inst_cwid in self._instructors_dict:
                
                self._instructors_dict[inst_cwid].add_students(course)
            
            else:
                
                print(f"instrutor grade {inst_cwid}")

    def student_table(self) -> None:
        
        prettytable: PrettyTable = PrettyTable(field_names=Student.st_field_names)

        for student in self._students_dict.values():
            
            prettytable.add_row(student.st_data())

        return prettytable

    def instructor_table(self) -> None:
        
        prettytable: PrettyTable = PrettyTable(field_names=Instructor.inst_field_names)

        for instructor in self._instructors_dict.values():
            
            for row in instructor.inst_data():
               
                prettytable.add_row(row)

        return prettytable

def main() -> None:
   
    File: Repository = Repository("D:\\Documents\\School\\Stevens\\810\\HW09", True)


if __name__ == "__main__":
    main()
