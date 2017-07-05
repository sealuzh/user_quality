import re
import fileinput
import AndroidViews


class NetworkTimeout(object):


    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numHTTPClients = 0
        self.numConTimeouts = 0 #connection timeouts
        self.numSoTimeouts = 0 #socket timeouts
    
    
    def getNumberofFiles(self):
        return self.numFiles
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        self.printData()
    
    
    def extractSrcFileData(self, path):
        fileinput.close()
        androidClientRegex = "invoke-static (.*?)Landroid/net/http/AndroidHttpClient;->newInstance(.*?)Landroid/net/http/AndroidHttpClient;"
        httpClientRegex = "new-instance (.*?)Lorg/apache/http/impl/client/DefaultHttpClient"
        conTimeoutRegex = "invoke-static (.*?)Lorg/apache/http/params/HttpConnectionParams;->setConnectionTimeout"
        soTimeoutRegex = "invoke-static (.*?)Lorg/apache/http/params/HttpConnectionParams;->setSoTimeout"
        for line in fileinput.input([path]):
            matches1 = re.findall(androidClientRegex, line)
            matches2 = re.findall(httpClientRegex, line)
            if len(matches1) > 0 or len(matches2) > 0:
                self.numHTTPClients = self.numHTTPClients + 1
            matches3 = re.findall(conTimeoutRegex, line)
            if len(matches3) > 0:
                self.numConTimeouts = self.numConTimeouts + 1
            matches4 = re.findall(soTimeoutRegex, line)
            if len(matches4) > 0:
                self.numSoTimeouts = self.numSoTimeouts + 1
                
    def extractLayoutFileData(self, path):
        fileinput.close()
        tempMax = 0
        viewRegex = "<" + AndroidViews.getAndroidViewsRegex()
        for line in fileinput.input([path]):
            numMatches = len(re.findall(viewRegex, line))


    def getNumHttpClients(self):
        return self.numHTTPClients

    def getNumConTimeouts(self):
        return self.numConTimeouts

    def getNumSoTimeouts(self):
        return self.numSoTimeouts

    def getNumNoConTimeout(self):
        return self.numHTTPClients - self.numConTimeouts

    def getNumNoSoTimeout(self):
        return self.numHTTPClients - self.numSoTimeouts

    def printData(self):
        print "HTTP Clients "+str(self.numHTTPClients)
        print "Connection Timeouts "+str(self.numConTimeouts)
        print "Socket Timeouts "+str(self.numSoTimeouts)
        print "Connections no timeout "+str(self.getNumNoConTimeout())
        print "Connections no Socket timeout "+str(self.getNumNoSoTimeout())        
