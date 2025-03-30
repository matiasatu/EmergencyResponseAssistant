from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests
import json
from typing import List, Dict, Any, Optional
from twilio.rest import Client
import configparser
import smtplib
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Account(BaseModel):
    username: str
    email: str
    phone_number: int
    location: str
    bio: str

class Message(BaseModel):
    username: str
    msg: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
    cur.execute("INSERT INTO user VALUES(?,?,?,?,?)", [a.username, a.phone_number, a.email, a.location, a.bio])
    con.commit()

@app.get("/start-flow")
def emergency():
    users = get_users()
    for u in users:
        report = generate_report(u["location"], u["bio"])
        print(report)
        report = report.replace('\n', '')
        reportDict = json.loads(report)

        if reportDict["concern"]:
            send_text(u["phone_number"], reportDict["summary"])
            cur = con.cursor()

            cur.execute("SELECT * FROM summary WHERE username=?", [u["username"]])

            # if cur.fetchall():
            #     cur.execute("UPDATE summary SET summary=? WHERE username=?", [reportDict["extended_info"], u["username"]])
            #     con.commit()
            # else:
            cur.execute("INSERT INTO summary VALUES(?,?)", [u["username"], reportDict["extended_info"]])
            con.commit()

@app.get("/summary/{username}")
def get_summary(username: str):
    cur = con.cursor()

    cur.execute("SELECT * FROM summary WHERE username=?", [username])

    _, summary = cur.fetchone()

    r = {
        "summary": summary
    }
    return JSONResponse(json.dumps(r))

@app.get("/user/{username}")
def get_user(username: str):
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE username=?", [username])

    x = cur.fetchone()
    if x is not None:
        u = {
            "username": x[0],
            "phone_number": x[1],
            "email": x[2],
            "location": x[3],
            "bio": x[4]
        }
    else:
        u = {
            "username": "null"
        }

    return JSONResponse(json.dumps(u))

