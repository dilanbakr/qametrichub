import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
# loading variables from .env file
load_dotenv()

DBNAME=os.getenv('DBNAME')
DBHOST=os.getenv('DBHOST')
DBPORT=os.getenv('DBPORT')
DBUSER=os.getenv('DBUSER')
DBPASS=os.getenv('DBPASS')


data = pd.read_excel("dbdata.xlsx")
userid=1
conn = psycopg2.connect(dbname=DBNAME,user=DBUSER,password=DBPASS,host=DBHOST,port=DBPORT)
cur = conn.cursor()

for index, row in data.iterrows():
    contexts = row['contexts']
    questions = row['questions']
    answers = row['answers']
    predicts = row['predicts']
    cur.execute("INSERT INTO tez(paragraf, question, real_answer, predict_answer, userid) VALUES (%s, %s, %s, %s, 1);", (contexts , questions, answers, predicts))
    conn.commit()






