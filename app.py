from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///projects.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(400), nullable=False)
    url = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/about')
def info():
    return render_template('about.html')


@app.route('/projects')
def projects():
    lst = Project.query.order_by(Project.date.desc()).all()
    return render_template('projects.html', projects=lst)


@app.route('/projects/<int:project_id>')
def project_info(project_id):
    try:
        project = db.session.get(Project, project_id)
        print(project.name)
        return render_template('detail.html', project=project)
    except AttributeError:
        return 'Project not found!'


@app.route('/create', methods=['POST', 'GET'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['text']
        url = request.form['url']
        project = Project(name=name, description=description, url=url)
        try:
            db.session.add(project)
            db.session.commit()
            return redirect('/projects')
        except:
            return "Error!"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
