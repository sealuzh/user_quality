import fileinput
import Class
import Method
import re
ignoreFiles = ["R.smali","R$attr.smali","R$dimen.smali","R$drawable.smali",
"R$id.smali","R$layout.smali","R$menu.smali","R$string.smali","R$style.smali"]


class CKMetrics(object):


    def __init__(self, sourceCodePaths, package):
        self.paths = sourceCodePaths
        self.numFiles = len(self.paths)
        self.lcom = 0.0
        self.cbo = 0.0
        self.maxDit = 0
        self.noc = 0
        self.classes = []
        self.ppiv = 0.0
        self.apd = 0
        self.package = package
        self.pkgpath = 'L' + self.package.replace('.','/') + '/'


    def getNumberofFiles(self):
        return self.numFiles


    def extractData(self):

        for path in self.paths:
            self.extractFileData(path)

        self.determineChildrenFromParents()
        self.noc = self.calculateNOC()
        print "Children "+str(self.noc)
        self.maxDit = self.calculateMaxDIT()
        print "DIT "+str(self.maxDit)
        self.lcom = self.calculateLCOM()
        print "LCom "+str(self.lcom)
        self.cbo = self.calculateCBO()
        print "CBO "+str(self.cbo)
        self.apd = self.apd / float(len(self.classes))
        self.ppiv = self.calculatePercentPublicInstanceVariables()
        print "PPIV "+str(self.ppiv)
        self.printData()


    def extractFileData(self, path):

        curClass = Class.Class()

        for line in fileinput.input([path]):
            if line.startswith('.class '):
                if self.pkgpath not in line:
                    continue

                curClass.setPackage(self.extractPackage(line))
                curClass.setName(self.extractClassName(line))

            elif line.startswith('.super '):
                if(self.pkgpath in line):
                    curClass.setParent(self.extractClassName(line))
                matches = re.findall("Landroid/app/(.*?)Activity", line)
                curClass.isController = (len(matches) > 0)
            elif(line.startswith('.field')):
                fieldName = line[line.rfind(" ")+1:line.rfind(":")]
                curClass.addField(fieldName)
                if(' public ' in line or ' protected ' in line):
                    curClass.addPublicField(fieldName)
            elif(line.startswith('.method ')):
                if('<init>' in line):
                    curMethod = Method.Method('constructor')
                else:
                    match = re.findall(".method (.*?)\(", line)[0].split(" ")
                    l = len(re.findall(".method (.*?)\(", line)[0].split(" "))
                    if l == 3:
                        curMethod = Method.Method(str(match[2]))
                    elif l == 2:
                        curMethod = Method.Method(str(match[1]))
                    elif l ==1:
                        curMethod = Method.Method(str(match[0]))
                    curMethod = Method.Method("Generic")

                    curClass.addMethod(curMethod)
            elif(";->" in line):
                if(self.usesField(curClass, line)): #for LCOM
                    fieldName = line[line.rfind(";->")+3:line.rfind(":")]
                    curMethod.addFieldUsed(fieldName)
                    if fieldName in curClass.getPublicFields():
                        self.apd = self.apd + 1
                    else: #for CBO
                        if not curClass.isController and self.refsNonJavaClass(line):
                            objName = line[line.index("L"):line.index(";->")]
                            if not objName == curClass.getName() and not self.inSameTree(curClass, objName):
                                curClass.addCoupledObject(objName)
        self.classes.append(curClass)



    def refsNonJavaClass(self, line):
        pkgRegex = "L(.*?);"
        javaPkgRegex = "Ljava/(.*?)"
        pkgMatches = re.findall(pkgRegex, line)
        javaPkgRegex = re.findall(javaPkgRegex, line)
        return len(pkgMatches) - len(javaPkgRegex) > 0


    def extractPackage(self, line):
        pkg = line.split()[-1]
        pkg = pkg[:pkg.rfind("/")]
        return pkg


    #Gets the class name
    def extractClassName(self, line):

        return line.split()[-1].replace(";","")


    def determineChildrenFromParents(self):
        for aClass in self.classes:
            if aClass.getParent() != '':
                parent = self.getClassByName(aClass.getParent())
                parent.addChild(aClass)


    def getClassByName(self, name):
        for aClass in self.classes:
            if aClass.getName() == name:
                return aClass


    def calculateLCOM(self):
        classLCOM = []
        for aClass in self.classes:
            if aClass.getName() != "":
                if(len(aClass.getFields()) == 0) or (len(aClass.getMethods()) == 0):
                    continue
                #numFieldCalls = 0
                methodLCOM = []
                fieldcount = {} #number of methods using each field in a class
                for aField in aClass.getFields():
                    fieldcount[aField] = 0

                for aMethod in aClass.getMethods():
                    for aField in aMethod.getFieldsUsed():
                        fieldcount[aField] = fieldcount[aField] + 1

                for aField in aClass.getFields():
                    methodLCOM.append(float(fieldcount[aField]) /len(aClass.getMethods()))
                    #c = fieldcount.intersection(fieldcountanother)
                classLCOM.append(1 - self.avg(methodLCOM))
        return self.avg(classLCOM) * 100
        #return 50

    #determine it objName is the name of any class in the inheritance tree of curClass
    def inSameTree(self, curClass, objName):
        try:
            while not curClass.getParent() == '':
                if curClass.getName() == objName:
                    return True
                curClass = self.getClassByName(curClass.getParent())
            return self.depthFirstTreeSearch(curClass, objName)
        except AttributeError:
            return False


    def depthFirstTreeSearch(self, curClass, objName):
        if(curClass.getName() == objName):
            return True
        for aChild in curClass.getChildren():
            return self.depthFirstTreeSearch(curClass, aChild.getName())
        return False


    def avg(self, list):
        if(len(list)) == 0:
            return 0
        total = 0.0
        for num in list:
            total = total + num
        return total / len(list)


    #calculate avg number of coupled objects per class
    def calculateCBO(self):
        totalCBO = 0
        length = 0
        for aClass in self.classes:
            totalCBO = totalCBO + len(aClass.getCoupledObjects())
            length = length + 1
        return totalCBO / float(length)


    def calculateNOC(self):
        noc = 0
        for aClass in self.classes:
            #print "Classe "+aClass.getName()+" noc "+str(len(aClass.getChildren()))
            if(len(aClass.getChildren()) > self.noc):
                noc = len(aClass.getChildren())
        return noc


    def calculateMaxDIT(self):
        maxHeight = 0
        for aClass in self.classes:
            if aClass.getParent() == '':
                height = self.getTreeHeight(aClass)
                if height > maxHeight:
                    maxHeight = height
        return maxHeight


    def getTreeHeight(self, aClass):
        if len(aClass.getChildren()) == 0:
            return 1
        max = 0
        for child in aClass.getChildren():
            curHeight = 1 + self.getTreeHeight(child)
            if curHeight > max:
                max = curHeight
        return max


    def calculatePercentPublicInstanceVariables(self):
        public = 0
        total = 0
        for aClass in self.classes:
            public = public + len(aClass.getPublicFields())
            total = total + len(aClass.getFields())
        if total == 0:
            return 0
        return (public / float(total)) * 100


    def usesField(self, curClass, line):
        field = line[line.rfind(";->")+3:line.rfind(":")]
        return field in curClass.getFields()


    def getNOC(self):
        return self.noc


    def getDIT(self):
        return self.maxDit

    def getLCOM(self):
        return self.lcom

    def getCBO(self):
        return self.cbo

    def getPPIV(self):
        return self.ppiv

    def getAPD(self):
        return self.apd

    #for debugging - will write to database (this will drive schema)
    def printData(self):
        print 'Max NOC: ' + str(self.noc)
        print 'Max DIT: ' + str(self.maxDit)
        print 'LCOM: ' + str(self.lcom) + '%'
        print 'CBO: ' + str(self.cbo)
        print 'PPIV: ' + str(self.ppiv) + '%'
        print 'APD: ' + str(self.apd) + ' accesses per class'