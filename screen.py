from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import modifier
import text


class Screen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.__title = 'Ladder Modifier -'
        self.pack()
        self.master.geometry('1200x600+0+0')
        #self.__fontInstruction = Font('arial')
        
        self.__indexMenuBar = []
        self.__indexFileMenu = []
        self.__indexOptionMenu = []
        self.__indexLanguageMenu = []
        self.__texts = text.TextLibrary()
        
        self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        
        self.__languages = ('English', 'Spanish')
        self.__languageSelected = 'English'
        self.__text = {}
        
        self.__createMenuBar()
        
        self.__textEditor = {}
        self.__programs = {}
        
        self.__treeView = ttk.Treeview(master, height = 30)
        self.__treeView.place(x = 5, y = 30)
        
        self.__noteBook = ttk.Notebook(master)
        self.__noteBook.place(x = 210, y = 30)
            
        self.p = Button(self, text = 'hola', width = 10)
        self.p.pack()
        
        
    def __loadProyect(self):
        self.__path = askdirectory()
        
        if self.__path == None or self.__path == ():
            return 'no project select'
        
        project = self.__path.split('/')
        project = project[len(project) - 1]
        
        self.master.title(self.__title + ' ' + project)
        self.__treeView.heading('#0', text = project)
        self.__treeView.tag_configure('default', font = ('arial', 8))
        self.__treeView.tag_configure('project', font = ('arial', 10))
        self.__treeView.tag_configure('types', font = ('arial', 10))
        self.__treeView.bind('<Double-1>', self.__doubleClickTreeView)
        
        projectContent = os.listdir(self.__path)
        
        item = self.__treeView.insert('', 'end', text = project, tag = 'project')
        job = self.__treeView.insert(item, 'end', text = self.__texts.getText('Jobs'), tag = 'types')
        ladder = self.__treeView.insert(item, 'end', text = self.__texts.getText('Ladder'), tag = 'types')
        other = self.__treeView.insert(item, 'end', text = self.__texts.getText('Others'), tag = 'types')
        for element in projectContent:
            ext = self.__extensionFile(element)
            if ext == 'JBI':
                self.__treeView.insert(job, 'end', text = element, tag = 'default')
            elif ext == 'LST':
                self.__treeView.insert(ladder, 'end', text = element, tag = 'default')
            else:
                self.__treeView.insert(other, 'end', text = element, tag = 'default')
                
                
    def __doubleClickTreeView(self, event):
        file = self.__treeView.selection()
        file = self.__treeView.item(file)['text']
        file = self.__path + '/' + file
        self.__openFile(file)
    
    
    def __loadFile(self):
        error = ''
        file = askopenfilename(title = self.__texts.getText('Open'), filetypes=((self.__texts.getText('Ladder files'), '*.LST'),\
                                          (self.__texts.getText('Job files'), '*.JBI'),\
                                          (self.__texts.getText('All files'), '*.*')))
        if file == None or file == ():
            return 'no file select'
        self.__openFile(file)
        
        
    def __openFile(self, file):
        partFile = file.split('/')
        partFile = partFile[len(partFile) - 1]
        extFile = self.__extensionFile(partFile)
        
        if extFile == 'LST':
            self.__programs[partFile] = modifier.Ladder()
            error = self.__programs[partFile].readFile(file)
        elif extFile == 'JBI':
            self.__programs[partFile] = modifier.Job()
            error = self.__programs[partFile].readFile(file)
        if error != 'ok':
            print(error)
            return error
        
        self.master.title(self.__title + ' ' + file)
        self.__textEditor[partFile] = Text(self.__noteBook)
        self.__textEditor[partFile].insert('insert', self.__programs[partFile].getProgram())
        self.__defineColourProgram(partFile)
        self.__noteBook.add(self.__textEditor[partFile], text = self.__programs[partFile].file())
        self.__noteBook.select(self.__textEditor[partFile])
        
        return 'ok'
    
    
    def __defineColourProgram(self, program):
        nInstruction = 0
        posIni = '1.0'
        
        self.__textEditor[program].tag_config('instruction', foreground = 'blue')
        self.__textEditor[program].tag_config('text', foreground = 'black')
        self.__textEditor[program].tag_config('comment', foreground = 'grey')
        
        instructions = self.__programs[program].getInstructions()
        instruction = r'\y(?:{})\y'.format('|'.join(instructions))
        #instruction = '|'.join(instructions)
        countVar = StringVar()
        while True:
            instruction = instructions[nInstruction] + ' '
            pos = self.__textEditor[program].search(instruction, posIni, count = countVar)
            print(pos, instruction, countVar.get())
            if not pos or pos == '' or self.__compareStr(pos, posIni):
                nInstruction += 1
                posIni = '1.0'
                #break
                if nInstruction >= len(instructions):
                    break
            else:
                posEnd = '{} + {}c'.format(pos, countVar.get())
                self.__textEditor[program].tag_add('instruction', pos, posEnd)
                #t = self.__textEditor[program].get(pos, posEnd)
                #self.__textEditor[program].delete(pos, posEnd)
                posIni = pos.split('.')
                posIni = int(posIni[0]) + 1
                posIni = str(posIni) + '.0'
                print(pos, posIni, instruction)
                
                
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
        program = self.__noteBook.select()
        file = self.__programs[program].file()
        self.__programs[program].writeFile(file)
    
    
    def __saveAs(self):
        file = asksaveasfilename()
        program = self.__noteBook.select()
        self.__programs[program].writeFile(file)
    
    
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
        self.__fileMenu.add_command(label = self.__texts.getText('Open'), command = self.__loadFile)
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
        if self.__programs == {}:
            self.master.title(self.__title + ' ' + self.__texts.getText('No project'))
        #text = self.__texts.getText()
        
        self.__menuBar.entryconfig(self.__indexMenuBar[0], label = self.__texts.getText('File'))
        self.__menuBar.entryconfig(self.__indexMenuBar[1], label = self.__texts.getText('Edit'))
        self.__menuBar.entryconfig(self.__indexMenuBar[2], label = self.__texts.getText('Options'))
        
        self.__fileMenu.entryconfig(self.__indexFileMenu[0], label = self.__texts.getText('Select project'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[1], label = self.__texts.getText('Open'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[2], label = self.__texts.getText('Close'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[3], label = self.__texts.getText('Save'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[4], label = self.__texts.getText('Save as'))
        self.__fileMenu.entryconfig(self.__indexFileMenu[5], label = self.__texts.getText('Exit'))
        
        self.__optionMenu.entryconfig(self.__indexOptionMenu[0], label = self.__texts.getText('Language'))
        
        self.__languageMenu.entryconfig(self.__indexLanguageMenu[0], label = self.__texts.getText('English'))
        self.__languageMenu.entryconfig(self.__indexLanguageMenu[1], label = self.__texts.getText('Spanish'))
        
    
        

if __name__ == '__main__':
    root = Tk()
    app = Screen(root)
    app.mainloop()