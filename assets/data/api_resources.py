from flask import jsonify
from flask_restful import abort, Resource
from werkzeug.security import check_password_hash

from . import db_session
from .users import *
from .news import *
from .game_data import *
from .api_reqparsers import *


def abort_if_account_not_found(username):
    session = db_session.create_session()
    account = session.query(User).filter(User.name == username)
    if not account:
        abort(404, message=f"Account named <{username}> not found")


class LoginResource(Resource):
    def get(self):
        args = notxonix_login_parser.parse_args()
        abort_if_account_not_found(args['username'])
        session = db_session.create_session()

        accid = session.query(UserIdentifier).get(args['username']).userid
        acc = session.query(User).get(accid)
        res = '1' if check_password_hash(acc.hashed_password, args['pwdhash']) else '0'
        return jsonify(res)


class NotxonixResource(Resource):
    def get(self):
        args = notxonix_get_parser.parse_args()
        abort_if_account_not_found(args['username'])
        session = db_session.create_session()
        id = session.query(UserIdentifier).get(args['username']).userid
        acc = session.query(User).get(id)
        if check_password_hash(acc.hashed_password, args['pwdhash']):
            nxdata = session.query(NotxonixData).get(acc.id)
            res = {
                'LB': nxdata.LB,
                'WB': nxdata.WB,
                'MainB': nxdata.MainB,
                'Money': nxdata.Money,
                'MexB': nxdata.MexB,
                'Skin': nxdata.Skin,
                'ShrekB': nxdata.ShrekB,
                'Main': nxdata.Main,
                'Loki': nxdata.Loki,
                'Warrior': nxdata.Warrior,
                'Mexicanes': nxdata.Mexicanes,
                'Shrek': nxdata.Shrek,
                'SkinCount': nxdata.SkinCount
            }
            return jsonify(res)
        else:
            abort(403, message=f'Wrong password')

    def post(self):
        args = notxonix_post_parser.parse_args()
        abort_if_account_not_found(args['username'])
        session = db_session.create_session()
        id = session.query(UserIdentifier).get(args['username']).userid
        acc = session.query(User).get(id)
        if check_password_hash(acc.hashed_password, args['pwdhash']):
            data = args['data']
            nxdata = NotxonixData(
                user_id=id,
                LB=data['LB'],
                WB=data['WB'],
                MainB=data['MainB'],
                Money=data['Money'],
                MexB=data['MexB'],
                Skin=data['Skin'],
                ShrekB=data['ShrekB'],
                Main=data['Main'],
                Loki=data['Loki'],
                Warrior=data['Warrior'],
                Mexicanes=data['Mexicanes'],
                Shrek=data['Shrek'],
                SkinCount=data['SkinCount']
            )
            session.add(nxdata)
            session.commit()
            return jsonify(True)
        else:
            abort(403, message=f'Wrong password')