from mongoengine import *
from Course import Course
from Major import Major


class Requirement(Document):
    name = StringField(min_length=2, max_length=50, required=True, primary_key=True)
    description = StringField(min_length=5, max_length=100, required=True)
    credits = IntField(min_value=1, max_value=150, required=True)
    major = ReferenceField(Major, required=True)
    parent_requirement = ReferenceField('Requirement', reverse_delete_rule=DENY)
    sub_requirement_names = ListField(StringField())
    course_names = ListField(ReferenceField('Course', reverse_delete_rule=NULLIFY))

    meta = {'collection':'requirements', 'allow_inheritance':True, 'index_cls':False}

    def __str__(self):
        return f'{self.name} requirement with description: {self.description}.'

