from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.TitleAuthor_Module import TitleAuthorModelClass
from Model.Titles_Module import TitlesModelClass

class TitlesDALClass:
    def __init__(self):
        pass

    def getTitlesList(self):
        commandText = "EXEC [dbo].[GetTitlesList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getPublishersList(self):
        commandText = "EXEC [dbo].[GetPublishersName]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getAuthorsNameList(self):
        commandText = "EXEC [dbo].[GetAuthorsName]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getTitlesNameList(self):
        commandText = "EXEC [dbo].[GetTitlesName]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getTitleAuthorList(self):
        commandText = "EXEC [dbo].[GetTitleAuthorList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def deleteTitle(self, titleID):
        commandText = "EXEC [dbo].[DeleteTitle] ?"
        params = (titleID,)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def deleteTitleAuthor(self, authorID, titleID):
        commandText = "EXEC [dbo].[DeleteTitleAuthor] ?,?"
        params = (authorID, titleID)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def registerTitle(self, title: TitlesModelClass):
        commandText = "EXEC [dbo].[RegisterTitles] ?,?,?,?,?,?,?,?,?,?"
        params = (title.TitleID, title.Title, title.Type, title.PublishersID, title.Price,
                  title.Advance, title.Royalty, title.YearToDateSales, title.Note, title.PublishDate)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def registerTitleAuthor(self, titleAuthor: TitleAuthorModelClass):
        commandText = "EXEC [dbo].[RegisterTitleAuthor]?,?,?,?"
        params = (titleAuthor.AuthorID, titleAuthor.TitleID, titleAuthor.AuthorOrder, titleAuthor.RoyaltyPer)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getTitleID(self):
        commandText = "EXEC [dbo].[GetTitlesID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getAuthorIDFromTitleAuthor(self):
        commandText = "EXEC [dbo].[GetAuthorIDFromTitleAuthor]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getTitleIDFromTitleAuthor(self):
        commandText = "EXEC [dbo].[GetTitleIDFromTitleAuthor]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def editTitle(self, title: TitlesModelClass):
        commandText = "EXEC [dbo].[EditTitles]?,?,?,?,?,?,?,?,?,?"
        params = (title.TitleID, title.Title, title.Type, title.PublishersID, title.Price,
                  title.Advance, title.Royalty, title.YearToDateSales, title.Note, title.PublishDate)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def editTitleAuthor(self, titleAuthor: TitleAuthorModelClass):
        commandText = "EXEC [dbo].[EditTitleAuthor]?,?,?,?"
        params = (titleAuthor.AuthorID, titleAuthor.TitleID, titleAuthor.AuthorOrder, titleAuthor.RoyaltyPer)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()
