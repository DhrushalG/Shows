from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Like:
    def __init__(self, data):
        self.users_id = data['users_id']
        self.shows_id = data['shows_id']

    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes(users_id, shows_id) SELECT %(users_id)s, %(shows_id)s WHERE  NOT EXISTS (SELECT * FROM likes WHERE users_id = %(users_id)s and shows_id = %(shows_id)s);"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result

    @classmethod
    def delete_like(cls,data):
        query = "DELETE FROM likes WHERE users_id= %(users_id)s AND shows_id= %(shows_id)s;"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result