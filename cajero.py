
import sqlite3
import os
import time
import uuid

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

class Usuario:

    def __init__(self, username):
        self.username = username
        self.password = cursor.execute("select password from usuarios where username = ?", (username,)).fetchone()
        self.userid = cursor.execute("select userid from usuarios where username = ?", (username,)).fetchone()

    @staticmethod
    def userExist(username):
        exist = cursor.execute("select * from usuarios where username = ?", (username,)).fetchone()
        if exist:
            return True
        else:
            return False

    @staticmethod
    def login():
        username = input("Nombre de usuario: ")
        exist = Usuario.userExist(username)
        if not exist:
            print("No existe ningun usuario con ese nombre.")
            return
        password = input("Contraseña: ")
        rightPswd = cursor.execute("select password from usuarios where username = ?", (username,)).fetchone()
        if not password == rightPswd[0]:
            print("Contraseña incorrecta.")
            return
        return Usuario(username)
    
    @staticmethod
    def signin():
        username = input("Nombre de usuario: ").strip()
        if not username:
            print("Introduce un nombre válido.")
            return
        password = input("Contraseña: ").strip()
        if not password:
            print("Introduce una contraseña válida.")
            return
        userid = str(uuid.uuid4())
        cursor.execute("insert into usuarios (userid, username, password) values (?, ?, ?)", (userid, username, password))
        connection.commit()
        print("\nUsuario registrado exitosamente.")

    def consultarSaldo(self):
        saldo = cursor.execute("select saldo from usuarios where username = ?", (self.username,)).fetchone()
        return saldo[0]


class Cajero:

    def menu_login():
        ejecutando = True
        while ejecutando:
            os.system("clear")
            print("Cajero automatico\n\nComandos:\n\n1. Iniciar sesion\n2. Crear cuenta\n3. Salir")
            usrInput = input("\nComando: ")

            match (usrInput):
                case "1":
                    user = Usuario.login()
                    if user:
                        Cajero.menu_usuario(user)
                case "2":
                    Usuario.signin()
                case "3":
                    print("Saliendo...")
                    connection.close()
                    return
                case _:
                    print("Comando inválido.")
            time.sleep(1)
    
    def menu_usuario(user):
        while True:
            os.system("clear")
            print(f"Cajero automatico | Usuario: {user.username}\n\nComandos:\n\n1. Depositar\n2. Retirar\n3. Consultar saldo\n4. Consultar info\n5. Salir")
            usrInput = input("\nComando: ")
            
            match (usrInput):
                case "1":
                    cantidad = input("Cantidad a depositar: ")
                    try:
                        cantidad = int(cantidad)
                        saldo = Usuario.consultarSaldo(user)
                        if cantidad > 0:
                            cantidad = saldo + cantidad
                            cursor.execute("update usuarios set saldo = ? where username = ?", (cantidad, user.username))
                            connection.commit()
                            print("Deposito exitoso.")
                        else:
                            print("Introduce una cantidad válida.")
                    except:
                        print("Introduce una cantidad válida.")
                case "2":
                    cantidad = input("Cantidad a retirar: ")
                    try:
                        cantidad = int(cantidad)
                        saldo = Usuario.consultarSaldo(user)
                        if cantidad <= saldo:
                            cantidad = saldo - cantidad
                            cursor.execute("update usuarios set saldo = ? where username = ?", (cantidad, user.username))
                            connection.commit()
                            print("Retiro exitoso.")
                        else:
                            print("No hay suficientes fondos.")
                    except:
                        print("Introduce una cantidad válida.")
                case "3":
                    saldo = Usuario.consultarSaldo(user)
                    print(f"Saldo: ${saldo}")
                case "4":
                    os.system("clear")
                    print(f"Cajero automatico | Usuario: {user.username}\n\nInformacion:\n\nUser ID: {user.userid[0]}\nNombre de usuario: {user.username}\nContraseña: {user.password[0]}")
                    input("\nPresiona ENTER para volver.")
                case "5":
                    print("Saliendo...")
                    return
                case _:
                    print("Comando inválido.")
            time.sleep(1)

if __name__ == "__main__":
    Cajero.menu_login()