import mongoengine
from pymongo import monitoring
from pymongo.client_session import ClientSession
from mongoengine import ValidationError, OperationError, NotUniqueError
from pymongo.client_session import ClientSession
from CommandLogger import CommandLogger, log
from Menu import Menu
from input_utilities import input_int_range
from menu_definitions import (menu_mainME, add_select, delete_select, list_select, select_select, update_select)
from Department import Department
from Major import Major
from Course import Course
from Requirement import Requirement
from TotalRequirement import TotalRequirement
from ChoiceRequirement import ChoiceRequirement
from MandatoryRequirement import MandatoryRequirement


class Session(ClientSession):
    """I'm hoping to be able to actually use the Session in the transactions in this eventually,
    so I'm faking it here with this class definition."""
    pass


def menu_loop(menu: Menu, session: Session):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see.
    :param  sess:   The database connect session that the operation selected will use."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add(session: Session):
    """Top level menu prompt for any add operation."""
    menu_loop(add_select, session)


def list_members(session: Session):
    """Top level menu prompt for any list members operation."""
    menu_loop(list_select, session)


def select(session: Session):
    """Top level menu prompt for any select operation."""
    menu_loop(select_select, session)


def delete(session: Session):
    """Top level menu prompt for any delete operation."""
    menu_loop(delete_select, session)


def update(session: Session):
    """Top level menu prompt for any update operation."""
    menu_loop(update_select, session)


def add_department(session: Session):
    valid: bool = False
    while not valid:
        # check valid position (B4)
        name = input("Enter department name -->")
        abrev = input("Enter department abrev -->")
        try:
            department = Department(name, abrev)
            department.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')


def add_major(session: Session):
    valid: bool = False
    while not valid:
        department: Department = select_department(session)
        name = input("Enter major name -->")
        description = input(f'Write a description of {name} major-->')
        try:
            major = Major(department, name, description)
            major.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')

def add_course(session: Session):
    valid: bool = False
    while not valid:
        department: Department = select_department(session)
        name = input("Enter course name -->")
        description = input(f'Write a description of {name} course-->')
        units = input_int_range("Enter the units of this course-->", 1, 4)
        try:
            course = Course(department, name, description, units)
            course.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
            
def add_office(session: Session):
    valid: bool = False
    while not valid:
        building: Building = select_building(session)
        number = input_int_range("Enter the room number of the office-->", 0, 10000)
        office = Office(building, number)
        option = input_int_range("Answer the prompt:\n1. Office is shared\n2. Office is Single\n-->", 1, 2)
        # implement a choice for shared or single
        try:
            office.save()
            if option == 1:
                shared_office = SharedOffice(office)
            building.add_office(office)
            building.save()
            valid = True
        except ValidationError as VE:
            print(f"Invalid data: {VE}.  Try again.")
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')


def add_office_hours(session: Session):
    valid: bool = False
    while not valid:
        office: Office = select_office(session)
        instructor: Instructor = select_instructor(session)
        office_hour = (office, instructor)
        # implement a choice for shared or single
        try:
            office.save()
            office_hour.add(office)
            office_hour.save()
            valid = True
        except ValidationError as VE:
            print(f"Invalid data: {VE}.  Try again.")
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')


