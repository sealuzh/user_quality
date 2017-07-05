
import re
import fileinput
import AndroidViews


class OtherMetrics(object):


    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numBundles = 0
        self.numCheckedBundles = 0
        self.objMap = {}
        
        
    def getNumberofFiles(self):
        return self.numFiles
    
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        self.printData()
            
    
    def extractSrcFileData(self, path):
        fileinput.close()
        bundleAssignment = ".local (.*?):Landroid/os/Bundle;"
        androidObj = "Landroid/(.*?)/(.*?);";
        bundleRegisters = []
        for line in fileinput.input([path]):
            matches = re.findall(bundleAssignment, line)
            if len(matches) > 0 and not ".end" in line:
                reg = matches[0][0:matches[0].find(",")]
                if not reg in bundleRegisters:
                    bundleRegisters.append(reg)
                self.numBundles = self.numBundles + 1
            else:
                if len(bundleRegisters) != 0:
                    nullCheck = "(if-nez|if-eqz) "
                    regName = ""
                    for reg in bundleRegisters:
                        matches = re.findall(nullCheck + reg, line)
                        if len(matches) > 0:
                            self.numCheckedBundles = self.numCheckedBundles + 1
                            regName = reg
                    if regName != "":
                        bundleRegisters.remove(regName)
            objMatches = re.findall(androidObj, line)
            if len(objMatches) > 0:
                for tuple in objMatches:
                    list = []
                    list.append('android')
                    list.append(tuple[0])
                    list.append(tuple[1])
                    fulQual = '.'.join(list)
                    fulQual = fulQual.replace('$', '.')
                    if fulQual in self.objMap:
                        self.objMap[fulQual] = self.objMap[fulQual] + 1
                    else:
                        self.objMap[fulQual] = 1
                    
                    
    def extractLayoutFileData(self, path):
        fileinput.close()
        tempMax = 0
        viewRegex = "<" + AndroidViews.getAndroidViewsRegex()
        for line in fileinput.input([path]):
            numMatches = len(re.findall(viewRegex, line))
                    
                    
                    
    def getNumUncheckedBundles(self):
        return self.numBundles - self.numCheckedBundles
        
                    
    def getObjectMap(self):
        return self.objMap
    
    def getNumBundles(self):
        return self.numBundles
    
    def getNumCheckedBundles(self):
        return self.numCheckedBundles
    
    
    def printData(self):
        print "Num Bundles: "+str(self.numBundles)
        print "Num Checked Bundles: "+str(self.numCheckedBundles)
        print "Num Unchecked Bundles "+str(self.getNumUncheckedBundles())
        print "Object Map "+str(len(self.objMap))
