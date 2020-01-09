import sqlite3
from flask import render_template, redirect, url_for, session, request
from app import app, User, Question

#conn = sqlite3.connect(app.database_url)
#cursor = conn.cursor()
#cursor.execute("INSERT INTO questions (id, quest, type) VALUES (?,?,?)", [1,'Сколько тебе лет?', 'default'])
#cursor.execute("INSERT INTO questions (id, quest, type) VALUES (?,?,?)", [2,'Сколько ты спишь?', 'radio'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [2,'v1', 'Меньше 6 часов'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [2,'v2', '6-8 часов'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [2,'v3', '8-10 часов'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [2,'v3', 'Больше 10 часов'])
#cursor.execute("INSERT INTO questions (id, quest, type) VALUES (?,?,?)", [3,'Какую кухню ты предпочитаешь?', 'checkbox'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [3,'v1', 'Русская'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [3,'v2', 'Японская'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [3,'v3', 'Мексиканская'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [3,'v4', 'Украiнская'])
#cursor.execute("INSERT INTO answers (question_id, name, value) VALUES (?,?,?)", [3,'v5', 'Французская'])
#conn.commit()
# cursor.execute("""CREATE TABLE "users" (
# 	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
# 	"username"	TEXT NOT NULL,
# 	"password"	TEXT NOT NULL,
# 	"last"		INTEGER DEFAULT 0
# );

# CREATE TABLE "questions" (
# 	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
# 	"quest"	TEXT NOT NULL,
# 	"type"	TEXT NOT NULL
# );

# CREATE TABLE "answers" (
# 	"question_id"	INTEGER NOT NULL,
# 	"name"	TEXT NOT NULL,
# 	"value"	TEXT NOT NULL
# )

# CREATE TABLE "results" (
# 	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
# 	"user_id"	INTEGER,
# 	"last"	INTEGER,
# 	"question"	INTEGER
# );

# CREATE TABLE "ans" (
# 	"result_id"	INTEGER,
# 	"value"	TEXT
# );
# """)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    error=None 
    last=0
    if 'username' in session:
        username=session['username']
        last=session['last']
    else:
        username=None
    if 'next' in session:
        next=session['next']
    else:
        next=0
    if request.method == 'POST':
        user = User.getUser(app.database_url, request.form['username'], request.form['password'])
        if user == None:
            error='error password'
        else:
            session['id'] = user['id']
            session['username'] = user['username']
            session['last'] = user['last']
            return redirect(url_for('index'))
    return render_template('index.html', error=error, username=username, next=next, last=last)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    question = Question.getQuestion(app.database_url, question_id)
    if question == None:
        return redirect(url_for('finish'))
    if request.method == 'POST':
        Question.setAnswer(question_id, request.form)
        return redirect('/question/'+str(question_id+1))
    return render_template('question.html', question=question)

@app.route('/finish')
def finish():
    if 'id' not in session or 'answers' not in session or session['answers']==[]:
        return redirect(url_for('index'))
    Question.setFinish(app.database_url)
    return render_template('finish.html')

@app.route('/result')
def result():
    if 'id' not in session:
        return redirect(url_for('index'))
    result = Question.getResult(app.database_url)
    return render_template('result.html', result=result)
