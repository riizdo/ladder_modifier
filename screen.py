#file: modifier.py
#author: riizdo
#date: 20/12/20
#description: screen class of the program

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import modifier
import text


class Screen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.__title = 'Ladder Modifier -'
        self.pack()
        self.master.geometry('1200x600+0+0')
        self.master.resizable(True, True)
        #self.__fontInstruction = Font('arial')
        
        self.__indexMenuBar = []
        self.__indexFileMenu = []
        self.__indexViewMenu = []
        self.__indexOptionMenu = []
        self.__indexLanguageMenu = []
        self.__optionDirection = StringVar()
        self.__optionName = StringVar()
        self.__optionComment = StringVar()
        self.__texts = text.TextLibrary()
        self.__textEditor = {}
        self.__project = ''
        
        self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        
        self.__createMenuBar()
        
        self.__treeView = ttk.Treeview(master, height = 30)
        self.__treeView.place(x = 5, y = 30)
        
        self.__noteBook = ttk.Notebook(master)
        self.__noteBook.place(x = 210, y = 30)
            
        self.p = Button(self, text = 'hola', width = 10)
        self.p.pack()
        
        
    def __loadProyect(self):
        path = askdirectory()
        
        if path == None or path == ():
            return 'no project select'
        
        self.__project = modifier.Project(path)
        
        self.master.title(self.__title + ' ' + self.__project.getName())
        self.__treeView.heading('#0', text = self.__project.getName())
        self.__treeView.tag_configure('default', font = ('arial', 8))
        self.__treeView.tag_configure('project', font = ('arial', 10))
        self.__treeView.tag_configure('types', font = ('arial', 10))
        self.__treeView.bind('<Double-1>', self.__doubleClickTreeView)
        
        item = self.__treeView.insert('', 'end', text = self.__project.getName(), tag = 'project')
        job = self.__treeView.insert(item, 'end', text = self.__texts.getText('Jobs'), tag = 'types')
        ladder = self.__treeView.insert(item, 'end', text = self.__texts.getText('Ladder'), tag = 'types')
        other = self.__treeView.insert(item, 'end', text = self.__texts.getText('Others'), tag = 'types')
        
        projectContent = self.__project.getJobsList()
        for element in projectContent:
            self.__treeView.insert(job, 'end', text = element, tag = 'default')
        projectContent = self.__project.getLadder()
        self.__treeView.insert(ladder, 'end', text = projectContent, tag = 'default')
        projectContent = self.__project.getOtherFilesList()
        for element in projectContent:
            self.__treeView.insert(other, 'end', text = element, tag = 'default')
                
                
    def __doubleClickTreeView(self, event):
        path = ''
        file = self.__treeView.selection()
        file = self.__treeView.item(file)['text']
        '''
        if self.__project.existsFile(file):
            path = self.__project.getPath()
        file = path + '/' + file'''
        self.__openFile(file)
    
    
    def __selectFile(self):
        error = ''
        file = askopenfilename(title = self.__texts.getText('Open'), filetypes=((self.__texts.getText('Ladder files'), '*.LST'),\
                                          (self.__texts.getText('Job files'), '*.JBI'),\
                                          (self.__texts.getText('All files'), '*.*')))
        if file == None or file == ():
            return 'no file select'
        self.__openFile(file)


    def __openFile(self, file):
        self.master.title(self.__title + ' ' + file)
        self.__textEditor[file] = Text(self.__noteBook)
        print('openning file in screen: ', self.__project.getProgram(file, False, False, False))
        self.__textEditor[file].insert('insert', self.__project.getProgram(file, False, False, False))
        self.__defineColour(file)
        self.__noteBook.add(self.__textEditor[file], text = file)
        self.__noteBook.select(self.__textEditor[file])
        
        return 'textEditor open file'
    
    
    def __defineColour(self, file):
        self.__textEditor[file].tag_config('instruction', foreground = 'blue')
        self.__textEditor[file].tag_config('text', foreground = 'black')
        self.__textEditor[file].tag_config('comment', foreground = 'gray')
        self.__textEditor[file].tag_config('movement', foreground = 'royal blue')
        self.__textEditor[file].tag_config('variable', foreground = 'sea green')
        self.__textEditor[file].tag_config('simbol', foreground = 'dark slate blue')

        instructions = self.__project.getPositionInstructions(file)
        self.__appColour(file, instructions, 'instruction')
        movements = self.__project.getPositionMovements(file)
        self.__appColour(file, movements, 'movement')
        variables = self.__project.getPositionVariables(file)
        self.__appColour(file, variables, 'variable')
        comments = self.__project.getPositionComments(file)
        self.__appColour(file, comments, 'comment')
        simbols = self.__project.getPositionSimbols(file)
        self.__appColour(file, simbols, 'simbol')
        
        
    def __appColour(self, program, elements, tag):
        for element in elements:
            self.__textEditor[program].tag_add(tag, element['ini'], element['end'])
                
                
    def __comparePositions(self, pos1, pos2):
        pos1 = pos1.split('.')
        pos1 = int(pos1[0])
        pos2 = pos2.split('.')
        pos2 = int(pos2[0])
        
        if pos1 == pos2:
            return 0
        elif pos1 > pos2:
            return 1
        elif pos1 < pos2:
            return -1
                
                
    def __nextRow(self, position):
        position = position.split('.')
        position = int(position[0]) + 1
        position = str(position) + '.0'
        return position
                
                
    def __compareStr(self, str1, str2):
        num1 = float(str1)
        num2 = float(str2)
        return num1 < num2
    
    
    def __extensionFile(self, file):
        file = file.split('.')
        extension = file[len(file) -1]
        return extension
                    
    
    def __closeFile(self):
        self.__noteBook.forget(self.__noteBook.select())
        
        
    def __saveFile(self):
        pass
    
    
    def __saveAs(self):
        pass
    
    
    def __exit(self):
        self.master.destroy()
        
        
    def __createMenuBar(self):
        self.__menuBar = Menu(self)
        self.master.config(menu = self.__menuBar)
        
        self.__fileMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('File'), menu = self.__fileMenu)
        self.__indexMenuBar.append(self.__menuBar.index(self.__texts.getText('File')))
        self.__fileMenu.add_command(label = self.__texts.getText('Select project'), command = self.__loadProyect)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Select project')))
        self.__fileMenu.add_command(label = self.__texts.getText('Open'), command = self.__selectFile)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Open')))
        self.__fileMenu.add_command(label = self.__texts.getText('Close'), command = self.__closeFile)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Close')))
        self.__fileMenu.add_command(label = self.__texts.getText('Save'), command = self.__saveFile)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Save')))
        self.__fileMenu.add_command(label = self.__texts.getText('Save as'), command = self.__saveAs)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Save as')))
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label = self.__texts.getText('Exit'), command = self.__exit)
        self.__indexFileMenu.append(self.__fileMenu.index(self.__texts.getText('Exit')))
        
        self.__editMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('Edit'), menu = self.__editMenu)
        self.__indexMenuBar.append(self.__menuBar.index('Edit'))
        
        self.__viewMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('View'), menu = self.__viewMenu)
        self.__indexMenuBar.append(self.__menuBar.index('View'))
        self.__viewMenu.add_checkbutton(label = self.__texts.getText('Variable directions'), variable = self.__optionDirection,\
                                        onvalue = True, offvalue = False)
        self.__indexViewMenu.append(self.__viewMenu.index(self.__texts.getText('Variable directions')))
        self.__viewMenu.add_checkbutton(label = self.__texts.getText('Variable names'), variable = self.__optionName,\
                                        onvalue = True, offvalue = False)
        self.__indexViewMenu.append(self.__viewMenu.index(self.__texts.getText('Variable names')))
        self.__viewMenu.add_checkbutton(label = self.__texts.getText('Variable comments'), variable = self.__optionComment,\
                                        onvalue = True, offvalue = False)
        self.__indexViewMenu.append(self.__viewMenu.index(self.__texts.getText('Variable comments')))

        self.__optionMenu = Menu(self.__menuBar, tearoff = 0)
        self.__menuBar.add_cascade(label = self.__texts.getText('Options'), menu = self.__optionMenu)
        self.__indexMenuBar.append(self.__menuBar.index('Options'))
        self.__languageMenu = Menu(self.__optionMenu, tearoff = 0)
        self.__optionMenu.add_cascade(label = self.__texts.getText('Language'), menu = self.__languageMenu)
        self.__indexOptionMenu.append(self.__optionMenu.index(self.__texts.getText('Language')))
        self.__languageMenu.add_command(label = self.__texts.getText('English'), command = self.__selectLanguageEnglish)
        self.__indexLanguageMenu.append(self.__languageMenu.index(self.__texts.getText('English')))
        self.__languageMenu.add_command(label = self.__texts.getText('Spanish'), command = self.__selectLanguageSpanish)
        self.__indexLanguageMenu.append(self.__languageMenu.index(self.__texts.getText('Spanish')))
        
        
    def __selectLanguageEnglish(self):
        language = self.__texts.languagesList()[0]
        error = self.__texts.language(language)
        self.__chargeTexts()
    
    
    def __selectLanguageSpanish(self):
        language = self.__texts.languagesList()[1]
        error = self.__texts.language(language)
        self.__chargeTexts()
        
        
    def __chargeTexts(self):
        if self.__project == '':
            self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        #text = self.__texts.getText()
        
        self.__menuBar.entryconfig(self.__indexMenuBar[0], label = self.__texts.getText('File'))
        self.__menuBar.entryconfig(self.__indexMenuBar[1], label = self.__texts.getText('Edit'))
        self.__menuBar.entryconfig(self.__indexMenuBar[2], label = self.__texts.getText('View'))
        self.__menuBar.entryconfig(self.__indexMenuBar[3], label = self.__texts.getText('Options'))
        
        self.__fileMenu.entryconfig(self.__indexFileMenu[0], label = self.__texts.getText('Select project'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[1], label = self.__texts.getText('Open'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[2], label = self.__texts.getText('Close'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[3], label = self.__texts.getText('Save'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[4], label = self.__texts.getText('Save as'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[5], label = self.__texts.getText('Exit'))
        
        self.__viewMenu.entryconfig(self.__indexViewMenu[0], label = self.__texts.getText('Variable directions'))
        self.__viewMenu.entryconfig(self.__indexViewMenu[1], label = self.__texts.getText('Variable names'))
        self.__viewMenu.entryconfig(self.__indexViewMenu[2], label = self.__texts.getText('Variable comments'))
        
        self.__optionMenu.entryconfig(self.__indexOptionMenu[0], label = self.__texts.getText('Language'))
        
        self.__languageMenu.entryconfig(self.__indexLanguageMenu[0], label = self.__texts.getText('English'))
        self.__languageMenu.entryconfig(self.__indexLanguageMenu[1], label = self.__texts.getText('Spanish'))
        
    
        

if __name__ == '__main__':
    root = Tk()
    app = Screen(root)
    app.mainloop()