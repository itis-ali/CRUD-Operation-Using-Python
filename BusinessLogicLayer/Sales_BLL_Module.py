from Model.Sales_Module import SalesModelClass
from DataAccessLayer.Sales_DAL_Module import SalesDALClass

class SalesBLLClass:
    def __init__(self):
        pass

    def registerSalesBLL(self, sale: SalesModelClass):
        salesBLLObject = SalesDALClass()
        salesBLLObject.registerSales(sale=sale)

    def getSalesListBLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getSalesList()

    def getStoreNameListBLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getStoresName()

    def getTitleNameListBLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getTitlesName()

    def deleteSaleBLL(self, storeID, orderNum, titleID):
        salesBLL_Object = SalesDALClass()
        salesBLL_Object.deleteSale(storeID, orderNum, titleID)

    def editSalesBLL(self, sale:SalesModelClass):
        salesBLL_Object = SalesDALClass()
        salesBLL_Object.editSale(sale=sale)

    def getStoresIDSalesBLLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getStoresIDSales()

    def getTitlesIDSalesBLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getTitlesIDSales()

    def getOrderNumberSalesBLL(self):
        salesBLL_Object = SalesDALClass()
        return salesBLL_Object.getOrderNumberSales()