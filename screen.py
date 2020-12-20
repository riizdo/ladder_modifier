from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory


class Screen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.master.geometry('1200x600+0+0')
        self.master.title('Ladder Modifier')
        
        self.__createMenuBar()
        
        
        self.p = Button(self, text = 'hola', width = 10)
        self.p.pack()
    
    
    def __loadFile(self):
        file = askopenfilename(filetypes=(("Ladder files", "*.LST"), ("All files", "*.*") ))
        
        
    def __saveFile(self):
        pass
    
    
    def __saveAs(self):
        pass
        
        
    def __createMenuBar(self):
        self.__menuBar = Menu(self)
        self.master.config(menu = self.__menuBar)
        
        self.__fileMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = 'Archivo', menu = self.__fileMenu)
        self.__fileMenu.add_command(label = 'Abrir', command = self.__loadFile)
        self.__fileMenu.add_command(label = 'Guardar', command = self.__saveFile)
        self.__fileMenu.add_command(label = 'Guardar como..', command = self.__saveAs)
        
        self.__editMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = 'Editar', menu = self.__editMenu)
        
    
    def destroyElement(self, element):
        element.destroy()
        
        
    def main(self):
        pass
        

if __name__ == '__main__':
    root = Tk()
    app = Screen(root)
    app.mainloop()