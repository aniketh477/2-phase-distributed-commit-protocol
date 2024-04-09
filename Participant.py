import time

def doit(connection, processID, fail_List, isWorking, fail_processID):
    Participant([2,10,3]).participant(connection, processID, fail_List, isWorking, fail_processID)

class Participant:
    def __init__(self,delayes):
        self.TIMEOUT, self.FAILURE_DELAY, self.RECOVERY_DELAY = delayes[0], delayes[1], delayes[2] #2, 10, 3
    

    def participant(self, connection, processID, fail_List, isWorking, fail_processID):
        if processID != fail_processID:
            fail_List = []

        if "participant_no_response" in fail_List:
            print(f"P-{processID}: Failing to respond(YES) to TC")
            time.sleep(self.FAILURE_DELAY)

        start_time = time.time()
        while not connection.poll(self.TIMEOUT):
            if (time.time() - start_time) > self.TIMEOUT:
                print(f"P-{processID}: ABORT")
                connection.send("NO")
                return

        prepare_msg = connection.recv()
        if "participant_no_response" in fail_List:
            time.sleep(1)
            connection.send("YES")

        if prepare_msg == "PREPARE":
            time.sleep(1)
            connection.send("YES")
            if "participant_fail_after_yes" in fail_List:
                print(f"P-{processID}: Failing after replying YES")
                time.sleep(self.FAILURE_DELAY)
        else:
            connection.send("NO")
        while not connection.poll(self.TIMEOUT):
            if isWorking.is_set():
                print(f"P-{processID}: ABORT")
                return

        des = connection.recv()

        if "participant_fail_after_yes" not in fail_List:
            #if (time.time() - start_time) > self.TIMEOUT:
              #  print(f"P-{processID}: ABORT")
               # connection.send("NO")
           # else:
            print(f"P-{processID}: {des}")

        if "participant_fail_after_yes" in fail_List:
            time.sleep(self.RECOVERY_DELAY)
            connection.send("FETCH_COMMIT_INFO")
            fetched_des = connection.recv()
            print(f"P-{processID}: Fetched Info from TC : {fetched_des}")

        if des == "COMMIT":
            return
