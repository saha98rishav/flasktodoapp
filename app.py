from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime

# database configuration with SQLITE (mysql or postgresql can also be used)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # /// --> relative //// --> absolute
db = SQLAlchemy(app)


##_________________________________________________________________

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id

##__________________________________________________________________
    

@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

##___________________________________________________________________

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

##______________________________________________________________________
    
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating that task"
    else:
        return render_template('update.html', task = task)


##_______________________________________________________________________
    
if __name__ == '__main__':
    app.run(debug = True)

