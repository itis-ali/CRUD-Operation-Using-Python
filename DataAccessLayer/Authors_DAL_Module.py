from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Authors_Module import AuthorsModelClass

class AuthorsDALClass:
    def __init__(self):
        pass

    def registerAuthorDal(self, author:AuthorsModelClass):
        commandText = "EXEC [dbo].[RegisterAuthors] ?,?,?,?,?,?,?,?,?"
        params = (author.AuthorID, author.LastName, author.FirstName, author.PhoneNumber,
                  author.Address, author.City, author.State, author.ZipCode, author.Contract)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getAuthorsList(self):
        commandText = "EXEC [dbo].[GetAuthorsList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def editAuthor(self, author: AuthorsModelClass):
        commandText = "EXEC	 [dbo].[EditAuthor] ?,?,?,?,?,?,?,?,?"
        params = (author.AuthorID, author.FirstName, author.LastName, author.PhoneNumber,
                  author.Address, author.City, author.State, author.ZipCode, author.Contract)
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def deleteAuthor(self, auID):
        commandText = "EXEC [dbo].[DeleteAuthor] ?"
        params = (auID,)
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getAuthorID(self):
        commandText = "EXEC [dbo].[GetAuthorID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows