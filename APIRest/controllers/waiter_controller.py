from database.database import get_dbc
from common.functions import cipher_password, compare_password, create_session
import datetime as dt
from __main__ import app
'''def waiter_to_json(row):
    return {
        "id": row[0],
        "identification": row[1],
        "firstname": row[2],
        "lastname1": row[3],
        "lastname2": row[4],
        "phone": row[5],
        "email": row[6],
        "username": row[7],
        "isadmin": row[8],
        "password": row[9],
        "lastaccess": row[10],
        "loginerror": row[11]
    }'''



def register_user(username, legal_name, email, password):
    try:
        conn = get_dbc()
        with conn.cursor() as cursor:
            cursor.execute("SELECT type FROM waiters WHERE username = %s",(username,))
            user = cursor.fetchone()
            if user is None:
                cursor.execute("INSERT INTO waiters (username, legal_name, email type password, state , login_error) VALUES (%s, %s, %s, 'user', %s, 'active', 0)",
                               username, legal_name, email, cipher_password(password))
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



'''def get_all_waiters():
    try:
        conexion = database.get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM waiters")
            waiters = cursor.fetchall()
            waiters_json = []
            if waiters:
                for w in waiters:
                    print(w.__repr__)
                    waiters_json.append(waiter_to_json(w))
        conexion.close()
        code = 200
    except:
        print("Error al obtener los camareros", file=sys.stdout)
        waiters_json = []
        code = 500
    return waiters_json, code



def get_waiter_by_id(id: int):
    waiter_json = {}
    try:
        conexion = database.get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM waiters WHERE id = %s", id)
            waiter = cursor.fetchone()
            if waiter is not None:
                waiter_json = waiter_to_json(waiter)
        conexion.close()
        code = 200
    except:
        print("Error al recuperar el camarero", file=sys.stdout)
        code = 500
    return waiter_json, code


def delete_waiter(id: int):
    try:
        conexion = database.get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM waiters WHERE id = %s", (id))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except:
        print("Error al eliminar al camarero", file=sys.stdout)
        ret = {"status": "Failure"}
        code = 500
    return ret, code


def update_waiter(waiter: Waiter, id: int):
    try:
        conexion = database.get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE waiters SET identification = %s, firstname = %s, lastname1 = %s, lastname2=%s, phone=%s, email=%s, username=%s, password=%s WHERE id = %s",
                (waiter.identification, waiter.firstname, waiter.lastname1, waiter.lastname2, waiter.phone, waiter.email, waiter.username, waiter.password, id))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except:
        print("Error al actualizar el camareros", file=sys.stdout)
        ret = {"status": "Failure"}
        code = 500
    return ret, code'''

def login_user(username, passwordIn):
    try:
        conn = get_dbc()
        #print(cipher_password(passwordIn))
        with conn.cursor() as cursor:
            cursor.execute("SELECT type, password,login_errors FROM waiters WHERE state = 'active' and username = %s",(username))
            user = cursor.fetchone()
            
            if user is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                type            = user[0]
                password        = user[1]
                login_errors    = user[2]

                current_date = dt.date.today()
                today = current_date.strftime('%Y-%m-%d')
                    
                if (compare_password(password.encode("utf-8"),passwordIn.encode("utf-8"))):
                    ret = {
                            "status": "OK",
                            "csrf_token": generate_csrf(),
                            "type": type
                           }
                    app.logger.info("Acceso usuario %s correcto", username)
                    create_session(username, type)
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