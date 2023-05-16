import sqlite3

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    response_id = request.params.get("id")
    response_label = request.params.get("label")
    if s.query(News).filter(News.id == response_id) is not None:
        s.query(News).filter(News.id == response_id).update({"label": response_label})
        s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()

    rows = get_news("https://news.ycombinator.com/", 2)

    for row in rows:
        if len(s.query(News).filter(News.title == row["title"] and News.author == row["author"]).all()) == 0:
            s.add(
                News(
                    title=row["title"],
                    author=row["author"],
                    url=row["url"],
                    comments=row["comments"],
                    points=row["points"],
                    label=None,
                )
            )
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classified = s.query(News).filter(News.label != None).all()
    p = [i.title if i.title is not None else "" for i in classified]
    z = [
        p[i] + " " + classified[i].author if classified[i].author is not None else p[i] for i in range(len(classified))
    ]
    y = [i.label for i in classified]

    model = NaiveBayesClassifier()
    model.fit(z, y)
    unclassified = s.query(News).filter(News.label == None).all()
    rows = unclassified[:10]
    new_rows = []
    for row in rows:
        t = (lambda x: x if x is not None else "")(row.title)
        a = (lambda x: x if x is not None else "")(row.author)
        output = model.predict([t + " " + a])
        s.query(News).filter(News.id == row.id).update({"label": output[0]})
        new_rows.append(row)

    s.commit()
    # sorted_list = sorted(new_rows, key=lambda x: x.label)
    sorted_list = sorted([row for row in new_rows if row.label is not None], key=lambda x: x.label)
    return template("news_recommendations", rows=sorted_list)


if __name__ == "__main__":
    run(host="localhost", port=8080)
