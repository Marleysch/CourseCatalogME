import mongoengine
from pymongo import monitoring
from pymongo.client_session import ClientSession
from mongoengine import ValidationError, OperationError, NotUniqueError
from pymongo.client_session import ClientSession
from CommandLogger import CommandLogger, log
from Menu import Menu
from input_utilities import input_int_range
from menu_definitions import (menu_main, add_select, delete_select, update_select, select_select)
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

def select(session):
    menu_loop(select_select, session)

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
        issub_requirement = input("Does the parent requirement exist?(Y/N)-->")
        if issub_requirement == 'Y':
            print('Define parent requirement:')
            parent_requirement = select_requirement(session)
        else:
            parent_requirement = None

        isparent_requirement = input('Does this requirement have sub requirements?(Y/n)-->')
        sub_requirements = []
        if isparent_requirement =='Y':
            while isparent_requirement != 'N':
                print('Define sub requirement:')
                sub_requirement = select_requirement(session)
                sub_requirements.append(sub_requirement)
                isparent_requirement = input('Are there more sub requirements?(Y/N)-->')

        type = int(input('Enter the type of requirement:\n\t1 for Total requirement\n\t2 for Mandatory requirement\n\t3 for Choice requirement\n-->'))
        if type == 1:
            try:
                total = Total(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                total.save()
                if parent_requirement is not None:
                    parent_requirement.add_sub_requirement(total)
                    parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=total)
                    courserequirement.save()
                for requirement in sub_requirements:
                    requirement.parent_requirement = total
                    requirement.save()
                    mandatory.add_sub_requirement(requirement)
                    mandatory.save()
                valid = True
            except Exception as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        if type == 2:
            try:
                mandatory = Mandatory(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                mandatory.save()
                if parent_requirement is not None:
                    parent_requirement.add_sub_requirement(mandatory)
                    parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=mandatory)
                    courserequirement.save()
                for requirement in sub_requirements:
                    requirement.parent_requirement = mandatory
                    requirement.save()
                    mandatory.add_sub_requirement(requirement)
                    mandatory.save()
                valid = True
            except Exception as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')
        if type == 3:
            try:
                choice = Choice(name=name, description=description, credits=credits, major=major, parent_requirement=parent_requirement)
                choice.save()
                if parent_requirement is not None:
                    parent_requirement.add_sub_requirement(choice)
                    parent_requirement.save()
                for course in courses:
                    courserequirement = CourseRequirement(course=course, requirement=choice)
                    courserequirement.save()
                for requirement in sub_requirements:
                    requirement.parent_requirement = choice
                    requirement.save()
                    mandatory.add_sub_requirement(requirement)
                    mandatory.save()
                valid = True
            except Exception as NUID:
                print(f'You violated a uniqueness constraint: {NUID}.  Try again')


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
            course_requirement = select_course_requirement_via_course(session, course)
            while course_requirement != "That course requirement could not be found. Try again.":
                course_requirement.delete()
                course_requirement = select_course_requirement_via_course(session, course)
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
            course_requirement = select_course_requirement_via_requirement(session, requirement)
            while course_requirement != "That course requirement could not be found. Try again.":
                course_requirement.delete()
                course_requirement = select_course_requirement_via_requirement(session, requirement)
            for prequirement in Requirement.objects:
                if requirement.name in prequirement.sub_requirement_names:
                    prequirement.remove_sub_requirement(requirement)
            requirement.delete()
            ok = True
            print(f'Department {requirement.name} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} courses are dependant on this department")



""""SELECTS"""
def select_course_requirement_via_course(session, course):
    found: bool = False
    while not found:
        pipeline = [{"$match": {"course": course.id}}]
        course_requirement_count = len(list(CourseRequirement.objects().aggregate(pipeline)))
        if course_requirement_count != 0:
            found = True
        else:
            return "That course requirement could not be found. Try again."
    for courserequirement in CourseRequirement.objects().aggregate(pipeline):
        return CourseRequirement.objects(id=courserequirement.get('_id')).first()

def select_course_requirement_via_requirement(session, requirement):
    found: bool = False
    while not found:
        pipeline = [{"$match": {"requirement": requirement.id}}]
        course_requirement_count = len(list(CourseRequirement.objects().aggregate(pipeline)))
        if course_requirement_count != 0:
            found = True
        else:
            return "That course requirement could not be found. Try again."
    for courserequirement in CourseRequirement.objects().aggregate(pipeline):
        return CourseRequirement.objects(id=courserequirement.get('_id')).first()

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
def update_requirement_name(session: Session):
    requirement = select_requirement(session)
    new_name = input(f'Current name is: {requirement.name}.  Enter new name -->')
    old_name = requirement.name
    try:
        requirement.name = new_name
        requirement.save()
        for requirement in Requirement.objects:
            if old_name in requirement.sub_requirement_names:
                requirement.sub_requirement_names.remove(old_name)
                requirement.sub_requirement_names.append(new_name)
                requirement.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this course")


def update_course_name(session: Session):
    course = select_department(session)
    new_name = input(f'Current name is: {course.name}.  Enter new name -->')
    try:
        course.name = new_name
        course.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this major")


def update_department_name(session: Session):
    department = select_department(session)
    new_name = input(f'Current name is: {department.name}.  Enter new name -->')
    try:
        department.name = new_name
        department.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A requirement relies on this major")


if __name__ == '__main__':
    print('Starting in main.')

    mongoengine.connect('Demonstration',host='mongodb+srv://marleyschneider01:Fire212121!@cecs-323-fall-2024.60zon.mongodb.net/?retryWrites=true&w=majority&appName=CECS-323-Fall-2024')
    db = mongoengine.connection.get_db()
    monitoring.register(CommandLogger())
    sess: Session = db.client.start_session()
    # print(select_course_requirement_via_requirement(sess, select_requirement(sess)))
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
