from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from twilio.rest import Client
import configparser
import smtplib

app = FastAPI()

class Account(BaseModel):
    username: str
    phone_number: int
    email: str
    zipcode: int
    bio: str

# ENDPOINTS ----------------

@app.on_event("startup")
def root():
    global con
    con = sqlite3.connect("db/emergencyResponseAssistant.db", check_same_thread=False)

    cur = con.cursor()

    with open("db/create.sql", "r") as f:
        script = f.read()
        cur.executescript(script)

@app.post("/create-account/")
def create_account(a: Account):
    cur = con.cursor()
    cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", [a.username, a.phone_number, a.email, a.zipcode, a.bio])
    con.commit()

# FUNCTIONS --------------------

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

def send_text(number: int, msg: str):
    carriers = {
        'AT&T':	'@mms.att.net',
        'T-Mobile USA, Inc.':' @tmomail.net',
        'Verizon Wireless':  '@vtext.com'
    }

    config = configparser.ConfigParser()

    config.read(".env")

    googleAuthPass = config["sms"]["GOOGLE_APP_PASSWORD"]
    googleAuthName = config["sms"]["GOOGLE_EMAIL"]
    twilioAuth = config["twilio"]["TWILIO_AUTH_KEY"]
    sid = config["twilio"]["TWILIO_SID"]

    client = Client(sid, twilioAuth)

    numberData = client.lookups.v2.phone_numbers(f"+1{number}").fetch(fields='line_type_intelligence')
    numberData.line_type_intelligence["carrier_name"]
    to_number = f"{number}{carriers[numberData.line_type_intelligence["carrier_name"]]}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(googleAuthName, googleAuthPass)

    server.sendmail(googleAuthName, to_number, msg)


# TESTING ENDPOINTS ----------------------------------

@app.get("/test-send-text")
def test_send():
    send_text(7206821818, "test")

@app.get("/test-get-users")
def get_users():
    print(get_relevant_users(10000))