@app.post("/live-feedback/")
def feedback(msg: Message):
    cur = con.cursor()
    cur.execute("SELECT * FROM messages WHERE username=?", [msg.username])

    row = cur.fetchone()

    config = configparser.ConfigParser()
    config.read(".env")
    API_KEY = config["groq"]["GROQ_API_KEY"]
    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    prompt = f"""
    Using the following description give me any feedback on the description and any improvements I could make. 
    Consider medical conditions, disabilities, other people or pets in the users home they may need to take care of, unique details about the users transportation situation and anything else you think would be relevant.
    make your response sentences concise and constructive for example "consider adding X"
    You should focus on the charictaristics of the users situation not the things they should do
    focus your response around additional categories of data the user could add rather than the ways they could improve the ones they ahve added
    for example telling the user that they need to give more information about X is useless but telling them that they did not mention anything in a given category is useful
    aim for simplicity in your response
    do not use complicated sentences
    DO NOT USE COMPLICATED SENTENCES
    A COMPLICATED SENTENCE IS ONE WITH MULTIPLE CLAUSES
    YOU ARE GIVING ME COMPLICATED SENTENCES
    DESCRIPTION:
    {msg.msg}
    YOUR OUTPUT:
    bullet points of categories that could be added or updated
    give me at most 3 bullet points and do not be afraid to repond with "No suggestions"
    each bullet point should be in the format "-%content%\n
    bullet points do not need to be longer than 5 words
    if you think there are no suggestions needed reply "No Suggestions"
    the only output should be these bullet points
    remember to reply with "No suggestions" when you think the input covers most categories
    """

    if row is not None:
        output = row[1]
        input = row[2]
    else:
        output = "None"
        input = "None"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    feedbackMsg = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": 
             "You are helping people write descriptions containting information about their unique needs in an natural disaster or emergency situation.\
              Provide guidance on sections of their description that need more information or sections that could be added to improve their description\
              This description is coming to you as a stream so each subsequent input will contain the last with the users changes"},
            {"role": "user", "content": f"The last input you were given was {input} and the last response you gave was {output}"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3  # Lower temperature for more factual responses
    }

    try:
        response = requests.post(API_URL, headers=headers, json=feedbackMsg)
        response.raise_for_status()
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            feedback = result['choices'][0]['message']['content']

            differentMsg = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": 
                    "You are tasked with analyzing two responses to see if they are significantly different"},
                    {"role": "user", "content": 
                    f"""
                    Here are the two responses. a difference of a few words is not enough to consider them different. tell me if the content is different Do not let us down
                    RESPONSE 1:
                    {output}
                    RESPONSE 2:
                    {feedback}
                    YOUR OUTPUT:
                    your output should be a single character 'Y' if the responses contain different content. 'N' otherwise
                    DO NOT OUTPUT MORE THAN A SINGLE CHARACTER
                    """}
                ],
                "temperature": 0.3  # Lower temperature for more factual responses
            }

            response = requests.post(API_URL, headers=headers, json=differentMsg)
            response.raise_for_status()
            result = response.json()
            different = result['choices'][0]['message']['content']


            if different == 'Y':
                cur = con.cursor()
                cur.execute("SELECT * FROM messages WHERE username=?", [msg.username])

                if cur.fetchall():
                    cur.execute("UPDATE messages SET output=?, input=? WHERE username=?", [feedback, input, msg.username])
                    con.commit()
                else:
                    cur.execute("INSERT INTO messages VALUES(?,?,?)", [msg.username, feedback, msg.msg])
                    con.commit()

            r = {
                "new_response": different == 'Y',
                "response": feedback
            }
            return JSONResponse(json.dumps(r))
            # return analysis
        else:
            return f"Error: Unable to get a proper response from Groq API. Response: {result}"
            
    except requests.RequestException as e:
        return f"Error communicating with Groq API: {str(e)}"
    except json.JSONDecodeError:
        return f"Error parsing response from Groq API. Response was not valid JSON."
    except Exception as e:
        return f"Unexpected error during analysis: {str(e)}"


# FUNCTIONS --------------------



