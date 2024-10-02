from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
import datetime

class Tree:
    # my_date = datetime.datetime.strptime("my date", "%b %d %Y %H:%M")
    this_db = "exam_schema"
    
    def __init__(self,data):
        self.id = data["id"]
        self.species = data["species"]
        self.location = data["location"]
        self.reason = data["reason"]
        self.date_planted = data["date_planted"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None
        
    @classmethod
    def create_tree(cls,data):
        query = "INSERT INTO trees (species, location, reason, date_planted, user_id) VALUES (%(species)s, %(location)s, %(reason)s, %(date_planted)s, %(user_id)s);"
        return connectToMySQL(cls.this_db).query_db(query,data)
    
    @staticmethod
    def validate_tree(tree_data):
        is_valid = True
        if len(tree_data["species"]) < 2:
            flash("Invalid species!")
            is_valid = False
        if len(tree_data["location"]) < 2:
            flash("Invalid location!")
            is_valid = False
        if len(tree_data["reason"]) < 8:
            flash("You need a better reason!")
            is_valid = False
        # if tree_data["created_at"] != tree_data["created_at"]:
        #     flash("Invalid Date!")
        #     is_valid = False
        
        return is_valid
    
    @classmethod
    def add_users_to_trees(cls):
        query = "SELECT * FROM trees JOIN users ON users.id = trees.user_id"
        results = connectToMySQL(cls.this_db).query_db(query)
        if len(results) == 0:
            return None
        else:
            all_trees = []
            for a_tree in results:
                tree_instance = cls(a_tree)
                dictionary = {
                    "id" : a_tree["user_id"],
                    "first_name" : a_tree["first_name"],
                    "last_name" : a_tree["last_name"],
                    "email" : a_tree["email"],
                    "password" : a_tree["password"],
                    "created_at" : a_tree["created_at"],
                    "updated_at" : a_tree["updated_at"]
                }
                planter = user.User(dictionary)
                tree_instance.user = planter
                all_trees.append(tree_instance)
            return all_trees
        
    @classmethod
    def get_one_tree(cls,data):
        query = "SELECT * FROM trees JOIN users ON users.id = trees.user_id WHERE trees.id = %(id)s;"
        results = connectToMySQL(cls.this_db).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            this_tree = cls(results[0])
            user_dictionary = {
                
                    "id" : results[0]["user_id"],
                    "first_name" : results[0]["first_name"],
                    "last_name" : results[0]["last_name"],
                    "email" : results[0]["email"],
                    "password" : results[0]["password"],
                    "created_at" : results[0]["created_at"],
                    "updated_at" : results[0]["updated_at"]
            }
            planter = user.User(user_dictionary)
            this_tree.user = planter
            return this_tree
        
    @classmethod
    def edit_tree(cls, data):
        query = "UPDATE trees SET species = %(species)s, location = %(location)s, reason = %(reason)s, date_planted = %(date_planted)s WHERE id = %(id)s;"
        return connectToMySQL(cls.this_db).query_db(query, data)
    
    @classmethod
    def delete_tree(cls, data):
        query = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL(cls.this_db).query_db(query, data)
            
    
    
        
    
    