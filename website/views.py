from flask import Blueprint,render_template,request, flash ,redirect,url_for,send_from_directory
from flask_login import login_required,current_user
from.models import Blog,User,Followers,Comment
from.import db
from.import UPLOAD_FOLDER
import urllib.request
import os
from werkzeug.utils import secure_filename
views=Blueprint('views',__name__)
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
    
@views.route('/')
@login_required
def home():
    allBlogs=Blog.query.all()
    return render_template('home.html',allBlogs=allBlogs)

    
@views.route('/Add_blog', methods=['GET','POST'])
@login_required
def Add_blog():
    if request.method == "POST":
        poster=current_user.id
        title=request.form['title']
        Desc=request.form['Desc']
        file=request.files['images']
        if len(Desc)<1:
            flash('Blog is small',category='error')
        elif file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,filename))
            blog=Blog(title=title,Desc=Desc,blog_pic=filename,user_id=poster)
            db.session.add(blog)
            db.session.commit()
            flash('Blog added', category='success')
            print(filename)
            user=current_user.id
            allBlog=Blog.query.filter_by(user_id=user)
    
            return render_template('Profile.html',allBlog=allBlog)
        else:
            blog=Blog(title=title,Desc=Desc,user_id=poster)
            db.session.add(blog)
            db.session.commit()
            flash('Blog added', category='success')
            return redirect(url_for("views.Profile",blog=blog))

    return render_template('Add_blog.html', user=current_user)
@views.route('/Profile/')
@login_required
def Profile():
    user=current_user.id
    
    allBlog=Blog.query.filter_by(user_id=user)
    comments=Comment.query.all()
    print(comments)
    
    return render_template('Profile.html',allBlog=allBlog,comments=comments)
@views.route('/others_Profile/<item>')
@login_required
def others_Profile(item):
    user=User.query.filter(User.User_name.like(item)).first()
    print(user.id)
    
    comments=Comment.query.all()
    
    allBlog=Blog.query.filter_by(user_id=user.id)
    
    return render_template('others_Profile.html',allBlog=allBlog,letid=item,user=user, comments=comments)

@views.route('/delete/<int:sno>')
@login_required
def delete(sno):
    delete=Blog.query.filter_by(sno=sno).first()
    user=current_user.id
    if(user==delete.poster.id):
        
        if Comment.query.filter_by(Blog_id=sno).all():
            deletee=Comment.query.filter_by(Blog_id=sno).all()
            for bloge in deletee:
                db.session.delete(bloge)
                db.session.commit()
        
            delete=Blog.query.filter_by(sno=sno).first()
            db.session.delete(delete)
            db.session.commit()
        else:
            delete=Blog.query.filter_by(sno=sno).first()
            db.session.delete(delete)
            db.session.commit()
    else:    
        flash('not able to delete',category='error')
    return redirect(url_for("views.home",user=current_user))
@views.route('/update/<int:sno>',methods=['GET','POST'])
@login_required
def update(sno):
    user=current_user.id
    update=Blog.query.filter_by(sno=sno).first()
    if(user==update.poster.id):
        if request.method=='POST':
            title=request.form['title']
            Desc=request.form['Desc']
            file=request.files['images']
            if file and allowed_file(file.filename):
                filename=secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER,filename))
                update=Blog.query.filter_by(sno=sno).first()
                update.title=title
                update.Desc=Desc
                update.blog_pic=filename
                db.session.add(update)
                db.session.commit()
                flash('Blog updated', category='success')
                print(filename)
                return redirect(url_for("views.home",filename=filename))

            else:    
                update=Blog.query.filter_by(sno=sno).first()
                update.title=title
                update.Desc=Desc
                db.session.add(update)
                db.session.commit()
                flash('blog updated',category='success')
                return redirect(url_for("views.home"))
        return render_template('update.html',update=update)

    else:
        flash('not able to update.',category='error')
        return redirect(url_for("views.home"))

  
@views.route('/Feeds')
@login_required
def Followed_blogs():
    followed = Blog.query.join(
        Followers, (Followers.c.followed_id == Blog.user_id)).filter(
            Followers.c.follower_id == current_user.id)
    own = Blog.query.filter_by(user_id=current_user.id)
    blogs=followed.union(own).order_by(Blog.date_created.desc()).all()
    
    return(render_template('feeds.html',blogs=blogs))     
@views.route('/display/<filename>')
def display_image(filename):
    print('display_image filename:'+filename)
    return redirect(url_for('static',filename='static/'+filename),code=301) 
@views.route('/open_blog/<int:sno>')
@login_required
def open_blog(sno):
    Blog1=Blog.query.filter_by(sno=sno).first()
    return render_template("open_blog.html",Blog1=Blog1)
@views.route('/like/<int:sno>')
@login_required
def like(sno):
    likec=Blog.query.filter_by(sno=sno).first()
    if likec.likes==None :
        likec.likes=1
    elif likec.likes>=1:
        likec.likes+=1
        print(likec.likes)
    db.session.commit()
    allBlogs=Blog.query.all()
    
    return render_template('home.html',allBlogs=allBlogs,lik=likec.likes)

    
@views.route('/comments/<int:sno>',methods=['POST'])
@login_required
def comment(sno):
    comment_text=request.form['comments']
    comment=Comment(comment=comment_text,Blog_id=sno)
    db.session.add(comment)
    db.session.commit()
    
    allBlogs=Blog.query.all()
    return render_template('home.html',allBlogs=allBlogs)
    

