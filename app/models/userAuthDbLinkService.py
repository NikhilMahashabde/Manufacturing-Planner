# file: userServiceDb.py
import psycopg2
from abc import ABC, abstractmethod
from models.dbAcessService import * 
import json
import bcrypt
from flask import session

#when adding to DB
class UserAuthDataStructure():
    def __init__(self, name:str = None, email:str = None, uuid:str = None, isAdmin:bool = None, password_hash:str = None) -> None:
        self.uuid:str = uuid
        self.name:str = name
        self.email:str = email
        self.isAdmin:bool = isAdmin
        self.password_hash:str = password_hash

    def printUserAuthDataStructure(self):
        return (print(f'{self.uuid} - {self.name} - {self.email} - {self.isAdmin} - {self.password_hash}'))

#when returning data from db 
class UserAuthDBStructure(UserAuthDataStructure):
    def __init__(self, id:int = None, uuid = None, name:str = None, email:str = None, isAdmin:bool = False, password_hash:str = None ) -> None:
        self.id:int = id
        super().__init__(name, email, uuid, isAdmin, password_hash)

    def validateUser(self, emailEntry:str, password:str= None):
        if ((self.email == emailEntry) and bcrypt.checkpw(password.encode(), self.password_hash.encode())):
            session["user_id"] = self.id
            session["signature"] = self.email
            return True
        return False

#usser database interface -> calls on db access instance. 

class UserAuthDbLinkInterface(ABC):

    @abstractmethod
    def addUserAuth():
        None

    @abstractmethod
    def getUserAuthByEmail():
        None

    @abstractmethod
    def getUserAuthById():
        None

    @abstractmethod
    def updateUserAuth():
        None

    @abstractmethod
    def getAllUsers():
        None

    @abstractmethod
    def deleteUserAuthRecord():
        None
      
class UserAuthDbLink(UserAuthDbLinkInterface):
    def __init__(self) -> None:
        self.dbAccessServiceInstance: DatabaseAcessInterface = PGDBAcessService()
  
    def addUserAuth(self, data:UserAuthDataStructure):
        self.dbAcessInstance:DatabaseAcessInterface = PGDBAcessService()
        command = f""" 
                    INSERT INTO userauth
                    (uuid, name, email, isAdmin, password_hash)
                    values
                    (%s, %s, %s, %s, %s)
                    """
        args = (data.uuid, data.name, data.email, data.isAdmin, data.password_hash)
        self.dbAcessInstance.dbCreateRecord(command, args)
        return True
    
    def createUserAuthTable(self, tableName:str):
        self.dbAcessInstance:DatabaseAcessInterface = PGDBAcessService()
        command = f"""
                    CREATE TABLE {tableName} (
                        id SERIAL PRIMARY KEY,
                        uuid TEXT NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        isAdmin BOOLEAN, 
                        password_hash TEXT
                    );"""
        self.dbAcessInstance.dbCreateTable(command)
        return True

    def getUserAuthByEmail(self, emailId):
        searchQuery = f"SELECT * FROM userauth WHERE email = '{emailId}'"
        results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
        return results
    
    def getUserAuthById(self, id:int):
        searchQuery = f"SELECT * FROM userauth WHERE id = '{id}'"
        results:UserAuthDBStructure = UserAuthDBStructure(*self.dbAccessServiceInstance.dbReadRecord(searchQuery)[0])
        return results
    
    def updateUserAuth(self, data):

        commandList = []
        argsList = []
        command = ''
        args = ()
        for item in data:

            if item.password_hash == None or item.password_hash == "":
                command = """
                            UPDATE userauth
                            SET 
                            name = %s,
                            uuid = %s, 
                            email = %s,
                            isAdmin = %s
                            where id = %s       
                        """
                args = (item.name, item.uuid, item.email, item.isAdmin, item.id)
            else:
                command = """
                                UPDATE userauth
                                SET 
                                name = %s,
                                uuid = %s, 
                                email = %s,
                                isAdmin = %s,
                                password_hash = %s
                                where id = %s       
                            """
                args = (item.name, item.uuid, item.email, item.isAdmin, item.password_hash, item.id)
            commandList.append(command)
            argsList.append(args)
        self.dbAccessServiceInstance.dbUpdateRecord(commandList, argsList)
    
    def getAllUsers(self):
        searchQuery = f"SELECT * FROM userauth"
        results = self.dbAccessServiceInstance.dbReadRecord(searchQuery)

        #JSON string output for API 
        userList = []
        for item in results:
            userDict = dict(zip(UserAuthDBStructure().__dict__.keys(), item))
            userList.append(json.dumps(userDict))
        return userList
    
    def deleteUserAuthRecord(self, id):
        searchQuery = f"DELETE FROM userauth WHERE id = %s"
        args = id
        self.dbAccessServiceInstance.dbDeleteRecord(searchQuery, args)

#updatemain:UserAuthDBStructure = UserAuthDBStructure(1, '123', 'nikhil', 'nik.m1992@gmail.com', )., True)
# bcrypt.hashpw('test'.encode(), bcrypt.gensalt().decode()

__all__ = ['UserAuthDbLink','UserAuthDbLinkInterface', 'UserAuthDBStructure', 'UserAuthDataStructure']



