from flask import Flask, render_template, g, request, redirect, url_for
import csv;
import os;
import random;
import os
from dotenv import load_dotenv
from pymongo import MongoClient, server_api
import certifi, datetime


load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
db_name = os.getenv('MONGO_DBNAME')

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), server_api=server_api.ServerApi('1'))
db = client[db_name]
users_collection = db.users
ratings_collection = db.ratings
# mongo = PyMongo(app)

def create_user(username, password):
    user = {
        "username": username,
        "password": password,  # Maybe hash this?
        "daily_movie":{
            "movie_id": random.randint(1,1000),
            "recommended_date": datetime.datetime.now()
        },
        "watched_movies": []
    }
    return user

def random_movie_id(watched_ids):
    id = 0;
    while True:
        id = random.randint(1,1000)
        if id not in watched_ids:
            break
    return id

# Runs before requests - reads csv file and puts each row into all_movies variable
@app.before_request
def read_movies():
    g.all_movies = []
    with open(os.path.join(os.path.dirname(__file__), 'input/imdb_top_1000.csv'), 'r') as file:
       csv_reader = csv.reader(file)
       for row in csv_reader:
          g.all_movies.append(row)

@app.route('/')
def index():

    # user = create_user('WilliamTest2','unhashedpass')
    # users_collection.insert_one(user);
    # mongo.db.users.insert_one(user)

    # TODO: This will have to change to find the user that is logged in, hardcoded for now to test
    selected_user = users_collection.find_one({"username":"WilliamTest2"})

    # print("User's date: " + selected_user["daily_movie"]["recommended_date"].strftime("%Y %m %d"))
    # print("Computer's date: " + datetime.datetime.now().strftime("%Y %m %d"))
    # print("Equal?: "+ str(selected_user["daily_movie"]["recommended_date"] == datetime.datetime.now()))

    # Checks if movie has been assigned for the day if last recommended movie date is same as today
    user_movie_id = selected_user["daily_movie"]["movie_id"]
    user_recommended_date = selected_user["daily_movie"]["recommended_date"]
    
    is_already_assigned = user_recommended_date.strftime("%Y %m %d") == datetime.datetime.now().strftime("%Y %m %d")

    # # For testing: to forcefully update movie even if date hasn't changed
    # is_already_assigned = False

    # if movie hasn't been assigned for the day, set a new movie that user hasn't seen before
    if not is_already_assigned:
        new_movie_id = random_movie_id(selected_user["watched_movies"])
        users_collection.update_one(
            {"username":"WilliamTest2"},    # TODO: replace username with actual user logged in
            { 
                "$set": {
                    "daily_movie.movie_id": new_movie_id,
                    "daily_movie.recommended_date": datetime.datetime.now()
                }
            }
        )
        selected_movie = g.all_movies[new_movie_id] # uses newly generated movie id
        movie_id = new_movie_id

    # if move has been assigned
    else:
        selected_movie = g.all_movies[user_movie_id] # uses existing movie id found in user doc in db
        movie_id = user_movie_id

    return render_template("index.html", selectedMovie=selected_movie, movieId=movie_id)

@app.route('/setwatched', methods=["POST"])
def setWatched():
    user = users_collection.find_one({"username":"WilliamTest2"})
    has_watched = eval(request.form['hasWatched'])
    movie_id = int(request.form['movieId'])

    print(has_watched)

    if has_watched is True:
        # ratings_collection.update_one(
        #     {
        #         "user": user["_id"],
        #         "movie_id": movie_id
        #     },
        #     {
        #         "$set": {
        #             "user": user["_id"],
        #             "movie_id": movie_id,
        #             "date_watched": datetime.datetime.now()
        #         }
        #     }
        # )
        ratings_collection.insert_one(
            {
                "user": user["_id"],
                "movie_id": movie_id,
                "date_watched": datetime.datetime.now()
            }
        )
    
    # if they unclick the watched button
    else:
        ratings_collection.delete_one({
            "user": user["_id"],
            "movie_id": movie_id
        })
    # return redirect(url_for("index", userId=user["_id"], selectedMovie=g.all_movies[movie_id], movieId=movie_id))
    

@app.route('/update', methods=["POST"])
def updateWatched():
    user = "WilliamTest2"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)