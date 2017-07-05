'''

Extractor Metric Manager
'''

import os
import os.path
import xml.dom.minidom as minidom
import ManifestDataExtractor as mde
import SizeMetrics
import CKMetrics
import MVCMetrics
import OtherMetrics
from Disass import Disass
import UncheckedBadSmellMethodCalls
import BatteryMetrics
import BlackHole
import NetworkTimeout
import ANRMetrics
import IntentLaunchMetrics
#from DBWriter import DBWriter
import datetime
import sys
import zipfile
import traceback
import re
import ConfigParser
import shutil

ignoreFiles = ['BuildConfig.smali', 'R$attr.smali', 'R$dimen.smali',
'R$drawable.smali', 'R$id.smali',
'R$layout.smali','R$menu.smali','R$string.smali','R$style.smali','R.smali']

Config = ConfigParser.ConfigParser()
Config.read("config.ini")


MALWARE_MODE = 'true'
DISASS          = Config.getboolean('disass', 'isDisass')
origin          = Config.get('paths', 'input')
output		= Config.get('paths', 'output')
TRUSTED_METRICS = Config.get('paths', 'trusted_metrics')
THIRD_METRICS 	= Config.get('paths', 'third_metrics')
BASE_PATH	= Config.get('paths', 'third_metrics')

TRUSTED_MODE	= Config.getboolean('mode', 'trusted')

def getAppSize(outputPath,appName):

	return os.path.getsize(outputPath+"/"+appName) / (1024*1024.0)

def getSourceCodeDirectoryPaths(root, packageName):

    os.chdir(root)
    dirNames = os.listdir(os.getcwd())
    firstIdentifier = packageName.split('.')[0]
    secondIdentifier = packageName.split('.')[1]
    dirPaths = []

#    dirPaths.append(root + "/" + firstIdentifier + "/" + secondIdentifier)
    dirPaths.append(root)
    return dirPaths


def getDate(dir, file):

    #origin = "/home/giovanni/TesiM/toDisass/"
    #print "Get date "+origin+dir+"/"+file
    file = str(origin+dir+"/"+file)
    zf = zipfile.ZipFile(file, 'r')
    for file in zf.infolist():
        if file.filename == "classes.dex":
            dt = datetime.datetime(*(file.date_time))
	    return dt


def parseManifest(manifestDataExt,filePath):
    #EXTRACTING APP LABEL
    appLabel = manifestDataExt.extractAppLabel()
    try:
        appLabel = re.sub(r'[^\w]', ' ', appLabel) # elimina caratteri speciali
        print "App Label -> " + appLabel
    except:
        appLabel = "DATA NOT FOUND - INVALID ENCODING"
        print "App Label -> " + appLabel
        #EXTRACTING FULLY QUALIFIED APP NAME
    appFQName = manifestDataExt.extractFQName()
    print "Fully Qualified Name -> " + appFQName

    return appLabel, appFQName


def getMalwareFamily(origin):

    path = origin
    for dir in os.walk(path):
        for x in dir[1]:
            print x


def getReviews(appFQName):

	#check reviews
	file_rev = "/"+appFQName+".txt"
	if os.path.exists(file_rev):

		print "Review trovata!"
		with open(file_rev) as fp:
			for line in fp:
				if ";" in line:
					a = (line.split(";", 4))
					print line.rstrip('\n')

def getOtherMetricTrusted(apk):

	apk = re.sub(".apk", "", apk)
	print "APK "+apk
	FILE = ""
	if TRUSTED_MODE:
		FILE = TRUSTED_METRICS

	else:
		FILE = THIRD_METRICS

	with open(FILE) as fp:
		for line in fp:
			if ";" in line:
				a = (line.split(";", 8))[0]
				if apk == a:
					print "Ok trovato"
					print re.sub(" ;", ";", line)
					p = (line.split(";", 8))
					return {'title' : p[0], 'package' : p[0].lower()+".apk", 'creator' : p[3], 'price' : p[4], 'version' : p[2], 'size' : p[5], 'rating' : p[6].rstrip(), 'downloads' : p[1], 'reviews' : p[7].rstrip()}



