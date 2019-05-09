from flask_login import UserMixin
from workout_tracker.database import Database


class User(UserMixin):
    def __init__(self, user_id, username, pw_hash, role):
        self.id = user_id
        self.username = username
        self.pw_hash = pw_hash
        self.role = role
    
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.role}')"
    
    def get_id(self):
        return int(self.id)
    
    @classmethod
    def get(cls, user_id):
        with Database() as conn:
            query = 'SELECT * FROM user_data WHERE id = :user_id'
            return conn.query(query, user_id=user_id).first()
