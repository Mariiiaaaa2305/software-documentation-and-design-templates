from flask import Flask, render_template, request, redirect, url_for
from models.apartment import db
from services.apartment_service import ApartmentService

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airbnb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

service = ApartmentService()


@app.route('/')
def index():
    items = service.get_all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        service.add_apartment(request.form)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = service.get_by_id(id)
    if request.method == 'POST':
        service.update_apartment(id, request.form)
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    service.delete_apartment(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)