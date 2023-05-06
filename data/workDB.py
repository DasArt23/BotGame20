import mysql.connector
import sqlite3

# def connectToInternetBD(*query):
#     curA = None
#     cnx = mysql.connector.connect(
#             host='wersiy6h.beget.tech',
#             password='z&Cm17qL',
#             user='wersiy6h_bakin_a',
#             database='wersiy6h_bakin_a',
#         )
#     if len(query) == 1:
#         curA = cnx.cursor(buffered=True)
#         curA.execute(query[0])
#     elif len(query) == 2:
#         curA = cnx.cursor(buffered=True)
#         curA.execute(query[0], query[1])
#     try:
#         endOfQuery = curA.fetchall()
#     except:
#         endOfQuery = 0
#     cnx.commit()
#     cnx.close()
#     return endOfQuery

def connectToLocalDB(*query):
    playerDB = sqlite3.connect("data/project.db")
    curA = playerDB.cursor()
    if len(query) == 1:
        curA.execute(query[0])
    elif len(query) == 2:
        curA.execute(query[0], query[1])
    try:
        result = curA.fetchall()
    except:
        result = 0
    playerDB.commit()
    playerDB.close()
    return result

connectToDB = connectToLocalDB