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

    def addUserAuth():
        pass


class UserAuthService(UserAuthInterface):

    def __init__(self) -> None:
        self.userDBLinkService: UserAuthDbLinkInterface = UserAuthDbLink()
       
    def checkLogin(self, request, session):
        email = request.form.get("email")
        password = request.form.get("password")
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthByEmail(email)

        print("Email:",userAuthData.email,"emailEntered: ", email, "pwenter: ",password, "pwEnterEncoded: ", password.encode(),"pwDBhash:", userAuthData.password_hash, "- " )

        if (userAuthData.email == email): #and bcrypt.checkpw(password.encode(), userAuthData.password_hash.encode())):
            session["user_id"] = userAuthData.id
            return True
        return False
    
    def getUserAuthData(self, session):
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        return userAuthData
    
    def getUserAuthName(self, session):
        if not session.get("user_id", ""): return ""
        userAuthData:UserAuthDBStructure = self.userDBLinkService.getUserAuthById(session.get("user_id", ""))
        print(userAuthData.name)
        return userAuthData.name
    
    def addUserAuth(self, request):
       
        newUser:UserAuthDataStructure = UserAuthDataStructure(request.form['name'], request.form['email'], request.form['password'], bool(request.form['isAdmin'])  )
       # newUser.printUserAuthDataStructure()

__all__ = ['UserAuthService','UserAuthInterface']