def get_emergency_information() -> List[Dict[str, Any]]:
    """
    Fetches emergency information from multiple APIs, parses the relevant data,
    and returns a structured list of emergency events.
    
    Returns:
        List[Dict[str, Any]]: List of emergency events with parsed information
    """
    # List to store processed emergency events
    all_emergencies = []
    
    # Function to handle API request errors
    def safe_api_request(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict]:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching data from {url}: {str(e)}")
            return None
    
    # API 1: FEMA API for disasters
    fema_url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
    fema_data = safe_api_request(fema_url)
    
    if fema_data and 'DisasterDeclarationsSummaries' in fema_data:
        for disaster in fema_data['DisasterDeclarationsSummaries'][:10]:  # Limit to 10 recent events
            event = {
                'source': 'FEMA',
                'type': disaster.get('disasterType', 'Unknown'),
                'title': disaster.get('declarationTitle', 'No title available'),
                'location': f"{disaster.get('designatedArea', 'Unknown Area')}, {disaster.get('state', 'Unknown State')}",
                'date': disaster.get('incidentBeginDate', 'Unknown date'),
                'status': disaster.get('declarationStatus', 'Unknown status'),
                'id': disaster.get('disasterNumber', 'Unknown ID'),
                'summary': f"{disaster.get('disasterType', 'Event')} in {disaster.get('designatedArea', 'Unknown Area')}, {disaster.get('state', 'Unknown State')}"
            }
            all_emergencies.append(event)
    
    # # API 2: USGS Earthquake API
    # usgs_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson"
    # usgs_data = safe_api_request(usgs_url)
    
    # if usgs_data and 'features' in usgs_data:
    #     for quake in usgs_data['features']:
    #         props = quake.get('properties', {})
    #         coords = quake.get('geometry', {}).get('coordinates', [0, 0])
            
    #         # Convert timestamp to readable date
    #         timestamp = props.get('time', 0) / 1000  # Convert milliseconds to seconds
    #         date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
    #         event = {
    #             'source': 'USGS',
    #             'type': 'Earthquake',
    #             'title': props.get('title', 'Earthquake event'),
    #             'location': props.get('place', f"Lat: {coords[1]}, Long: {coords[0]}"),
    #             'date': date_str,
    #             'magnitude': props.get('mag', 'Unknown magnitude'),
    #             'status': props.get('status', 'Unknown status'),
    #             'id': props.get('code', 'Unknown ID'),
    #             'summary': f"Magnitude {props.get('mag', 'Unknown')} earthquake near {props.get('place', 'unknown location')}"
    #         }
    #         all_emergencies.append(event)
    
    # # API 3: National Weather Service Alerts
    # weather_url = "https://api.weather.gov/alerts/active"
    # headers = {"Accept": "application/geo+json"}
    # weather_data = safe_api_request(weather_url, headers)
    
    # if weather_data and 'features' in weather_data:
    #     for alert in weather_data['features'][:10]:  # Limit to 10 recent alerts
    #         props = alert.get('properties', {})
            
    #         event = {
    #             'source': 'National Weather Service',
    #             'type': props.get('event', 'Weather alert'),
    #             'title': props.get('headline', props.get('event', 'Weather alert')),
    #             'location': props.get('areaDesc', 'Unknown area'),
    #             'date': props.get('sent', 'Unknown date'),
    #             'status': props.get('status', 'Unknown status'),
    #             'severity': props.get('severity', 'Unknown severity'),
    #             'id': props.get('id', 'Unknown ID'),
    #             'summary': props.get('description', 'No description available')[:200] + '...' if props.get('description') and len(props.get('description')) > 200 else props.get('description', 'No description available'),
    #             'instruction': props.get('instruction', 'No instructions provided')
    #         }
    #         all_emergencies.append(event)
    
    # Sort all emergencies by date (most recent first)
    try:
        all_emergencies.sort(key=lambda x: x.get('date', ''), reverse=True)
    except Exception as e:
        print(f"Error sorting emergencies by date: {str(e)}")
    
    return all_emergencies

