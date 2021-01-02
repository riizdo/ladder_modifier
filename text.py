


class TextLibrary():
    def __init__(self):
        self.__languages = ('English', 'Spanish')
        self.__languageSelected = 'English'
        self.__texts = {}
        
        self.__chargeTexts()
        
        
    def getText(self, text = None):
        if text == None:
            return self.__texts
        for element in self.__texts:
            if text == element:
                return self.__texts[element][self.__languageSelected]
    
    
    def lenTexts(self):
        return len(self.__texts)
    
    
    def languagesList(self):
        return self.__languages
    
    
    def language(self, language = None):
        if language == None:
            return self.__languageSelected
        for element in self.__languages:
            if language == element:
                self.__languageSelected = language
                return 'ok'
            
        return 'language not exists'
            
            
    def __chargeTexts(self):
        self.__texts['No project'] = {self.__languages[0]: 'No project', self.__languages[1]: 'Sin proyecto'}
        self.__texts['File'] = {self.__languages[0]: 'File', self.__languages[1]: 'Archivo'}
        self.__texts['Edit'] = {self.__languages[0]: 'Edit', self.__languages[1]: 'Editar'}
        self.__texts['Options'] = {self.__languages[0]: 'Options', self.__languages[1]: 'Opciones'}
        self.__texts['Open'] = {self.__languages[0]: 'Open', self.__languages[1]: 'Abrir'}
        self.__texts['Close'] = {self.__languages[0]: 'Close', self.__languages[1]: 'Cerrar'}
        self.__texts['Save'] = {self.__languages[0]: 'Save', self.__languages[1]: 'Guardar'}
        self.__texts['Save as'] = {self.__languages[0]: 'Save as', self.__languages[1]: 'Guardar como'}
        self.__texts['Exit'] = {self.__languages[0]: 'Exit', self.__languages[1]: 'Salir'}
        self.__texts['Language'] = {self.__languages[0]: 'Language', self.__languages[1]: 'Idioma'}
        self.__texts['English'] = {self.__languages[0]: 'English', self.__languages[1]: 'Ingles'}
        self.__texts['Spanish'] = {self.__languages[0]: 'Spanish', self.__languages[1]: 'Español'}
        self.__texts['Ladder files'] = {self.__languages[0]: 'Ladder files', self.__languages[1]: 'Archivos ladder'}
        self.__texts['Job files'] = {self.__languages[0]: 'Job files', self.__languages[1]: 'Archivos de programa'}
        self.__texts['All files'] = {self.__languages[0]: 'All files', self.__languages[1]: 'Todos los archivos'}
        
        