"""

"""

#In Windows, we must use threads instead of processes
#In Linux, we can use either (little difference). Processes may be slightly faster in some cases, but this is unverified.
#As such, we will use threads first and add process support later if we want.
#Sideline: Because of how cPython is implemented, only processes truly run simultaneously (but this doesn't matter for I/O access (according to the docs, that type of activity is still improved with threads))

import time
import Queue

try:
    import threading
except:
    raise Exception("Unable to load threading Python module.")

class TrueThread(threading.Thread):
    """
    A wrapper for multiple threads based on Allen Downey's threading wrapper.
    """
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        #self.daemon = True
        self.start()

class Server:
    def __init__(self):
        receiver = Receiver()
        simulator = Simulator(receiver)

class Receiver:
    def __init__(self):
        self.simulatorQueue = Queue.Queue(maxsize=0) #No size limit; may want to use priority queues once events are actually sent (and sort by time)
        self.proc = TrueThread(self.listen)

    def listen(self):
        while True:
            print "Listening"
            time.sleep(1) #Pause in order to not freeze the program
            #Check if message was received from client
            self.receiveIfNecessary()

    def getMessageQueue(self):
        return self.simulatorQueue

    def receiveIfNecessary(self):
        received = True
        if received:
            self.simulatorQueue.put("Test")

class Sender:
    def __init__(self):
        self.proc = None

class Simulator:
    def __init__(self, receiver):
        self.messageQueue = receiver.getMessageQueue()
        self.proc = TrueThread(self.simulate)

    def simulate(self):
        while True:
            print "Simulating"
            time.sleep(0.1)

            try:
                print self.messageQueue.get(False) #Do not block
            except:
                print "Message Queue is empty"

if __name__ == '__main__':
    aServer = Server()