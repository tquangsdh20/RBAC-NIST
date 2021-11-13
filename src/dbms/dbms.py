class InValidValue(Exception): ...
import sqlite3
import json
import casbin
from .const import *
from .operations import *

def validation(cursor,query,role,exception):
    cursor.execute(query)
    validList = cursor.fetchall()
    if (role,) not in validList: raise exception

class DB:
    def __init__(self,filename):
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()
        
    def init_database(self):
        self.cur.executescript(INIT_DATABASE)
        self.conn.commit()
    
    def insert_user(self,record):
        self.cur.execute(INSERT_USER)
        
    def reset_roles_for_user(self,user):
        __reset_role__ = "UPDATE users SET role_in_session = '{}' WHERE username=? ;"
        self.cur.execute(__reset_role__,(user,))
        
    def UA(self,user,session,role):
        __GET_USER = "SELECT role_in_session FROM users WHERE username = ? ;"
        __UPDATE_ROLE = "UPDATE users SET role_in_session = ? WHERE username = ?;"
        
        #Validate Users in RBAC Model
        __VALIDATE_USER__ = "SELECT username FROM users;"
        validation(self.cur,
                   __VALIDATE_USER__,
                   user,
                   InValidValue(f"Username '{user}' does not exist in database")
                  )
        
        #Validation Roles in RBAC Model
        __VALIDATE_ROLE__ = "SELECT name FROM roles;"
        validation(self.cur,
                   __VALIDATE_ROLE__,
                   role,
                   InValidValue(f"Role '{role}' does not exist in database")
                  )
        
        # Validation Sessions in RBAC Model
        __VALIDATE_SESSION__ = "SELECT name FROM sessions;"
        validation(self.cur,
                   __VALIDATE_SESSION__,
                   session,
                   InValidValue(f"Session '{session}' does not exist in database")
                  )
        # Role Assignment for User 
        self.cur.execute(__GET_USER,(user,))
        prev_session = json.loads(self.cur.fetchone()[0])
        if session not in prev_session.keys():
            prev_session[session] = role
        elif prev_session[session]==role: print('This role has been assigned to this user')
        else: raise InValidValue(f"Failure to assign the role '{role}' for the session '{session}' because the current role comflict with the new role")
        new_session = json.dumps(prev_session)
        self.cur.execute(__UPDATE_ROLE,(new_session,user))
        
    def insert_role(self,record):
        self.cur.execute(INSERT_ROLE)
        
    def get_users(self):
        self.cur.execute(GET_USERS)
        return self.cur.fetchall()
    
    def sign_in(self,username,password):
        self.cur.execute(GET_USER,(username,password))
        return self.cur.fetchone()
    
    def check_roles(self,user):
        self.cur.execute('SELECT role_in_session FROM users WHERE username = ?',(user,))
        role_str = self.cur.fetchone()[0]
        roles = json.loads(role_str)
        for s,r in roles.items():
            print(f'{s} : {r}')
    
    def policy_update(self):
        # Get all permisions
        self.cur.execute(GET_PRMS)
        prms = self.cur.fetchall()
        
        # Get all users' roles
        self.cur.execute(GET_USERS)
        users = self.cur.fetchall()
        
        # Write content with formats
        PRM = 'p, {role}, {session}, {obj}, {action}\n'
        GRT = 'g, {user}, {role}, {session}\n'
        
        # Write down all Permisions and all Users' Assignment
        with open('./model/rbac_policy.csv','w') as fp:
            for prm in prms:
                fp.write(PRM.format(role=prm[0],session=prm[1],obj=prm[2],action=prm[3]))
            for user in users:
                username,role_str = user
                roles = json.loads(role_str)
                for session,role in roles.items():
                    fp.write(GRT.format(user=username,role=role,session=session))
            fp.close()
            
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

RBAC_NIST = ("./model/rbac.conf", "./model/rbac_policy.csv")
class OpenModel:
    def __init__(self,model:tuple):
        _conf,_policy = model
        self.__user__ = ''
        self.__enforcer__ = casbin.Enforcer(_conf,_policy)
        
    def init(self):
        func = actions["INIT"]
        func()
    
    def login(self,username:str,password:str,db:DB):
        res = db.sign_in(username,password)
        if res is None:
            print('Error: Password or User is incorrect.')
        else:
            self.__user__,name,role_str = res
            print(f'Hello {name},')
            print('Your roles:')
            roles = json.loads(role_str)
            print(roles)
        
    def request(self,domain:str,obj:str,act:str):
        __sub = self.__user__ 
        res = self.__enforcer__.enforce(__sub,domain,obj,act)
        result = None
        if res:
            print('Your request is accepted')
            operation = actions[act]
            result = operation(obj)
        else:
            print('Access Denied.')
        return result