from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import like

class Show:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.user = None
        self.favorites = []

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows JOIN users ON users.id = shows.user_id;"
        results = connectToMySQL('exam1_schema').query_db(query)
        shows = []
        for item in results:
            new_show = cls(item)
            new_user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at'],
            }
            new_user = user.User(new_user_data)
            new_show.user = new_user
            shows.append(new_show)

        return shows

    @classmethod
    def create_new_show(self, data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES(%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s);"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result
    
    
    @staticmethod
    def validate_show(data):
        is_valid = True

        if len(data['title']) < 3:
            is_valid = False
            flash("Show name needs to be greater than 3 characters")

        if len(data['network']) < 3:
            is_valid = False
            flash("Show network needs to be greater than 3 characters")
        
        if len(data['release_date']) != 10:
            is_valid = False
            flash("Please insure theres is a release date")

        if len(data['description']) < 3:
            is_valid = False
            flash("Show description needs to be greater than 3 characters")

        return is_valid

    @classmethod
    def view_description(cls, data):
        query = "SELECT * FROM shows LEFT JOIN likes ON likes.shows_id = shows.id LEFT JOIN users ON users.id = likes.users_id WHERE shows.id = %(shows_id)s;"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        single_show = cls(result[0])
        for row in result:
            if['users_id'] != None:
                new_user_data = { 
                    'id' : row['user_id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'password' : row['password'],
                    'email' : row['email'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
            new_user = user.User(new_user_data)
            single_show.favorites.append(new_user)

        return single_show

    @classmethod
    def update_show(cls,data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE shows.id = %(id)s;"
        connectToMySQL('exam1_schema').query_db(query, data)
        
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        connectToMySQL('exam1_schema').query_db(query, data)

    @classmethod
    def get_show_creator(cls, data):
        query = 'SELECT * FROM users LEFT JOIN shows ON shows.user_id = users.id WHERE shows.id = %(shows_id)s;'
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_creator_likes(cls, data):
        query = 'SELECT * FROM shows JOIN likes ON likes.shows_id = shows.id JOIN users ON users.id = likes.users_id WHERE users.id = %(user_id)s;'
        result = connectToMySQL('exam1_schema').query_db(query, data)
        single_like = []
        for row in result:
            if['users_id'] != None:
                new_like_data = {
                    'users_id' : row['users_id'],
                    'shows_id' : row['shows_id']
                }
            new_like = like.Like(new_like_data)
            single_like.append(new_like)

        return single_like

    @classmethod
    def get_other_shows(cls, data):
        query='SELECT * FROM shows WHERE shows.id NOT IN (SELECT likes.shows_id FROM likes WHERE likes.users_id = %(user_id)s);'
        result = connectToMySQL('exam1_schema').query_db(query, data)
        shows = []
        for row in result:
            data = {
                'id' : row['id']
            }
            shows.append(data)

        return shows
