from Timing import mostAccurateTime

class TimedEvent:
    
    def __init__(self):
        
        self.time = mostAccurateTime()
        
    def getTime(self):
        """Returns time for the event to execute."""
        return self.time
        
    def __cmp__(self, other):
        """Compares two TimedEvents."""
        return self.getTime() > other.getTime()
