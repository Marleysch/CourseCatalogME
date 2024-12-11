from Department import Department
import mongoengine
from mongoengine import *


class Major(Document):
    department = ReferenceField(Department, required=True, reverse_delete_rule=DENY)

    name = StringField(db_field='name', required=True)
    description= StringField(db_field='description', required=True)
  
    requirements = ListField(ReferenceField('Requirements'), default=[])
    meta = {'collection': 'majors',
            'indexes': [
                {
                    'fields': ['name'],
                    'name': 'major_pk',
                    'unique': True
                }]
            }

    def __init__(self, department: Department, name: str, description: str, **kwargs):
        super(Major, self).__init__(**kwargs)
        self.department = department
        self.name = name
        self.description = description

    def __str__(self):
        return f'{self.department.name}: {self.name}'

    def add_requirement(self, requirement):
        if requirement not in self.requirements:
            self.requirements.append(requirement)

    def remove_requirement(self, requirement):
        if requirement in self.requirements:
            self.requirements.remove(requirement)
