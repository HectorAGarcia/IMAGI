#Command Check
class CommandCheck():
    def __init__(self,cmdList):
        self.commands=cmdList


    def validCommand(self,Name,nAtributes):
        if self.validName(Name):
            if self.validNAtributes(Name,nAtributes):
                return ""
            else:
                return "Illegal Number of Atributes: "+str(nAtributes)
        return "Not valid command: "+Name


    def validName(self,Name):
        for key in self.commands.keys():
            if key == Name:
                return True
        return False

    def validNAtributes(self,Name,nAtributes):
        if self.commands[Name].getNAtributes()==nAtributes:
            return True
        return False



#Command Class
class Command():
    def __init__(self,Name,nAtributes,executable):
        self.name=Name
        self.nAtributes=nAtributes
        self.executable=executable


    def getName(self):
        return self.name

    def getNAtributes(self):
        return self.nAtributes

    def getExe(self):
        return self.executable



#CommandProccessor
class CommandProccesor():

    def __init__(self):
        self.commands={}
        self.loadCommands()
        self.cmdcheck= CommandCheck(self.commands)

    def execute(self, cmd, natributes,target):
        valid=self.cmdcheck.validCommand(cmd,natributes)
        if valid=="":
                self.commands[cmd].getExe()(target)
        else:
            print valid


    def addCommand(self,Name, natributes,executable):
        self.commands[Name]=Command(Name,natributes,executable)

    def loadCommands(self):
        self.addCommand("jump",0,jumpexe)
        self.addCommand("sing",0, singexe)
        self.addCommand("domath",0,domathexe)


#Commands executables

def jumpexe(tokens):
    print tokens[0].getValue()+" jump!"

def singexe(tokens):
    print tokens[0].getValue()+" Sing!"

def domathexe(tokens):
    if tokens[2].getValue()=="+":
        print sum(tokens[3].getValue())
    elif tokens[2].getValue()=="-":
        print sub(tokens[3].getValue())
    elif tokens[2].getValue()=="*":
        print mult(tokens[3].getValue())
    else:
        print div(tokens[3].getValue())


#Check Variables existance
def check_Num_Exist(name,list):

    for item in list.keys():
        if name == item:
            return True
    return False

#Math operations:

def sub(items):
    return "subtraction"

def mult(items):
    return "mult"

def div(items):
    return "division"

def sum(items):
    sum=0
    i=0
    list=compiler.get_TokenizerNUMVAR()
    for item in items:
        i=0
        try:
            i=int(item)
        except ValueError:
            if check_Num_Exist(item,list):
                i=int(list[item])
            else:
                return "Not valid variable: "+item
        sum=sum+i
    return str(sum)












#Tokenizer

class Tokenizer():
    def __init__(self):
        self.setUpTokenizer()
        self.interrupt=Interrupt()
        self.WordVariables={}
        self.NumberVariables={}

    def tokenize(self,line):
        items=line.split(" ")
        tokens=[]
        self.interrupt.clrFlag()
        for token in items:
            if not self.interrupt.checkFlag():
                item=self.checkToken(token)
                if item !="":
                    tokens.append(item)
                else:
                    print "Not valid token: "+str(token)
        if self.interrupt.checkFlag():
            self.interrupt.executeISR(self,tokens,items)

        if len(items)!= len(tokens) and not self.interrupt.checkFlag():
            print "Operation can't be completed"
            return tokens
        else:
            return tokens



    def checkifStringRule(self,items):
        count =0
        if items[2][0]=='"':
            x=len(items[len(items)-1])
            if items[len(items)-1][x-1] =='"':
                for item in items:
                    for c in item:
                        if c =='"':
                            count+=1
        return count ==2

    def checkToken(self, token):
        if self.if_character(token):
            return self.createToken(token,"character")
        if self.if_command(token) and token != "domath":
            return self.createToken(token,"command")
        if self.if_atribute(token):
            return self.createToken(token,"atribute")
        if self.if_word(token):
            self.interrupt.raiseFlag("Word")
            return self.createToken(token,"Word")
        if self.if_Math(token):
            self.interrupt.raiseFlag("Math")
            return self.createToken(token,"command")
        if self.if_Number(token):
            self.interrupt.raiseFlag("Number")
            return self.createToken(token,"Number")
        return ''


    def setUpTokenizer(self):
        self.characters=["fish",'lion','bird']
        self.commands=["sing","dance","jump","walk",'say','grow','shrink','flip','run','domath']
        self.atributes=["right",'left']
        self.operators=["+","-","*"]


    def if_Number(self,token):
        if token =="Number":
            return True
        return False


    def if_character(self,token):
        for character in self.characters:
            if token == character:
                return True
        return False

    def if_command(self,token):
        for command in self.commands:
            if token == command:
                return True
        return False

    def if_atribute(self,token):
        for atribute in self.atributes:
            if token == atribute:
                return True
        return False

    def if_word(self,token):
        if token=="Word":
            return True
        return False

    def if_Math(self,token):
        if token=="domath":
            return True
        return False

    def toString(self, items):
        token=''
        for item in items[2:]:
            token=token+" "+item
        return self.createToken(token[2:len(token)-1],"String")

    def validateOP(self,op):
        for oper in self.operators:
            if op == oper:
                return True
        return False

    def getWordDict(self):
        return self.WordVariables

    def getNumberDict(self):
        return self.NumberVariables

    def createToken(self,value,ID):
        token=Token(value)
        token.setID(ID)
        return token

