#modifier for ladder program in motoman's robots



class Modifier():
    def __init__(self):
        self.__version = 0
        self.__header = 'is a program to simplify the modification of the motoman ladder, {} version'.format(self.__version)
        self.__path = ''
        
        
    def __str__(self):
        return self.__header
    
    
    def begin(self):
        print(self)
        self.__path = input('enter the name of archive and his path: ')
        
        
    
    
    
if __name__ == '__main__':
    app = Modifier()
    app.begin()