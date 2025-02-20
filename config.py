import os
from dotenv import load_dotenv

load_dotenv()

# Bot token should be set in Railway.com environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Game constants
MINING_COOLDOWN = 60  # seconds
DAILY_BONUS = 100
REFERRAL_BONUS = 50

# Equipment costs
EQUIPMENT = {
    'drill': {
        'cost': 250,
        'mining_bonus': 20
    },
    'pickaxe': {
        'cost': 100,
        'mining_bonus': 10
    }
}

# Mining rewards
MIN_MINING_REWARD = 5
MAX_MINING_REWARD = 15