def generate_report(my_location: str = "San Francisco, CA", user_info: str = "") -> str:
    """
    Sends emergency information to Groq LLM API to assess if the user's location
    might be impacted by any recent emergency events.
    
    Args:
        my_location (str): User's location (city, state or address)
        
    Returns:
        str: Analysis from Groq LLM on potential impacts
        {
            concers: bool,
            emergencies: list[json],
            summary: str, 
            text_msg: str
        }
    """
    # Get emergency information
    print("FETCHING EMERGENCY INFORMATION...\n")
    emergencies = get_emergency_information()
    
    if not emergencies:
        return "No emergency information available or all API requests failed."
    
    # Format emergency information for the LLM
    emergency_descriptions = []
    for i, event in enumerate(emergencies, 1):
        description = f"Emergency #{i}:\n"
        description += f"- Source: {event.get('source', 'Unknown')}\n"
        description += f"- Type: {event.get('type', 'Unknown')}\n"
        description += f"- Title: {event.get('title', 'No title')}\n"
        description += f"- Location: {event.get('location', 'Unknown location')}\n"
        description += f"- Date: {event.get('date', 'Unknown date')}\n"
        
        # Add additional fields if they exist
        for key, value in event.items():
            if key not in ['source', 'type', 'title', 'location', 'date', 'summary'] and value:
                description += f"- {key.capitalize()}: {value}\n"
        
        description += f"- Summary: {event.get('summary', 'No summary available')}\n"
        emergency_descriptions.append(description)
    
    formatted_emergencies = "\n".join(emergency_descriptions)
    # print(formatted_emergencies)
    # Send to Groq API

    config = configparser.ConfigParser()
    config.read(".env")
    API_KEY = config["groq"]["GROQ_API_KEY"]

    # API_KEY = "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"
    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Based on the following recent emergency events, analyze if my location "{my_location}" might be affected by any of them.
    Consider distance, type of emergency, and other relevant factors. If the emergencies are not nearby just return false like described below. If there are any precautions the person should take, include those.
    Treat all events as if they are happening right now. If there are historical FEMA events, treat them like they are currently ongoing. Be generous with declarcing emergencies.
    If there is one happening nearby, even if status is unknown, assume the worst as to be safe is better than to be sorry. By nearby I mean extremely nearby. Like within 50 miles.
    If it is more than 50 miles do not declare it an emergency under any circumstances.
    
    EMERGENCY EVENTS:
    {formatted_emergencies}
    
    MY LOCATION: {my_location}

    USER INFO: {user_info}

    write things like how to plan escape routes, where to hide for safety, how to make makeshift items to help, etc. Be generous with how much info you tell them. Don't keep these tips short. Make them at least a paragraph each and add examples. 
    Seperate each tip with a new line. Remember each category should be at least 10 sentences long. For example, don't say "plan an evacuation route", make it detailed about how you make a good evacuation plan. 
    This should be multiple paragraphs long. Remember to take into account the specific information about the user and factor that into your reponse and tips. 
    
    Format your response as a valid JSON object this means you cannot write new lines, instead of new lines you must use backslash n. like the following:

    concern: true or false value based on whether there are any emergencies to be worried about
    emergencies: a list of relevent emergencies to be worried about, their name and location listed
    summary: a short blurb about what's happening and what to know immidiately. this should only be a few words. Example : "WARNING! WILDFIRES NEARBY. VIEW THIS FOR MORE INFO". Alaways have VIEW THIS FOR MORE INFO part there.
    extended_info: the large amount of information the user should know described in other places in this prompt, formatted as a simple string.
    At the top of the extended information, have an emergency overview section. This will be formatted like this: a list of relevent dangerous to the user emergencies, with their status next to them, seperated by a new line. If status is unknown assume active status.Also include rational about how your location and its location is close enough to worry about
    Ensure each category has at least 10 sentences in it.
    be very strict about this formatting, have nothing else in your response besides this json object.title each paragraph with  **title**, and backslash n before and after it. remember to close the bracket.
    make sure you use quotes around the values of the json objecy and have a closing bracket at the end of the object
    have a 500 word limit
    """
    #make extra sure all newlines aren't actually new lines, and instead are backslash n. Don't have any backslashes by themselves.
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an emergency analysis assistant. Provide factual, helpful information about whether emergency events might impact a specific location."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3  # Lower temperature for more factual responses
    }

    try:
        print(f"Sending request to Groq API to analyze impact on {my_location}...")
        response = requests.post(API_URL, headers=headers, json=data)
        print("HELLO MAN")
        response.raise_for_status()
        print("here is the result:")
        result = response.json()
        # print(result)
        if 'choices' in result and len(result['choices']) > 0:
            analysis = result['choices'][0]['message']['content']

            # print(analysis)
            return analysis
        else:
            return f"Error: Unable to get a proper response from Groq API. Response: {result}"
            
    except requests.RequestException as e:
        return f"Error communicating with Groq API: {str(e)}"
    except json.JSONDecodeError:
        return f"Error parsing response from Groq API. Response was not valid JSON."
    except Exception as e:
        return f"Unexpected error during analysis: {str(e)}"

def get_users() -> list[dict]:
    cur = con.cursor()
    cur.execute("SELECT * FROM user")

    output = []
    for x in cur.fetchall():
        account = {
            "username": x[0],
            "phone_number": x[1],
            "email": x[2],
            "location": x[3],
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
def test_get_users():
    print(get_users())


