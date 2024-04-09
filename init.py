import time
from multiprocessing import Process, Pipe, Event
from TC import transaction_coordinator
from Participant import doit
import sys

TIMEOUT = 2
FAILURE_DELAY = 10
RECOVERY_DELAY = 3


failure_scenarios = [
    "TC_before_prepare",
    "TC_after_one_commit",
    "participant_no_response",
    "participant_fail_after_yes",
    "NONE"
]
if __name__ == '__main__':
    k=1
    print("arguments needs to be numbers ")
    for i in failure_scenarios:
        print(f'{k}.{i}')
        k=k+1
    user_input = sys.argv[1]
    fail_type = failure_scenarios[int(user_input)-1]
    print()
    print()
    print(f"Failure Type: {fail_type}")
    TransactionCoordinator1, c1 = Pipe()
    TransactionCoordinator2, c2 = Pipe()
    t = Event()
    transactionCoordinator = Process(target=transaction_coordinator, args=(TransactionCoordinator1, TransactionCoordinator2, [fail_type], t))
    process1 = Process(target=doit, args=(c1, 1, [fail_type], t, 1))
    process2 = Process(target=doit, args=(c2, 2, [fail_type], t, 1))
    transactionCoordinator.start(), process1.start(), process2.start()
    transactionCoordinator.join(), process1.join(), process2.join()
    print()