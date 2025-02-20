from datetime import datetime, timedelta
import random
from config import MINING_COOLDOWN, MIN_MINING_REWARD, MAX_MINING_REWARD, EQUIPMENT

def can_mine(last_mining):
    if last_mining is None:
        return True
    last_mining = datetime.fromisoformat(last_mining)
    return datetime.now() - last_mining > timedelta(seconds=MINING_COOLDOWN)

def calculate_mining_reward(equipment):
    base_reward = random.randint(MIN_MINING_REWARD, MAX_MINING_REWARD)
    bonus = sum(EQUIPMENT[item]['mining_bonus'] for item in equipment)
    return base_reward + bonus

def can_claim_daily(last_daily):
    if last_daily is None:
        return True
    last_daily = datetime.fromisoformat(last_daily)
    return datetime.now().date() > last_daily.date()

def format_time_until_next_mining(last_mining):
    if last_mining is None:
        return "şimdi"
    last_mining = datetime.fromisoformat(last_mining)
    next_mining = last_mining + timedelta(seconds=MINING_COOLDOWN)
    remaining = next_mining - datetime.now()
    if remaining.total_seconds() <= 0:
        return "şimdi"
    return f"{remaining.seconds} saniye"
