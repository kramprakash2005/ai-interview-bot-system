from pydantic import BaseModel


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str
    organization: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class OTPVerifyRequest(BaseModel):
    email: str
    otp: str