def delete_department(session: Session):
    ok: bool = False
    while not ok:
        department: Department = select_department(session)
        try:
            department.delete()
            ok = True
            print(f'Department {department.name} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} courses are dependant on this department")


# check for corruption with deletion, likely flawed
def delete_major(session: Session):
    departement: Department = select_department(session)
    major = major.department
    department.remove_department(department)
    department.save()
    major.delete()

def delete_course(session: Session):
    departement: Department = select_department(session)
    course = course.department
    department.remove_department(department)
    department.save()
    course.delete()

def delete_requirement(session: Session):

'''
def delete_address(session: Session):
    ok: bool = False
    while not ok:
        address: Address = select_address(session)
        try:
            address.delete()
            ok = True
            print(f'Address {str(address)} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} A Vendor has parts on this address")


def delete_vendor(session: Session):
    ok: bool = False
    while not ok:
        vendor: Vendor = select_vendor(session)
        try:
            if len(vendor.parts) >= 1:
                for part in vendor.parts:
                    part.delete()
            vendor.delete()
            ok = True
            print(f'office {vendor.name} deleted.')
        except ValidationError as VE:
            print(f"Invalid data: {VE}.  Try again.")
'''


def select_deparment(session: Session) -> Department:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter department name -->")
        pipeline = [{"$match": {"name": name}}]
        deparment_count = len(list(Department.objects().aggregate(pipeline)))
        if department_count != 0:
            found = True
        else:
            print("That department could not be found.  Try again.")
    for department in Department.objects().aggregate(pipeline):
        return Department.objects(id=department.get('_id')).first()

# Check the construction of major and courses
def select_major(session: Session) -> Major:
    found: bool = False
    while not found:
        department = select_department(session)
        name = input("Enter department name -->")
        pipeline = [{"$match": {"$and": [{"department_name": department.name}, {"name": name}]}}]
        major_count = len(list(Major.objects().aggregate(pipeline)))
        if major_count != 0:
            found = True
        else:
            print("That major could not be found.  Try again.")
    for major in Major.objects().aggregate(pipeline):
        return Major.objects(id=major.get('_id')).first()

def select_course(session: Session) -> Course:
    found: bool = False
    while not found:
        department = select_department(session)
        name = input("Enter course name -->")
        pipeline = [{"$match": {"$and": [{"department_name": department.name}, {"name": name}]}}]
        course_count = len(list(Course.objects().aggregate(pipeline)))
        if course_count != 0:
            found = True
        else:
            print("That course could not be found.  Try again.")
    for course in Course.objects().aggregate(pipeline):
        return Course.objects(id=course.get('_id')).first()


def select_requirement(session: Session) -> Requirement:
    found: bool = False
    while not found:
        major = select_major(session)
        name = input("Enter requirement name -->")
        pipeline = [{"$match": {"$and": [{"major_name": major.name}, {"name": name}]}}]
        requirement_count = len(list(Major.objects().aggregate(pipeline)))
        if requirement_count != 0:
            found = True
        else:
            print("That requirement could not be found.  Try again.")
    for requirement in Requirement.objects().aggregate(pipeline):
        return Requirement.objects(id=requirement.get('_id')).first()

def list_department(session: Session):
    departments: [Department] = Department.objects().order_by('+name')
    for department in departments:
        print(department)


def list_course(session: Session):
    courses: [Course] = Course.objects().order_by('+department_name','+name')
    for course in courses:
        print(course)


def list_major(session: Session):
    majors: [Major] = Major.objects().order_by('+department_name','+name')
    for major in majors:
        print(major)

def list_requirement(session: Session):
    requirements: [Requirement] = Requirement.objects().order_by('+major_name','+name')
    for requirement in requirements:
        print(requirement)


def update_department(session: Session):
    department = select_department(session)
    new_name = input(f'Current name is: {department.name}.  Enter new name -->')
    try:
        # Necessary changes may be needed for child classes
        # Change the subsequent seminars ?
        '''
        for part in vendor.parts:
            part.vendorName = newName
            part.save()
        '''
        deparment.name = new_name
        department.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A Major or Course relies on this Department")


def update_course(session: Session):
    department = select_department(session)
    new_name = input(f'Current name is: {course.name}.  Enter new name -->')
    try:
        course.name = new_name
        course.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this course")


def update_major(session: Session):
    department = select_department(session)
    new_name = input(f'Current name is: {course.name}.  Enter new name -->')
    try:
        # Necessary changes may be needed for child classes
        # Change the subsequent seminars ?
        '''
        for part in vendor.parts:
            part.vendorName = newName
            part.save()
        '''
        major.name = new_name
        major.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this major")


def update_requirement(session: Session):
    major = select_major(session)
    new_first_name = input(f'Current name is: {instructor.first_name}.  Enter new name -->')
    try:
        instructor.first_name = new_first_name
        instructor.last_name = new_last_name
        instructor.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A Part relies on this office")


if __name__ == '__main__':
    print('Starting in main.')
    mongoengine.connect('BillofMaterials',
                        host='mongodb+srv://vincentcarreon01:8141329@billofmaterials.nblnu.mongodb.net/?retryWrites'
                             '=true&w=majority&appName=BillofMaterials')
    db = mongoengine.connection.get_db()
    monitoring.register(CommandLogger())
    sess: Session = db.client.start_session()
    main_action: str = ''
    while main_action != menu_mainME.last_action():
        main_action = menu_mainME.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
