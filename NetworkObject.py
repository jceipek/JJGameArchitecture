class ProxyableObjectCreator:
    
    def __init__(self):
        
        self.numberOfObjectsCreated = 0
        self.IDsToObjects = dict()
    
    def registerObject(self, obj):
        
        ID = self.numberOfObjectsCreated
        self.IDsToObjects[ID] = obj
        
        self.numberOfObjectsCreated+=1
        
        return ID
    
    def unregisterObject(self, obj):
        
        ID = obj._ID
        if ID in self.IDsToObjects:
            del self.IDsToObjects[ID]

class ProxyableObject:
    """
    This class should be the parent class of all classes which are to
    be passed from the server to the client.  A ProxyableObject will
    have a full representation on the server from which a client (proxy)
    representation can be easily extracted.  Network traffic can be
    easily reduced by passing only the changes made to the server
    representation which are relevant to the proxy over the network.
    """

    # class dictionary which stores the attributes which will be
    # included in proxies
    __proxyAttrs__ = {}
    # class dictionary which stores the attributes which will be
    # accessible to proxies
    __proxyMethods__ = {}
    
    def __init__(self):

        # instance dictionary which stores changes to attributes between
        # calls to the flushChanges function
        self.__changedAttrs__ = {}

    def __setattr__(self, name, value):
        """
        Overrides the normal __setattr__ behavior to add changes made to
        attributes which are to be included in proxies to the
        __changedAttrs__ dictionary.
        """

        if name in self.__proxyAttrs__:
            self.__changedAttrs__[name] = value

        # normal __setattr__ behavior
        self.__dict__[name] = value

    def flushChanges(self):
        """
        Returns changes made to the instance since the previous call
        to this function.  The __changedAttrs__ dictionary is emptied.
        """
        changes, self.__changedAttrs__ = self.__changedAttrs__, {}
        return changes

    @classmethod
    def registerAttributeForProxy(cls, name):
        """
        Adds an attribute to a dictionary of attributes which will be
        included in the proxy object returned by getProxyObject.
        """
        cls.__proxyAttrs__[name] = True
        
    @classmethod
    def registerMethodForProxy(cls, name):
        """
        Adds a method to a dictionary of methods which will be
        accessible to the proxy object returned by getProxyObject.
        """
        cls.__proxyMethods__[name] = True
    
    def getProxyObject(self):
        """
        Returns a proxy version of an object.
        """
        return ProxyObject(self)

    def getProxyObjectChange(self):
        """
        Returns the changes made to an instance which should be
        reflected in a proxy since the previous call.
        """
        return ProxyObjectChange(self)

class NetworkObject(ProxyableObject):
    """
    Adds a private ID attribute to all instances which can be used to
    connect proxies on clients to objects on the server.
    """
    
    ProxyableObject.registerAttributeForProxy('_id')
    
    def __init__(self, creator):
        
        ProxyableObject.__init__(self)
        self._id = creator.registerObject(self)

class ProxyObject:
    """
    Proxy representation of an object on the server.  This object
    does little more than provide attribute values.
    """

    def __init__(self, obj):
        
        # class of the object which this instance is a proxy of
        self.__parentClass = obj.__class__
        
        # add attributes from the obj to the proxy representation
        for attr in obj.__proxyAttrs__.iterkeys():
             self.__dict__[attr] = obj.__dict__[attr]
    
    def getProxyClass(self):
        return self.__parentClass
    
    def __getattr__(self, name):
        proxyObjCls = self.getProxyClass()
        if name in proxyObjCls.__proxyMethods__:
            return proxyObjCls.__dict__[name].__get__(self,self.__class__)
        else:
            raise AttributeError
    
    def updateWithChanges(self, proxyObjChange):
        """
        Update a ProxyObject with a ProxyObjectChange.
        """

        # for every attribute and the associated value in the changes
        # specified in the ProxyObjectChange, reflect these changes in
        # the ProxyObject
        for attr, value in proxyObjChange.getChanges().iteritems():
            self.__dict__[attr] = value

class ProxyObjectChange:
    """
    Changes which are made on a server-side object which should be
    reflected in its proxies.
    """

    def __init__(self, obj):

        # name of the class of the obj
        self.name = obj.__class__.__name__

        # store changes relevant to a proxy
        self.changes = {}

        # flush the changes from the object into the changeDict
        changeDict = obj.flushChanges()

        # add entries from the flushed changes to the passed object
        # to the changes dictionary of the ProxyObjectChange
        for attr in changeDict.iterkeys():
             self.changes[attr] = changeDict[attr]

    def getChanges(self):
        """
        Returns the change dictionary of the ProxyObjectChange.
        """
        return self.changes

if __name__ == '__main__':

    class TestObject(NetworkObject):
        
        NetworkObject.registerAttributeForProxy('hp')
        NetworkObject.registerAttributeForProxy('money')
        NetworkObject.registerMethodForProxy('damage')
        
        def __init__(self,hp,money,creator):
            
            NetworkObject.__init__(self,creator)
            
            self.hp = hp
            self.money = money
            self.secret = 'hi'

        def damage(self,change=1):
            self.hp-=1
    
    creator = ProxyableObjectCreator()
    
    b = TestObject(20,100,creator)
    bp = b.getProxyObject()
    
    print 'Proxy damage func: ',bp.damage
    
    b.damage()
    b.damage()

    print bp.__dict__
    delta=b.getProxyObjectChange()
    print delta.getChanges()
    bp.updateWithChanges(delta)
    print bp.__dict__

    b.damage()
    delta=b.getProxyObjectChange()
    print delta.getChanges()
    bp.updateWithChanges(delta)
    print bp.__dict__
