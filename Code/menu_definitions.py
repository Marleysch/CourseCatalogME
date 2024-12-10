from Menu import Menu
from Option import Option

"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on the various object types
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add(sess)"),
    Option("Delete existing instance", "delete(sess)"),
    Option("List existing instances", "list_members(sess)"),
    Option("Select existing instance", "select(sess)"),
    Option("Update existing instance", "update(sess)"),
    Option("Flush", "sess.flush()"),
    Option("Commit", "sess.commit()"),
    Option("Abort", "sess.rollback()"),
    Option("Exit", "pass")
])

menu_mainME = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add(sess)"),
    Option("Delete existing instance", "delete(sess)"),
    Option("List existing instances", "list_members(sess)"),
    Option("Select existing instance", "select(sess)"),
    Option("Update existing instance", "update(sess)"),
    Option("Exit", "pass")
])

menu_main_mongo = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add(sess)"),
    Option("Delete existing instance", "delete(sess)"),
    Option("List existing instances", "list_members(sess)"),
    Option("Select existing instance", "select(sess)"),
    Option("Update existing instance", "update(sess)"),
    Option("Commit", "sess.commit_transaction()"),
    Option("Abort", "sess.abort_transaction()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    # Option("Automotive manufacturer", "add_manufacturer(sess)"),
    Option("Building", "add_building(sess)"),
    Option("Office", "add_office(sess)"),
    Option("Instructor", "add_instructor(sess)"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    # Option("Automotive manufacturer", "delete_manufacturer(sess)"),
    Option("Building", "delete_building(sess)"),
    Option("Office", "delete_office(sess)"),
    Option("Instructor", "delete_instructor(sess)"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    # Option("Automotive manufacturer", "list_manufacturer(sess)"),
    # Option("Car Model", "list_car_model(sess)"),
    # Option("Vendor", "list_vendors(sess)"),
    # Option("Piece Part", "list_piece_parts(sess)"),
    Option("Offices and their instructors", "list_offices_and_instructors(sess)"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    # Option("Automotive manufacturer", "print(select_manufacturer(sess))"),
    Option("Building", "print(select_building(sess))"),
    Option("Instructor", "print(select_instructor(sess))"),
    Option("Office", "print(select_office(sess))"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu('update select', 'Which type of object do you want to update:', [
    # Option("Automotive manufacturer", "update_manufacturer(sess)"),
    # Option("Car Model", "update_car_model(sess)"),
    Option("Instructor first name", "update_instructor_first_name(sess)"),
    Option("Instructor last name", "update_instructor_last_name(sess)"),
    Option("Building name", "update_building_name(sess)"),
    # Option("Piece Part Description", "update_piece_part_description(sess)"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])

# A menu to prompt for the amount of logging information for MongoEngine.
menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

yes_no = Menu("yes/no", 'Answer yes or no:', [
    Option('Yes', 'yes'),
    Option('No', 'no')
])

transmission_type = Menu('transmission type', 'Please select a transmission type:', [
    Option('Automatic', 'automatic'),
    Option('Manual', 'manual'),
    Option('Continuously Variable', 'CVT'),
    Option('Semi-Automatic', 'semi-automatic')
])
