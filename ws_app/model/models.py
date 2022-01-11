from ws_app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(100), unique=True)
    mail1 = db.Column(db.String(50))
    mail2 = db.Column(db.String(50))
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    password = db.Column(db.String(200))
    active = db.Column(db.Boolean("active"))
    reg_date = db.Column(db.BigInteger)
    ver_mail = db.Column(db.Boolean("ver_mail"))
    ver_phone = db.Column(db.Boolean("ver_phone"))
    delete_date = db.Column(db.BigInteger)
    socnet = relationship("Socnet")
    pics = relationship('Pic')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'nickname': self.nickname,
            'mail1': self.mail1,
            'mail2': self.mail2,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'password': self.password,
            'active': self.active,
            'reg_date': self.reg_date,
            'ver_mail': self.ver_mail,
            'ver_phone': self.ver_phone,
            'delete_date': self.delete_date,
            'socnet': [s.to_dict() for s in self.socnet],
            'pics': [p.to_dict() for p in self.pics]
        }

    @staticmethod
    def from_json(json):
        return Users(
            user_id=json.get('user_id', None),
            name=json.get('name', None),
            nickname=json.get('nickname', None),
            mail1=json.get('mail1', None),
            mail2=json.get('mail2', None),
            phone1=json.get('phone1', None),
            phone2=json.get('phone2', None),
            password=json.get('password', None),
            active=json.get('active', True),
            reg_date=json.get('reg_date', None),
            ver_mail=json.get('ver_mail', False),
            ver_phone=json.get('ver_phone', False),
            delete_date=json.get('delete_date', '0'),
            socnet=[],
            pics=[])


class Socnet(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), primary_key=True)
    vk = db.Column(db.String(20))
    fb = db.Column(db.String(20))
    insta = db.Column(db.String(20))
    telegram = db.Column(db.String(20))
    youtube = db.Column(db.String(20))
    linkedin = db.Column(db.String(20))
    ok = db.Column(db.String(20))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'vk': self.vk,
            'fb': self.fb,
            'insta': self.insta,
            'telegram': self.telegram,
            'youtube': self.youtube,
            'linkedin': self.linkedin,
            'ok': self.ok,
        }

    @staticmethod
    def from_json(json):
        return Socnet(
            user_id=json.get('user_id', None),
            vk=json.get('vk', None),
            fb=json.get('fb', None),
            insta=json.get('insta', None),
            telegram=json.get('telegram', None),
            youtube=json.get('youtube', None),
            linkedin=json.get('linkedin', None),
            ok=json.get('ok', None))


class Pic(db.Model):
    pic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    filepath = db.Column(db.String(200))
    ava = db.Column(db.Boolean("ava"))

    def to_dict(self):
        return {
            'pic_id': self.pic_id,
            'user_id': self.user_id,
            'filepath': self.filepath,
            'ava': self.ava
        }

    @staticmethod
    def from_json(json):
        return Pic(
            pic_id=json.get('pic_id', None),
            user_id=json.get('user_id', None),
            filepath=json.get('filepath', None),
            ava=json.get('ava', False),
        )
