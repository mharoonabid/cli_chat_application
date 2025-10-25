from enum import Enum


class ResType(Enum):
    PRIVATE = 0
    PUBLIC = 1
    SERVER = 2

class ReqType(Enum):
    LOGIN = 0
    SIGNUP = 1
    PUBLIC = 2
    PRIVATE = 3