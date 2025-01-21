from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Stores_Module import StoresModelClass

class StoresDALClass:
    def __init__(self):
        pass

    def registerStoresDAL(self, store:StoresModelClass):
        commandText = "EXEC [dbo].[RegisterStores] ?,?,?,?,?,?"
        params = (store.StoreID, store.StoreName, store.StoreAddress, store.City,
                  store.State, store.Zip)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getStoresList(self):
        commandText = "EXEC [dbo].[GetStoresList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def deleteStore(self, storeID):
        commandText = "EXEC [dbo].[DeleteStore] ?"
        params = (storeID,)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def editStore(self, store: StoresModelClass):
        commandText = "EXEC [dbo].[EditStore] ?,?,?,?,?,?"
        params = (store.StoreID, store.StoreName, store.StoreAddress, store.City,
                  store.State, store.Zip)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getStoreID(self):
        commandText = "EXEC [dbo].[GetStoreID]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows
