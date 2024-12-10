from Requirement import Requirement
from Course import Course
from mongoengine import *

class CourseRequirement(Document):
    course = ReferenceField(Course)
    requirement = ReferenceField(Requirement)