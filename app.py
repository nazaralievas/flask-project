from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


# начинаем создавать базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# описываем какие столбцы будут в таблице Todo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# этот код непосредственно создает таблицу в БД
with app.app_context():
    db.create_all()


@app.route('/', methods=["POST", "GET"])
def homepage():
    tasks = Todo.query.all()
    if request.method == "POST":
        task_text = request.form['text']
        image = request.form['image']
        new_task = Todo(text=task_text, image=image)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    return render_template('homepage.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
       task_to_update.text = request.form['text']
       task_to_update.image = request.form['image']
       db.session.commit()
       return redirect('/')
    return render_template('update.html', task_to_update=task_to_update)


@app.route('/about')
def about():
    return render_template('about.html')


# этот код позволяет нам не перезапускать сервер после каждого изменения кода
if __name__ == "__main__":
    app.run(debug=True)
