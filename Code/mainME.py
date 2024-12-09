import mongoengine
from pymongo import monitoring
from pymongo.client_session import ClientSession
from mongoengine import ValidationError, OperationError, NotUniqueError
from pymongo.client_session import ClientSession
from CommandLogger import CommandLogger, log
from Menu import Menu
from input_utilities import input_int_range
from menu_definitions import (menu_mainME, add_select, delete_select, list_select, select_select, update_select)
from Building import Building
from Instructor import Instructor
from FullTimeInstructor import FullTimeInstructor
from PartTimeInstructor import PartTimeInstructor
from Office import Office
from SharedOffice import SharedOffice
from SingleOffice import SingleOffice


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


def add_building(session: Session):
    valid: bool = False
    while not valid:
        # check valid position (B4)
        position_area = input("Enter grid position letter -->")
        position_num = input_int_range("Enter grid position num -->", 1, 9)
        name = input("Enter building name -->")
        position = ''.join([position_area.upper(), position_num])
        try:
            building = Building(name, position)
            building.save()
            valid = True
        except NotUniqueError as NUID:
            print(f'You violated a uniqueness constraint: {NUID}.  Try again')


def add_instructor(session: Session):
    valid: bool = False
    while not valid:
        first_name = input("Enter instructor's first name -->")
        last_name = input("Enter instructor's last name -->")
        instructor_id = input_int_range("Enter the identification number of instructor-->", 0, 2000)
        # institute a creator depending on time
        # ex. PartTimeInstructor(instructor_id, last_name, first_name)
        # Instructor creator makes it so no other of one id can exist
        try:
            instructor = Instructor(instructor_id, last_name, first_name)
            instructor.save()
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
'''
def add_schedule(session: Session):
    valid: bool = False
    while not valid:
        # implement an addition for holiday
        employee: Employee = select_employee(session)
        work_day: WorkDay = select_work_day(session)
        shift: Shift = select_shift(session)
        try:
            schedule = Schedule(employee, work_day, shift)
            session.add(schedule)
            session.flush()
            valid = True
        except IntegrityError as IE:
            print(f'Error type: {IE.__class__.__name__} was raised.')
            print("There must be an existing schedule conflict.")
            session.rollback()
    session.commit()
'''
def delete_building(session: Session):
    ok: bool = False
    while not ok:
        building: Building = select_building(session)
        try:
            building.delete()
            ok = True
            print(f'Address {str(building)} deleted.')
        except OperationError as OE:
            print(f"Error: {OE} Office(s) has office hours in this building")


# check relation office <--> instructor
def delete_office(session: Session):
    office: Office = select_office(session)
    building = office.building
    building.remove_office(building)
    building.save()
    office.delete()


def delete_instructor(session: Session):
    ok: bool = False
    while not ok:
        instructor: Instructor = select_instructor(session)
        try:
            # instructor.officeHours, cascade delete all office hours
            '''
            if len(vendor.parts) >= 1:
                for part in vendor.parts:
                    part.delete()
            '''
            instructor.delete()
            ok = True
            print(f'Instructor {instructor.id} deleted.')
        except ValidationError as VE:
            print(f"Invalid data: {VE}.  Try again.")


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


def select_building(session: Session) -> Building:
    found: bool = False
    zipcode: int = 0
    while not found:
        name = input("Enter building name -->")
        pipeline = [{"$match": {"name": name}}]
        building_count = len(list(Building.objects().aggregate(pipeline)))
        if building_count != 0:
            found = True
        else:
            print("That building could not be found.  Try again.")
    for building in Building.objects().aggregate(pipeline):
        return Building.objects(id=building.get('_id')).first()


def select_instructor(session: Session) -> Instructor:
    found: bool = False
    instructor_id: int = 0
    while not found:
        instructor_id = input_int_range("Enter the identification number of instructor-->", 0, 2000)
        pipeline = [{"$match": {"id": instructor_id}}]
        id_count = len(list(Instructor.objects().aggregate(pipeline)))
        if id_count != 0:
            found = True
        else:
            print("That instructor could not be found.  Try again.")
    for instructor in Instructor.objects().aggregate(pipeline):
        return Instructor.objects(id=instructor.get('_id')).first()


def select_office(session: Session) -> Office:
    found: bool = False
    while not found:
        building = select_building(session)
        room_number = input_int_range(f"Enter the room number in building: {building.name}-->", 0, 2000)
        pipeline = [{"$match": {"$and": [{"building_name": building.name}, {"number": room_number}]}}]
        office_count = len(list(Office.objects().aggregate(pipeline)))
        if office_count != 0:
            found = True
        else:
            print("That office could not be found.  Try again.")
    for office in Office.objects().aggregate(pipeline):
        return Office.objects(id=office.get('_id')).first()


def list_building(session: Session):
    buildings: [Building] = Building.objects().order_by('+name')
    for building in buildings:
        print(building)


def list_instructor(session: Session):
    instructors: [Instructor] = Instructor.objects().order_by('+id')
    for instructor in instructors:
        print(instructor)


def list_office(session: Session):
    # select a given building, print out all its offices
    offices: [Office] = Office.objects().order_by('+name', '+number')
    for office in offices:
        print(office)


def update_building(session: Session):
    building = select_building(session)
    new_name = input(f'Current name is: {building.name}.  Enter new name -->')
    try:
        # Necessary changes may be needed for child classes
        # Change the subsequent seminars ?
        '''
        for part in vendor.parts:
            part.vendorName = newName
            part.save()
        '''
        building.name = new_name
        building.save()
    except NotUniqueError as NUID:
        print(f'You violated a uniqueness constraint: {NUID}.  Try again')
    except OperationError as OE:
        print(f"Error: {OE} A Part relies on this office")


def update_instructor(session: Session):
    instructor = select_instructor(session)
    new_first_name = input(f'Current name is: {instructor.first_name}.  Enter new name -->')
    new_last_name = input(f'Current name is: {instructor.last_name}.  Enter new name -->')
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
