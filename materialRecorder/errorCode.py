from enum import Enum, unique

class ErrorCode(Enum):
    Success=0
    RecordNotExist= -1
    SearchTypeNotExist=-2
    ChangeNameForbidden=-3
    ServerInternalError=-4
    MultiRecords=-5
    WrongInput=-6
