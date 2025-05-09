from flask_restful import reqparse


notxonix_login_parser = reqparse.RequestParser()
notxonix_login_parser.add_argument('username', required=True, type=str)
notxonix_login_parser.add_argument('pwdhash', required=True, type=str)

notxonix_get_parser = reqparse.RequestParser()
notxonix_get_parser.add_argument('username', required=True, type=str)
notxonix_get_parser.add_argument('pwdhash', required=True, type=str)

notxonix_post_parser = reqparse.RequestParser()
notxonix_post_parser.add_argument('username', required=True, type=str)
notxonix_post_parser.add_argument('pwdhash', required=True, type=str)
notxonix_post_parser.add_argument('data', required=True, type=dict)