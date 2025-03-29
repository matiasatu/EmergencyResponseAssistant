from fastapi import FastAPI
import sqlite3

app = FastAPI()


@app.get("/")
def main():
    con = sqlite3.connect("emergencyResponseAssistant.db")
    cur = con.cursor()


    with open("../db/create.sql", "r") as f:
        script = f.read()
        cur.executescript(script)

@app.get("/text")
def send_text()