"""

"""

#In Windows, we must use threads instead of processes
#In Linux, we can use either (little difference). Processes may be slightly faster in some cases, but this is unverified.
#As such, we will use threads first and add process support later if we want.
#Sideline: Because of how cPython is implemented, only processes truly run simultaneously (but this doesn't matter for I/O systems)

class Server:
    def __init__(self):
        pass


class Receiver:
    def __init__(self):
        pass

class Sender:
    def __init__(self):
        pass

class Simulator:
    def __init__(self):
        pass