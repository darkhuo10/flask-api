from flask_wtf.csrf import generate_csrf
from database.database import get_dbc
import sys
from common.functions import compare_password, cipher_password,create_session
import sys
import datetime as dt
from __main__ import app

def login_usuario(username,passwordIn):
    try:
        conexion = get_dbc()
        #print(cipher_password(passwordIn))
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil,clave,numeroAccesosErroneo FROM usuarios WHERE estado='activo' and usuario = %s",(username))
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                perfil=usuario[0]
                password=usuario[1]
                numAccesosErroneos=usuario[2]

                current_date = dt.date.today()
                hoy=current_date.strftime('%Y-%m-%d')
                    
                if (compare_password(password.encode("utf-8"),passwordIn.encode("utf-8"))):
                    ret = {"status": "OK",
                           "csrf_token": generate_csrf(),
                           "perfil":perfil}
                    app.logger.info("Acceso usuario %s correcto",username)
                    create_session(username,perfil)
                    numAccesosErroneos=0
                    estado='activo'
                else:
                    app.logger.info("Acceso usuario %s incorrecto",username)
                    numAccesosErroneos=numAccesosErroneos+1
                    if (numAccesosErroneos>2):
                        estado="bloqueado"
                        app.logger.info("Usuario %s bloqueado",username)
                    else:
                        estado='activo'
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo"}
                cursor.execute("UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",(numAccesosErroneos,hoy,estado,username))
                conexion.commit()
                conexion.close()
            code=200
    except:
        print("Excepcion al validar al usuario")   
        ret={"status":"ERROR"}
        code=500
    return ret,code

def alta_usuario(username,password,perfil,correo):
    try:
        conexion = get_dbc()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
            usuario = cursor.fetchone()
            if usuario is None:
                passwordC=cipher_password(password)
                cursor.execute("INSERT INTO usuarios(usuario,clave,correo,perfil,estado,numeroAccesosErroneo) VALUES(%s,%s,%s,'normal','activo',0)",(username,passwordC,correo))
                if cursor.rowcount == 1:
                    conexion.commit()
                    app.logger.info("Nuevo usuario creado")
                    ret={"status": "OK" }
                    code=200
                else:
                    ret={"status": "ERROR" }
                    code=500
            else:
                ret = {"status": "ERROR","mensaje":"Usuario ya existe" }
                code=200
        conexion.close()
    except:
        print("Excepcion al registrar al usuario")   
        ret={"status":"ERROR"}
        code=500
    return ret,code    