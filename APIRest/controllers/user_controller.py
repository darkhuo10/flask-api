from flask_wtf.csrf import generate_csrf
from database.database import get_dbc
from common.functions import compare_password, cipher_password, create_session
import sys
import datetime as dt
from __main__ import app

def login_usuario(username,passwordIn):
    try:
        conexion = get_dbc()
        #print(cipher_password(passwordIn))
        with conexion.cursor() as cursor:
            cursor.execute("SELECT role,passwd,login_errors FROM users WHERE activity='activo' and user = %s",(username))
            user = cursor.fetchone()
            
            if user is None:
                ret = {"activity": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                role=user[0]
                password=user[1]
                numAccesosErroneos=user[2]

                current_date = dt.date.today()
                hoy=current_date.strftime('%Y-%m-%d')
                    
                if (compare_password(password.encode("utf-8"),passwordIn.encode("utf-8"))):
                    ret = {"activity": "OK",
                           "csrf_token": generate_csrf(),
                           "role":role}
                    app.logger.info("Acceso user %s correcto",username)
                    create_session(username,role)
                    numAccesosErroneos=0
                    activity='activo'
                else:
                    app.logger.info("Acceso user %s incorrecto",username)
                    numAccesosErroneos=numAccesosErroneos+1
                    if (numAccesosErroneos>2):
                        activity="bloqueado"
                        app.logger.info("Usuario %s bloqueado",username)
                    else:
                        activity='activo'
                    ret = {"activity": "ERROR","mensaje":"Usuario/clave erroneo"}
                cursor.execute("UPDATE users SET login_errors=%s, last_login=%s, activity=%s WHERE user = %s",(numAccesosErroneos,hoy,activity,username))
                conexion.commit()
                conexion.close()
            code=200
    except:
        print("Excepcion al validar al user")   
        ret={"activity":"ERROR"}
        code=500
    return ret,code

def alta_usuario(username,password,role,email):
    try:
        conexion = get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT role FROM users WHERE user = %s",(username,))
            user = cursor.fetchone()
            if user is None:
                passwordC=cipher_password(password)
                cursor.execute("INSERT INTO users(user,passwd,email,role,activity,login_errors) VALUES(%s,%s,%s,'normal','activo',0)",(username,passwordC,email))
                if cursor.rowcount == 1:
                    conexion.commit()
                    app.logger.info("Nuevo user creado")
                    ret={"activity": "OK" }
                    code=200
                else:
                    ret={"activity": "ERROR" }
                    code=500
            else:
                ret = {"activity": "ERROR","mensaje":"Usuario ya existe" }
                code=200
        conexion.close()
    except:
        print("Excepcion al registrar al user")   
        ret={"activity":"ERROR"}
        code=500
    return ret,code    