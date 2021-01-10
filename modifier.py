#file: modifier.py
#author: riizdo
#date: 18/11/20
#description: modifier for ladder program in motoman's robots


class Program():
    def __init__(self):
        self.fileName = ''
        self.simpleProgram = ''
        self.consDirections = {}
        self.instructions = []
        self.movements = []
        self.comments = ''
        self.iniProgram = ''
        self.endProgram = ''
        self.positionComments = []
        self.positionInstructions = []
        self.positionMovements = []
        self.positionVariables = []
    
    
    def file(self, file = None):
        if file == None:
            if self.fileName == None or self.fileName == '':
                return None
            partsFile = self.fileName.split('/')
            latest = len(partsFile) -1
            return partsFile[latest]
        else:
            self.fileName = file
            
            
    def readFile(self, file):
        ini = 0
        counter = 1
        outList = []
        program = []
        
        try:
            with open(file) as f:
                self.simpleProgram = f.read()
        except:
            print('the file no exist or the path is incorrect')
            return 'read file failed'    
                
        self.fileName = file
        lines = self.simpleProgram.split('\n')
        for line in lines:
            comment = {}
            instruction = {}
            movement = {}
            words = line.split(' ')
            for word in words:
                nWord = len(word)
                position = self.isInstruction(word)
                if position != None:
                    instruction['ini'] = '{}.{}'.format(counter, ini)
                    instruction['end'] = '{}.{} + {}c'.format(counter, ini, position)
                    self.positionInstructions.append(instruction)
                position = self.isMovement(word)
                if position != None:
                    movement['ini'] = '{}.{}'.format(counter, ini)
                    movement['end'] = '{}.{} + {}c'.format(counter, ini, position)
                    self.positionMovements.append(movement)
                ini += nWord + 1
            
            position = self.isComment(line)
            if position != None:
                comment['ini'] = '{}.{}'.format(counter, position['ini'])
                comment['end'] = '{}.{} + {}c'.format(counter, position['ini'], position['nChars'])
                self.positionComments.append(comment)
                
            counter += 1
            ini = 0
        
        #self.__formSegments(program, outList)
        return 'ok'
            
            
    def isComment(self, text):
        position = {}
        nText = len(text)
        nChar = len(self.comments)
        count = 0
        word = ''
        
        for i in text:
            for i in range(count, count + nChar):
                word += text[i]
            if word == self.comments:
                position['ini'] = count
                position['nChars'] = nText - count
                #position = '{} + {}c'.format(count, nText - count)
                return position
            count += 1
            word = ''
            
        return None
    
    
    def isInstruction(self, text):
        for instruction in self.instructions:
            if text == instruction:
                return len(text)
        return None
                        
    
    def isMovement(self, text):
        for movement in self.movements:
            if text == movement:
                return len(text)
        return None
    
    
    def isVariable(self, text):
        pass
    
    
    def getPositionComments(self):
        return self.positionComments
    
    
    def getPositionInstructions(self):
        return self.positionInstructions
    
    
    def getPositionMovements(self):
        return self.positionMovements
    
    
    def getPositionVariables(self):
        return self.positionVariables
    
            
    def getTypeFile(self):
        partFile = self.fileName.split('.')
        return partFile[len(partFile) - 1]
    
    
    def getProgram(self):
        return self.simpleProgram
    
    
    def getInstructions(self):
        return self.instructions
    
    
    def getMovements(self):
        return self.movements
    
    
    def getComments(self):
        return self.comments
    
    
    def getVariables(self):
        return self.variables
    
    
    def getIniProgram(self):
        return self.iniProgram
    
    
    def getEndProgram(self):
        return self.endProgram
            
            
            
            
        
