#Work order service.py
from models.workOrdersDbLinkService import *
from abc import ABC, abstractmethod
import json
from flask import session

########################## Work order master interface -> two services ########################
class WorkOrderServiceInterface(ABC):
        
        @abstractmethod
        def getAllWorkOrders(self):
            pass

        @abstractmethod
        def workOrderAdd(self, request):
            pass

        @abstractmethod
        def getWorkOrderDetailById(self, woid:int):
            pass
               
        @abstractmethod
        def updateWorkOrder():
            pass

        @abstractmethod
        def workOrderDelete(self, session):
             pass
        
class WorkOrderService(WorkOrderServiceInterface):
    
    def __init__(self) -> None:
        self.WorkOrderDBInstance:WorkOrdersDbLinkInterface = WorkOrdersDbLink()
        self.WorkOrderDetailDBInstance = WorkOrderDetailsDBLinkService()
        self.WorkOrderHistoryDBInstance = WorkOrderHistoryDBLinkService()
        self.WorkOrderFilesDBInstance = WorkOrderFilesDBLinkService()
        self.dbConsolidator = WorkOrderDBConsolidator()

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

            WOdetail:WorkOrderDetailDBStructure = WorkOrderDetailDBStructure(wonumber=request.form[f'{i}.name'])
            WOHistory:WorkOrderHistoryDBStructure = WorkOrderHistoryDBStructure(wonumber=request.form[f'{i}.name'], signature=session.get("signature", "default"))
            WOFiles: WorkOrderFilesDBStructure = WorkOrderFilesDBStructure(wonumber=request.form[f'{i}.name'])

            self.dbConsolidator.writeDB(newWorkOrder,WOdetail, WOHistory, WOFiles)

            self.WorkOrderDetailDBInstance.addWorkOrderDetail(WOdetail)
            self.WorkOrderDBInstance.addWorkOrder(newWorkOrder)
            i+=1
            
        return True
    
    def getWorkOrderDetailById(self, woid:int):
        
        woDataStack = []

        woHeader = WorkOrderListDataDBStructure(wonumber=woid)
        woDataStack.append(woHeader)

        woDetail = WorkOrderDetailDBStructure(wonumber=woid)
        woDataStack.append(woDetail)

        woHistory = WorkOrderHistoryDBStructure(wonumber=woid)
        woDataStack.append(woHistory)

        woFiles = WorkOrderFilesDBStructure(wonumber=woid)
        woDataStack.append(woFiles)
     
        data = self.dbConsolidator.readDB(self.WorkOrderDBInstance.getWorkOrderHeaderByIdTest(woHeader),
                                  self.WorkOrderDetailDBInstance.getWorkOrderDetailById(woDetail),
                                  self.WorkOrderHistoryDBInstance.getWorkOrderHistoryById(woHistory),
                                  self.WorkOrderFilesDBInstance.getWorkOrderFilesById(woFiles))
    
        woHeaderDict = self.WorkOrderDBInstance.convertToDict(data[0], woHeader)
        woDetailDict = self.WorkOrderDBInstance.convertToDict(data[1], woDetail)
        woHistoryDict = self.WorkOrderDBInstance.convertToDict(data[2], woHistory)
        woFilesDict = self.WorkOrderDBInstance.convertToDict(data[3], woDetail)

        workOrderData = {'header':woHeaderDict, 'detail':woDetailDict, 'history': woHistoryDict, 'files': woFilesDict}
        print(workOrderData)
        workOrderJson = json.dumps(workOrderData)
        print(workOrderJson)
        
        return workOrderJson

    def workOrderDelete(self, request, wonumber:int = ""):
        
        idList: int = []
        if wonumber != "": idList.append(wonumber)

        requestList = list(request.form.items())
        for key,value in requestList:
            if value == "on":
                idList.append(key.split('.')[0])

        print(idList)        
        self.WorkOrderDBInstance.deleteWorkOrderRecords(idList)
            
        return

    def updateWorkOrder(self, request):
        
        formData = list(request.form.items())
        datalist: list[WorkOrderListDataDBStructure] = []
        print(formData)
        for key, value in formData:
            if key.endswith('.id'):
                i = key.split('.')[0]
                item:WorkOrderListDataDBStructure = WorkOrderListDataDBStructure(request.form.get(f'{i}.id'),
                                                                request.form.get(f'{i}.wonumber'),
                                                                request.form.get(f'{i}.itemnumber'),
                                                                request.form.get(f'{i}.itemdescription'),
                                                                request.form.get(f'{i}.project'),
                                                                request.form.get(f'{i}.quantity'),
                                                                request.form.get(f'{i}.duedate'))
                print("item:.....",item)
                datalist.append(item)
        print("datlist=:.....", datalist)

        self.WorkOrderDBInstance.updateWOlist(datalist)

        return True

__all__ = ['WorkOrderService', 'WorkOrderServiceInterface']