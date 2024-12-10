from mongoengine import Document, StringField, IntField, ListField, ReferenceField, NULLIFY, LazyReferenceField

from Department import Department


class Course(Document):
    # Fields that represent the columns in the SQL table
    name = StringField(max_length=30, required=True, primary_key=True)
    department = ReferenceField(Department, required=True)
    departments_abbr = StringField(max_length=50, required=True)
    number = IntField(required=True)
    description = StringField(max_length=100, required=True)
    units = IntField(required=True)

    # Unique constraint for the combination of departments_abbr and number
    meta = {
        'indexes': [
            {'fields': ['departments_abbr', 'number'], 'unique': True}
        ],
        # Ensure the MongoDB collection is named 'courses'
        'collection': 'courses'
    }

    def __str__(self):
        return f'{self.name} ({self.departments_abbr} {self.number})'

