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
