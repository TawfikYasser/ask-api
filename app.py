import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route('/getallstores')
def get_stores():
    stores = []
    conn = sqlite3.connect('Storedb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM stores_table")
    rows = cur.fetchall()
    for i in rows:
        store = {}
        store["id"] = i[0]
        store["name"] = i[1]
        store["description"] = i[2]
        store["lat"] = i[4]
        store["lng"] = i[3]
        store["imgpath"] = i[5]
        stores.append(store)
    conn.close()
    # convert row objects to dictionary
    return jsonify(stores)

@app.route('/getfavstores',methods=['GET'])
def get_fav_stores():
    id = request.args.get("id")
    stores = []
    conn = sqlite3.connect('Storedb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM favstores_table WHERE UserId=?",[id])
    rows = cur.fetchall()
    if rows==None:
        conn.close()
        return "No Favorite stores for this user"
    else:
        for i in rows:
            store = {}
            cur.execute("SELECT * FROM stores_table WHERE Id=?",[i[0]])
            resul=cur.fetchall()
            for t in resul:
                store["id"] = t[0]
                store["name"] = t[1]
                store["description"] = t[2]
                store["lat"] = t[4]
                store["lng"] = t[3]
                store["imgpath"] = t[5]
                stores.append(store)
        conn.close()
        return jsonify(stores)

    # convert row objects to dictionary

if __name__ == "__main__":
    app.run(debug=True)
