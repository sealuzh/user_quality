
import fileinput
from DBWriter import DBWriter

class SizeMetrics(object):


    def __init__(self, sourceCodePaths):
        '''
        Constructor
        '''
        self.paths = sourceCodePaths
        self.numFiles = len(self.paths)
        self.numInstr = 0
        self.numMethods = 0
        self.numClasses = 0
        self.methodsPerClass = 0
        self.cyclomatic = 0
        self. wmc = 0
        
        
    def getNumberofFiles(self):
        return self.numFiles

    def extractData(self):
	
        for path in self.paths:
            self.extractFileData(path)
        if self.numMethods == 0:
            self.instrPerMethod = 0
        else:
            self.instrPerMethod = self.numInstr / float(self.numMethods)
        if self.numClasses == 0:
            self.methodsPerClass = 0
            self.wmc = 0
            self.cyclomatic = 0
        else:
            self.methodsPerClass = self.numMethods / float(self.numClasses)
            #self.wmc = (self.cyclomatic + self.numMethods) / float(self.numClasses)
            #self.cyclomatic = (self.cyclomatic + self.numClasses) / float(self.numClasses) #number conditions plus one for each method
            self.cyclomatic = self.cyclomatic + 1
            self.wmc = (self.methodsPerClass) * float(self.cyclomatic)
        self.printData()
            
            
    def extractFileData(self, path):
        fileinput.close()
        for line in fileinput.input([path]):
            if line.startswith('.class '):
                self.numClasses = self.numClasses + 1
            if line.startswith('.method '):
                self.numMethods = self. numMethods + 1
            if len(line.strip()) > 0 and not line.strip()[0] == '.' and not line.strip()[0] == '#':
                self.numInstr = self.numInstr + 1
            if 'if-' in line or 'If-' in line:
                self.cyclomatic = self.cyclomatic + 1
                
                
    def getNumFiles(self):
        return self.numFiles

    def getNumClasses(self):
        return self.numClasses
    
    def getNumMethods(self):
        return self.numMethods

    def getNumInstructions(self):
        return self.numInstr


    def getMethodsPerClass(self):
        return self.methodsPerClass

    def getInstructionsPerMethod(self):
        return self.instrPerMethod

    def getCyclomatic(self):
        return self.cyclomatic

    def getWMC(self):
        return self.wmc
    #for debugging - will write to database (this will drive schema)

    def printData(self):
        print 'Number of files: ' + str(self.numFiles)
        print 'Number of Classes: ' + str(self.numClasses)
        print 'Number of Methods ' + str(self.numMethods)
        print 'Number of Bytecode Instructions: ' + str(self.numInstr)
        print 'Methods per Class: ' + str(self.methodsPerClass)
        print 'Bytecode Instructions per method: ' + str(self.instrPerMethod)
        print 'Cyclomatic complexity: ' + str(self.cyclomatic)
        print 'WMC: ' + str(self.wmc)
