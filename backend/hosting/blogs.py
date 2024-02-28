from backend.config import *
from backend.forms.__init__ import *
from backend.ai.text_completion import *
from backend.authentication.user import User
from django.core.paginator import Paginator
from backend.blog.blog import Blog
from backend.blog.comments import Comments
from backend.social.social import Social
from backend.ai.spell_correction import *
from backend.blog.rating import Rating
from backend.ai.text_generation_model.main import *
# from backend.ai.falcon_7B.model import *
from backend.db import *

blog = Blueprint('blog', __name__)

TITLE = 'Ambrose Treacy College'

@blog.route('/blog', methods=['GET', 'POST'])
def blogs(): 
    # print(SpellChecker().suggest('helo'))
    # print(SpellChecker().suggest('toay'))
    # print(SpellChecker().suggest('tommoow'))
    paginator = Paginator(Blog.get_all(db), 6)
    page = request.args.get('page')
    blogs = paginator.get_page(page)
    return render_template('blogs/blogs.html', 
                           title=TITLE, user=current_user, 
                           blogs=blogs, 
                           featured_blogs=Rating().get_featured_blogs(db, Blog()),  #change 
                           authors=User().get_all(db),
                           recommended_blogs=Blog.get_all(db)[:4],
                           social=Social().get_all(db),
                           ratings=Rating.get_all(db))

@blog.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def blog_page(blog_id):
    paginator = Paginator(Comments().get_by_blog_id(db, blog_id), 6)
    page = request.args.get('page')
    comments = paginator.get_page(page)
    return render_template('blogs/blog.html', title=TITLE, 
                           blog=Blog.get_by_id(db, blog_id), user=current_user,
                           current_time=datetime.utcnow(),
                           author=User.get_by_id(db, Blog.get_by_id(db, blog_id).user_id),
                           comment_authors = User().get_all(db),
                           ratings=Rating().get_by_blog_id(db, blog_id),
                           social=Social().get_all(db),
                           likes=Rating().count_likes(db, blog_id),
                           dislikes=Rating().count_dislikes(db, blog_id),
                           comments=comments,
                           related_comments=Comments().get_by_blog_id_related(db, blog_id))


@blog.route('/blog/create', methods=['GET', 'POST'])
#@handle_blog_request 
@login_required
def create_blog_page():
    return render_template('blogs/create.html', title=TITLE, user=current_user)

@blog.route('/blog/create/post', methods=['POST'])
@login_required
def post_blog():
    try: image = request.files['image'] 
    except: image = None
    valid, error, blog_id = Blog().create_blog(db, current_user.id, request.form.get('title'), request.form.get('description'), request.form.get('content'), image)
    return jsonify(success=valid, error=error, id=blog_id)

@blog.route('/blog/<int:blog_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog_page(blog_id):
    return render_template('blogs/edit.html', title=TITLE, user=current_user, blog=Blog.get_by_id(db, blog_id))

@blog.route('/blog/<int:blog_id>/edit/post', methods=['POST'])
@login_required
def post_blog_edit(blog_id):
    image = Blog().save_image(request.files['image'], request.form.get('description')) if request.form.get('image') == None else request.form.get('image')
    valid, error = Blog().edit_blog(db, blog_id, request.form.get('title'), request.form.get('description'), request.form.get('content'), image)
    return jsonify(success=valid, error=error)

@blog.route('/blog/<int:blog_id>/delete', methods=['POST'])
@login_required
def delete_blog(blog_id):
    success, error = Blog().delete_blog(db, blog_id)
    print(success, error)
    if success: return redirect('/account')
    return jsonify(success=success, error=error)

@blog.route('/blog/<int:blog_id>/follow', methods=['POST'])
@login_required
def follow_blog(blog_id):
    author=User.get_by_id(db, Blog.get_by_id(db, blog_id).user_id)
    Social().follow(db, current_user.id, author.id)
    return jsonify({'success': True})
    
@blog.route('/blog/<int:blog_id>/is_following', methods=['POST'])
@login_required
def is_following(blog_id):
    author=User.get_by_id(db, Blog.get_by_id(db, blog_id).user_id)
    return jsonify({'following':Social().is_following(db, current_user.id, author.id)})

@blog.route('/blog/<int:blog_id>/like', methods=['POST'])
@login_required
def like_blog(blog_id):
    Rating().add_rating(db, blog_id, True)
    return jsonify({'success': True})

@blog.route('/blog/<int:blog_id>/dislike', methods=['POST'])
@login_required
def dislike_blog(blog_id):
    Rating().add_rating(db, blog_id, False)
    return jsonify({'success': True})


@blog.route('/blog/<int:blog_id>/comment', methods=['POST'])
@login_required
def create_comment(blog_id):
    Comments().add_comment(db, current_user.id, blog_id, request.json['comment'])
    return jsonify({'success': True})

@blog.route('/blog/<int:blog_id>/comment/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(blog_id, comment_id):
    print(request.json['comment'])
    Comments().edit_comment(db, comment_id, request.json['comment'])
    return jsonify({'success': True})

@blog.route('/blog/<int:blog_id>/comment/<int:comment_id>/reply', methods=['POST'])
@login_required
def reply_comment(blog_id, comment_id):
    Comments().reply_to_comment(db, comment_id, current_user.id, blog_id, request.json['comment'])
    return jsonify({'success': True})

@blog.route('/blog/<int:blog_id>/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(blog_id, comment_id):
    Comments().delete_comment(db, comment_id)
    return jsonify({'success': True})

@blog.route('/blog/<int:blog_id>/comment/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment():
    #function to like (check if user is already liking, if so unlike)
    return jsonify({'message': 'POST request received'}), 200

@blog.route('/blog/<int:blog_id>/comment/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment():
    #function to like (check if user is already disliking, if so undislike) 
    return jsonify({'message': 'POST request received'}), 200
