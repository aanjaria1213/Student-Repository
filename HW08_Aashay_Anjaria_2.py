from datetime import datetime, timedelta
from typing import Tuple, Iterator
from prettytable import PrettyTable
import os


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ returns date three days after Feb 27, 2000, Feb 27, 2017 and number of days between Feb,1 2019 and Sept 30, 2019 """

    three_days_after_02272000: datetime = datetime.strptime('Feb 27, 2020', "%b %d, %Y") + timedelta(days=3)
    three_days_after_02272017: datetime = datetime.strptime('Feb 27, 2019', "%b %d, %Y") + timedelta(days=3)
    # Multiplied by -1 so it give positive value when moving forward & negative value when moving backwards
    days_passed_01012017_10312017: int = ((datetime.strptime('Feb 1, 2019', "%b %d, %Y") - datetime.strptime(
        'Sep 30, 2019', "%b %d, %Y")).days) * -1

    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017

def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    """returns a tuple containing values which are separated by '|' or ','"""

    lineCount = 1
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f'Cannot open the file in the path {path}')

    else:
        with fp:
            if header:
                next(fp)

            for line in fp:
                values = line.rstrip('\n').split(sep)

                if len(values) != fields:
                    raise ValueError(
                        f'{os.path.basename(path)} has  {len(values)} fields on line {lineCount} but excepted {fields}')

                lineCount += 1
                yield tuple(values)
                
class FileAnalyzer:
    """ class contains functions which takes folder path as input and anlayze the files to find .py files
        & counts the func,class,lines and characters"""

    def __init__(self, directory: str) -> None:
        """intial function which takes path and create the file summary and calls the analyze_file func"""

        self.directory: str = directory
        self.files_summary: dict[str, dict[str, int]] = dict()
        self.analyze_files()

    def analyze_files(self) -> None:
        """ opens .py extension files and analyzes files to count the func,classes,lines & characters in file """
        try:
            directory: [str] = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError('Directory not exist')
        else:
            for file in directory:
                if file.endswith(".py"):
                    self.files_summary[file] = {}
                    try:
                        fp = open(os.path.join(self.directory, file), 'r')
                    except FileNotFoundError:
                        raise FileNotFoundError('File not exist')
                    else:
                        with fp:
                            self.files_summary[file]['line'] = sum(1 for line in fp)
                            defCount = 0
                            classCount = 0
                            fp.seek(0)
                            data = fp.read()
                            characters = len(data)
                            fp.seek(0)
                            for line in fp:
                                line = line.strip('\n')
                                wordslist = line.split()

                                if 'def' in wordslist and line.endswith(':'):
                                    defCount = defCount + 1
                                if 'class' in wordslist and line.endswith(':'):
                                    classCount = classCount + 1

                            self.files_summary[file]['function'] = defCount
                            self.files_summary[file]['class'] = classCount
                            self.files_summary[file]['char'] = characters

    def pretty_print(self) -> None:
        """ printing file name, class count, func count, lines & characters in each .py file"""

        pt: PrettyTable = PrettyTable()
        pt.field_names: list = [
            "File Name",
            "Classes",
            "Functions",
            "Lines",
            "Characters"]

        for k1, v1 in self.files_summary.items():
            l = list()
            l = [
                k1
                , v1['class']
                , v1['function']
                , v1['line']
                , v1['char']
            ]
            pt.add_row(l)

        return pt