from sqlite3 import Connection
import pandas as pd

# Part init for the operation
INIT_MATH = '''
DROP TABLE IF EXISTS "math" ;
CREATE TABLE "math" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "grade"    REAL CHECK("grade" BETWEEN 0 AND 10),
    PRIMARY KEY("id" AUTOINCREMENT)
);


INSERT INTO "math" ("name", "grade") VALUES ('Nguyen Ty Fu', '9.5');
INSERT INTO "math" ("name", "grade") VALUES ('Nguyen Dinh Hoang Quit', '9.2');
INSERT INTO "math" ("name", "grade") VALUES ('Nguyen Huu Food', '8.5');
INSERT INTO "math" ("name", "grade") VALUES ('Than Hai Nhat Min', '9.8');
'''

INIT_IT = ''' 
DROP TABLE IF EXISTS "it" ;
CREATE TABLE "it" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "grade"    REAL CHECK("grade" BETWEEN 0 AND 10),
    PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "it" ("id", "name", "grade") VALUES ('1','Than Hai Nhat Min', '9.8');
INSERT INTO "it" ("id", "name", "grade") VALUES ('2','Vu Phuong Thal', '9.8');
INSERT INTO "it" ("id", "name", "grade") VALUES ('3','Kim Ngoan', '9.7');
INSERT INTO "it" ("id", "name", "grade") VALUES ('4','Nguyen Dinh Hoang Quit', '3.5');
'''

INIT_CHEMISTRY = '''
DROP TABLE IF EXISTS "chemistry" ;
CREATE TABLE "chemistry" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "grade"    REAL CHECK("grade" BETWEEN 0 AND 10),
    PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "chemistry" ("id", "name", "grade") VALUES ('1','Nguyen Ty Fu', '9.5');
INSERT INTO "chemistry" ("id", "name", "grade") VALUES ('2','Nguyen Dinh Hoang Quit', '4');
INSERT INTO "chemistry" ("id", "name", "grade") VALUES ('3','Nguyen Huu Food', '8.5');
INSERT INTO "chemistry" ("id", "name", "grade") VALUES ('4','Than Hai Nhat Min', '9.8');
INSERT INTO "chemistry" ("id", "name", "grade") VALUES ('5','Vu Phuong Thal', '9.8');
'''

INIT_SCHOOL = {
    'math': INIT_MATH,
    'it' : INIT_IT,
    'chemistry': INIT_CHEMISTRY
}

def init_school():
    databases = ['math','it','chemistry']
    for database in databases:
        conn = Connection(f'./model/{database}.db')
        cur = conn.cursor()
        cur.executescript(INIT_SCHOOL[database])
        conn.commit()
        cur.close()
        conn.close()

# View Name operation
def get_name(obj):
    conn = Connection('./model/'+obj)
    cur = conn.cursor()
    __table = obj.split('.')[0]
    __SELECT_NAME__ = f'''
    SELECT id,name FROM {__table};'''
    cur.execute(__SELECT_NAME__)
    names = cur.fetchall()
    return pd.DataFrame(names,columns=["id","name"])

# View Grade operation
def get_grade(obj):
    conn = Connection('./model/'+obj)
    cur = conn.cursor()
    __table = obj.split('.')[0]
    __SELECT_NAME__ = f'''SELECT id,name,grade FROM {__table};'''
    cur.execute(__SELECT_NAME__)
    grades = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(grades,columns=["id","name","grade"])

# Write Grade operation
def write_grade(obj):
    conn = Connection('./model/'+obj)
    cur = conn.cursor()
    __table = obj.split('.')[0]
    __SELECT_NAME__ = f'''
    SELECT id,name,grade FROM {__table};'''
    cur.execute(__SELECT_NAME__)
    grades = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(grades,columns=["id","name","grade"])

# Edit Grade operation
def edit_grade(obj):
    conn = Connection('./model/'+obj)
    cur = conn.cursor()
    __id = input('Enter the ID of Student: ')
    __grade = input('Enter the new grade: ')
    __table = obj.split('.')[0]
    __UPDATE__ = f'''UPDATE {__table} SET grade = ? WHERE id=? ;'''
    cur.execute(__UPDATE__,(__grade,__id))
    conn.commit()
    cur.close()
    conn.close()

# Edit information of student
def edit_info(obj):
    conn = Connection('./model/'+obj)
    cur = conn.cursor()
    TEXT = '''Choose actions:
    1. Update
    2. Delete
Enter your choose: '''
    __act = input(TEXT)
    __id = input('Enter the ID of Student: ')
    __table = obj.split('.')[0]
    if __act=='1':
        __name = input('Enter the new name: ')
        __UPDATE__ = f'''UPDATE {__table} SET name = ? WHERE id=? ;'''
        cur.execute(__UPDATE__,(__name,__id))
    else:
        __id
        __DELETE__ = f'''DELETE FROM {__table} WHERE id=? ;'''
        cur.execute(__DELETE__,(__id,))
    conn.commit()
    cur.close()
    conn.close()
    
actions =  {
    "INIT" : init_school,
    "VIEW NAME":   get_name,
    "VIEW GRADE": get_grade,
    "WRITE GRADE": write_grade,
    "EDIT GRADE": edit_grade,
    "EDIT INFO":  edit_info,
    }