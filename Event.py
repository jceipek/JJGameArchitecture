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
        
"""
Event Module
--------------------
Summary: Executes events* when needed.

*An event is a distinct temporal event that results in a well-defined 
(i.e. non-random) state-change. For ease of use, an event may optionally
be a wrapper for executing a sequence of other events at specific times.
Such a wrapper is not intended to be used as a way to control animation 
curves (for example, ease-in and ease-out curves), which is best achieved
using a system in which the active velocity function can be changed.

The state change encoded in an event may take the form of a delta change
(as in: increase velocity by 10u/s) or an absolute command (set velocity 
to 5m/s).

Events are forbidden from performing rendering related functions (for example,
drawing a sprite at a location), but may perform actions involving object
creation and manipulation that will eventually be rendered

Detailed Description:
Examines the timestamps of the events on the event queue and manages the 
creation and deletion of threads/processes to execute those events. The queue
is not a queue in the traditional sense in that adding an event inserts that
event 

"""

import time

class Manager:

    def __init__(self):
        #Create the event Queue, or register with it, as the case may be
        pass

    def addEvent(self, event):
        #Add event to the queue
        pass

    def tick(self):
        #Called as often as possible, at the system management level

        #Loop through the top events in the queue, such that we have the next n
        #events until a certain timestamp, where n is <= the max thread/proc
        #count allocated for the event module

        #For each of these n events, assign the event to an executor that exists
        #or make a new one (this way, multiple events can be executed at once)

        pass

class AbstractQueue:
    def __init__(self):
        """
        Sets up the event queue using a currently undefined structure
        (possibly a mix of a dictionary and an array????)
        """
        pass

    def addEvent(self,event):
        """
        Adds 'event' chronologically to the queue
        """
        pass

    def popNextEvent(self):
        """
        Returns the newest event while removing it (if an event exists)
        """
        pass

    def getNextEvent(self):
        """
        Returns the newest event, leaving it on the queue (if an event exists)
        """
        pass

    def getEventCount(self):
        """
        Returns the amount of events on the queue
        """
        # (Dev Note: remember, direct object access by 
        # an external system is BAD for extensibility and modular design)
        pass

    def getEventAtIndex(self,index):
        """
        Returns the event at the given index, if it exists.
        """
        pass

    def removeEventAtIndex(self,index):
        """
        Destroys the event at index, returning nothing
        """
        pass

    def getEventIterator(self):
        """
        Returns an iterator object for all of the events on the queue
        """
        pass

class Executor: #inherits from a thread/process class like Allen Downey's, but
                # with more intelligence about its own existence.
    # It should be some kind of daemon that does not interrupt
    # standard execution flow

    #Executors must die if they have no event for a certain amount of time
    def __init__(self):
        pass

import Queue, Timing

from heapq import heappush, heappop
class HeapSortList:
    
    def __init__(self):
        
        self._list = []
    
    def append(self, item):
        heappush(self._list, item)
    
    def pop(self):
        return heappop(self._list)
        
    def __len__(self):
        return len(self._list)

from threading import Timer

class EventQueue4:
    
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self.executedEvents = []
        
    def addEvent(self,event):
        timeDelay = event.getTime()-Timing.mostAccurateTime()
        
        if timeDelay >= 0:
            Timer(timeDelay,self.executedEvents.append,[event]).start()

class EventQueue3:
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self._queue = Queue.PriorityQueue()
        
    def addEvent(self,event):
        self._queue.put_nowait(event)
        
    def getNextEvents(self, currentTime=None):
        """
        Returns the events which have yet to be executed and occur before
        currentTime.
        """
        if currentTime is None: currentTime = Timing.mostAccurateTime()
        
        events = []
        
        queueEmptyFunc = self._queue.empty
        
        while not queueEmptyFunc():
        
            event = self._queue.get_nowait()
            if event.getTime() <= currentTime:
                events.append(event)
            else:
                self._queue.put_nowait(event)
                break
                
        return events

class EventQueue2a:
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self._list = list()
        
    def addEvent(self,event):
        self._list.append(event)
        
    def getNextEvents(self, currentTime=None):
        """
        Returns the events which have yet to be executed and occur before
        currentTime.
        """
        if currentTime is None: currentTime = Timing.mostAccurateTime()
        
        events = []
        appendToEvents = events.append
        self._list.sort()
        for it in xrange(len(self._list)):
            if self._list[0].getTime() <= currentTime:
                appendToEvents(self._list.pop(0))
            else:
                break
                
        return events

class EventQueue2:
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self._list = SortCacheList()
        
    def addEvent(self,event):
        self._list.append(event)
        
    def getNextEvents(self, currentTime=None):
        """
        Returns the events which have yet to be executed and occur before
        currentTime.
        """
        if currentTime is None: currentTime = Timing.mostAccurateTime()
        
        events = []
        appendToEvents = events.append
        self._list.sort()
        for it in xrange(len(self._list)):
            if self._list[0].getTime() <= currentTime:
                appendToEvents(self._list.pop(0))
            else:
                break
                
        return events

