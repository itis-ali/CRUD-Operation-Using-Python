from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Publishers_Module import PublishersModelClass

class PublishersDALClass:
    def __init__(self):
        pass

    def registerPublishersDAL(self, publisher:PublishersModelClass):
        commandText = "EXEC [dbo].[RegisterPublishers] ?,?,?,?,?"
        params = (publisher.PubID, publisher.PubName, publisher.City, publisher.State, publisher.Country)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getPublishersList(self):
        commandText = "EXEC [dbo].[GetPublishersList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def deletePublisher(self, pubID):
        commandText = "EXEC [dbo].[DeletePublisher] ?"
        params = (pubID,)
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def editPublisher(self, publisher:PublishersModelClass):
        commandText = "EXEC [dbo].[EditPublisher]?,?,?,?,?"
        params = (publisher.PubID, publisher.PubName, publisher.City, publisher.State, publisher.Country)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getPublisherID(self):
        commandText = "EXEC [dbo].[GetPublisherID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows
