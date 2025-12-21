from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)

with open("data/data.json", "r", encoding="utf-8") as file:
    blog_posts = json.load(file)


@app.route('/')
def index():
    """Show all blog posts on the homepage."""
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        new_id = blog_posts[-1]['id'] + 1
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_post = {"id": new_id, "title": title, "author": author, "content": content}
        blog_posts.append(new_post)
        with open("data/data.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4, ensure_ascii=False)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by ID."""
    blog_posts = delete_post(post_id)

    with open("data/data.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4, ensure_ascii=False)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update a blog post by ID."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        for post in blog_posts:
            if post['id'] == post_id:
                post['title'] = title
                post['author'] = author
                post['content'] = content

        with open("data/data.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file, indent=4, ensure_ascii=False)

        return redirect('/')

    return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """Return a blog post by ID or None if not found."""
    post = [post for post in blog_posts if post["id"] == post_id]
    if post:
        return post[0]
    return None

def delete_post(id):
    return [post for post in blog_posts if post["id"] != id]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
