#Work order service.py
from models.workOrdersDbLinkService import *
from abc import ABC, abstractmethod
import json
from flask import session
import datetime

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
            WOHistory:WorkOrderHistoryDBStructure = WorkOrderHistoryDBStructure(wonumber=request.form[f'{i}.name'], signature=session.get("signature", "default"), message="WO Created")
            WOFiles: WorkOrderFilesDBStructure = WorkOrderFilesDBStructure(wonumber=request.form[f'{i}.name'])

            commandList = []
            commandList.append(self.WorkOrderDBInstance.addWorkOrder(newWorkOrder))
            commandList.append(self.WorkOrderDetailDBInstance.addWorkOrderDetailTupple(WOdetail))
            commandList.append(self.WorkOrderHistoryDBInstance.addHistoryItem(WOHistory))
            commandList.append(self.WorkOrderFilesDBInstance.addfilesItem(WOFiles))
            #unpack an array
            self.dbConsolidator.writeDB(*commandList)

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
        woFilesDict = self.WorkOrderDBInstance.convertToDict(data[3], woFiles)


        workOrderData = {'header':woHeaderDict, 'detail':woDetailDict, 'history': woHistoryDict, 'files': woFilesDict}
        
        workOrderJson = json.dumps(workOrderData, default=json_serial)
      
        return workOrderJson

    def workOrderDelete(self, request, wonumber:int = ""):
        
        idList: int = []
        if wonumber != "": idList.append(wonumber)

        requestList = list(request.form.items())
        for key,value in requestList:
            if value == "on":
                idList.append(key.split('.')[0])
     
        self.WorkOrderDBInstance.deleteWorkOrderRecords(idList)
            
        return

    def updateWorkOrder(self, request, woid):
        
        formData = list(request.form.items())

        print("woid:", woid, "formdata...:",formData)
        WOheaderList = []
        WOheader = WorkOrderListDataStructure(wonumber=request.form.get('wonumber'), 
                                              itemnumber=request.form.get('itemnumber'),
                                              itemdescription=request.form.get('itemdescription'),
                                              project=request.form.get('project'),
                                              quantity=request.form.get('quantity'),
                                              duedate=request.form.get('duedate'))
        WOheaderList.append(WOheader)
        
        WOdetailList = []
        WOdetail = WorkOrderDetailDBStructure(firmed=request.form.get('firmed', False), 
                                              disassembled=request.form.get('disassembled', False),
                                              received=request.form.get('received', False),
                                              reassembled=request.form.get('reassembled', False),
                                              rework=request.form.get('rework', False),
                                              closed=request.form.get('closed', False), 
                                              wonumber=request.form.get('wonumber'))
        WOdetailList.append(WOdetail)
        
        updateList = []
        updateList.append(self.WorkOrderDBInstance.updateWOlistTuple(WOheaderList))
        updateList.append(self.WorkOrderDetailDBInstance.updateWOdetail(WOdetailList))


        commands = []
        args = []

        for query in updateList:
            command, arguments = query
            commands.append(command[0])
            args.append(arguments[0])

        self.dbConsolidator.updateDBzip(commands, args)
        
        updateHist = WorkOrderHistoryDBStructure(wonumber=request.form.get('wonumber'), signature=session.get("signature", "default"), message="WO updated")
        commandList = []
        commandList.append(self.WorkOrderHistoryDBInstance.addHistoryItem(updateHist))
        self.dbConsolidator.writeDB(*commandList)
        

        # datalist: list[WorkOrderListDataDBStructure] = []
        # print(formData)
        # for key, value in formData:
        #     if key.endswith('.id'):
        #         i = key.split('.')[0]
        #         item:WorkOrderListDataDBStructure = WorkOrderListDataDBStructure(request.form.get(f'{i}.id'),
        #                                                         request.form.get(f'{i}.wonumber'),
        #                                                         request.form.get(f'{i}.itemnumber'),
        #                                                         request.form.get(f'{i}.itemdescription'),
        #                                                         request.form.get(f'{i}.project'),
        #                                                         request.form.get(f'{i}.quantity'),
        #                                                         request.form.get(f'{i}.duedate'))

        #         datalist.append(item)


        # self.WorkOrderDBInstance.updateWOlist(datalist)


        return True

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


__all__ = ['WorkOrderService', 'WorkOrderServiceInterface']