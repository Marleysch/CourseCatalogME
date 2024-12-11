from Requirement import Requirement
from Course import Course
from mongoengine import *

class CourseRequirement(Document):
    course = ReferenceField(Course)
    requirement = ReferenceField(Requirement)
    meta = {'collection': 'course_requirements', 'indexes':[{'fields':['course','requirement'],'name':'course_requirements_pk', 'unique':True}]}