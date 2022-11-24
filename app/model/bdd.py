import mysql.connector
from mysql.connector import errorcode
from ..config import DB_SERVER
from app import utils


# connexion au serveur de BDD
def connexion():
    cnx = mysql.connector.connect(**DB_SERVER)
    return cnx# error: remonte problème connexion
        # fermeture de la connexion au serveur de BDD

def close_bd(cursor, cnx):
    cursor.close()
    cnx.close()


# ================================== COMPTES ========================================
def create_account(username, password):
    cnx = connexion()
    cnx.autocommit = False
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT username FROM utilisateurs WHERE username=%s"
    cursor.execute(sql, (username,))
    db_response = cursor.fetchall()
    if len(db_response) == 0:
        # Si aucun autre utilisateur n'a le même nom on l'enregistre
        hashed_pass, sel = utils.hash(password)
        sql = "INSERT (username, password, sel) INTO utilisateurs VALUES(%s,%s,%s)"
        cursor.execute(sql, (username, hashed_pass, sel))
        cnx.commit()
        close_bd(cursor, cnx)
        return True
    close_bd(cursor, cnx)
    return False

def log_user(username, password):
    cnx, error = connexion()
    if error is not None:
        raise mysql.connector.Error("Can't connect")
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT sel, password, id FROM utilisateurs WHERE username=%s"
    cursor.execute(sql, (username,))
    query = cursor.fetchall()
    print(query)
    hashed_pass = utils.check_hash(password, query["sel"])
    if hashed_pass == query["password"]:
        return query["id"]
    return False

# ===================================================================================


def get_user_info(id):
    cnx = connexion()
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * from utilisateurs WHERE id=%s"
    cursor.execute(sql, (id,))
    user_info = cursor.fetchall()
    close_bd(cursor, cnx)
    if len(user_info) == 0:
        user_info = None 
    return user_info
    

def get_membresData():
    try:
        cnx, error = connexion()
        if error is not None:
            return error, None
        cursor = cnx.cursor(dictionary=True)
        sql = "SELECT * FROM membres"
        cursor.execute(sql)
        listeMembre = cursor.fetchall()
        close_bd(cursor, cnx)
        msg = "OKmembres"
    except mysql.connector.Error as err:
        listeMembre = None
        msg = "Failed get membres data : {}".format(err)
    return msg, listeMembre


def init_utilisateur_database():
    cnx, error = connexion()
    if error is not None:
        return errorcode.CR_CONNECTION_ERROR
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * from utilisateurs WHERE id=%s"
    cursor.execute(sql, (id,))
    user_info = cursor.fetchall()
    close_bd(cursor, cnx)
    if len(user_info) == 0:
        user_info = None 
    return user_info