class EventQueue1:
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self.queue = HeapSortList()
        
        if startTime is None: startTime = Timing.mostAccurateTime()
        self.lastTime = startTime

    def addEvent(self,event):
        """
        Adds 'event' chronologically to the queue
        """
        eventTime = event.getTime()
        if eventTime > self.lastTime:
            self.queue.append(event)
            return True
        else:
            print 'Warning: event missed.'
            return False

    def getNextEvents(self, currentTime=None):
        """
        Returns the events which have yet to be executed and occur before
        currentTime.
        """
        if currentTime is None: currentTime = Timing.mostAccurateTime()
        
        events = []
        appendToEventList = events.append
        for it in xrange(len(self.queue)):
            event = self.queue.pop()
            if currentTime >= event.getTime():
                appendToEventList(event)
            else:
                # add event back to queue
                self.queue.append(event)
                break
        return events
        
class EventQueue:
    def __init__(self, startTime = None):
        """
        Sets up the event queue, which is a dictionary using keys
        of the form int(time.time).  The keys point to SortCacheLists,
        which store the events.
        """
        
        self.queuedEvents = {}
        
        if startTime is None: startTime = Timing.mostAccurateTime()
        self.lastTime = startTime

    def addEvent(self,event):
        """
        Adds 'event' chronologically to the queue
        """
        eventTime = event.getTime()
        if eventTime > self.lastTime:
            self.queuedEvents.setdefault( int(eventTime), SortCacheList() ).append(event)
            return True
        else:
            print 'Warning: event missed.'
            return False

    def getNextEvents(self, currentTime=None):
        """
        Returns the events which have yet to be executed and occur before
        currentTime.
        """
        if currentTime is None: currentTime = Timing.mostAccurateTime()
        
        eventList = []
        appendToEventList = eventList.append
        currentTimeIndex = int(currentTime)
        
        for timeIndex in xrange( int(self.lastTime), currentTimeIndex ):
            
            timeIndexEvents = self.queuedEvents.get(timeIndex,None)
            
            if timeIndexEvents is not None:
                
                timeIndexEvents.sort()
                
                for event in timeIndexEvents:
                    appendToEventList(event)
                
                del self.queuedEvents[timeIndex]
            
        currentEvents = self.queuedEvents.get(currentTimeIndex,None)
        
        if currentEvents is not None:
            
            currentEvents.sort()
            
            for i in xrange(len(currentEvents)):
                
                event = currentEvents[0]
                if event.time <= currentTime:
                    appendToEventList(currentEvents.pop(0))
                else:
                    break
        
        self.lastTime = currentTime
        
        return eventList

    def getEventCount(self):
        """
        Returns the amount of events on the queue
        """
        # (Dev Note: remember, direct object access by 
        # an external system is BAD for extensibility and modular design)
        return reduce(lambda x,y: x+y, [len(t) for t in self.queuedEvents.itervalues()])

class SortedList(list):
    
    def __init__(self):
        list.__init__(self)
        
    def append(self, newElement):
        
        self.appendInOrder( newElement )
        
    def appendInOrder(self, newElement):
        
        bottomIndex,topIndex = 0,len(self)
        middleIndex = int( topIndex/2 )
        
        while bottomIndex != topIndex:
            
            if newElement < self[middleIndex]:
                topIndex = middleIndex
            else:
                bottomIndex = middleIndex + 1
            middleIndex = int( (bottomIndex + topIndex)/2 ) 

        self.insert( middleIndex, newElement )
        
class SortCacheList(list):
    
    def __init__(self):
        
        list.__init__(self)
        self.isSorted = False
        
    def sort(self):
        
        if not self.isSorted:
            super(SortCacheList, self).sort()
            self.isSorted = True
    
    def append(self, item):

        self.isSorted = False
        super(SortCacheList, self).append(item)

class TestEvent:
    
    def __init__(self, data=None, delay=0):
        
        self.time = Timing.mostAccurateTime()+delay
        self.data = data
    
    def getTime(self):
        
        return self.time
        
    def __cmp__(self, other):

        return self.time > other.time

if __name__ == '__main__':
    
    import random
    
    startTime = currentTime = Timing.mostAccurateTime()
    delay = 5.250
    eq=EventQueue2a(startTime)
    numEv=500
    # add 500 events to the queue to execute after "delay" seconds.
    for t in xrange(numEv):   
        eq.addEvent(TestEvent(delay=delay))
    
    numEvents = 0
    while numEvents < numEv:
        currentTime = Timing.mostAccurateTime()
        numEvents+=len(eq.getNextEvents(currentTime))
    print 'Elapsed time: %.6f'%(currentTime-startTime)
