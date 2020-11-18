#modifier for ladder program in motoman's robots



class Modifier():
    def __init__(self):
        self.__version = 0
        self.__header = 'is a program to simplify the modification of the motoman ladder, version: {}.'.format(self.__version)
        self.__path = ''
        self.__data = ''
        
        self.__begin()
        
        
    def __str__(self):
        return self.__header
    
    
    def __begin(self):
        print(self)
        self.__path = input('enter the name of archive: ')
        
        try:
            f = open(self.__path, 'r')
            f.close()
            self.__readFile(self.__path)
        except:
            print('the file no exist or the path is incorrect')
            
            
    def __menu():
        pass
        
        
    def __readFile(self, file):
        f = open(file, 'r')
        self.__data = f.read()
        f.close()
        
        
    def printData(self):
        print(self.__data)
        
    
    
if __name__ == '__main__':
    app = Modifier()
    app.printData()