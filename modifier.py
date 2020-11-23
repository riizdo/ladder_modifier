#file: modifier.py
#author: riizdo
#date: 18/11/20
#description: modifier for ladder program in motoman's robots



class Modifier():
    def __init__(self):
        self.__version = 0
        self.__header = 'is a program to simplify the modification of the motoman ladder, version: {}.'.format(self.__version)
        self.__path = ''
        self.__program = []
        self.__segments = []
        self.__menus = ('CHANGE', 'CONSULT', 'EXIT')
        self.__instructions = ('STR', 'GSTR', 'OUT', 'GOUT', 'AND', 'OR', 'AND-NOT', 'OR-NOT', 'OR-STR', 'AND-STR')
        
        
    def __str__(self):
        return self.__header
    

    def searchDirection(self, direction):
        #print(self.__segments)
        pass       
                
    def __comproveLine(self, line):
        l = []
        for element in line:
            if element == '#':
                l = line.split(' #')
                l[1] = self.__isDigit(l[1])
                return l
        return line
    
    
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
                    
            print(segment)
            self.__segments.append(segment)
            currentLine += positions[counter]
            counter += 1
            
            
            
    def __isLine(self, data):
        for text in self.__instructions:
            if data == text:
                return True
            return False
                
        
    def exit(self):
        exit()
        
        
    def readFile(self, file):
        counter = 0
        outList = []
        try:
            with open(file) as f:
                for line in f:
                    treatLine = self.__comproveLine(line)
                    self.__program.append(treatLine)
                    if treatLine[0] != None and (treatLine[0] == 'OUT' or treatLine[0] == 'GOUT'):
                        outList.append(counter)
                    counter += 1
        except:
            print('the file no exist or the path is incorrect')
            self.exit()
        
        self.__formSegments(self.__program, outList)
        #print(self.__segments)
        

    def printData(self):
        print(self.__program)
        
        
    def getMenus(self):
        return self.__menus
        
    
    
if __name__ == '__main__':
    app = Modifier()
    print('')
    app.readFile(input('enter the name of archive: '))
    
    print('')
    menus = app.getMenus()
    text = 'select operation: ' + str(menus).upper()
    menu = input(text).upper()
    print('')
    if menu == menus[0]:
        pass
    elif menu == menus[1]:
        direction = input('enter the direction: ')
        app.searchDirection(direction)
    elif menu == menus[2]:
        app.exit()
    else:
        print('this menu is not correct')
        app.exit()