def extractData(location, family):

    #db = DBWriter()
    #conn = db.connect()
    path = location
    files = os.listdir(path)
    directorySize = len(files)
    errorFile = open(BASE_PATH+"_"+family+"_metric_errors.txt", "w")
    print "!"*150
    print "NOW EXTRACTING DATA FROM " + path
    print str(directorySize)+" APPS FOUND"
    print  "!"*150

    i = 1
    for f in files:

        sourceCodePaths = []
        layoutFilePaths = []
        decFolderPath = path+f

        filename = f + ".apk"
        #PRINTING HEADER
        print "*"*50
        print "EXTRACTING DATA FROM FILE "+ str(i) +" OF "+ str(directorySize)
        print "*"*50
        i += 1

        try:
            manifestDataExt = mde.ManifestDataExtractor(decFolderPath)
            if manifestDataExt.validateManifest():
		#get app name and package name from manifest
                appLabel, packageName = parseManifest(manifestDataExt,decFolderPath)
                #get path for each source code file that we will consider
                smaliPath = decFolderPath + '/smali'

                dirPaths = getSourceCodeDirectoryPaths(smaliPath, packageName)

                ######  dir is malware family

                market = family

                package = f

                print "Market "+market
                date = getDate(market, f+".apk")
                date = str(date.date())
                print "Date "+date

		if TRUSTED_MODE:

		        trusted = getOtherMetricTrusted(f)
		        appFQName = trusted['title']
		        package = trusted['package']
		        downloads = trusted['downloads']
		        version = trusted['version']
		        creator = trusted['creator']
		        superDev = 0
		        price = trusted['price']
		        offerT = 0
		        size = trusted['size']
		        rating = trusted['rating']
			reviews = trusted['reviews']

		else:

			appFQName = packageName
		        package = appLabel
		        downloads = ""
		        version = ""
		        creator = ""
		        superDev = 0
		        price = ""
		        offerT = 0
			size = str(getAppSize(origin+market, filename))

			rating = 0
			reviews = 0

		#revs = getReviews(appFQName)
		#db.saveApkFile(package, appFQName, appFQName, '', date, market, downloads, version, creator, superDev, price, offerT, size, rating, reviews)


                #navigate using fully qualified packageName
                for codeDir in dirPaths:
                    for root, dirs, files in os.walk(codeDir):
                        for file in files:
                            if file not in ignoreFiles:
                                sourceCodePaths.append(os.path.join(root, file))


                #calculate size metrics
                print "========  Size Metrics =========\n"
                sizeMetrics = SizeMetrics.SizeMetrics(sourceCodePaths)
		sizeMetrics.extractData()
		numInstructions = sizeMetrics.getNumInstructions()
		numMethods = sizeMetrics.getNumMethods()
		numClasses = sizeMetrics.getNumClasses()
		methodsPerClass = sizeMetrics.getMethodsPerClass()
		instrPerMethod = sizeMetrics.getInstructionsPerMethod()
		cyclomatic = sizeMetrics.getCyclomatic()
		wmc = sizeMetrics.getWMC()
		print "\n"
		#db.saveSizeMetric(numInstructions, numMethods, numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc)

                print "========  Chidamber and Kemerer Metrics =========\n"
                #calculate CK metrics
                ckMetrics = CKMetrics.CKMetrics(sourceCodePaths, packageName)

                ckMetrics.extractData()
                noc = ckMetrics.getNOC()
                dit = ckMetrics.getDIT()
                lcom = ckMetrics.getLCOM()
                cbo = ckMetrics.getCBO()
                ppiv = ckMetrics.getPPIV()
                apd = ckMetrics.getAPD()
                print "\n"

                #db.saveCKMetric(noc, dit, lcom, cbo, ppiv, apd)


                print "========  MVC Metrics =========\n"
                #calculate MVC metrics
                mvcMetrics              =   MVCMetrics.MVCMetrics(sourceCodePaths, layoutFilePaths)
                mvcMetrics.extractData()
                mvc                     = mvcMetrics.getSepVCScore()
                avgNumViewsInXML        = mvcMetrics.getAvgNumViewsInXML()

                maxNumViewsInXML        = mvcMetrics.getMaxNumViewsInXML()
                numViewsInXml           = mvcMetrics.getNumViewsInXml()
                numViewsInController    = mvcMetrics.getNumViewsInController()
                numViewsNotInController = mvcMetrics.getNumViewsNotInController()
                viewsNotInControllerPerc = mvcMetrics.getSepVCScore()
                potBadToken             = mvcMetrics.getPotentialBadTokenExceptions()
                numFragments            = mvcMetrics.getNumFragments()
                print "\n"


                #db.saveMVCMetric(numViewsInController, numViewsNotInController, numViewsInXml, maxNumViewsInXML, viewsNotInControllerPerc, potBadToken, numFragments)


                #calculate other metrics

                print "========  Unchecked bundles Metrics =========\n"
                otherMetrics = OtherMetrics.OtherMetrics(sourceCodePaths,layoutFilePaths)
                otherMetrics.extractData()

                numBundles          =   otherMetrics.getNumBundles()
                checkedBundles      =   otherMetrics.getNumCheckedBundles()
                uncheckedBundles    =   otherMetrics.getNumUncheckedBundles()
                objMap              =   len(otherMetrics.getObjectMap())


                print "\n"

                #db.saveOtherMetric(numBundles, checkedBundles, uncheckedBundles, objMap)


                #bad smell methods
