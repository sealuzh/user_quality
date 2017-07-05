
import re
import fileinput
import AndroidViews
#from duplicity.path import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    


class UncheckedBadSmellMethodCalls(object):
    
    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.dismiss = 0
        self.show = 0
        self.setContentView = 0
        self.createScaledBitmap = 0
        self.onKeyDown = 0
        self.isPlaying = 0
        self.unregisterReceiver = 0
        self.onBackPressed = 0
        self.showDialog = 0
        self.create = 0
        self.inTryCatch = False
        
        
    def getNumberofFiles(self):
        return self.numFiles


    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        for path in self.layoutPaths:
            self.extractLayoutFileData(path)
        self.printData()


    def extractSrcFileData(self, path):
        fileinput.close()
        i =0;
        for line in fileinput.input([path]):
            i+=1
            if not self.inTryCatch: 
                if line.lstrip().startswith(":try_start"):
                    self.inTryCatch = True
                else:
                    
                    matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->dismiss\(", line)
                    if len(matches) > 0:
                        self. dismiss = self.dismiss + 1
                    matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->show\(", line)
                    if len(matches) > 0:
                        self.show = self.show + 1
                    matches = re.findall("invoke-virtual (.*?), (.*?);->setContentView\(", line)
                    if len(matches) > 0:
                        self.setContentView = self.setContentView + 1
                    matches = re.findall("invoke-static (.*?), Landroid/(.*?);->createScaledBitmap\(", line)
                    if len(matches) > 0:
                        self.createScaledBitmap = self.createScaledBitmap + 1
                        
                    matches = re.findall("invoke-super (.*?), (.*?);->onKeyDown\(",line)
                    if len(matches) > 0:
                        self.onKeyDown = self.onKeyDown + 1
                    matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->isPlaying\(", line)
                    if len(matches) > 0:
                        self.isPlaying = self.isPlaying + 1
                    matches = re.findall("invoke-virtual (.*?), (.*?);->unregisterReceiver\(", line)
                    if len(matches) > 0:
                        self.unregisterReceiver = self.unregisterReceiver + 1
                    matches = re.findall("invoke-super (.*?), (.*?);->onBackPressed\(", line)
                    if len(matches) > 0:
                        self. onBackPressed = self.onBackPressed + 1
                    matches = re.findall("invoke-super (.*?), (.*?);->showDialog\(",line)
                    if len(matches) > 0:
                        self.showDialog = self.showDialog + 1
                    matches = re.findall("invoke-virtual (.*?), Landroid/(.*?);->create\(", line)
                    if len(matches) > 0:
                        self.create = self.create + 1
            else:
                if line.lstrip().startswith(":try_end"):
                    self.inTryCatch = False
                    
                    
                    
    def extractLayoutFileData(self, path):
        fileinput.close()


    def getNumShowCalls(self):
        return self.show


    def getNumDismissCalls(self):
        return self.dismiss


    def getNumSetContentViewCalls(self):
        return self.setContentView


    def getNumCreateScaledBitmapCalls(self):
        return self.createScaledBitmap


    def getNumOnKeyDownCalls(self):
        return self.onKeyDown


    def getNumIsPlayingCalls(self):
        return self.isPlaying


    def getNumUnregisterRecieverCalls(self):
        return self.unregisterReceiver


    def getNumOnBackPressedCalls(self):
        return self.onBackPressed
    
    def getNumShowDialogCalls(self):
        return self.showDialog


    def getNumCreateCalls(self):
        return self.create


    def printData(self):
        
        print "Dismiss Method Call "+str(self.dismiss)
        print "Show Method Call "+str(self.show)
        print "setContentView  Method Call "+str(self.setContentView)
        print "Create Scaled Bitmap "+str(self.createScaledBitmap)
        print "onKeyDown Method Call "+str(self.onKeyDown)
        print "Is Playing "+str(self.isPlaying)
        print "Unregisterreceiver Method Call "+str(self.unregisterReceiver)
        print "onBackPressed Method Call "+str(self.onBackPressed)
        print "show dialog "+str(self.showDialog)
        print "create Method Call "+str(self.create)
        
