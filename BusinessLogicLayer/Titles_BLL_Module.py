from Model.Titles_Module import TitlesModelClass
from Model.TitleAuthor_Module import TitleAuthorModelClass
from DataAccessLayer.Titles_DAL_Module import TitlesDALClass

class TitlesBLLClass:
    def __init__(self):
        pass

    def getTitlesListBLL(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getTitlesList()

    def getPublishersList(self):
        employeeDALObject = TitlesDALClass()
        return employeeDALObject.getPublishersList()

    def getAuthorsNameListBLL(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getAuthorsNameList()

    def getTitlesNameListBLL(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getTitlesNameList()

    def getTitleAuthorListBLL(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getTitleAuthorList()

    def deleteTitleBLL(self, titleID):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.deleteTitle(titleID)

    def deleteTitleAuthor(self, authorID, titleID):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.deleteTitleAuthor(authorID, titleID)

    def registerTitle(self, title: TitlesModelClass):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.registerTitle(title)

    def registerTitleAuthor(self, titleAuthor: TitleAuthorModelClass):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.registerTitleAuthor(titleAuthor)

    def getTitleIDBLL(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getTitleID()

    def getAuthorIDFromTitleAuthor(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getAuthorIDFromTitleAuthor()

    def getTitleIDFromTitleAuthor(self):
        titlesBLLObject = TitlesDALClass()
        return titlesBLLObject.getTitleIDFromTitleAuthor()

    def editTitleBLL(self, title: TitlesModelClass):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.editTitle(title)

    def editTitleAuthorBLL(self, titleAuthor: TitleAuthorModelClass):
        titlesBLLObject = TitlesDALClass()
        titlesBLLObject.editTitleAuthor(titleAuthor)