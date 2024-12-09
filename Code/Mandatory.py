from mongoengine import *
from Requirement import Requirement
from Course import Course


class MandatoryRequirement(Requirement):
    courses = ListField(ReferenceField('Courses'))

    def __init__(self, major: Major, requirement_name: str, description: str, credit: int, **kwargs):
        super().__init__(major=major, requirement_name=requirement_name, description=description, credit=credit, **kwargs)

    def __str__(self):
        return f'{super().__str__()}'

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
