import json
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.data = self._load_data()
        logger.info("Database initialized")

    def _load_data(self):
        try:
            if os.path.exists('data.json'):
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info("Existing database loaded successfully")
                    return data
            logger.info("Creating new database")
            return {'users': {}}
        except Exception as e:
            logger.error(f"Error loading database: {e}")
            return {'users': {}}

    def _save_data(self):
        try:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
                logger.info("Database saved successfully")
        except Exception as e:
            logger.error(f"Error saving database: {e}")

    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data['users']:
            logger.info(f"Creating new user: {user_id}")
            self.data['users'][user_id] = {
                'coins': 50,
                'equipment': [],
                'last_mining': None,
                'last_daily': None,
                'referrals': [],
                'referred_by': None
            }
            self._save_data()
        return self.data['users'][user_id]

    def update_user(self, user_id, data):
        self.data['users'][str(user_id)] = data
        self._save_data()

    def add_coins(self, user_id, amount):
        user = self.get_user(user_id)
        user['coins'] += amount
        self._save_data()
        return user['coins']

    def remove_coins(self, user_id, amount):
        user = self.get_user(user_id)
        if user['coins'] >= amount:
            user['coins'] -= amount
            self._save_data()
            return True
        return False

    def add_equipment(self, user_id, equipment):
        user = self.get_user(user_id)
        if equipment not in user['equipment']:
            user['equipment'].append(equipment)
            self._save_data()

    def get_top_miners(self, limit=10):
        users = self.data['users'].items()
        sorted_users = sorted(users, key=lambda x: x[1]['coins'], reverse=True)
        return sorted_users[:limit]

    def add_referral(self, user_id, referrer_id):
        user = self.get_user(user_id)
        referrer = self.get_user(referrer_id)

        if user_id != referrer_id and user['referred_by'] is None:
            user['referred_by'] = str(referrer_id)
            referrer['referrals'].append(str(user_id))
            self._save_data()
            return True
        return False