from Department import Department
import mongoengine
from mongoengine import *


class Major(Document):
    # Foreign Key
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    department_name = StringField(db_field='department_name', required=True)

    name = StringField(db_field='name', required=True)
    description= StringField(db_field='description', required=True)
  
    requirements = ListField(ReferenceField('Requirements'))
    meta = {'allow_inheritance': True, 'collection': 'majors',
            'indexes': [
                {
                    'fields': ['name'],
                    'name': 'major_pk',
                    'unique': True
                }]
            }

    def __init__(self, department: Department, department_name: str, name: str, description: str, **kwargs):
        super(Major, self).__init__(**kwargs)
        self.department = department
        self.department_name = department_name
        self.name = name
        self.description = description

    def __str__(self):
        return f'{self.department_name}: {self.name}'

    def add_requirement(self, requirement):
        if requirement not in self.requirements:
            self.requirements.append(requirement)

    def remove_requirement(self, requirement):
        if requirement in self.requirements:
            self.requirements.remove(requirement)
