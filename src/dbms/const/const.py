INSERT_USER = """
INSERT INTO "users" 
    ("username", "fullname", "password", "role_in_session") 
VALUES 
    (?, ?, ?, ?); """

GET_USER = '''
SELECT 
    username, fullname, role_in_session
FROM users
WHERE (username,password) = (?,?) 
LIMIT 1; 
'''

GET_USERS = '''
SELECT 
    username, role_in_session
FROM users;
'''

INIT_DATABASE = '''
DROP TABLE IF EXISTS "users" ;
CREATE TABLE "users" (
    "id"    INTEGER NOT NULL UNIQUE,
    "username"    TEXT NOT NULL UNIQUE,
    "fullname"    TEXT NOT NULL,
    "password"    TEXT NOT NULL,
    "role_in_session"    TEXT NOT NULL DEFAULT '{}',
    PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS "roles";
CREATE TABLE "roles" (
    "id"    INTEGER NOT NULL,
    "name"    TEXT NOT NULL UNIQUE,
    "level"    INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS "sessions" ;
CREATE TABLE "sessions" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL UNIQUE,
    "dbms"    TEXT NOT NULL DEFAULT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS "operations" ;
CREATE TABLE "operations" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "level" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
);

DROP TABLE IF EXISTS "objects" ;
CREATE TABLE "objects" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
);

--INSERT objects Table
INSERT INTO "objects" ("name") VALUES ('math.db');
INSERT INTO "objects" ("name") VALUES ('it.db');
INSERT INTO "objects" ("name") VALUES ('chemistry.db');

--Insert operations table
INSERT INTO "operations" ("name","level") VALUES ('VIEW NAME','1');
INSERT INTO "operations" ("name","level") VALUES ('VIEW GRADE','2');
INSERT INTO "operations" ("name","level") VALUES ('WRITE GRADE','3');
INSERT INTO "operations" ("name","level") VALUES ('EDIT GRADE','3');
INSERT INTO "operations" ("name","level") VALUES ('EDIT INFO','4');

--Insert Roles
INSERT INTO "roles" ("name", "level") VALUES ('STUDENT', '1');
INSERT INTO "roles" ("name", "level") VALUES ('TA', '2');
INSERT INTO "roles" ("name", "level") VALUES ('LECTURER', '3');
INSERT INTO "roles" ("name", "level") VALUES ('ADMIN', '4');

--Insert Sessions
INSERT INTO "sessions" ("name","dbms") VALUES ('MATH','math.db');
INSERT INTO "sessions" ("name","dbms") VALUES ('IT','it.db');
INSERT INTO "sessions" ("name","dbms") VALUES ('CHEMISTRY','chemistry.db');

--Insert Users
INSERT INTO "users" ("username", "fullname", "password","role_in_session") VALUES ('admin', 'Admin', 'password','{"MATH":"ADMIN","IT":"ADMIN","CHEMISTRY":"ADMIN"}');
INSERT INTO "users" ("username", "fullname", "password") VALUES ('one.sdh20', 'Tran One', 'password');
INSERT INTO "users" ("username", "fullname", "password") VALUES ('min.sdh20', 'Than Hai Nhat Min', 'password');
INSERT INTO "users" ("username", "fullname", "password") VALUES ('quit.sdh20', 'Nguyen Dinh Hoang Quit', 'password');
'''

GET_PRMS = '''
--PRM , ROLE, OBJECT, OPERATION
SELECT 
    roles.name as Role
    ,sessions.name as Session
    ,objects.name as Object 
    ,operations.name as Operation
FROM
    roles JOIN sessions JOIN objects JOIN operations
    ON (sessions.dbms=objects.name)
WHERE 
    (operations.level <= roles.level);
'''