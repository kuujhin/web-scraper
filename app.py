from flask import Flask, render_template, request, redirect, send_file
from file import save_to_file, keyword_db
from scraper import scrape, rescrape
from db import get_from_db, search_file

app = Flask(__name__)


@app.route("/")
def home():
    get_from_db()
    file_list = search_file()
    return render_template("home.html", name="jhin", files=file_list)


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    site = request.args.get("site")

    if keyword == None:
        return redirect("/")

    jobs = scrape(keyword, site)

    if jobs == []:
        return render_template(f"search_empty.html", keyword=keyword, site=site)
    else:
        return render_template(f"search.html", keyword=keyword, site=site, jobs=jobs)


@app.route("/update")
def update():
    keyword = request.args.get("keyword")
    site = request.args.get("site")

    if keyword == None:
        return redirect("/")

    jobs = rescrape(keyword, site)

    return render_template(f"search.html", keyword=keyword, site=site, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    site = request.args.get("site")

    if keyword == None:
        return redirect("/")

    db = keyword_db(site)

    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    save_to_file(keyword, site, db[keyword])

    return send_file(f"./file/{keyword}_{site}.csv", as_attachment=True)


@app.route("/updates")
def updates():

    return render_template("updates.html")


app.run("0.0.0.0", debug=True)
