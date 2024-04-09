1.TC_before_prepare
2.TC_after_one_commit
3.participant_no_response
4.participant_fail_after_yes
5.NONE

Running Formmate:
python3 init.py <nth failure_type>

Example outputs:
Failure Type: TC_after_one_commit
After TC send PREPARE --->  P-1 response: YES ; P-2 response: YES
TC: Failing after sending one COMMIT
P-1: COMMIT
P-2: ABORT