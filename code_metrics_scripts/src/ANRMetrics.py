'''
This measures four metrics related to ANR, the use of each of the following on the
main thread:
networking
file IO
SQL Lite
bitmaps
'''
import re
import fileinput


class ANRMetrics(object):


    def __init__(self, sourceCodePaths, layoutPaths):
    
        self.srcpaths = sourceCodePaths
        self.layoutPaths = layoutPaths
        self.numSrcFiles = len(self.srcpaths)
        self.numLayoutFiles = len(self.layoutPaths)
        self.numNetworkOnMainThread = 0
        self.numSQLLiteOnMainThread = 0
        self.numFileIOOnMainThread = 0
        self.numBitmapOnMainThread = 0
        
    
    def getNumberofFiles(self):
        return self.numFiles
    
    def extractData(self):
        for path in self.srcpaths:
            self.extractSrcFileData(path)
        self.printData()
    
    def extractSrcFileData(self, path):
        fileinput.close()
        
        activityRegex = "Landroid/app/Activity" 
        httpRequestRegex1 = "Landroid/net/http/AndroidHttpClient;->execute\("
        httpRequestRegex2 = "Lorg/apache/http/impl/client/DefaultHttpClient;->execute\("
        fileIORegex = "new-instance(.*?)Ljava/io/File"
        sqlLiteMethodRegex = "Landroid/database/sqlite/SQLiteDatabase;->(.*?)\("
        bitmapRegex = "(.*?)Landroid/graphics/BitmapFactory;->decode(.*?)\("
        for line in fileinput.input([path]):
                matches1 = re.findall(httpRequestRegex1, line)
                matches2 = re.findall(httpRequestRegex2, line)
                if len(matches1) > 0 or len(matches2) > 0:
                    self.numNetworkOnMainThread = self.numNetworkOnMainThread + 1
                matches = re.findall(sqlLiteMethodRegex, line)
                if len(matches) > 0:
                    self.numSQLLiteOnMainThread = self.numSQLLiteOnMainThread + 1
                matches = re.findall(fileIORegex, line)
                if len(matches) > 0:
                    self.numFileIOOnMainThread = self.numFileIOOnMainThread + 1
                matches = re.findall(bitmapRegex, line)
                if len(matches) > 0:
                    self.numBitmapOnMainThread = self.numBitmapOnMainThread + 1
            
    
    
    def extractLayoutFileData(self, path):
        pass
    
    
    def getNumNetworkOnMainThread(self):
        return self.numNetworkOnMainThread
    
    
    def getNumSQLLiteOnMainThread(self):
        return self.numSQLLiteOnMainThread
    
    
    def getNumFileIOOnMainThread(self):
        return self.numFileIOOnMainThread
    
    
    def getNumBitmapOnMainThread(self):
        return self.numBitmapOnMainThread
    
    
    
    
    def printData(self):
        
        print "Network operations "+str(self.numNetworkOnMainThread)
        print "SQL lite operations "+str(self.numSQLLiteOnMainThread)
        print "File IO operations "+str(self.numFileIOOnMainThread)
        print "Bitmap Decoding operations "+str(self.numBitmapOnMainThread)