#                 bsmc = BadSmellMethodCalls.BadSmellMethodCalls(sourceCodePaths,layoutFilePaths)
#                 bsmc.extractData()
#                 show = bsmc.getNumShowCalls()
#                 dismiss = bsmc.getNumDismissCalls()
#                 setContentView = bsmc.getNumSetContentViewCalls()
#                 createScaledBitmap = bsmc.getNumCreateScaledBitmapCalls()
#                 onKeyDown = bsmc.getNumOnKeyDownCalls()
#                 isPlaying = bsmc.getNumIsPlayingCalls()
#                 unregisterReceiver = bsmc.getNumUnregisterRecieverCalls()
#                 onBackPressed = bsmc.getNumOnBackPressedCalls()
#                 showDialog = bsmc.getNumShowDialogCalls()
#                 create = bsmc.getNumCreateCalls()


                print "========  unchecked Bad Smells Metrics =========\n"
                #unchecked bad smell methods
                cbsmc = UncheckedBadSmellMethodCalls.UncheckedBadSmellMethodCalls(sourceCodePaths, layoutFilePaths)
                cbsmc.extractData()


                cshow               = cbsmc.getNumShowCalls()
                cdismiss            = cbsmc.getNumDismissCalls()
                csetContentView     = cbsmc.getNumSetContentViewCalls()
                ccreateScaledBitmap = cbsmc.getNumCreateScaledBitmapCalls()
                conKeyDown          = cbsmc.getNumOnKeyDownCalls()
                cisPlaying          = cbsmc.getNumIsPlayingCalls()
                cunregisterReceiver = cbsmc.getNumUnregisterRecieverCalls()
                conBackPressed      = cbsmc.getNumOnBackPressedCalls()
                cshowDialog         = cbsmc.getNumShowDialogCalls()
                ccreate             = cbsmc.getNumCreateCalls()

                print "\n"

                #db.saveUncheckedBadSmellsMetric(cshow, cdismiss, csetContentView, ccreateScaledBitmap, conKeyDown, cisPlaying, cunregisterReceiver, conBackPressed, cshowDialog, ccreate)


                print "========  Battery Life Metrics =========\n"
                #Battery Life metrics
                batteryMetrics = BatteryMetrics.BatteryMetrics(sourceCodePaths,
                layoutFilePaths)
                batteryMetrics.extractData()

                noTimeoutWakeLocks  = batteryMetrics.getNumNoTimeoutWakeLocks()
                locListeners        = batteryMetrics.getNumLocationListeners()
                gpsUses             = batteryMetrics.getNumGpsUses()
                domParsers          = batteryMetrics.getNumDomParsers()
                saxParsers          = batteryMetrics.getNumSaxParsers()
                xmlPullParsers      = batteryMetrics.getNumXMLPullParsers()

                print "\n"

                #db.saveBatteryMetric(noTimeoutWakeLocks, locListeners, gpsUses, domParsers, saxParsers, xmlPullParsers)



                #network timeout metrics
                print "========  Network Timeout Metrics =========\n"
                networkTimeout = NetworkTimeout.NetworkTimeout(sourceCodePaths,
                layoutFilePaths)
                networkTimeout.extractData()
                httpClients = networkTimeout.getNumHttpClients()
                numConTimeouts = networkTimeout.getNumConTimeouts()
                numSoTimeouts = networkTimeout.getNumSoTimeouts()
                numNoConTimeouts = networkTimeout.getNumNoConTimeout()
                numNoSoTimeouts = networkTimeout.getNumNoSoTimeout()

                print "\n"

                #db.saveNetworkMetric(httpClients, numConTimeouts, numSoTimeouts, numNoConTimeouts, numNoSoTimeouts)


                #black hole exception handling
                print "========  Black Hole Exception Handling Metrics =========\n"
                blackHole = BlackHole.BlackHole(sourceCodePaths, layoutFilePaths)
                blackHole.extractData()
                numCatchBlocks = blackHole.getNumCatchBlocks()
                numLogOnly = blackHole.getNumLogOnly()
                numNoAction = blackHole.getNumNoAction()
