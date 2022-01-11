from ws_app.model.models import Users
from ws_app.model.models import Socnet

a = {
    "nickname": "TestUser01",
    "name": "Юзер Юзеров Юзерович",
    "password": "mc451b84dab4fe148ba887bebf65fe2dd",
    "mail1": "TestUser",
    "phone1": "1234567",
    "socnet": [
        {
            "vk": "testVK",
            "fb": "",
            "insta": "",
            "telegram": "",
            "user_id": 19
        }
    ]
}

print(a)
u = Users.from_json(a)
print(u.password)