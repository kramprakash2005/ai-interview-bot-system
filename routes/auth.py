import random
import string
from fastapi import APIRouter, HTTPException

from database.db import users_collection, otp_collection
from models.user_model import (
    RegisterRequest,
    LoginRequest,
    OTPVerifyRequest
)
from services.email_service import send_otp_email

from utils.jwt_handler import create_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- REGISTER ----------------

@router.post("/register")
def register(data: RegisterRequest):

    existing = users_collection.find_one(
        {"email": data.email}
    )

    if existing:
        raise HTTPException(400, "User exists")

    user = {
        "name": data.name,
        "email": data.email,
        "password": data.password,
        "role": data.role,
        "organization": data.organization
    }

    users_collection.insert_one(user)

    return {"ok": True}


# ---------------- SEND OTP ----------------

@router.post("/send_otp")
def send_otp(data: LoginRequest):

    user = users_collection.find_one(
        {"email": data.email}
    )

    if not user:
        raise HTTPException(400, "User not found")

    if user["password"] != data.password:
        raise HTTPException(400, "Wrong password")

    otp = "".join(
        random.choices(string.digits, k=6)
    )

    otp_collection.update_one(
        {"email": data.email},
        {"$set": {"otp": otp}},
        upsert=True
    )

    print("OTP:", otp)
    #send_otp_email(data.email, otp)

    return {"ok": True}


# ---------------- VERIFY OTP ----------------

@router.post("/verify_otp")
def verify_otp(data: OTPVerifyRequest):

    record = otp_collection.find_one(
        {"email": data.email}
    )

    if not record:
        raise HTTPException(400, "OTP not found")

    if record["otp"] != data.otp:
        raise HTTPException(400, "Invalid OTP")

    token = create_token({
        "email": data.email
    })

    return {
        "access_token": token
    }