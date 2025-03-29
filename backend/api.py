from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Account(BaseModel):
    username: str
    email: str
    phone_number: int
    zipcode: int
    bio: str


@app.get("/")
def root():
    con = sqlite3.connect("emergencyResponseAssistant.db")
    cur = con.cursor()


    with open("../db/create.sql", "r") as f:
        script = f.read()
        cur.executescript(script)

@app.get("/text")
def send_text(text_str: str):
    ...

@app.post("/create-account/")
def create_account(a: Account):
    ...