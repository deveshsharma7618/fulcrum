from flask import render_template, Blueprint
from ...utils.blog.blog_utils import get_blog_by_slug, get_all_blogs

blog = Blueprint('blog', __name__)


@blog.route("/blog/<string:slug>")
def BlogPost(slug):
    from app import cursor

    blog = get_blog_by_slug(cursor, slug)
    if blog is None:
        return "Blog not found"
    print(blog)
    blog_data = {
        "title": blog[1],
        "creator_email": blog[2],
        "created_at": blog[3],
        "slug": blog[4],
        "content": blog[5]
    }
    return render_template("blog-post.html", blog=blog_data)



@blog.route("/blogs")
def BlogsPage():
    blogs = [
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        },
        {
            "title": "The Impact of Social Media on Mental Health",
            "description": "Exploring the correlation between social media usage and mental health issues among teenagers."
        }
    ]
    from app import cursor

    blogs_from_db = get_all_blogs(cursor)
    print(blogs_from_db)
    for blog in blogs_from_db:
        blogs.append({
            "title": blog[1],
            "description": blog[5]
        })
    
    return render_template("blogs.html", blogs=blogs)
