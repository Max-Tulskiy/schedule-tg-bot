import os
from dotenv import load_dotenv

load_dotenv()

schedule_even_name = "schedule_even.csv"
schedule_odd_name = "schedule_odd.csv"

try:
    TOKEN = os.getenv("TG_API_TOKEN")
except:
    raise ValueError("Token not found")
