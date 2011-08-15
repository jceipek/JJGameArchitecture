import os, time

# Define the mostAccurateTime function
if os.name == 'nt':
    mostAccurateTime = time.clock #time in seconds since program started (more accurate on Windows)
else:
    mostAccurateTime = time.time #time in seconds since epoch (more accurate on *nix)

class BasicTimer:
    """
    A basic timer which can keep track of the amount of time which has
    elapsed since a previous call.
    """
    
    def __init__(self):
        
        self.timeOfLastCall = mostAccurateTime()
        
    def reset(self):
        """
        Reset time of last call to current time, thus returning the
        difference between the current time and the last call to zero.
        """
        self.timeOfLastCall = mostAccurateTime()
    
    def getElapsedTime(self,reset=False):
        """
        Return the elapsed time since the last call, and make the time
        since the last call equal to the current time.
        """
        currentTime = mostAccurateTime()
        
        if reset:
            # calculate elapsed time and reset elapsed time to zero
            elapsedTime, self.timeOfLastCall = currentTime - self.timeOfLastCall, currentTime
        else:
            # calculate the elapsed time
            elapsedTime = currentTime - self.timeOfLastCall
            
        return elapsedTime

class StopWatch:
    """
    A stop watch which records time differences between a "start" and
    a "stop".
    """
    
    def __init__(self):
        
        self.startTime = mostAccurateTime()
        self.running = False
        
    def reset(self):
        """
        Reset the start time to the current time, thus returning the
        elapsed time to zero.
        """
        
        self.startTime = mostAccurateTime()
    
    def start(self):
        """Start the stop watch.  Returns the start time."""
        
        running, self.startTime = True, mostAccurateTime()
        return self.startTime
        
    def stop(self):
        """
        Stop the stop watch and return the elapsed time since the
        stop watch was started.
        """
        
        if running:
            dt, running = mostAccurateTime - self.startTime, False
        else:
            dt = 0
        return dt
