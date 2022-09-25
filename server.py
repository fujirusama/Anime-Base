from flask import Flask, Response, request
import pymongo
from bson import json_util, ObjectId
import json

app = Flask(__name__)

#connexion avec mongodb compass
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() #déclancher l'execpection si nous ne pouvons pas nous connecter à la base de donnée
except:     
    print("ERROR - Cannot connect to data base")

#recuperation des données de tous les anime
@app.route('/getAllAnime', methods=["GET"])
def get_all_anime():
    try:
        data = list(db.anime_list.find())
        print(data)
        page_sanitized = json.loads(json_util.dumps(data))
        return page_sanitized
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps(
                {"message": "anime list cannot found"}
            ),
            status=500,
            mimetype="application/json"
        )
#recuperation des données d'un anime précis grace à son ObjectId
@app.route('/getAnime/<id>', methods=["GET"])
def get_anime(id):
    try:
        data = db.anime_list.find_one(
            {"_id":ObjectId(id)}
        )
        page_sanitized = json.loads(json_util.dumps(data))
        return page_sanitized
        
    except Exception as ex: 
        print("****************************")
        print(ex) 
        print("****************************") 
        return Response( 
            response= json.dumps( 
                {"message": "anime name cannot found"} 
            ), 
            status=500,
            mimetype="application/json"
        )

#ajout d'un animé dans la base de donnée
@app.route("/postAnime", methods=["POST"])
def add_anime():
    try:
        anime = {"name":"Demon Slayer",
                 "description":"Tanjiro Kamado is a kind-hearted and intelligent boy who lives with his family in the mountains. He became his family's breadwinner after his father's death, making trips to the nearby village to sell charcoal. Everything changed when he came home one day to discover that his family was attacked and slaughtered by a demon. Tanjiro and his sister Nezuko were the sole survivors of the incident, with Nezuko being transformed into a demon, but still surprisingly showing signs of human emotion and thought", 
                 "Rating": 8.53, "episode": 26,
                 "studio": "Ufotable","img":"https://cdn.myanimelist.net/images/anime/1286/99889.jpg"}
        dbResponse = db.anime_list.insert_one(anime)
        print(dbResponse.inserted_id)
        return Response(
            response= json.dumps(
                  {"message": "Anime added sucessfull"},
            ),
            status=200,
            mimetype="application/json"
        )  
    except Exception as ex:
        print("****************************")
        print(ex) 
        print("****************************") 
        return Response(
            response= json.dumps(
                {"message": "cannot add this anime"}
            ),
            status=500,
            mimetype="application/json"
        )

#mise à  jour d'un anime bien précis grace à son ObjectId
@app.route("/patchAnime/<id>", methods=["PATCH"])
def update_anime(id):
    try:
        dbResponse = db.anime_list.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":"Viland Sa",
                 "description":"In 10 AD, the young Thorfinn works for Askeladd in the hopes of challenging to a duel and kill him in revenge for his father's death in 1002 AD when they were attacked by him on a journey to England. Askeladd's company found employment in 1013 AD as mercenaries under the Danish King Sweyn in the Danish invasion of London by the British and Thorkell the Tall, Thorfinn's fight-loving uncle who served with Thors in the Jomsvikings. When Thorkel takes Sweyn’s son Prince Canute captive, Askeladd's company capture the prince with the intent of selling him to either side for a profit. Askeladd changes his plan to act on his personal agenda as a descendant of Artorius to secure his mother's homeland of Wales from being invaded. While Askeladd succeeds in making Canute assertive, he learned that Sweyn intended for his son to die so that his oldest son Harald would succeed him and prevent a schism among the Danes.", 
                 "Rating": 8.3, "episode": 2,
                 "studio": "wit Stuio","img":"https://cdn.myanimelist.net/images/anime/1500/103005.jpg"}}
        )
        return Response(
            response= json.dumps(
                {"message": "Anime updated sucessfull"}
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*********************")
        print(ex)
        print("*********************")
        return Response(
        response= json.dumps(
                {"message": "cannot update this anime"}
            ),
            status=500,
            mimetype="application/json"
        )

#supression d'un animé grace à son ObjectId
@app.route("/delAnime/<id>", methods=["DELETE"])
def delete_anime(id):
    try:
        dbResponse = db.anime_list.delete_one(
            {"_id":ObjectId(id)}
        )
        return Response(
            response= json.dumps(
                {"message": "Anime deleted sucessfull"}
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("*********************")
        print(ex)
        print("*********************")
        return Response(
        response= json.dumps(
                {"message": "cannot delete this anime"}
            ),
            status=500,
            mimetype="application/json"
        )

if __name__ == "__main__":
	app.run(port=80, debug=True)