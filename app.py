from flask import Flask, render_template, json
import json

app = Flask(__name__)


with open("data/data.json", "r", encoding="utf-8") as file:
    blog_posts = json.load(file)


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)