#
                print "Catch Blocks "+str(numCatchBlocks)
                print "LogOnly "+str(numLogOnly)
                print "No action "+str(numNoAction)
                print "\n"


                #db.saveBlackHolekMetric(numCatchBlocks, numLogOnly, numNoAction)



                #ANR Metrics
                print "========  ANR Metrics =========\n"
                anrMetrics = ANRMetrics.ANRMetrics(sourceCodePaths, layoutFilePaths)
                anrMetrics.extractData()

                network = anrMetrics.getNumNetworkOnMainThread()
                sqlLite = anrMetrics.getNumSQLLiteOnMainThread()
                fileIO = anrMetrics.getNumFileIOOnMainThread()
                bitmap = anrMetrics.getNumBitmapOnMainThread()

                print "\n"

                #db.saveANRkMetric(network, sqlLite, fileIO, bitmap)



                #intent launch metrics
                print "========  Intent Launch Metrics =========\n"
                intentLaunchMetrics = IntentLaunchMetrics.IntentLaunchMetrics(sourceCodePaths, layoutFilePaths, packageName)
                intentLaunchMetrics.extractData()

                startActivities             = intentLaunchMetrics.getNumStartActivities()
                startActivity               = intentLaunchMetrics.getNumStartActivity()
                startInstrumentation        = intentLaunchMetrics.getNumStartInstrumentation()
                startIntentSender           = intentLaunchMetrics.getNumStartIntentSender()
                startService                = intentLaunchMetrics.getNumStartService()
                startActionMode             = intentLaunchMetrics.getNumStartActionMode()
                startActivityForResult      = intentLaunchMetrics.getNumStartActivityForResult()
                startActivityFromChild      = intentLaunchMetrics.getNumStartActivityFromChild()
                startActivityFromFragment   = intentLaunchMetrics.getNumStartActivityFromFragment()
                startActivityIfNeeded       = intentLaunchMetrics.getNumStartActivityIfNeeded()
                startIntentSenderForResult  = intentLaunchMetrics.getNumStartIntentSenderForResult()
                startIntentSenderFromChild  = intentLaunchMetrics.getNumStartIntentSenderFromChild()
                startNextMatchingActivity   = intentLaunchMetrics.getNumStartNextMatchingActivity()
                startSearch                 = intentLaunchMetrics.getNumStartSearch()

                print "\n"

                #db.saveIntentLaunchkMetric(startActivities, startActivity, startInstrumentation, startIntentSender, startService, startActionMode, startActivityForResult, startActivityFromChild, startActivityFromFragment, startActivityIfNeeded, startIntentSenderForResult, startIntentSenderFromChild, startNextMatchingActivity, startSearch)


                folder = decFolderPath

                print "========  API Information =========\n"
                yml = open(decFolderPath+ '/apktool.yml')
                print(yml.read())
                yml.close()
                print "\n"

                print "Eliminazione "+decFolderPath

                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception, e:
                        print e

