from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

users_collection = db["users"]
sessions_collection = db["sessions"]
questions_collection = db["questions"]
participants_collection = db["participants"]
answers_collection = db["answers"]
evaluations_collection = db["evaluations"]

otp_collection = db["otp_codes"]
form_candidates_collection = db["form_candidates"]
interview_sessions_collection = db["interview_sessions"]