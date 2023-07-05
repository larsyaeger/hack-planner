# imports functionality into project, destructured import i think, just like javascript and react
from flask import Flask, render_template, request, redirect
import sqlite3

# i should probably lookup what flask is and the syntax
# routes in flask determine the url paths that the application can respond to. flask similar to reactrouter?
#                                                                              ^^^ "It basically does" -Stephen from MLH
# Views    in Flask, views are python functions that handle http requests and generate responses to be sent back to the client. Think GET, POST etc
app = Flask(__name__)

items = []
db_path = "checklist.db"


# C
def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS checklist (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)"""
    )
    conn.commit()
    conn.close()


# R
def get_items():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM checklist")
    items = c.fetchall()
    conn.close()
    return items


# U
def add_item(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO checklist (item) VALUES (?)", (item,))
    conn.commit()
    conn.close


def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
    conn.commit()
    conn.close()


# D
def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close


# basically if the user is in the home page, return checklist.html
# items=items passes in dynamic stuff
# .route defaults to GET, so method=["GET"] is implied and does not need to be specified like with POST
@app.route("/")
def checklist():
    create_table()
    items = get_items()
    return render_template("checklist.html", items=items)


# route
@app.route("/add", methods=["POST"])
# view function
def add():
    item = request.form["item"]
    add_item(item)
    # items.append(item)  # Append the new item to the list
    # # not store in database (yet)
    return redirect("/")


# update
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    # item = items[item_id - 1]  # Retrieve the item based on its index

    if request.method == "POST":
        new_item = request.form["item"]
        update_item(item_id, new_item)
        # items[item_id - 1] = new_item  # overwriting what used to be there
        return redirect("/")
    else:
        items = get_items()
        item = next((x[1] for x in items if x[0] == item_id), None)
    return render_template("edit.html", item=item, item_id=item_id)


# Delete
@app.route("/delete/<int:item_id>")
def delete(item_id):
    delete_item(item_id)
    # del items[item_id - 1]
    return redirect("/")
