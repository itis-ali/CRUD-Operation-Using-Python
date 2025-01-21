from Model.Authors_Module import AuthorsModelClass
from DataAccessLayer.Authors_DAL_Module import AuthorsDALClass

class AuthorsBLLClass:
    def __init__(self):
        pass

    def registerAuthorsBLL(self, author:AuthorsModelClass):
        authorDALObject = AuthorsDALClass()
        authorDALObject.registerAuthorDal(author=author)

    def getAuthorsList(self):
        authorDAL_Object = AuthorsDALClass()
        return authorDAL_Object.getAuthorsList()

    def deleteAuthor(self,auID):
        authorDAL_Object = AuthorsDALClass()
        authorDAL_Object.deleteAuthor(auID)

    def editAuthor(self, author: AuthorsModelClass):
        authorDAL_Object = AuthorsDALClass()
        authorDAL_Object.editAuthor(author)

    def getAuthorIDBLL(self):
        authorDAL_Object = AuthorsDALClass()
        return authorDAL_Object.getAuthorID()