import os
import os.path
import shutil
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read("config.ini")
INPUT_APKS 	= Config.get('paths', 'input')
OUTPUT 		= Config.get('paths', 'output')

class Disass(object):

    def __init__(self):
        print ""
        
    def cleanUp(self):
        
        print "Cleaning up.."
        folder = OUTPUT
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception, e:
                print e
        
    def decompile(self, family):
    
        count = 0
        for root, dirs, files in os.walk(INPUT_APKS+"/"+family):
            for file in files:
                out = str(str(file)).replace(" ", "")
                print "Selected package "+out
		out = out.replace('.apk', '')
                try:
                    print "********************************************"
                    os.system("java -jar apktool.jar -v d -f \""+os.path.join(root, file)+"\" -o "+OUTPUT+"/"+out)
                    count += 1
                except Exception:
                    pass
                print "********************************************"
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print ""+str(count)+" files decompiled in "+OUTPUT+"/"+out
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
