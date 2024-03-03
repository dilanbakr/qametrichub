import psycopg2
from dotenv import load_dotenv
import os
# loading variables from .env file
load_dotenv()

DBNAME=os.getenv('DBNAME')
DBHOST=os.getenv('DBHOST')
DBPORT=os.getenv('DBPORT')
DBUSER=os.getenv('DBUSER')
DBPASS=os.getenv('DBPASS')

def update_data(question1 , question2, question3, question4, question5, question6, question7, question8, id):
    try:
        print("id", id)
        conn = psycopg2.connect(dbname=DBNAME,user=DBUSER,password=DBPASS,host=DBHOST,port=DBPORT)
        cur = conn.cursor()
        cur.execute("UPDATE tez SET anlam= %s, ortaktema= %s , iknaedici= %s, etkili= %s, bilgilendirici= %s, tarafsiz= %s, dil=%s, etki=%s WHERE id=%s;", (question1 , question2, question3, question4, question5, question6, question7, question8, id))
        conn.commit()
        print("Veri eklendi.")
    except psycopg2.Error as e:
        print("Veri eklenirken bir hata oluştu:", e)
    finally:
        conn.close()

def get_data(user_id):
    try:
        paragraf=''
        question=''
        real_answer=''
        predict_answer=''
        id=1
        conn = psycopg2.connect(dbname=DBNAME,user=DBUSER,password=DBPASS,host=DBHOST,port=DBPORT)
        cur = conn.cursor()
        cur.execute("SELECT paragraf, question, real_answer, predict_answer, id FROM tez where anlam IS NULL and ortaktema IS NULL and iknaedici IS NULL and etkili IS NULL and bilgilendirici IS NULL and tarafsiz IS NULL and dil IS NULL and etki IS NULL and userid = %s limit 1;", (user_id,))
        row = cur.fetchall()
        for item in row:
            paragraf = item[0]
            question = item[1]
            real_answer = item[2]
            predict_answer = item[3]
            id = item[4]

    except psycopg2.Error as e:
        print("Veri okunurken bir hata oluştu:", e)
    finally:
        conn.close()

    return paragraf, question, real_answer, predict_answer, id

def login_user(username, password):
    try:
        conn = psycopg2.connect(dbname=DBNAME,user=DBUSER,password=DBPASS,host=DBHOST,port=DBPORT)
        cur = conn.cursor()
        cur.execute("SELECT id FROM userlogin WHERE username = %s AND pass = %s", (username, password))
        user = cur.fetchone()
        user_exists =user is not None

        if user_exists:
            print(user[0])
            print("User exists in the table.")
            return user[0]
        else:
            print("User does not exist in the table.")

    except psycopg2.Error as e:
        print("Veri çekilirken bir hata oluştu:", e)
    finally:
        conn.close()





