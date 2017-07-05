'''
This class represents a java method.
'''
class Method(object):

    def __init__(self, name):

        self.name = name
        self.fieldsUsed = []
        
    def addFieldUsed(self, field):
        if field not in self.fieldsUsed:
            self.fieldsUsed.append(field)
    
    def getFieldsUsed(self):
        return self.fieldsUsed
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name