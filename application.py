from flask import render_template, session, \
    redirect, url_for, request, \
    flash, get_flashed_messages


from config import application, db
# importing classes
from tables import users, notes, discussion


# to be installed with PIP 
# flask
# mysqlclient 

# ===============================================
#         main home route 
# ===============================================
@application.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        # getting user details to know score 
        user = users.query.filter_by(username=session['username']).first() 
        user_points = user.points

        # fetching all notes for this course 
        n = notes.query.filter_by(course=session['course'])

        # fetching all threads for this course 
        d = discussion.query.filter_by(course=session['course'], reply_id="")

        return render_template("home.html", score=user_points, threads=d, notes=n)



# ===============================================
#         signup, logout & login routes
# ===============================================

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    # if user clicked on "ok" on sign up form they will use POST 
    if request.method == 'POST':
        # validation
        # checking if username is unique
        if users.query.filter_by(username=request.form['username']).first():
            flash("Username already exists!")
            return render_template('login.html')

        # checking password == password-confirm
        new_user = users(request.form['username'], request.form['password'],
                            request.form['email'], "0", 
                            request.form['course'],
                            request.form['user_type'], 
                            request.form['auth'])
        # adding user to session (automatically logging in) 
        session['username'] = new_user.username
        session['user_type'] = new_user.user_type
        session['course'] = new_user.course
        session['points'] = new_user.points


        # adding user to db
        db.session.add(new_user)
        db.session.commit()

        # redirecting to welcome page
        return redirect(url_for('home'))
 
    else:
        return render_template('lost.html')



# loggin out 
@application.route('/logout')
def logout():
    # removing username from session 
    session.pop('username', None)
    # redirecting to login page 
    return redirect(url_for('login'))


@application.route('/login', methods=['GET', 'POST'])
def login():

    # if user clicked on "submit" on login form they will use POST 
    if request.method == 'POST':
        # getting user with username

        form_username = request.form['username']

        user = users.query.filter_by(username=form_username).first()
        if not user:
            flash("you entered a wrong username!")
        else:
            if user.password == request.form['password']:
                # creating new session 
                session['username'] = user.username
                session['user_type'] = user.user_type
                session['course'] = user.course 
                session['points'] = user.points
                session['auth'] = user.auth

                return redirect(url_for('home'))
            else:
                flash("incorrect password")
        
        return redirect(url_for('login'))

    elif request.method == 'GET': 
        # user is using GET -> just show login page 
        return render_template('login.html')






# ===============================================
#         threads & discussion routes 
# ===============================================

# route for creating new thread
@application.route('/new_thread', methods=['POST']) # only post for this route 
def new_thread(): 

    # creating new thread object 
    d = discussion(session['course'], session['username'], request.form['threadcontent'], "")

    # saving and commiting changed to database
    db.session.add(d)
    db.session.commit()

    # returning to home page 
    return redirect(url_for("home"))


# route to open existing thread 
@application.route('/thread/<thread_id>', methods=['GET'])
def open_thread(thread_id): 
    # fetching thread from db 
    thread = discussion.query.get(thread_id)

    # fetching thread replies 
    replies = discussion.query.filter_by(reply_id=str(thread_id))

    # passing all to html
    return render_template("thread.html", thread=thread, replies=replies)



# route to delete existing discussion 
@application.route('/delete_thread/<thread_id>')
def delete_thread(thread_id): 
    # fetching it from db 
    d  = discussion.query.get(thread_id) 

    # deleting 
    db.session.delete(d) 

    # commiting 
    db.session.commit()

    # redirecting to home 
    return redirect(url_for("home"))


# route to post new reply 
@application.route('/new_reply/<reply_id>', methods=['POST'])
def new_reply(reply_id): 
    d = discussion(session['course'], session['username'], request.form['text'], reply_id)

    # saving 
    db.session.add(d) 
    db.session.commit() 

    # redirecting to main thread 
    return redirect(url_for('open_thread', thread_id=reply_id))
    
# ===============================================
#                   notes routes 
# ===============================================


# route for creating new note
@application.route('/new_note', methods=['POST']) # only post for this route  
def new_note(): 
    # creating new note object 
    n = notes(session['course'], session['username'], request.form['notecontent'], "not yet")

    # getting user details to increase their points score 
    user = users.query.filter_by(username=session['username']).first()
    new_points = int(user.points) + 10
    user.points = str(new_points)

    # saving and commiting changed to database
    db.session.add(n)
    db.session.commit()

    # returning to home page 
    return redirect(url_for("home"))


# route to open existing note 
@application.route('/note/<note_id>', methods=['GET'])
def open_note(note_id): 
    # fetching note from database 
    note = notes.query.get(note_id) # fetching by note_id that was passed in the url 

    # passing note to html 
    return render_template("note.html", note=note) 


# route to delete existing note 
@application.route('/delete_note/<note_id>')
def delete_note(note_id): 
    # fetching it from db 
    note  = notes.query.get(note_id) 

    # deleting 
    db.session.delete(note) 

    # commiting 
    db.session.commit()

    # redirecting to home 
    return redirect(url_for("home"))


# route to auth a note 
@application.route('/note_auth/<note_id>/<auth>/<username>')
def note_auth(note_id, auth, username): 
    # getting username from db  
    user = users.query.filter_by(username=username).first() 
    
    # getting note from db 
    note = notes.query.get(note_id)

    # making changes based on auth 
    if auth == "yes": 
        # increasing score 
        user.points = str(int(user.points) + 100)

        # setting note as auth = yes 
        note.auth = "yes"
    else: # note is rejected 
        # decreasing user points 
        user.points = str(int(user.points) - 100) 

        # setting note as auth = no 
        note.auth = "no"

    # saving changes to db 
    db.session.commit() 

    # redicting to note 
    return redirect(url_for("open_note", note_id=note_id))





if __name__ == "__main__":
    # initializing database
    db.create_all()
    # running application
    application.run(host="0.0.0.0", debug=True, port=5000)