class Ladder(Program):
    def __init__(self):
        Program.__init__(self)
        self.__version = 0
        self.__header = 'is a program to simplify the modification of the motoman ladder, version: {}.'.format(self.__version)
        self.__path = ''
        self.__program = []
        self.__segments = []
        self.__menus = ('CHANGE', 'CONSULT', 'EXIT')
        self.instructions = ['STR', 'GSTR', 'OUT', 'GOUT', 'AND', 'OR', 'AND-NOT', 'OR-NOT', 'OR-STR', 'AND-STR', 'STR-NOT', 'PART', 'END']
        self.comments = '/'
        self.iniProgram = ''
        self.endProgram = 'END'
        
        
        self.consDirections['general input'] = ['input', 10, 2567]
        self.consDirections['general output'] = ['output', 10010, 12567]
        self.consDirections['external input'] = ['input', 20010, 22567]
        self.consDirections['external output'] = ['output', 30010, 32567]
        self.consDirections['specific input'] = ['input', 40010, 41607]
        self.consDirections['specific output'] = ['output', 50010, 52007]
        self.consDirections['interface panel input'] = ['input', 60010, 60647]
        self.consDirections['auxiliary relay'] = ['input/output', 70010, 79997]
        self.consDirections['control status'] = ['', 80010, 80647]
        self.consDirections['pseudo input'] = ['input', 82010, 82207]
        self.consDirections['network input'] = ['input', 25010, 27567]
        self.consDirections['network output'] = ['output', 35010, 37567]
        #self.consDirections['general registrer'] = ['input/output', 'm000', 'm559']
        #self.consDirections['analog input registrer'] = ['input', 'm600', 'm639']
        #self.consDirections['analog output registrer'] = ['output', 'm560', 'm599']
        #self.consDirections['system registrer'] = ['', 'm640', 'm999']
        
        
    def __str__(self):
        return self.__header
    

    def __searchDirection(self, direction):
        counterSegment = 0
        positions = []
        for segment in self.__segments:
            counterLine = 0
            pos = []
            for line in segment:
                if (direction == line[1] and line[0] != 'GSTR' and line[0] != 'GOUT')\
                   or ((line[0] == 'GSTR' or line[0] == 'GOUT') and int(line[1]) <= int(direction)\
                       and int(self.__addStr(line[1], 7)) >= int(direction)):
                    pos.append(counterSegment)
                    pos.append(counterLine)
                    positions.append(pos)
                    break
                counterLine += 1
                    
            counterSegment += 1
        
        return positions
    
    
    def __comproveDirection(self, dir1, dir2 = None):
        if len(dir1) != 5:
            return 'the first direction is incorrect'
        try:
            dir1 = int(dir1)
        except:
            return 'the first direction is incorrect'
        if dir2 != None:
            if len(dir2) != 5:
                return 'the second direction is incorrect'
            try:
                dir2 = int(dir2)
            except:
                return 'the second direction is incorrect'
            
            tDir1 = ''
            tDir2 = ''
            for element in self.consDirections:
                if dir1 > self.consDirections[element][1] and dir1 < self.consDirections[element][2]:
                    tDir1 = self.consDirections[element][0]
                if dir2 > self.consDirections[element][1] and dir2 < self.consDirections[element][2]:
                    tDir2 = self.consDirections[element][0]
            if tDir1 == tDir2 and tDir1 == 'input':
                return 'the two directions are inputs, it is incorrect'
            elif tDir1 == tDir2 and tDir1 == 'output':
                return 'the two directions are outputs, it is incorrect'
            
        return 'ok'
    
    
    def assignDirection(self, dir1, dir2):
        segment = []
        line1 = []
        line2 = []
        pos1 = self.__searchDirection(dir1)
        pos2 = self.__searchDirection(dir2)
        error = ''
        
        error = self.__comproveDirection(dir1, dir2)
        if error != 'ok':
            return error
        
        if len(pos1) > 2:
            return 'the {} direction is used in several segments'.format(dir1)
        if len(pos2) > 2:
            return 'the {} direction is used in several segments'.format(dir2)
        
        if self.__segments[pos1[0][0]][0][0] == 'GSTR':
            self.__separateGroup(pos1[0][0])
            pos1 = self.__searchDirection(dir1)
            pos2 = self.__searchDirection(dir2)
        if self.__segments[pos2[0][0]][0][0] == 'GSTR':
            self.__separateGroup(pos2[0][0])
            pos2 = self.__searchDirection(dir2)
            
        line1.append('STR')
        line1.append(dir1)
        line2.append('OUT')
        line2.append(dir2)
        segment.append(line1)
        segment.append(line2)
        
        self.__segments.pop(pos1[0][0])
        pos2 = self.__searchDirection(dir2)
        self.__segments.pop(pos2[0][0])
        self.__segments.append(segment)
        
        return 'ok'
        
    
    def __separateGroup(self, posSegment):
        counter = 0
        segGroup = self.__segments[posSegment]
        for i in range (0, 8):
            segment = []
            line1 = []
            line2 = []
            line1.append('STR')
            line1.append(str(int(segGroup[0][1]) + counter))
            line2.append('OUT')
            line2.append(str(int(segGroup[1][1]) + counter))
            segment.append(line1)
            segment.append(line2)
            counter += 1
            self.__segments.append(segment)
        self.__segments.pop(posSegment)
                
                
    def __comproveLine(self, line):
        l = []
        for element in line:
            if element == '#':
                l = line.split(' #')
                l[1] = self.__isDigit(l[1])
                return l
            else:
                l = line.split(' ')
                if l[0] == 'PART':
                    return l
        return line
    
    
    def __addStr(self, num1, num2):#add 2 strings and return string
        return str(int(num1) + int(num2))
    
    
    def __isDigit(self, data):
        number = ''
        for element in data:
            if element.isdigit():
                number += element
        return number
    
    
    def __formSegments(self, data, positions):
        counter = 0
        currentLine = 0
        for i in range (0, len(positions)):
            segment = []
            for i in range (currentLine, positions[counter] + 1):
                t = self.__isLine(data[i][0])
                if t:
                    segment.append(data[i])
                    
            self.__segments.append(segment)
            currentLine = positions[counter] + 1
            counter += 1
    
    
    def showDirection(self, direction):
        counter = 0
        positions = self.__searchDirection(direction)
        if positions != None:
            for element in positions:
                print(self.__segments[int(element[0])])
        else:
            print('{} is not used'.format(direction))
            
            
    def __isLine(self, data):
        for text in self.instructions:
            if data == text:
                return True
        return False
                
        
    def exit(self):
        exit()
        
    '''    
    def readFile(self, file):
        counter = 0
        outList = []
        program = []
        print('readFile')
        try:
            with open(file) as f:
                print('openFile', f)
                self.simpleProgram = f.read()
                self.fileName = file
                lines = self.simpleProgram.split('\n')
                for line in lines:
                    print('line')
                    self.__program.append(line)
                    comment = self.isComment(line)
                    print('comment: ', comment)
                    if comment != None:
                        self.positionComments.append(comment)
                    treatLine = self.__comproveLine(line)
                    program.append(treatLine)
                    if treatLine[0] != None and (treatLine[0] == 'OUT' or treatLine[0] == 'GOUT' or treatLine[0] == 'PART'):
                        outList.append(counter)
                    counter += 1
        except:
            print('the file no exist or the path is incorrect')
            return 'read file failed'
        
        self.__formSegments(program, outList)
        return 'ok'
    '''    
        
    def writeFile(self, file):
        counter = 0
        with open(file, 'w') as f:
            for lineFile in self.__program:
                treatLine = self.__comproveLine(lineFile)
                if self.__isLine(treatLine[0]):
                    if counter == 0:
                        for segment in self.__segments:
                            for line in segment:
                                if line[0] != 'PART':
                                    f.write(line[0] + ' #' + line[1] + '\n')
                                else:
                                    f.write(line[0] + ' ' + line[1])
                                counter += 1
                else:
                    f.write(lineFile)
            #f.write('\n')
            #f.write('\n')
            #f.write('\n')
        

    def printData(self):
        print(self.__program)
        
        
    def getMenus(self):
        return self.__menus
    
    
    
    
    
    def getSegments(self):
        return self.__segments
    
    
    
    
    
