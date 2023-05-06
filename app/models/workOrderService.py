#Work order service.py
from models.workOrdersDbLinkService import *
from abc import ABC, abstractmethod

########################## Work order master interface -> two services ########################
class WorkOrderServiceInterface(ABC):
        
        @abstractmethod
        def getAllWorkOrders(self):
            pass

        @abstractmethod
        def workOrderAdd(self, request):
            pass

        @abstractmethod
        def getWorkOrderById(self, woid:int):
            pass
        
        

        # def menuAdd(self):
        #     pass
        
        # def getMenuItem(self):
        #     pass

        # def menuItemEdit(self):
        #     pass

        @abstractmethod
        def workOrderDelete(self, session):
             pass
        
class WorkOrderService(WorkOrderServiceInterface):
    
    def __init__(self) -> None:
        self.WorkOrderDBInstance:WorkOrdersDbLinkInterface = WorkOrdersDbLink()

    def getAllWorkOrders(self):
        return self.WorkOrderDBInstance.getAllWorkOrders()
    
    def workOrderAdd(self, request) -> bool:

        items:int = len(request.form)/6
        print (f"total item tally: {items}")
        i:int=1
        while i <= items:
            newWorkOrder: WorkOrderListDataStructure = WorkOrderListDataStructure( 
                 request.form[f'{i}.name'], 
                 request.form[f'{i}.number'], 
                 request.form[f'{i}.itemdescription'], 
                 request.form[f'{i}.project'], 
                 request.form[f'{i}.quantity'], 
                 request.form[f'{i}.duedate'])
            self.WorkOrderDBInstance.addWorkOrder(newWorkOrder)
            i+=1
        return True
    
    def getWorkOrderById(self, woid:int):
        return self.WorkOrderDBInstance.getWorkOrderById(woid)
    
    # def getMenuItem(self, menuId):
    #     searchById = 'id'
    #     result = self.fTdatabaseInstance.searchFoodRecord(searchById, menuId)
    #     return result
    
    # def menuItemEdit(self, request):
    #     self.newItemEdit:MenuItemStructure =  MenuItemStructure( request.form['name'], request.form['URL'], request.form['price'])
    #     self.newItemId = request.form['id']
    #     self.fTdatabaseInstance.updateFoodRecord(self.newItemId, self.newItemEdit)

    def workOrderDelete(self, request):
        itemCount = len(request.form)
        print(itemCount)
        print(request.form)
        return
        # if 'submitYes' in request.form:
        #     self.fTdatabaseInstance.deleteFoodRecord(self.newItemId)
        #     return True
        # elif 'submitNo' in request.form:
        #     return False

__all__ = ['WorkOrderService', 'WorkOrderServiceInterface']