# Lab 4B - Task 5 - a promotion that broke the payroll history
#
# 5.1  The is-a test must hold for the WHOLE LIFE of the object. "A lecturer
#      is an employee" breaks on promotion: the same person keeps existing,
#      only the ROLE changes - and roles change more often than people do.
#      So Lecturer(Employee) was the wrong model: a role is not a kind of
#      employee, it is a STATE of an employee.
#
# 5.2  Redesigned: Employee HAS-A role object. LecturerRole(hours) and
#      HeadRole(salary) each own their pay rule; employee.monthly_pay()
#      simply asks the role - no if on the kind of role anywhere.
#
# 5.3  employee.change_role(new_role): the emp_id and the object stay the
#      same. The old pair of subclasses had to delete the Lecturer and
#      create a NEW HeadOfDepartment with a new id - payroll, timesheets
#      and access lists then pointed at a dead object.
#
# 5.4  Employee keeps own history of (role, start_date): COMPOSITION - the
#      entries exist only inside that employee and die with him
#      ("does the part disappear with the whole?" - yes).
#
# Done when: a promotion does not create a new Employee, references from
#            other objects still work, monthly_pay() has no if on the role.

from abc import ABC, abstractmethod
from datetime import date

import pytest


class Role(ABC):
    @abstractmethod
    def monthly_pay(self) -> int:
        """The pay rule this role brings."""


class LecturerRole(Role):
    def __init__(self, hours: int) -> None:
        self.hours = hours

    def monthly_pay(self) -> int:
        return self.hours * 120_000


class HeadRole(Role):
    def __init__(self, salary: int) -> None:
        self.salary = salary

    def monthly_pay(self) -> int:
        return self.salary + 3_000_000        # management bonus


class Employee:
    def __init__(self, emp_id: int, name: str, role: Role) -> None:
        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.role_history: list[tuple[Role, date]] = [(role, date.today())]

    # 5.3 - promote WITHOUT replacing the object.
    def change_role(self, new_role: Role, *, start_date: date | None = None) -> None:
        self.role = new_role
        self.role_history.append((new_role, start_date or date.today()))

    def monthly_pay(self) -> int:
        return self.role.monthly_pay()        # asks the role: no if anywhere


# --------------------------- tests ---------------------------

def test_promotion_keeps_the_same_object_and_id():
    lecturer = Employee(7, "Dilnoza", LecturerRole(160))
    payroll_ref = lecturer             # "the payroll history points here"

    lecturer.change_role(HeadRole(14_000_000))

    assert payroll_ref is lecturer            # references still work
    assert lecturer.emp_id == 7               # no new id
    assert lecturer.monthly_pay() == 17_000_000


def test_monthly_pay_follows_the_current_role():
    hired = Employee(7, "Dilnoza", LecturerRole(160))
    promoted = Employee(7, "Dilnoza", HeadRole(14_000_000))
    assert hired.monthly_pay() == 160 * 120_000
    assert promoted.monthly_pay() == 17_000_000


def test_role_history_records_when_each_role_started():
    emp = Employee(7, "Dilnoza", LecturerRole(160))
    emp.change_role(HeadRole(14_000_000), start_date=date(2026, 11, 1))

    assert len(emp.role_history) == 2
    assert isinstance(emp.role_history[0][0], LecturerRole)
    assert isinstance(emp.role_history[1][0], HeadRole)
    assert emp.role_history[1][1] == date(2026, 11, 1)


def test_last_months_payroll_uses_last_months_role():
    # A past payroll run picks the role that was active on that date.
    emp = Employee(7, "Dilnoza", LecturerRole(160))
    emp.change_role(HeadRole(14_000_000), start_date=date(2026, 11, 1))

    last_month_pay = emp.role_history[0][0].monthly_pay()
    assert last_month_pay == 160 * 120_000    # LecturerRole's rule
