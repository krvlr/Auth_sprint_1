from pydantic import BaseModel, Field, EmailStr, validator, UUID4


class SignupRq(BaseModel):
    login: str = Field(..., title="Login")
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., title="Password", min_length=6, max_length=72)

    @validator("login")
    def login_alphanumeric(cls, v):
        assert v.isalnum(), "Должен содержать числа и буквенные символы"
        return v


class UserDataRs(BaseModel):
    id: UUID4 = Field(..., title="Id")
    login: str = Field(..., title="Login")
    email: EmailStr = Field(..., title="Email")
