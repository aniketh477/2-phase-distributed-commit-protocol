import time
import simplejson
TIMEOUT = 2
FAILURE_DELAY = 10
RECOVERY_DELAY = 3

prepareMsg, commitMsg, abortMsg  = "PREPARE", "COMMIT", "ABORT"
Logs = set()
def transaction_coordinator(process1, process2, failure, isWorking):
    Transaction_Coordinator().transaction_coordinator(process1, process2, failure, isWorking)

class Transaction_Coordinator:
    def __init__(self):
       pass
    
    def send_commit(self, connection, pid):
        Logs.add(pid)
        connection.send(commitMsg)
    

    def transaction_coordinator(self, process1, process2, failure, isWorking):
        ps = [process1, process2]
        if "TC_before_prepare" in failure:
            print("TC: Failing before sending PREPARE")
            time.sleep(FAILURE_DELAY)
            isWorking.wait(RECOVERY_DELAY)
            for i in ps:
                i.send(prepareMsg)
        else:
            for i in ps:
                i.send(prepareMsg)

        response1, response2 = process1.recv() if process1.poll(TIMEOUT) else "NO", process2.recv() if process2.poll(TIMEOUT) else "NO"
        print("After TC send PREPARE ---> ","P-1 response:",response1, "; P-2 response:", response2)
        if response1 == "YES" and response2 == "YES":
            if "TC_after_one_commit" in failure:
                print("TC: Failing after sending one COMMIT")
                self.send_commit(process1, 1)
                f = open('output.txt', 'w')
                simplejson.dump(str(Logs), f)
                f.close()
                time.sleep(FAILURE_DELAY)
                isWorking.wait(RECOVERY_DELAY)
                if 2 not in Logs:
                    self.send_commit(process2, 2)
                f = open('output_after_failure.txt', 'w')
                simplejson.dump(str(Logs), f)
                f.close()    
            else:
                self.send_commit(process1,1)
                self.send_commit(process2,2)
        else:
            for i in ps:
                i.send(abortMsg)

        count = 0

        while count < 1 and "participant_fail_after_yes" in failure:
            sender, msg = None, None
            if process1.poll(TIMEOUT):
                sender, msg = 1, process1.recv()
            elif process2.poll(TIMEOUT):
                sender, msg = 2, process2.recv()

            if msg == "FETCH_COMMIT_INFO":
                count += 1
                if sender in Logs:
                    if sender == 1:
                        process1.send(commitMsg)
                    else:
                        process2.send(commitMsg)

        isWorking.set()

    

        