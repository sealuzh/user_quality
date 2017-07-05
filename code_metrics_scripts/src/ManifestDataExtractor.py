

import os
import os.path
import xml.dom.minidom as minidom

class ManifestDataExtractor(object):


    def __init__(self, filePath):
        self.filePath = filePath
        if self.validateManifest():
            self.valid = True
            self.manifest = minidom.parse(filePath+"/AndroidManifest.xml")
            
        else:
            self.valid = False
    
    
    def validateManifest(self):
		if os.path.exists(self.filePath+"/AndroidManifest.xml"):
			return True
		else:
			return False


    def extractAppLabel(self):
        tag = self.manifest.getElementsByTagName("application")
        for item in tag:
            appName = item.getAttribute("android:label")
            if len(appName) > 0:
                if appName[0] == "@":
                    return self.getResource(appName)
                else:
                    return appName
            else:
                return "DATA NOT FOUND"


    def getResource(self, appName):
        if os.path.exists(self.filePath+"/res/values/strings.xml"):
            try:
                strings = minidom.parse(self.filePath+"/res/values/strings.xml")
            except:
                return "DATA NOT FOUND - ERROR PARSING XML FILE"
            elements = strings.getElementsByTagName("string")
            for tag in elements:
                if tag.getAttribute("name") == appName[8:]:
                    return tag.firstChild.nodeValue
            return "DATA NOT FOUND - No STRINGS.XML"
        else:
            return "DATA NOT FOUND - NO STRINGS.XML"
            
            
            
    def extractFQName(self):
	
        tag = self.manifest.getElementsByTagName("manifest")
        for item in tag:
            fQName = item.getAttribute("package")
            return fQName


    def manifestIsValid(self):
        return self.isValid    
                
