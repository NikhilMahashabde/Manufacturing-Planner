############# UserAuthInterface

# file: userAuthService.py
from abc import ABC, abstractmethod
from models.userAuthDbLinkService import * 
from flask import session 
import bcrypt

#################

class UserAuthInterface(ABC):
    @abstractmethod
    def checkLogin():
        pass

    @abstractmethod
    def getUserAuthName():
        pass

    @abstractmethod
    def addUserAuth():
        pass

    @abstractmethod
    def getAllUserAuthData():
        pass

    @abstractmethod
    def updateAllUserAuthData():
        pass

    @abstractmethod
    def deleteUserAuthData(request):
        pass

class UserAuthService(UserAuthInterface):

    def __init__(self) -> None:
        self.userDBLinkService: UserAuthDbLinkInterface = UserAuthDbLink()
       
    def checkLogin(self, request, session):
        email = request.form.get("email")
        password = request.form.get("password")
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthByEmail(email)
        return userAuthData.validateUser(email, password)

        # if ((userAuthData.email == email) and bcrypt.checkpw(password.encode(), userAuthData.password_hash.encode())):
        #     session["user_id"] = userAuthData.id
        #     return True
        # return False
    
    def getUserAuthData(self, session):
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        return userAuthData
    
    def getUserAuthName(self, session):
        if not session.get("user_id", ""): return ""
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        print(userAuthData.name)
        return userAuthData.name
    
    def addUserAuth(self, request):

        if 'input.user.isAdmin' in request.form:
            isAdmin:bool = request.form['input.user.isAdmin']
        else:
            isAdmin:bool = False

        newUser:UserAuthDataStructure = UserAuthDataStructure(request.form['name'], request.form['email'], 'test', isAdmin, 
            bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt()).decode())
        newUser.printUserAuthDataStructure()
        return self.userDBLinkService.addUserAuth(newUser)

    def getAllUserAuthData(self):
        allUserData = self.userDBLinkService.getAllUsers()
        return allUserData

    def updateAllUserAuthData(self, request):
        
        formData = list(request.form.items())
        datalist: list[UserAuthDBStructure] = []
        for key,value in formData:
            if key.endswith('.id'):
                i = key.split('.')[0]
                passwordUpdate = ""
                if request.form.get(f'{i}.password') != "": passwordUpdate = bcrypt.hashpw(request.form.get(f'{i}.password').encode(), bcrypt.gensalt()).decode()

                item:UserAuthDBStructure = UserAuthDBStructure(request.form.get(f'{i}.id'),
                                                                request.form.get(f'{i}.uuid'),
                                                                request.form.get(f'{i}.name'),
                                                                request.form.get(f'{i}.email'),
                                                                request.form.get(f'{i}.isadmin') or False,
                                                                passwordUpdate)
                datalist.append(item)
                
        self.userDBLinkService.updateUserAuth(datalist)
        return True
        
    def deleteUserAuthData(self, request):

        for item in request.form:
            id = item.split('.')[1]
            self.userDBLinkService.deleteUserAuthRecord(id)

        pass

__all__ = ['UserAuthService','UserAuthInterface']