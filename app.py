# imports functionality into project, destructured import i think, just like javascript and react
from flask import Flask, render_template, request, redirect

# i should probably lookup what flask is and the syntax
# routes in flask determine the url paths that the application can respond to. flask similar to reactrouter?
#                                                                              ^^^ "It basically does" -Stephen from MLH
# Views    in Flask, views are python functions that handle http requests and generate responses to be sent back to the client. Think GET, POST etc
app = Flask(__name__)

items = []


# basically if the user is in the home page, return checklist.html
# items=items passes in dynamic stuff
# .route defaults to GET, so method=["GET"] is implied and does not need to be specified like with POST
@app.route("/")
def checklist():
    return render_template("checklist.html", items=items)


# route
@app.route("/add", methods=["POST"])
# view function
def add_item():
    item = request.form["item"]
    items.append(item)  # Append the new item to the list
    # not store in database (yet)
    return redirect("/")


# update
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = items[item_id - 1]  # Retrieve the item based on its index

    if request.method == "POST":
        new_item = request.form["item"]
        items[item_id - 1] = new_item  # overwriting what used to be there
        return redirect("/")
    return render_template("edit.html", item=item, item_id=item_id)


# Delete
@app.route("/delete/<int:item_id>")
def delete_item(item_id):
    del items[item_id - 1]
    return redirect("/")
