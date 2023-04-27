from numpy._typing import ArrayLike

from Backend.Models.course import Course, Sequence
from Backend.Models.unit import Unit
from typing import Iterable


# todo: write tests for all of these conditions
class Condition:
    """Base class for modeling constraint conditions"""

    # todo: consider using kwargs, fixed args may not be flexible enough. for example, some conditions may need to know
    #  the completed units, some might need to know the course being taken, etc.
    def check(self, **kwargs) -> bool:
        """
        Checks if the condition has been fulfilled

        :key units_completed:
        :key units_enrolled:
        :key enrolled_course:
        :key enrolled_sequence:
        :key current_wam:

        :return: True if the condition is met, otherwise False
        """
        raise NotImplementedError("Subclasses should implement this")


class MinimumNumberOfUnitsCondition(Condition):
    """Fulfilled when a minimum number of units is completed from a pre-defined set of units"""

    def __init__(self, unit_set: Iterable[Unit], minimum_count: int):
        self.set = set(unit_set)
        self.min = minimum_count

    def check(self, units_completed: Iterable[Unit], **kwargs) -> bool:
        units_completed = set(units_completed)
        return len(self.set.intersection(units_completed)) >= self.min


class PrerequisitesFulfilledCondition(Condition):
    """Fulfilled when all the units from a pre-defined set of units has been completed"""

    def __init__(self, prerequisite_units: Iterable[Unit]):
        # todo: repeated across constructors, consider using super class for pre-processing constructor args
        self.prerequisites = set(prerequisite_units)

    def check(self, units_completed: Iterable[Unit], **kwargs) -> bool:
        units_completed = set(units_completed)
        return self.prerequisites.issubset(units_completed)


# todo: having prerequisites and corequisites condition may be redundant
class CorequisitesFulfilledCondition(Condition):
    """Fulfilled when all the units from a pre-defined set of units has been completed or is being completed"""

    def __init__(self, corequisite_units: Iterable[Unit]):
        self.corequisites = set(corequisite_units)

    def check(self, units_completed: Iterable[Unit], units_enrolled: Iterable[Unit], **kwargs) -> bool:
        units_completed_or_enrolled = set(units_completed).union(units_enrolled)
        return self.corequisites.issubset(units_completed_or_enrolled)


# todo: may be redundant with coreqs condition
class MutualExclusiveUnitsCondition(Condition):
    """Fulfilled if none of the units from a pre-defined set of units has been completed or is being completed"""

    def __init__(self, incompatible_units: Iterable[Unit]):
        self.incompatible_units = set(incompatible_units)

    def check(self, units_completed: Iterable[Unit], units_enrolled: Iterable[Unit], **kwargs) -> bool:
        units_completed_or_enrolled = set(units_completed).union(units_enrolled)
        return bool(self.incompatible_units.intersection(units_completed_or_enrolled))


class EnrolledInSequenceCondition(Condition):
    """Fulfilled if the student is enrolled in the specified major/minor sequence"""

    def __init__(self, sequence: Sequence):
        self.sequence = sequence

    def check(self, enrolled_sequence: Sequence, **kwargs) -> bool:
        return self.sequence == enrolled_sequence


class EnrolledInCourseCondition(Condition):
    """Fulfilled if the student is enrolled in the specified course"""

    def __init__(self, course: Course):
        self.course = course

    def check(self, enrolled_course: Course, **kwargs) -> bool:
        return self.course == enrolled_course


class MinimumWamCondition(Condition):
    """Fulfilled if the student has the minimum amount of WAM"""

    def __init__(self, minimum_wam: float):
        self.minimum_wam = minimum_wam

    def check(self, current_wam: float, **kwargs) -> bool:
        return current_wam >= self.minimum_wam


class Constraint:
    def __init__(self):
        self.conditions: list[Condition] = []

    def is_fulfilled(self,
                     units_completed: Iterable[Unit],
                     units_enrolled: Iterable[Unit],
                     enrolled_course: Course,
                     enrolled_sequence: Sequence,
                     current_wam: float) -> bool:

        enrollment_info = {
            "units_completed": units_completed,
            "units_enrolled": units_enrolled,
            "enrolled_course": enrolled_course,
            "enrolled_sequence": enrolled_sequence,
            "current_wam": current_wam
        }

        return all([condition.check(**enrollment_info) for condition in self.conditions])
