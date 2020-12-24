from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import modifier
import text


class Screen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.__title = 'Ladder Modifier -'
        self.pack()
        self.master.geometry('1200x600+0+0')
        
        self.__indexMenuBar = []
        self.__texts = text.TextLibrary()
        
        self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        
        self.__languages = ('English', 'Spanish')
        self.__languageSelected = 'English'
        self.__text = {}
        
        self.__ladder = modifier.Modifier()
        
        self.__createMenuBar()
        
        self.__textEditor = []
        
        self.__noteBook = ttk.Notebook(master)
        self.__noteBook.pack(anchor = NW)
            
        self.p = Button(self, text = 'hola', width = 10)
        self.p.pack()
    
    
    def __loadFile(self):
        file = askopenfilename(filetypes=(('Ladder files', '*.LST'), ('Job files', '*.JBI'), ('All files', '*.*')))
        error = self.__ladder.readFile(file)
        if error != 'ok':
            return 'error load file'
        
        self.master.title(self.__title + ' ' + file)
        textEditor = Text(self.__noteBook)
        print(self.__ladder.getSegments())
        textEditor.insert('insert', self.__ladder.getProgram())
        self.__textEditor.append(textEditor)
        self.__noteBook.add(self.__textEditor[len(self.__textEditor) -1], text = self.__ladder.file())
        self.__noteBook.select(self.__textEditor[len(self.__textEditor) -1])
        
        return 'ok'
    
    
    def __closeFile(self):
        pass
        
        
    def __saveFile(self):
        file = self.__ladder.file()
        self.ladder.writeFile(file)
    
    
    def __saveAs(self):
        file = asksaveasfilename()
        self.__ladder.writeFile(file)
    
    
    def __exit(self):
        pass
        
        
    def __createMenuBar(self):
        self.__menuBar = Menu(self)
        self.master.config(menu = self.__menuBar)
        
        self.__fileMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('File'), menu = self.__fileMenu)
        self.__indexMenuBar.append(self.__menuBar.index(self.__texts.getText('File')))
        self.__fileMenu.add_command(label = 'Abrir', command = self.__loadFile)
        self.__fileMenu.add_command(label = 'Cerrar', command = self.__closeFile)
        self.__fileMenu.add_command(label = 'Guardar', command = self.__saveFile)
        self.__fileMenu.add_command(label = 'Guardar como..', command = self.__saveAs)
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label = 'Salir', command = self.__exit)
        
        self.__editMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('Edit'), menu = self.__editMenu)
        self.__indexMenuBar.append(self.__menuBar.index('Edit'))
        
        self.__optionMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('Options'), menu = self.__optionMenu)
        self.__indexMenuBar.append(self.__menuBar.index('Options'))
        self.__languageMenu = Menu(self.__optionMenu, tearoff = 0)
        self.__optionMenu.add_cascade(label = 'Idioma', menu = self.__languageMenu)
        self.__languageMenu.add_command(label = 'Ingles', command = self.__selectLanguageEnglish)
        self.__languageMenu.add_command(label = 'Español', command = self.__selectLanguageSpanish)
        
        
    def __selectLanguageEnglish(self):
        language = self.__texts.languagesList()[0]
        error = self.__texts.language(language)
        print(error)
        self.__chargeTexts()
    
    
    def __selectLanguageSpanish(self):
        language = self.__texts.languagesList()[1]
        print(language)
        error = self.__texts.language(language)
        print(error)
        self.__chargeTexts()
        
        
    def __chargeTexts(self):
        if self.__ladder.file() == None:
            self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        text = self.__texts.getText()
        
        self.__menuBar.entryconfig(self.__indexMenuBar[0], label = self.__texts.getText('File'))
        self.__menuBar.entryconfig(self.__indexMenuBar[1], label = self.__texts.getText('Edit'))
        self.__menuBar.entryconfig(self.__indexMenuBar[2], label = self.__texts.getText('Options'))
        
    
    def destroyElement(self, element):
        element.destroy()
        
        
    def main(self):
        pass
        

if __name__ == '__main__':
    root = Tk()
    app = Screen(root)
    app.mainloop()