from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from contextlib import contextmanager

app = FastAPI()

class Account(BaseModel):
    username: str
    email: str
    phone_number: int
    zipcode: int
    bio: str

@app.on_event("startup")
def root():
    global con
    con = sqlite3.connect("emergencyResponseAssistant.db", check_same_thread=False)

    cur = con.cursor()

    with open("../db/create.sql", "r") as f:
        script = f.read()
        cur.executescript(script)

@app.get("/text")
def send_text(text_str: str):
    ...

@app.post("/create-account/")
def create_account(a: Account):
    cur = con.cursor()
    cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", [a.username, a.phone_number, a.email, a.zipcode, a.bio])
    con.commit()