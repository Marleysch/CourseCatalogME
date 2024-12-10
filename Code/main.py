import mongoengine
from pymongo import monitoring
from pymongo.client_session import ClientSession
from mongoengine import ValidationError, OperationError, NotUniqueError
from pymongo.client_session import ClientSession
from CommandLogger import CommandLogger, log
from Menu import Menu
from input_utilities import input_int_range
from menu_definitions import (menu_main, add_select, delete_select, update_select)
from Department import Department
from Major import Major
from Course import Course
from Requirement import Requirement
from CourseRequirement import CourseRequirement
from Total import Total
from Choice import Choice
from Mandatory import Mandatory

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


def delete(session: Session):
    """Top level menu prompt for any delete operation."""
    menu_loop(delete_select, session)


def update(session: Session):
    """Top level menu prompt for any update operation."""
    menu_loop(update_select, session)


"""ADDS"""
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
        number = int(input("Enter course number -->"))
        description = input(f'Write a description of {name} course-->')
        units = input_int_range("Enter the units of this course-->", 1, 4)
        requirement_exists = input("Do any of this courses requirements exist?(Y/N)-->")
        requirements = []
        if requirement_exists == 'Y':
            more_requirements = 'Y'
            while more_requirements != 'N':
                requirement = select_requirement(session)
                requirements.append(requirement)
                more_requirements = input("Is this course part of more requirements?(Y/N)-->")
        try:
            course = Course(department=department, name=name, departments_abbr = department.abbreviation, number=number, description=description, units=units)
            course.save()
            for requirement in requirements:
                courserequirement = CourseRequirement(course = course, requirement=requirement)
                courserequirement.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')
            
def add_requirement(session: Session):
    valid: bool = False
    while not valid:
        major: Major = select_major(session)
        name = input("Enter requirement name -->")
        description = input(f'Write a description of {name} requirement-->')
        credits = input_int_range("Enter the credits for this requirement-->", 1, 150)
        course_exists = input("Do any of this requirements courses exist?(Y/N)-->")
        courses = []
        if course_exists == 'Y':
            more_courses = 'Y'
            while more_courses != 'N':
                course = select_course(session)
                courses.append(course)
                more_courses = input("Does this requirement have more courses?(Y/N)-->")
        sub_requirement = input("Is this a subrequirement?(Y/N)-->")
        if sub_requirement == 'Y':
            print('Define parent requirement:')
            parent_requirement = select_requirement(session)
        else:
            parent_requirement = None

        type = int(input('Enter the type of requirement:\n\t1 for Total requirement\n\t2 for Mandatory requirement\n\t3 for Choice requirement\n-->'))
        if type == 1:
            try:
                total = Total(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                total.save()
                parent_requirement.add_sub_requirement(total)
                parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=total)
                    courserequirement.save()
                valid = True
            except NotUniqueError as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        if type == 2:
            try:
                mandatory = Mandatory(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                mandatory.save()
                parent_requirement.add_sub_requirement(mandatory)
                parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=mandatory)
                    courserequirement.save()
                valid = True
            except NotUniqueError as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        if type == 3:
            try:
                choice = Choice(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                choice.save()
                parent_requirement.add_sub_requirement(choice)
                parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=choice)
                    courserequirement.save()
                valid = True
            except NotUniqueError as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')


# def add_office_hours(session: Session):
#     valid: bool = False
#     while not valid:
#         office: Office = select_office(session)
#         instructor: Instructor = select_instructor(session)
#         office_hour = (office, instructor)
#         # implement a choice for shared or single
#         try:
#             office.save()
#             office_hour.add(office)
#             office_hour.save()
#             valid = True
#         except ValidationError as VE:
#             print(f"Invalid data: {VE}.  Try again.")
#         except NotUniqueError as NUID:
#             print(f'You violated a uniqueness constraint: {NUID}.  Try again')

"""DELETES"""
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
    ok: bool = False
    while not ok:
        major: Major = select_major(session)
        try:
            major.delete()
            ok = True
            print(f'Department {major.name} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} courses are dependant on this department")

def delete_course(session: Session):
    ok: bool = False
    while not ok:
        course: Course = select_course(session)
        try:
            course.delete()
            ok = True
            print(f'Department {course.name} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} courses are dependant on this department")

def delete_requirement(session: Session):
    ok: bool = False
    while not ok:
        requirement: Requirement = select_requirement(session)
        try:
            requirement.delete()
            ok = True
            print(f'Department {requirement.name} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} courses are dependant on this department")



""""SELECTS"""
def select_department(session: Session) -> Department:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter department name -->")
        pipeline = [{"$match": {"name": name}}]
        department_count = len(list(Department.objects().aggregate(pipeline)))
        if department_count != 0:
            found = True
        else:
            print("That department could not be found.  Try again.")
    for department in Department.objects().aggregate(pipeline):
        return Department.objects(id=department.get('_id')).first()

# Check the construction of major and courses
def select_major(session: Session) -> Major:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter major name -->")
        pipeline = [{"$match": {"name": name}}]
        major_count = len(list(Major.objects().aggregate(pipeline)))
        if major_count != 0:
            found = True
        else:
            print("That major could not be found.  Try again.")
    for major in Major.objects().aggregate(pipeline):
        return Major.objects(id=major.get('_id')).first()

def select_course(session: Session) -> Course:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter course name -->")
        pipeline = [{"$match": {"name": name}}]
        course_count = len(list(Course.objects().aggregate(pipeline)))
        if course_count != 0:
            found = True
        else:
            print("That course could not be found.  Try again.")
    for course in Course.objects().aggregate(pipeline):
        return Course.objects(id=course.get('_id')).first()


def select_requirement(session: Session) -> Requirement:
    found: bool = False
    name: str = ''
    while not found:
        name = input("Enter requirement name -->")
        pipeline = [{"$match": {"name": name}}]
        requirement_count = len(list(Requirement.objects().aggregate(pipeline)))
        if requirement_count != 0:
            found = True
        else:
            print("That requirement could not be found.  Try again.")
    for requirement in Requirement.objects().aggregate(pipeline):
        return Requirement.objects(id=requirement.get('_id')).first()



"""UPDATES"""
def update_focus_area_name(session: Session):
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


def update_requirement_name(session: Session):
    department = select_department(session)
    new_name = input(f'Current name is: {course.name}.  Enter new name -->')
    try:
        course.name = new_name
        course.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this course")


def update_course_name(session: Session):
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


def update_department_name(session: Session):
    pass
    # major = select_major(session)
    # new_first_name = input(f'Current name is: {instructor.first_name}.  Enter new name -->')
    # try:
    #     instructor.first_name = new_first_name
    #     instructor.last_name = new_last_name
    #     instructor.save()
    # except NotUniqueError as NUID:
    #     print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    # except OperationError as OE:
    #     print(f"Error: {OE} A Part relies on this office")


if __name__ == '__main__':
    print('Starting in main.')
    mongoengine.connect('Demonstration',host='mongodb+srv://marleyschneider01:Fire212121!@cecs-323-fall-2024.60zon.mongodb.net/?retryWrites=true&w=majority&appName=CECS-323-Fall-2024')
    db = mongoengine.connection.get_db()
    monitoring.register(CommandLogger())
    sess: Session = db.client.start_session()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
