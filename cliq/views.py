from flask import render_template, flash, redirect, url_for, request, jsonify, session
from cliq import app, db
from cliq.models import User, Interactions, Shares
import json
from itertools import compress

@app.route('/')
def index():
    return redirect(url_for('login'))

# The following route is to be used in the Demo for VandyHacks IV only. It should be removed for other uses.
@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    db.session.commit()
    flash("Demo Reset")
    return redirect(url_for('search'))
    
@app.route('/search')
def search():
    if 'user_id' in session:
        users = User.query.filter(User.id != session['user_id']).order_by(User.name).all()
        users2 = []
        for user in users:
            if not Shares.query.filter(Shares.from_userid == session['user_id']).filter(Shares.to_userid==user.id).first():
                users2.append(user)
        return render_template('search.html', users=users2)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.get_by_email(email) and email == User.get_by_email(email).email:
            flash('An account with the same email already exists.')
            return redirect(url_for('register'))
        db.session.add(User(name=name,
                   email=email, password=password))
        db.session.commit()
        flash('Your account has been created. Please sign in.')
        return redirect(url_for('login'))

    if 'logged_in' in session:
        flash('You are already logged in.')
        return redirect(url_for('search'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        if user:# and user.check_password(password):
            session['user_id'] = user.id
            session['logged_in'] = True
            flash('Welcome, {}!'.format(user.name))
            return redirect(url_for('search'))
        else:
            flash('Incorrect email and/or password.')
            return redirect(url_for('login'))
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect(url_for('search'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    if 'logged_in' in session:
        session.pop('logged_in', None)
    flash('You have successfully logged out.')
    return redirect(url_for('search'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user = User.get_by_id(session['user_id'])
        user.bio = request.form['bio'] or ''
        user.major = request.form['major']
        user.year = request.form['year']
        user.phone = request.form['phone']
        user.facebook = request.form['fb']
        user.instagram = request.form['ig']
        user.snapchat = request.form['sc']
        user.linkedin = request.form['li']
        user.twitter = request.form['tw']
        db.session.commit()
        flash("Your profile has been successfully updated.")
        redirect(url_for('profile'))
    if 'user_id' in session:
        return render_template('profile.html', user=User.get_by_id(session['user_id']), requests=Interactions.query.filter_by(to_userid=session['user_id']).filter_by(accepted=False).all())
    return redirect(url_for('login'))

@app.route("/searchID/<userID>", methods=["GET"])
def searchID(userID):
    return jsonify({user.id:{"id": user.id, "name": user.name, "bio": user.bio, "pic": user.pic} for user in User.search(userID)})

@app.route('/friends')
def friends():
    friendInteractions = User.friends(session['user_id'])
    friends = []
    for share in friendInteractions:
        player2 = User.get_by_id(share.from_userid)
        arr = list(map(int, list(share.share)))
        soc = [player2.facebook, player2.instagram, player2.snapchat, player2.twitter, player2.linkedin, player2.phone, player2.email]
        avsoc = []
        for i in range(len(arr)):
            if arr[i]:
                avsoc.append(soc[i])
            else:
                avsoc.append("")
        print(avsoc)
        friends.append({"id": player2.id, "name": player2.name, "bio": player2.bio, "pic": player2.pic, "year": player2.year, "major":player2.major, "shared": share.share, "socMedia": avsoc})
    return render_template('friends.html', friends=friends)


@app.route('/requests', methods=['GET'])
def requests():
    requests = User.pending(session['user_id'])
    print(requests)
    requesters = []
    for request in requests:
        requester = User.get_by_id(request.from_userid)
        share = Shares.query.filter(Shares.from_userid == requester.id).filter(Shares.to_userid == session['user_id']).order_by('-id').first()
        requesters.append({'fromID': requester.id, 'name': requester.name, 'bio': requester.bio, 'pic': requester.pic, "share": share.share, 'request_id': request.id})
    print(requesters)
    return jsonify(requesters)



@app.route("/interact/<fromID>/<toID>/<shareBool>", methods=["POST"])
def interact(fromID, toID, shareBool):
    if fromID == toID:
        return "SUCCESS"
    db.session.add(Interactions(from_userid=fromID, to_userid=toID))
    db.session.add(Shares(from_userid=fromID, to_userid=toID, share=str(shareBool)))
    db.session.commit()
    return "SUCCESS"

@app.route("/accept/<interaction_id>/<reply>", methods=["POST"])
def accept(interaction_id, reply):
    transaction = Interactions.get_by_id(interaction_id)
    transaction.accepted = int(reply)
    db.session.commit()
    return "SUCCESS"
