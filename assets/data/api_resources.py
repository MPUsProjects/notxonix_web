from flask import jsonify
from flask_restful import abort, Resource

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
        acc = session.query(User).filter(User.name == args['username']).first()
        return jsonify(args['pwdhash'] == acc.hashed_password)


class NotxonixResource(Resource):
    def get(self):
        args = notxonix_get_parser.parse_args()
        abort_if_account_not_found(args['username'])
        session = db_session.create_session()
        acc = session.query(User).filter(User.name == args['username']).first()
        if args['pwdhash'] == acc.hashed_password:
            return jsonify(session.query(NotxonixData).get(acc.id))
        else:
            abort(403, message=f'Wrong password')

    def post(self):
        args = notxonix_post_parser.parse_args()
        abort_if_account_not_found(args['username'])
        session = db_session.create_session()
        acc = session.query(User).filter(User.name == args['username']).first()
        if args['pwdhash'] == acc.hashed_password:
            data = args['data']
            nxdata = NotxonixData(
                logged_in=data['logged_in'],
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