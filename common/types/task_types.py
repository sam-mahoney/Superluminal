from enum import Enum, auto


class Status(Enum):
    """
    Represents the status of a given Task

    -------------------------------------
    | ENUM      | DESCRIPTION
    -------------------------------------
    | WAITING   : Task is in the Queue
    | EXECUTING : Implant has taken the Task from the Queue
    | EXECUTED  : Implant has successfully executed the Task and sent the Result
    | FAILED    : Implant failed to execute the Task
    -------------------------------------
    """
    WAITING = auto()
    EXECUTING = auto()
    EXECUTED = auto()
    FAILED = auto()
