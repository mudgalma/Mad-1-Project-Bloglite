from flask import Blueprint,render_template,request,flash,redirect,url_for
from.models import User,Followers,Blog,Comment
from werkzeug.security import generate_password_hash,check_password_hash
from.import db
from flask_login import login_user,login_required,logout_user,current_user
auth=Blueprint('auth',__name__)
@auth.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        User_name=request.form['user_name']
        password=request.form['psw']
        user=User.query.filter_by(User_name=User_name).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.Add_blog'))
            else:
                flash('Incorrect password',category='error')
                
        else:
            flash('User_name not found',category='error')
                
    return render_template('login.html',user=current_user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method=='POST':
        User_name=request.form['User_name']
        password=request.form['psw']
        Repeate_password=request.form['psw-repeat']
        
        user=User.query.filter_by(User_name=User_name).first()
        print(user)
        if user:
            flash('user_name exits',category='error')

        elif len(User_name) <2:
            flash('name must be greater then 3 char',category='error')
        elif password!=Repeate_password:
            flash('Password not match',category='error')
        elif len(password)<7:
            flash('must be atleast 7 characters',category='error')

        
        else:
            new_user=User(User_name=User_name,password=generate_password_hash(password,method='sha256'))
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)  
            flash('account_created',category='success')
            return redirect(url_for('views.Add_blog',new_user=new_user))
            
    return render_template('create_account.html',user=current_user)

@auth.route('/User_delete/<int:id>',methods=['GET','POST'])
@login_required

def User_delete(id):
    if request.method=='POST':
        User_name=request.form['User_name_update']
        password=request.form['psw_update']
        if current_user.Followers:
            for user_id in current_user.Followers:
                current_user.unfollow(user_id)
        deleteee=Blog.query.filter_by(user_id=id).all()
        if deleteee:
            print(deleteee)
            for Bloge in deleteee:
                print(Bloge)
                if Comment.query.filter_by(Blog_id=Bloge.sno):
                    deletees=Comment.query.filter_by(Blog_id=Bloge.sno).all()
                    print(deletees)
                    print(Bloge.sno)
                    for Comments in deletees:
                        print(Comments)
                        db.session.delete(Comments)
                        db.session.commit()
                        print(Bloge)
                    db.session.delete(Bloge)
                    db.session.commit() 
                    User_delete=User.query.filter_by(id=id).first()
                    User_delete.User_name=User_name
                    User_delete.password=password
                    db.session.delete(User_delete)
                    db.session.commit()
                    return render_template('create_account.html',User_delete=User_delete)
                else:
                    db.session.delete(Bloge)
                    db.session.commit() 
                    print(Bloge)
                    User_delete=User.query.filter_by(id=id).first()
                    User_delete.User_name=User_name
                    User_delete.password=password
                    db.session.delete(User_delete)
                    db.session.commit()
                    return render_template('create_account.html',User_delete=User_delete)
        else:
            User_delete=User.query.filter_by(id=id).first()
            User_delete.User_name=User_name
            User_delete.password=password
            print(User_delete)
            db.session.delete(User_delete)
            db.session.commit()
            return render_template('create_account.html',User_delete=User_delete)
    return render_template('User_update.html')
@auth.route('/User_update/<int:id>',methods=['GET','POST'])
@login_required

def User_update(id):
    if request.method=='POST':
        User_name=request.form['User_name_update']
        password=request.form['psw_update']
        
        password=generate_password_hash(password,method='sha256')

        if len(User_name) <2:
            flash('name must be greater then 3 char',category='error')
        elif len(password)<7:
            flash('must be atleast 7 characters',category='error')
        else:
            User_update=User.query.filter_by(id=id).first()
            User_update.User_name=User_name
            User_update.password=password
            db.session.add(User_update)
            db.session.commit()
        
            flash('update successfully',category='success')
            return redirect(url_for("views.Profile",User_update=User_update))
    User_update=User.query.filter_by(id=id).first()
    return render_template('User_update.html')



@auth.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method=='POST':
        searched=request.form['searched']
        q="%"+searched+"%"
        search=User.query.filter(User.User_name.like(q)).all()
        print(search)

        return render_template("searched.html",searched=searched,search=search)
    
    return render_template("searched.html")



@auth.route('/follow/<User_name>')
@login_required
def follow(User_name):
    user = User.query.filter_by(User_name=User_name).first()
    letid=user.User_name
    if user == current_user:
        flash('You cannot follow yourself!')
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(User_name))
    return redirect(url_for('views.others_Profile', item=letid))

@auth.route('/unfollow/<User_name>')
@login_required
def unfollow(User_name):
    user = User.query.filter_by(User_name=User_name).first()
    letid=user.User_name
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('views.others_profile', User_name=User_name,user=user))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(User_name))
    return redirect(url_for('views.others_Profile', item=letid))


