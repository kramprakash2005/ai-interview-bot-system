from pymongo import MongoClient
from services.evaluation_service import evaluate_interview

# -----------------------
# MongoDB Connection
# -----------------------
client = MongoClient("mongodb://localhost:27017")

db = client["ai_interview_db"]   # change if your DB name is different

participants_collection = db["participants"]


# -----------------------
# Participant to Test
# -----------------------
participant_id = "572ef1ad-a218-4311-9bbb-29e27889f8c2"


# -----------------------
# Fetch Participant
# -----------------------
participant = participants_collection.find_one({"_id": participant_id})

if not participant:
    print("Participant not found")
    exit()


answers = participant.get("answers", [])

if not answers:
    print("No answers found")
    exit()


print("\nRunning Evaluation...\n")


# -----------------------
# Run Evaluation
# -----------------------
evaluation = evaluate_interview(answers)


# -----------------------
# Print Results
# -----------------------
print("Evaluation Result\n")
print("-------------------------")

for key, value in evaluation.items():
    print(f"{key} : {value}")


# -----------------------
# Save to MongoDB
# -----------------------
participants_collection.update_one(
    {"_id": participant_id},
    {"$set": {"evaluation": evaluation}}
)

print("\nEvaluation stored in MongoDB")