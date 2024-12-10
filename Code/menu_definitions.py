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
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Department", "add_department(sess)"),
    Option("Major", "add_major(sess)"),
    Option("Course", "add_course(sess)"),
    Option("Requirement", "add_requirement(sess)"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    # Option("Automotive manufacturer", "delete_manufacturer(sess)"),
    Option("Department", "delete_department(sess)"),
    Option("Major", "delete_major(sess)"),
    Option("Course", "delete_course(sess)"),
    Option("Requirement", "delete_requirement(sess)"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu('update select', 'Which type of object do you want to update:', [
    Option("Focus Area Name", "update_focus_area_name(sess)"),
    Option("Requirement Name", "update_requirement_name(sess)"),
    Option("Department Name", "update_department_name(sess)"),
    Option("Course Name", "update_course_name(sess)"),
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


