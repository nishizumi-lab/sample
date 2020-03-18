from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='RSS')


@app.route('/rss', methods=['POST'])
def rss():
    url = request.form['rss_url']
    dictionary = feedparser.parse(url)
    import json
    return json.dumps(dictionary.entries)


if __name__ == "__main__":
    app.run()
