import bybit
import os
from dotenv import load_dotenv

# Load API credentials from environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


# Connect to Bybit API
client = bybit.bybit(test=True, api_key=api_key, api_secret=api_secret)
