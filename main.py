from fastapi import FastAPI
from routes import sessions, participants, interview, resume

app = FastAPI(
    title="AI Interview System",
    version="1.0"
)

app.include_router(sessions.router)
app.include_router(participants.router)
app.include_router(interview.router)
app.include_router(resume.router)

@app.get("/")
def root():
    return {"message": "AI Interview Backend Running"}