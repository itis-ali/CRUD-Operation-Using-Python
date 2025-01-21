from gevent.testing.travis import command

from DataAccessLayer.ConnectionFactory import ConnectionFactoryClass
from Model.Sales_Module import SalesModelClass

class SalesDALClass:
    def __init__(self):
        pass

    def registerSales(self, sale: SalesModelClass):
        commandText = "EXEC [dbo].[RegisterSales] ?,?,?,?,?,?"
        params = (sale.StoreID, sale.OrderNumber, sale.OrderDate,
                  sale.Quantity, sale.PayTerms, sale.TitleID)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getSalesList(self):
        commandText = "EXEC [dbo].[GetSalesList]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getStoresName(self):
        commandText = "EXEC [dbo].[GetStoresName]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getTitlesName(self):
        commandText = "EXEC [dbo].[GetTitlesName]"
        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def editSale(self, sale: SalesModelClass):
        commandText = "EXEC [dbo].[EditSales] ?,?,?,?,?,?"
        params = (sale.StoreID, sale.OrderNumber, sale.OrderDate,
                  sale.Quantity, sale.PayTerms, sale.TitleID)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def deleteSale(self, storeID, orderNum, titleID):
        commandText = "EXEC [dbo].[DeleteSale] ?,?,?"
        params = (storeID, orderNum, titleID)

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, params)
            sqlConnection.commit()

    def getStoresIDSales(self):
        commandText = "EXEC [dbo].[GetStoreIDSales]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getTitlesIDSales(self):
        commandText = "EXEC [dbo].[GetTitleIDSales]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows

    def getOrderNumberSales(self):
        commandText = "EXEC [dbo].[GetOrderNumberSales]"

        with ConnectionFactoryClass().makeConnection() as sqlConnection:
            cursor = sqlConnection.cursor()
            cursor.execute(commandText, )
            rows = cursor.fetchall()
        return rows
