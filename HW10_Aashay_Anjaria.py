from typing import Dict, List, DefaultDict, Set
from collections import defaultdict
from HW08_Aashay_Anjaria_2 import file_reader
from prettytable import PrettyTable
import os
import sys
import statistics


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
        """Adding courses based on their type"""
        
        if type == "R":
            self._required.append(course)
       
        elif type == "E":
            self._electives.append(course)
        
        else:
            raise ValueError("Course not found")

    def get_required(self) -> List[str]:
        """In this functions, we will return the required courses.
        """
        return list(self._required)

    def get_electives(self) -> List[str]:
        """In this functions, we will return the elective courses.
        """
        return list(self._electives)

    def info(self) -> List[str]:
        """
        In this function, we will be returning the outputs.
        """
        return [self._major, self._required, self._electives]


class Student:
    """In this class, we will be creating an instance of a student.
    """
    __titles__ = ['_cwid', '_name', '_major', '_courses',
                 '_remaining_required', '_remaining_electives', '_fail',
                 '_grade']
    field_name: List[str] = ["Cwid", "Name", "Major", "Completed Courses",
                             "Remaining Required", "Remaining Elective", "GPA"]

    def __init__(
            self,
            cwid: str,
            name: str,
            major: str,
            required: List[str],
            electives: List[str]) -> None:
        """In this method, we will be initializing all the fields related to a student.
        Args:
            cwid (str)
            name (str)
            major (str)
            required (List[str])
            electives (List[str])
        """
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
        """In this method, we will add courses for each student in the dictionary.
        Args:
            course (str)
            grade (str)
        """
        if grade not in self._fail:
            self._courses[course] = grade
        if course in self._remaining_required:
            self._remaining_required.remove(course)
        if course in self._remaining_electives:
            self._remaining_electives.clear()

    def compute_gpa(self) -> float:
        """In this method, we will compute the GPA based on the courses.
        Returns:
            float: GPA
        """
        Gpas: List[float] = list()
        for i in self._courses.values():
            if i in self._grade:
                Gpas.append(self._grade[i])
            else:
                print("Invalid grade")
        if len(Gpas) == 0:
            return 0.0
        else:
            gpa: float = statistics.mean(Gpas)
        return format(gpa, '.2f')

    def info(self) -> List[str]:
        """In this function, we will be returning the outputs.
        """
        return [self._cwid, self._name, self._major,
                sorted(self._courses.keys()),
                sorted(self._remaining_required),
                sorted(self._remaining_electives),
                self.compute_gpa()]


class Instructor:
    """In this class, we will be creating an instance of an instructor.
    """
    __titles__ = ['_cwid', '_name', '_dept', '_courses']
    field_name: List[str] = ["Cwid", "Name", "Department", "Course", "Count"]

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """In this method, we will be initializing all the fields related to an
        Instructor.
        Args:
            cwid (str)
            name (str)
            dept (str)
        """
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def inst_courses_add(self, course: str) -> None:
        """In this method, we will add course name and number of students enrolled.
        Args:
            course (str): [description]
        """
        self._courses[course] += 1

    def info(self) -> List[str]:
        """In this function, we will be returning the outputs.
        """
       
        for course, count in self._courses.items():
            yield[self._cwid, self._name, self._dept, course, count]


class Repository:
    """In this class, we will be creating a repository of student
    and instructor in an University
    """
    __titles__ = ['_path', '_students', '_instructors', '_majors']

    def __init__(self, path: str, ptables: bool = True) -> None:
        """In this method, we will be initializing all the fields related to
        Repository.
        Args:
            path (str): path loaction of university
        """
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()
        self._read_majors()
        self._read_students()
        self._read_instructors()
        self._read_grades()
               

    def _read_majors(self) -> None:
        """
        Reading each major and creating its instance
        """
        try:
            for major, type, course in file_reader(os.path.join(self._path,
                                                                "majors.txt"),
                                                   3, sep='\t', header=True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(type, course)
        except FileNotFoundError:
            print(f"Cannot open file at {self._path}")

    def _read_students(self) -> None:
        """
        In this method, we will be reading each student and creating
        instances of each student as soon as it is read.
        """
        try:
            for cwid, name, major in file_reader(os.path.join(self._path,
                                                              "students.txt"),
                                                 3, sep=';', header=True):
                if cwid in self._students:
                    print("Student with CWID is already in the file")
                required: List[str] = self._majors[major].get_required()
                electives: List[str] = self._majors[major].get_electives()
                self._students[cwid] = Student(
                    cwid, name, major, required, electives)
        except FileNotFoundError:
            print(f"Cannot open file at {self._path}")
        except ValueError:
            print("Missing field")

    def _read_instructors(self) -> None:
        """
        In this method, we will be reading each student and creating
        instances of each instructor as soon as it is read.
        """
        try:
            for cwid, name, dept in file_reader(os.path.join
                                                (self._path,
                                                 "instructors.txt"),
                                                3, sep='|', header=True):
                if cwid in self._instructors:
                    print("Instructor with CWID is already in the file")
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(f"Cannot open file at {self._path}")
        except ValueError:
            print("Missing field")

    def _read_grades(self) -> None:
        """
        In this method, we will be reading the grades of each student.
        """
        try:
            for stud_cwid, course, grade, prof_cwid in file_reader(
                    os.path.join(self._path, "grades.txt"), 4, sep='|', header=True):
                if stud_cwid in self._students:
                    # handle the key error if a new student
                    s: Student = self._students[stud_cwid]
                    s.courses_add(course, grade)
                else:
                    print(f"No such Student with {stud_cwid}")
                if prof_cwid in self._instructors:
                    # handle the key error if a new instructor
                    p: Instructor = self._instructors[prof_cwid]
                    p.inst_courses_add(course)
                else:
                    print(f"No such Instructor with {prof_cwid}")

        except FileNotFoundError:
            print(f"Cannot open file at {self._path}")
        except ValueError:
            print("Wrong input")

    def major_pretty_table(self) -> PrettyTable:
        """
        In this function, we will be creating pretty table for Major
        """
        pt: PrettyTable = PrettyTable()
        pt.field_names = Major.field_name
        for s in self._majors.values():
            pt.add_row(s.info())
        print("Majors Summary")
        print(pt)
        return pt

    def student_pretty_table(self) -> PrettyTable:
        """
        In this function, we will be creating pretty table for Student
        """
        pt: PrettyTable = PrettyTable()
        pt.field_names = Student.field_name
        for s in self._students.values():
            pt.add_row(s.info())
        print("\nStudent Summary")
        print(pt)
        return pt

    def instructor_pretty_table(self) -> PrettyTable:
        """
        In this function, we will be creating pretty table for Instructor
        """
        pt: PrettyTable = PrettyTable()
        pt.field_names = Instructor.field_name
        for instval in self._instructors.values():
            for row in instval.info():
                pt.add_row(row)
        print("\nInstructor Summary")
        print(pt)
        return pt


def main():
    stevens: Repository = Repository(
        "D:\\Documents\\School\\Stevens\\810\\HW10")

if __name__ == '__main__':
    main()