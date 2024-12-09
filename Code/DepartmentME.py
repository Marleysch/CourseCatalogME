from mongoengine import *


class Department(Document):
    """An organization within a college within a university that provides one or more
    degree programs to its students."""
    name = StringField(min_length=3, max_length=80, required=True)
    abbreviation = StringField(min_length=3, max_length=16, required=True)

    meta = {'collection': 'departments',
            'indexes': [
                    {
                        'fields': ['name'],
                        'name': 'departments_pk',
                        'unique': True
                    }, {
                        'fields': ['abbreviation'],
                        'name': 'departments_uk_01',
                        'unique': True
                    }
                ]
            }

    def __init__ (self, name, abbreviation, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.abbreviation = abbreviation

    def __str__(self):
        return f"Department - abbreviation: {self.abbreviation} name: {self.name}"
