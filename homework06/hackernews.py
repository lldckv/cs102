from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


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
    bayes = NaiveBayesClassifier()
    classified = s.query(News).filter(News.label != None).all()
    x = [i.title for i in classified]
    y = [i.label for i in classified]
    bayes.fit(x, y)
    news = s.query(News).filter(News.label == None).all()[:3]
    X = [i.title if i.title is not None else "" for i in news]
    output = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = output[i]
    s.commit()
    classified_news = sorted(news, key=lambda x: x.label)
    return classified_news


@route("/recommend")
def recommend():
    classified_news = classify_news()
    return template("news_recommendations", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
