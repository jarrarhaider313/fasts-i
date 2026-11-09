from pydantic import BaseModel, ConfigDict


class users(BaseModel):
    name: str
    password: str


class tasks(BaseModel):
    title: str
    description: str


class userresponse(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class taskresponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str
