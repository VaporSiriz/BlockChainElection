from enum import Enum

class CandidateStatus(Enum):
    WAITING=0
    CANCEL=1
    REJECT=2
    APPROVE=3

class VoteStatus(Enum):
    PENDING='P'
    APPROVE='A'