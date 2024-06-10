import json
from pydantic import BaseModel
from typing import List

class JsonManager:
    def __init__(self, path = "database.json"):
        self.path = path

    def load(self, path: str | None = None) -> dict:
        path = path if path else self.path
        _data = {}
        try:
            with open(path) as fp:
                _data = json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(path, "w") as fp:
                json.dump(_data, fp)
                fp.close()
        return _data
    
    def save(self, _data: dict | BaseModel, path: str | None = None) -> None:
        _data = _data if isinstance(_data, dict) else _data.model_dump()
        try:
            with open(path, "w") as fp:
                json.dump(_data, fp)
        except Exception as e:
            print(f"ERROR :: <{e}> :: <JsonManager.save>")

class User(BaseModel):
    userid: int
    phonenumber: str
    gmail: str
    name: str
    sessionid: str
    images: List[str]

class UserManager:
    def __init__(self) -> None:
        self.jm = JsonManager()
    
    def save_user(self, user: User) -> None:
        data = self.jm.load()
        userid = data.get('userid', None)
        data[userid] = user.model_dump() if not userid else data[userid]
        self.jm.save(data)
    
    def get_user(self, user: User) -> User | None:
        data = self.jm.load()
        rawUser = data.get(user.userid, None)
        return user.model_construct(rawUser) if rawUser else None