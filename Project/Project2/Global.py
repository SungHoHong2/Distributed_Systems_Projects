import time

# constant values
READY = 1
FINISH = 2

# waiting for all processes to be at the same status
def waitWorker(type, queue):
    allSet = True
    while(True):
        time.sleep(1)
        allSet = True
        # print([i for i in queue])
        for i in range(0, len(queue)):
            if queue[i] != type:
                allSet = False
        if allSet == True:
            break

# dependency tracker
next = {
    'query_request':'query_receive',
    'query_receive': 'query_execute',
    'query_execute': 'query_reply',
    'query_reply': 'query_return',
    'deposit_request': 'deposit_receive',
    'deposit_receive': 'deposit_execute',
    'deposit_execute': 'deposit_reply',
    'deposit_reply': 'deposit_return',
    'withdraw_request': 'withdraw_receive',
    'withdraw_receive': 'withdraw_execute',
    'withdraw_execute': 'withdraw_reply',
    'withdraw_reply': 'withdraw_return',
}