#                 db.writeAppTable(filename, appLabel, packageName, market)
#                 db.writeSizeMetricsTable(filename, numInstructions, numMethods,
#                 numClasses, methodsPerClass, instrPerMethod, cyclomatic, wmc)
#                 db.writeOOMetricsTable(filename, noc, dit, lcom, cbo, ppiv, apd)
#                 db.writeMVCMetricsTable(filename, mvc, avgNumViewsInXML,
#                 maxNumViewsInXML)
#                 db.writeOtherMetricsTable(filename, uncheckedBundles, potBadToken)
#                 db.updateNumFragments(filename,numFragments)
#                 db.writeAndroidObjectsTable(filename, objMap)
# #                 db.writeBadSmellMethodCallsTable(filename, show, dismiss,
# #                 setContentView, createScaledBitmap, onKeyDown, isPlaying, unregisterReceiver,
# #                 onBackPressed, showDialog, create)
#                 db.writeUncheckedBadSmellMethodCallsTable(filename, cshow, cdismiss,
#                 csetContentView, ccreateScaledBitmap, conKeyDown, cisPlaying, cunregisterReceiver,
#                 conBackPressed, cshowDialog, ccreate)
#                 db.writeBatteryMetrics(filename, noTimeoutWakeLocks, locListeners,
#                 gpsUses, domParsers, saxParsers, xmlPullParsers)
#                 db.writeNetworkTimeoutMetrics(filename, httpClients, numConTimeouts,
#                 numSoTimeouts, numNoConTimeouts, numNoSoTimeouts)
#                 db.writeBlackHole(filename, numCatchBlocks, numLogOnly, numNoAction)
#                 db.writeANRMetrics(filename, network, sqlLite, fileIO, bitmap,
#                 networkBg, sqlLiteBg, fileIOBg, bitmapBg)
#                 db.writeIntentLaunchMetrics(filename, startActivities, startActivity,
#                 startInstrumentation, startIntentSender, startService, startActionMode,
#                 startActivityForResult, startActivityFromChild, startActivityFromFragment,
#                 startActivityIfNeeded, startIntentSenderForResult, startIntentSenderFromChild,
#                 startNextMatchingActivity, startSearch)
            else:
                print "ERROR FOUND WITH FILE AndroidManifest.xml"
                #errorFile.write(f + ": ERROR FOUND WITH FILE AndroidManifest.xml\n")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            #errorFile.write(f + ": " + ''.join('!! ' + line for line in lines) +"\n")
    errorFile.close()


if __name__ == "__main__":

    INPUT_APKS = origin

    if DISASS:
        disass = Disass()
        disass.cleanUp()

    for root, dirs, files in os.walk(INPUT_APKS):
        for dir in dirs:
            if dir:
                if DISASS:
                    disass.decompile(dir)
                extractData(output,dir)

