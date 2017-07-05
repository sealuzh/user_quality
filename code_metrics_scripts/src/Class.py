'''
Represents a java class
'''
class Class(object):

    def __init__(self):

        self.name = ''
        self.package = ''
        self.parent = ''
        self.children = []
        self.fields = []
        self.methods = []
        self.coupledObjects = []
        self.publicFields = []
        self.isController = False
        
        
    def setName(self, name):
        self.name = name
    
    def setPackage(self, package):
        self.package = package
    
    def setParent(self, parent):
        self.parent = parent
    
    def setChildren(self, children):
        self.children = children
    
    def getName(self):
        return self.name
    
    def getPackage(self):
        return self.package
    
    def getParent(self):
        return self.parent
    
    def getChildren(self):
        return self.children
    
    def addChild(self, child):
        self.children.append(child)
    
    def addField(self, field):
        self.fields.append(field)
    
    def getFields(self):
        return self.fields
    
    def getMethods(self):
        return self.methods
    
    
    def addMethod(self, method):
        self.methods.append(method)

    def getCoupledObjects(self):
        return self.coupledObjects
    
    def addCoupledObject(self, obj):
        if obj not in self.coupledObjects:
            self.coupledObjects.append(obj)
    
    def getPublicFields(self):
        return self.publicFields
    
    def addPublicField(self, field):
        if not field in self.publicFields:
            self.publicFields.append(field)
    
    def toString(self):
        childNames = []
        for aChild in self.children:
            childNames.append(aChild.getName())
        return 'Name: ' + self.name + '\nParent: ' + self.parent + '\nChildren: ' +str(childNames)