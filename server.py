from flask import Flask, render_template, request, redirect, url_for
import queries

app = Flask(__name__)


@app.get("/")
def index():
    data = queries.show_all_categories()
    return render_template("index.html", data=data)


@app.get("/category/<id>")
def category(id):
    details = queries.get_category_details(id)
    return render_template(
        "category.html",
        name=details.get("category_name"),
        description=details.get("description"),
    )


@app.get("/new")
def new_form():
    return render_template("new_cat.html")


@app.post("/new")
def add_new():
    category_name = request.form.get("category_name")
    description = request.form.get("description")
    id = queries.insert_new_category(category_name, description)
    return redirect(url_for("category", id=id.get("category_id")))


@app.get("/remove/<id>")
def remove(id):
    ics = queries.remove_category(id)
    print(ics)
    
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
