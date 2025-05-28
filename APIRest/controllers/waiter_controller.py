from database.database import get_dbc
from flask_wtf.csrf import generate_csrf
from common.functions import cipher_password, compare_password, create_session
import datetime as dt
from __main__ import app

def register_user(username, legal_name, email, password):
    try:
        conn = get_dbc()
        with conn.cursor() as cursor:
            cursor.execute("SELECT profile FROM waiters WHERE username = %s",(username,))
            user = cursor.fetchone()
            if user is None:
                cursor.execute("INSERT INTO waiters (username, legal_name, email, profile, password, state , login_errors) VALUES (%s, %s, %s, 'user', %s, 'active', 0)",
                               (username, legal_name, email, cipher_password(password)))

                if cursor.rowcount == 1:
                    conn.commit()
                    app.logger.info("Nuevo camarero creado")
                    ret={"status": "OK" }
                    code=200
                else:
                    ret={"status": "ERROR" }
                    code=500
            else:
                ret = {"status": "ERROR","mensaje":"Camarero ya existe" }
                code=200
        conn.close()
    except:
        print("Excepcion al registrar al usuario")   
        ret={"status":"ERROR"}
        code=500
    return ret,code  

def login_user(username, passwordIn):
    try:
        conn = get_dbc()
        #print(cipher_password(passwordIn))
        with conn.cursor() as cursor:
            cursor.execute("SELECT profile, password, login_errors FROM waiters WHERE state = 'active' and username = %s",(username))
            user = cursor.fetchone()
            
            if user is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                profile            = user[0]
                password        = user[1]
                login_errors    = user[2]

                current_date = dt.date.today()
                today = current_date.strftime('%Y-%m-%d')
                    
                if (compare_password(password.encode("utf-8"),passwordIn.encode("utf-8"))):
                    ret = {
                            "status": "OK",
                            "csrf_token": generate_csrf(),
                            "profile": profile
                           }
                    app.logger.info("Acceso usuario %s correcto", username)
                    create_session(username, profile)
                    login_errors = 0
                    state = 'active'
                else:
                    app.logger.info("Acceso usuario %s incorrecto", username)
                    login_errors = login_errors + 1
                    if (login_errors > 2):
                        state = "inactive"
                        app.logger.info("Usuario %s bloqueado", username)
                    else:
                        state = 'active'
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo"}
                cursor.execute("UPDATE waiters SET login_errors = %s, access_date = %s, state = %s WHERE username = %s",(login_errors, today, state, username))
                conn.commit()
                conn.close()
            code=200
    except:
        print("Excepcion al validar al usuario")   
        ret={"status":"ERROR"}
        code=500
    return ret,code