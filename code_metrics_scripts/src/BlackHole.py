import fileinput
import re


class BlackHole(object):

    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numCatchBlocks = 0
        self.numLogOnly = 0
        self.numNoAction = 0
        
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        for path in self.layoutPaths:
            self.extractLayoutFileData(path)
    
    
    def extractSrcFileData(self, path):
        fileinput.close()
        catchNum = 0
        correct = False
        log = False
        logRegex1 = "invoke-virtual(.*?) Ljava/lang/Exception;->printStackTrace()"
        logRegex2 = "invoke-static (.*?)Landroid/util/Log;->e"
        for line in fileinput.input([path]):
            if line.strip().startswith(":catch_"):
                
                self.numCatchBlocks = self.numCatchBlocks + 1
                if not log and not correct:
                    self.numNoAction = self.numNoAction + 1
                elif log and not correct:
                    self.numLogOnly = self.numLogOnly + 1
                correct = False
                log = False
                catchNum = catchNum + 1
                if catchNum > 0 and line.startswith(".end method"):#catch clauses come atthe end of the method
                    if not log and not correct:
                        self.numNoAction = self.numNoAction + 1
                    elif log and not correct:
                        self.numLogOnly = self.numLogOnly + 1
                    correct = False
                    log = False
                    catchNum = 0
                    continue
                if catchNum > 0:
                    if not line.strip().startswith(".") and not line.strip().startswith("goto") and not line.strip().startswith("move-exception"):#looking for developer method calls
                        matches1 = re.findall(logRegex1, line)
                        matches2 = re.findall(logRegex2, line)
                        if len(matches1) > 0 or len(matches2) > 0:
                            log = True
                        else:
                            correct = True


    def extractLayoutFileData(self, path):
        pass
    
    
    def getNumCatchBlocks(self):
        return self.numCatchBlocks
    
    
    def getNumNoAction(self):
        return self.numNoAction
    
    
    def getNumLogOnly(self):
        return self.numLogOnly
