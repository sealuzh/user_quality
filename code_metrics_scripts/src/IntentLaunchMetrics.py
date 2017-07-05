import re
import fileinput


class IntentLaunchMetrics(object):


    def __init__(self, sourceCodePaths, layoutPaths, package):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.startActivities = 0
        self.startActivity = 0
        self.startInstrumentation = 0
        self.startIntentSender = 0
        self.startService = 0
        self.startActionMode = 0
        self.startActivityForResult = 0
        self.startActivityFromChild = 0
        self.startActivityFromFragment = 0
        self.startActivityIfNeeded = 0
        self.startIntentSenderForResult = 0
        self.startIntentSenderFromChild = 0
        self.startNextMatchingActivity = 0
        self.startSearch = 0
        self.total = 0
        self.package = package
        self.pkgpath = 'L' + self.package.replace('.','/') + '/'
    
    
    def getNumberofFiles(self):
        return self.numFiles
    
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        self.printData()
    
    
    def extractSrcFileData(self, path):
        fileinput.close()
        startActionModeRegex = self.pkgpath + "(.*?);->startActionMode\("
        startActivitiesRegex = self.pkgpath + "(.*?)startActivities(.*?)"
        startActivityRegex = self.pkgpath + "(.*?);->startActivity\("
        startActivityForResultRegex = self.pkgpath + "(.*?);->startActivityForResult\("
        startActivityFromChildRegex = self.pkgpath + "(.*?);->startActivityFromChild\("
        startActivityFromFragmentRegex = self.pkgpath + "(.*?);->startActivityFromFragment\("
        startActivityIfNeededRegex = self.pkgpath + "(.*?);->startActivityIfNeeded\("
        startInstrumentationRegex = self.pkgpath + "(.*?);->startInstrumentation\("
        startIntentSenderRegex = self.pkgpath + "(.*?);->startIntentSender(.*?)"
        startIntentSenderForResultRegex = self.pkgpath + "(.*?);->startIntentSenderForResult\("
        startIntentSenderFromChildRegex = self.pkgpath + "(.*?);->startIntentSenderFromChild\("
        startNextMatchingActivityRegex = self.pkgpath + "(.*?);->startNextMatchingActivity\("
        startSearchRegex = self.pkgpath +"(.*?);->startSearch\("
        startServiceRegex = "(.*?);->startService\("
        
        for line in fileinput.input([path]):
            matches = re.findall(startActivitiesRegex, line)
            if len(matches) > 0:
                self.startActivities = self.startActivities + 1
        
            matches = re.findall(startActivityRegex, line)
            if len(matches) > 0:
                self.startActivity = self.startActivity + 1
            
            matches = re.findall(startInstrumentationRegex, line)
            if len(matches) > 0:
                self.startInstrumentation = self.startInstrumentation + 1
            
            matches = re.findall(startIntentSenderRegex, line)
            if len(matches) > 0:
                self.startIntentSender = self.startIntentSender + 1
                
            matches = re.findall(startServiceRegex, line)
            if len(matches) > 0:
                self.startService = self.startService + 1
        
            matches = re.findall(startActionModeRegex, line)
            if len(matches) > 0:
                self.startActionMode = self.startActionMode + 1
        
            matches = re.findall(startActivityForResultRegex, line)
            if len(matches) > 0:
                self.startActivityForResult = self.startActivityForResult + 1
        
            matches = re.findall(startActivityFromChildRegex, line)
            if len(matches) > 0:
                self.startActivityFromChild = self.startActivityFromChild + 1
            
            matches = re.findall(startActivityFromFragmentRegex, line)
            if len(matches) > 0:
                self.startActivityFromFragment = self.startActivityFromFragment + 1
        
            matches = re.findall(startActivityIfNeededRegex, line)
            if len(matches) > 0:
                self.startActivityIfNeeded = self.startActivityIfNeeded + 1
        
            matches = re.findall(startIntentSenderForResultRegex, line)
            if len(matches) > 0:
                self.startIntentSenderForResult = self.startIntentSenderForResult + 1
        
            matches = re.findall(startIntentSenderFromChildRegex, line)
            if len(matches) > 0:
                self.startIntentSenderFromChild = self.startIntentSenderFromChild + 1
            
            matches = re.findall(startNextMatchingActivityRegex, line)
            if len(matches) > 0:
                self.startNextMatchingActivity = self.startNextMatchingActivity + 1
        
            matches = re.findall(startSearchRegex, line)
            if len(matches) > 0:
                self.startSearch = self.startSearch + 1
        
    
    def extractLayoutFileData(self, path):
        pass
    
    
    def getNumStartActivities(self):
        return self.startActivities
    
    def getNumStartActivity(self):
        return self.startActivity
    
    def getNumStartInstrumentation(self):
        return self.startInstrumentation
    
    def getNumStartIntentSender(self):
        return self.startIntentSender
    
    def getNumStartService(self):
        return self.startService
        #new
    
    def getNumStartActionMode(self):
        return self.startActionMode
    
    def getNumStartActivityForResult(self):
        return self.startActivityForResult
    
    def getNumStartActivityFromChild(self):
        return self.startActivityFromChild
    
    def getNumStartActivityFromFragment(self):
        return self.startActivityFromFragment
    
    def getNumStartActivityIfNeeded(self):
        return self.startActivityIfNeeded
    
    def getNumStartIntentSenderForResult(self):
        return self.startIntentSenderForResult
    
    def getNumStartIntentSenderFromChild(self):
        return self.startIntentSenderFromChild
    
    def getNumStartNextMatchingActivity(self):
        return self.startNextMatchingActivity
    
    def getNumStartSearch(self):
        return self.startSearch
    
    def printData(self):


        print "Start Activities "+str(self.startActivities)
        print "Start Activity "+str(self.startActivity)
        print "Start Instrumentation "+str(self.startInstrumentation)
        print "Start intent Sender "+str(self.startIntentSender)
        print "Start Service "+str(self.startService)
        print "Start Action Mode "+str(self.startActionMode)
        print "Start Activity for Result "+str(self.startActivityForResult)
        print "Start Activity from Child "+str(self.startActivityFromChild)
        print "Start Activity from fragment "+str(self.startActivityFromFragment)
        print "Start Activity If needed "+str(self.startActivityIfNeeded)
        print "Start Intent Sender for Result "+str(self.startIntentSenderForResult)
        print "Start Intent Sender From Child "+str(self.startIntentSenderFromChild)
        print "Start Next Matching Activity "+str(self.startNextMatchingActivity)
        print "Start Search "+str(self.startSearch)
        
        
        
        
