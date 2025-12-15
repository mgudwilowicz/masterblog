from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)


with open("data/data.json", "r", encoding="utf-8") as file:
    blog_posts = json.load(file)


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        id = blog_posts[-1]['id'] + 1
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_post = {"id": id, "title": title, "author": author, "content": content}
        blog_posts.append(new_post)
        with open("data/data.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4, ensure_ascii=False)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    global blog_posts
    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    with open("data/data.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4, ensure_ascii=False)

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)