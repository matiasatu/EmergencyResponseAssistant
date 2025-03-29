from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI()

class Account(BaseModel):
    username: str
    phone_number: int
    email: str
    zipcode: int
    bio: str

@app.on_event("startup")
def root():
    global con
    con = sqlite3.connect("db/emergencyResponseAssistant.db", check_same_thread=False)

    cur = con.cursor()

    with open("db/create.sql", "r") as f:
        script = f.read()
        cur.executescript(script)

def send_text(text_str: str):
    ...

@app.post("/create-account/")
def create_account(a: Account):
    cur = con.cursor()
    cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", [a.username, a.phone_number, a.email, a.zipcode, a.bio])
    con.commit()

def get_relevant_users(zipcode: int) -> list[dict]:
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE zipcode=?", [zipcode])

    output = []
    for x in cur.fetchall():
        account = {
            "username": x[0],
            "phone_number": x[1],
            "email": x[2],
            "zipcode": x[3],
            "bio": x[4]
        }
        output += [account]

    return output

# TESTING FUNCS ----------------------------------


@app.get("/test_get_users")
def get_users():
    print(get_relevant_users(10000))
