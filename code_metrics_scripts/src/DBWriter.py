
import MySQLdb
import datetime
from datetime import date
from _mysql import connect
import ConfigParser

class DBWriter(object):
    


    def __init__(self):

	Config = ConfigParser.ConfigParser()
	Config.read("config.ini")
	
        self.user           = Config.get('db', 'username')
        self.password       = Config.get('db', 'passw')
        self.host           = Config.get('db', 'host')
        self.database       = Config.get('db', 'database') 
        self.currApkId      = 0;
        self.currApkPkg     = "";
        self.currFQN        = "";
        self.currAppLabel   = "";
    
    
    def connect(self):
        self.db = MySQLdb.connect(self.host, self.user, self.password, self.database)
        self.cursor = self.db.cursor()
        print "connection OK"
        return self.db


    def saveApkFile(self, package, fqn, al, mf, date, market, downloads, version, creator, superDev, price, offerT, size, rating, reviews):
     

	self.cursor.execute("""INSERT INTO apk_file VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",('default', package, fqn, al, '', date, market, '', '', '', superDev, '', offerT, size, rating, reviews))
        
		
        self.db.commit()
      
	self.currApkPkg     = package;
        self.currFQN        = fqn;
        self.currAppLabel   = al;
        
        self.cursor.execute("""SELECT id from apk_file WHERE package = %s and full_qualified_name = %s and applabel = %s""", (self.currApkPkg, self.currFQN, self.currAppLabel))
        row = self.cursor.fetchone()
        self.currApkId = row[0]



        
        
        print "APK file saved succesfully!"
        
        
        
        
    def saveSizeMetric(self, numInstructions, numMethods, numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc):
        apkid = self.currApkId;
        print str(numInstructions)+" "+str(numMethods)+" "+str(numClasses)+" "+str(methodsPerClass)+" "+str(instrPerMethod)+" "+str(cyclomatic)+" "+str(wmc)
        self.cursor.execute("""INSERT INTO size VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",('default', apkid,numInstructions, numMethods, numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc))
        
        self.db.commit()
        print "Size metrics saved succesfully!"   
        
        
        
    def saveCKMetric(self, noc, dit, lcom, cbo, ppiv, apd):
        
        apkid = self.currApkId;
        self.cursor.execute("""INSERT INTO ck VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",('default', apkid, noc, dit, lcom, cbo, ppiv, apd))
        
        self.db.commit()
        print "Chidamber and Kemerer metrics saved succesfully!"
        
        
    def saveMVCMetric(self, viewsInController, viewsNotInController, viewsInXml, maxViewsInXml, viewsNotInControllerPerc, badTokenexception, numFragment):
        
        apkid = self.currApkId;
        self.cursor.execute("""INSERT INTO mvc VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)""",('default', apkid, viewsInController, viewsNotInController, viewsInXml, maxViewsInXml, viewsNotInControllerPerc, badTokenexception, numFragment))
        
        self.db.commit()
        print "MVC metrics saved succesfully!"      
        
        
        
    def saveOtherMetric(self, numBundles, checkedBundles, uncheckedBundles, objMap):
        
        
        apkid = self.currApkId;
        self.cursor.execute("""INSERT INTO other VALUES (%s,%s,%s,%s,%s,%s)""",('default', apkid, numBundles, checkedBundles, uncheckedBundles, objMap))
        
        
        self.db.commit()
        print "Other metrics saved succesfully!"  
        
        
    def saveUncheckedBadSmellsMetric(self, cshow, cdismiss, csetContentView, ccreateScaledBitmap, conKeyDown, cisPlaying, cunregisterReceiver, conBackPressed, cshowDialog, ccreate):
        
        
        apkid = self.currApkId;
        self.cursor.execute("""INSERT INTO ubsmells VALUES (%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)""",('default', apkid, cshow, cdismiss, csetContentView, ccreateScaledBitmap, conKeyDown, cisPlaying, cunregisterReceiver, conBackPressed, cshowDialog, ccreate))
        
        
        self.db.commit()
        print "Unchecked Bad Smells metrics saved succesfully!"
        
        
    def saveBatteryMetric(self, noTimeoutWakeLocks, locListeners, gpsUses, domParsers, saxParsers, xmlPullParsers):
        
        
        apkid = self.currApkId;
        self.cursor.execute("""INSERT INTO battery VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",('default', apkid, noTimeoutWakeLocks, locListeners, gpsUses, domParsers, saxParsers, xmlPullParsers))
        
        
        self.db.commit()
        print "battery Life metrics saved succesfully!" 
        
        
    def saveNetworkMetric(self, httpClients, numConTimeouts, numSoTimeouts, numNoConTimeouts, numNoSoTimeouts):
        
        
        apkid = self.currApkId;
        
        self.cursor.execute("""INSERT INTO timeout VALUES (%s,%s,%s,%s,%s,%s,%s)""",('default', apkid, httpClients, numConTimeouts, numSoTimeouts, numNoConTimeouts, numNoSoTimeouts))
        
        
        self.db.commit()
        print "Network Timeout metrics saved succesfully!"          
              
              
    
    def saveBlackHolekMetric(self, numCatchBlocks, numLogOnly, numNoAction):
        
        
        apkid = self.currApkId;
        
        self.cursor.execute("""INSERT INTO blackHole VALUES (%s,%s,%s,%s,%s)""",('default', apkid, numCatchBlocks, numLogOnly, numNoAction))
        
        
        self.db.commit()
        print "Black Hole metrics saved succesfully!"   
        
        
    def saveANRkMetric(self, network, sqlLite, fileIO, bitmap):
        
        
        apkid = self.currApkId;
        
        self.cursor.execute("""INSERT INTO anr VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",('default', apkid, network, sqlLite, fileIO, bitmap, 0, 0, 0, 0))
        
        
        self.db.commit()
        print "ANR metrics saved succesfully!"            
              
              
    def saveIntentLaunchkMetric(self, startActivities, startActivity, startInstrumentation, startIntentSender, startService, startActionMode, startActivityForResult, startActivityFromChild, startActivityFromFragment, startActivityIfNeeded, startIntentSenderForResult, startIntentSenderFromChild, startNextMatchingActivity, startSearch):
        
        
        apkid = self.currApkId;
        
        self.cursor.execute("""INSERT INTO intentLaunch VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",('default', apkid, startActivities, startActivity, startInstrumentation, startIntentSender, startService, startActionMode, startActivityForResult, startActivityFromChild, startActivityFromFragment, startActivityIfNeeded, startIntentSenderForResult, startIntentSenderFromChild, startNextMatchingActivity, startSearch))
        
        
        self.db.commit()
        print "Intent Launch metrics saved succesfully!"  
