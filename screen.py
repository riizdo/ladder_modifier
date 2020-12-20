from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory


class Screen(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.master.geometry('900x600+0+0')
        self.master.title('Proj')
        
        self.p = Button(self, text = 'hola', command = self.loadFile, width = 10)
        self.p.pack()
        
        
    def button(self, text, location = None):
        pass
    
    
    def loadFile(self):
        file = askopenfilename(filetypes=(("Template files", "*.tplate"),\
                                              ("HTML files", "*.html;*.htm"),\
                                              ("All files", "*.*") ))
        
        

if __name__ == '__main__':
    root = Tk()
    app = Screen(root)
    app.mainloop()