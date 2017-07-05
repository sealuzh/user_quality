
import re
import fileinput
import AndroidViews

class MVCMetrics(object):


    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numViewsInController = 0
        self.numViewsNotInController = 0
        self.numViewsInXML = 0
        self.maxNumViewsInXML = 0
        self.sepVCScore = 0.0
        self.potBadToken = 0
        self.numFragments = 0
        
        
    def getNumberofFiles(self):
        return self.numSrcFiles
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        for path in self.layoutPaths:
            self.extractLayoutFileData(path)
        self.sepVCScore = self.calculateSepVCScore()
        self.printData()
    
    
    def extractSrcFileData(self, path):
        fileinput.close()
        className = ""
#        viewInitRegex = "new-instance(.*?)Landroid/widget/" +AndroidViews.getAndroidViewsRegex()
        viewInitRegex = "Landroid/widget/" +AndroidViews.getAndroidViewsRegex()
        isController = False
        for line in fileinput.input([path]):
            if line.startswith(".source"):
                className = line.split()[-1].replace("\"","").replace(".java","")
            if line.startswith('.super '):
                #matches = re.findall("Landroid/app/(.*?)Activity", line)
                matches = re.findall("Landroid/app/Activity", line)
                isController = (len(matches) > 0)
            else:
                matches = re.findall(viewInitRegex, line)
                
                if(len(matches) > 0):
                    if(isController):
                        self.numViewsInController = self.numViewsInController + 1
                    else:
                        
                        self.numViewsNotInController = self.numViewsNotInController +1
                if(isController):
                    if "getApplicationContext()Landroid/content/Context" in line:
                        self.potBadToken = self.potBadToken + 1


    def extractLayoutFileData(self, path):
        fileinput.close()
        tempMax = 0
        viewRegex = "<" + AndroidViews.getAndroidViewsRegex()
        for line in fileinput.input([path]):
            if "<fragment" in line:
                self.numFragments = self.numFragments + 1
                numMatches = len(re.findall(viewRegex, line))
                self.numViewsNotInController = self.numViewsNotInController + numMatches
                self.numViewsInXML = self.numViewsInXML + numMatches
                tempMax = tempMax + numMatches
        if tempMax > self.maxNumViewsInXML:
            self.maxNumViewsInXML = tempMax


    def calculateSepVCScore(self):
        if(self.numViewsNotInController + self.numViewsInController == 0):
            return 0
        return self.numViewsNotInController / float(self.numViewsNotInController + self.numViewsInController) * 100



    def getNumViewsInController(self):
        return self.numViewsInController


    
    def getNumViewsNotInController(self):
        return self.numViewsNotInController


    def getAvgNumViewsInXML(self):
        if len(self.layoutPaths) == 0:
            return 0
        return float(self.numViewsInXML) / float(len(self.layoutPaths))

    def getNumViewsInXml(self):
        return self.numViewsInXML
    

    def getMaxNumViewsInXML(self):
        return self.maxNumViewsInXML


    def getSepVCScore(self):
        return self.sepVCScore


    def getPotentialBadTokenExceptions(self):
        return self.potBadToken


    def getNumFragments(self):
        return self.numFragments

        
    def printData(self):
        print "Num views in controllers: " + str(self.numViewsInController)
        print "Num views not in controllers: " + str(self.numViewsNotInController)
        print "# views in XML: " + str(self.numViewsInXML)
        print "Max # views in an XML file: " + str(self.maxNumViewsInXML)
        print "Percentage of Views Defined Outside of Controllers: " +str(self.sepVCScore) + "%"
        print "Potential Bad Token Exception "+str(self.potBadToken)
        print "Number of fragments "+str(self.numFragments)
        
