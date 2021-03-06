from flask import current_app
from licsber import get_mongo

from wx.receive import Msg


class MsgLogger:
    def __init__(self):
        db = get_mongo(current_app.config['MONGO_PASSWD_B64'])
        self._db = db['xinshou_msg_log']

    def log(self, m: Msg):
        d = m.to_dict()
        self._db.insert_one(d)
