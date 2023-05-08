################## file: userServiceDb.py ############################### 
#########################################################################
#### DATABASE ACCESS SERVICE LAYER FOR PSQL SPECIFIC FUNCTIONS #########
import psycopg2
from abc import ABC, abstractmethod
import os

############# Generic interface for database accesss
class DatabaseAcessInterface(ABC):

    # table methods
    @abstractmethod
    def dbCreateTable():
        pass

    #CRUD operations for records
    @abstractmethod
    def dbCreateRecord(command, args):
        pass

    @abstractmethod
    def dbReadRecord(searchQuery):
        pass

    @abstractmethod
    def dbUpdateRecord(command, args):
        pass

    @abstractmethod
    def dbDeleteRecord(command, args):
        pass

    @abstractmethod
    def dbGeneric():
        pass

    @abstractmethod
    def dbReadRecordMultiple(self, searchQuery):
        pass

############# Specific implementation for PSQL database - implements standardised methods from interface

class PGDBAcessService(DatabaseAcessInterface):

    def dbConnect(self):
        #self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.connection = psycopg2.connect(host="dpg-ch8fgtg2qv2864ssurfg-a.oregon-postgres.render.com", user="project2_o8rr_user", password="3z3kTM6n1up51mttWkpPys1JpR3hq5ug", port="5432", dbname="project2_o8rr")
        self.cursor = self.connection.cursor()

    def dbClose(self):
        self.connection.close()

    def dbCreateTable(self, command):
        self.dbConnect()
        self.cursor.execute(command)
        self.connection.commit()
        self.dbClose()
    
    def dbCreateRecord(self, command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()

    def dbReadRecord(self, searchQuery):
        self.dbConnect()
        self.cursor.execute(searchQuery)
        self.results = self.cursor.fetchall()
        self.connection.commit()
        self.dbClose()
        return self.results

    def dbUpdateRecord(self, commands, args):
        self.dbConnect()

        for command, arg in zip(commands, args):
            self.cursor.execute(command, (arg))

        self.connection.commit()
        self.dbClose()

    def dbDeleteRecord(self, commandList):
        self.dbConnect()
        for command in commandList:
            self.cursor.execute(command)
        self.connection.commit()
        self.dbClose()

    def dbGeneric(self, command, args):
        self.dbConnect()
        self.cursor.execute(command, (args))
        self.connection.commit()
        self.dbClose()

    def dbReadRecordMultiple(self, searchTablesList):
        self.dbConnect()

        data = []
        for command,args in searchTablesList:
            self.cursor.execute(command, args)
            results = self.cursor.fetchall()
            print(results)
            data.append(results)

        return data





        
__all__ = ['DatabaseAcessInterface','PGDBAcessService']

# db.dbGeneric('update userdata set email = %s where email = %s' , ('nik.m1992@gmail.com', 'nik.m1992@gmai.com' ))