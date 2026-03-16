from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import sessions, participants, interview, resume
from routes.evaluation import router as evaluation_router
from routes.auth import router as auth_router
from routes.form_candidates import router as form_router

app = FastAPI(
    title="AI Interview System",
    version="1.0"
)


# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sessions.router)
app.include_router(participants.router)
app.include_router(interview.router)
app.include_router(resume.router)
app.include_router(evaluation_router)
app.include_router(auth_router)
app.include_router(form_router)

@app.get("/")
def root():
    return {"message": "AI Interview Backend Running"}