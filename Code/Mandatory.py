from mongoengine import *
from Requirement import Requirement
from Major import Major


class Mandatory(Requirement):

    def __init__(self, major: Major, name: str, description: str, credits: int, parent_requirement=None, courses=[],
                 sub_requirememnt_names=[], **kwargs):
        super().__init__(major=major, name=name, description=description, credits=credits,
                         parent_requirement=parent_requirement, courses=courses,
                         sub_requirememnt_names=sub_requirememnt_names, **kwargs)

    def __str__(self):
        return f'Mandatory {super().__str__()}'

