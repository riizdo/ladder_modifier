#modifier for ladder program in motoman's robots



class Modifier():
    def __init__(self):
        self.__version = 0
        self.__header = 'is a program to simplify the modification of the motoman ladder, {} version'.format(self.__version)
        
        
    def __str__(self):
        return self.__header
    
    
    
    
    
    
if __name__ == '__main__':
    app = Modifier()
    print(app)