class Job(Program):
    def __init__(self):
        Program.__init__(self)
        self.instructions = ['IF', 'SET', 'GET', 'SETE', 'MUL', 'GETS',\
                             'GETE', 'IFTHEN', 'ENDIF', 'REFP', 'DOUT',\
                             'WAIT', 'PULSE', 'PAUSE', 'END', 'NOP', 'TIMER',\
                             'DIN']
        self.movements = ['MOVJ', 'MOVL', 'MOVC', 'IMOV']
        self.comments = '/'
        self.iniProgram = 'NOP'
        self.endProgram = 'END'
            
            
        
    
    
    
    
if __name__ == '__main__':
    app = Ladder()
    print('')
    app.readFile(input('enter the name of archive: '))
    
    print('')
    menus = app.getMenus()
    text = 'select operation: ' + str(menus).upper()
    menu = input(text).upper()
    print('')
    if menu == menus[0]:
        dir1 = input('enter the direction: ')
        print('')
        dir2 = input('enter the other direction: ')
        
        app.showDirection(dir1)
        print('')
        app.showDirection(dir2)
        print('')
        if input('are you sure(y - n): ') != 'y':
            app.exit()
            
        print('')
        error = app.assignDirection(dir1, dir2)
        
        if error != 'ok':
            print('')
            print(error)
            app.exit()
            
        app.writeFile('test1.txt')
        print('')
        print('change succesful')
        
    elif menu == menus[1]:
        direction = input('enter the direction: ')
        print('')
        app.showDirection(direction)
    elif menu == menus[2]:
        app.exit()
    else:
        print('this menu is not correct')
        app.exit()
        
