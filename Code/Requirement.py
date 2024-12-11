from mongoengine import *
from Major import Major


class Requirement(Document):
    name = StringField(min_length=2, max_length=50, required=True)
    description = StringField(min_length=5, max_length=100, required=True)
    credits = IntField(min_value=1, max_value=150, required=True)
    major = ReferenceField(Major, required=True)
    parent_requirement = ReferenceField('Requirement', reverse_delete_rule=DENY)
    sub_requirement_names = ListField(StringField())

    meta = {'collection':'requirements', 'allow_inheritance':True, 'index_cls':False, 'indexes':[{'fields':['name'], 'name':'requirements_pk','unique':True}]}

    def __str__(self):
        return f'{self.name} requirement with description: {self.description}.'

    def add_sub_requirement(self, requirement):
        if requirement.name not in self.sub_requirement_names:
            self.sub_requirement_names.append(requirement.name)

    def remove_sub_requirement(self, requirement):
        if requirement.name in self.sub_requirement_names:
            self.sub_requirement_names.remove(requirement.name)