#token object
class Token():

    def __init__(self,value):
        self.value=value
        self.ID=""

    def getID(self):
        return self.ID

    def getValue(self):
        return self.value

    def setID(self,ID):
        self.ID=ID


#Compiler

class Compiler():
    def __init__(self):
        self.tokenizer=Tokenizer()
        self.loadValidStatements()
        self.cmdPC= CommandProccesor()

    def loadValidStatements(self):
        self.statements=[]
        statement1=['character','command','atribute']
        statement2=['character','command']
        statement3=['Word','Name','String']
        statement4=['Number','Name','Value']
        statement5=['character','command','Operator','List']
        self.statements.append(statement1)
        self.statements.append(statement2)
        self.statements.append(statement3)
        self.statements.append(statement4)
        self.statements.append(statement5)


    def checkIFValidStatement(self,tokens):
        i=0
        valid=False
        while i < len(self.statements)and (not valid):
            j=0
            coincidence=0
            if len(self.statements[i])== len(tokens):
                while j<len(tokens) and (not valid):
                    if self.statements[i][j]==tokens[j].getID():
                        coincidence+=1
                    if coincidence == len(self.statements[i]):
                        valid=True
                    j+=1

            i+=1
        return valid

    def compile(self, line):
        tokens=self.tokenizer.tokenize(line)
        if self.checkIFValidStatement(tokens):

            #self.printStatement(tokens)
            index=self.find_cmd(tokens)

            if index!=-1:
                self.cmdPC.execute(tokens[index].getValue(),self.count_atributes(tokens),tokens)

        else:
            print "Not valid statement!"

    def printStatement(self, tokens):
        out=""
        for item in tokens:
            out=out+item.getID()+": "+item.getValue()+" "
        print out

    def count_atributes(self,tokens):
        count=0
        for token in tokens:
            if token.getID()=="atribute":
                count+=1
        return count

    def find_cmd(self,tokens):
        index=0
        for token in tokens:
            if token.getID()=="command":
                return index
            index+=1
        return -1

    def get_TokenizerNUMVAR(self):
        return self.tokenizer.getNumberDict()



class Interrupt():
    def __init__(self):
        self.flag=0
        self.flagName=""
        self.ISR={"Word":self.WordISR,"Math": self.MathISR,"Number":self.NumberISR}


    def raiseFlag(self,name):
        self.flag=1
        self.flagName=name

    def clrFlag(self):
        self.flag=0
        self.flagName=""

    def checkFlag(self):
        return self.flag==1

    def executeISR(self, instance,tokens,items):
        self.ISR[self.flagName](instance,tokens,items)



    def NumberISR(self,instance,tokens,items):
        if len(items)==3:
             tokens.append(instance.createToken(items[1],"Name"))
             tokens.append(instance.createToken(items[2],"Value"))
             instance.NumberVariables[items[1]]=items[2]


    def WordISR(self,instance,tokens, items):

        if len(items) > 2 and instance.checkifStringRule(items):
            tokens.append(instance.createToken(items[1],"Name"))
            tokens.append(instance.toString(items))
            instance.WordVariables[items[1]]=tokens[len(tokens)-1].getValue()
            print instance.getWordDict()


    def MathISR(self,instance,tokens,items):
        list=[]
        if len(items)> 3:
            if instance.validateOP(items[2]):
                tokens.append(instance.createToken(items[2],"Operator"))
                for item in items[3:]:
                     if item !="":
                         list.append(item)
                tokens.append(instance.createToken(list,"List"))
        if len(tokens) < 3:
            tokens.append(instance.createToken("not valid","String"))




compiler=Compiler()
text="fish jump;fish domath + 5 6; jump fish "
s=text.split(";")
for line in s:
    compiler.compile(line)
