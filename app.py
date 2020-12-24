from tkinter import *
import screen
import modifier


class App():
    def __init__(self):
        root = Tk()
        self.__screen = screen.Screen(root)
        self.__modifier = modifier.Modifier()
        
        
        self.__screen.mainloop()
        
        
if __name__ == '__main__':
    app = App()