from flask import Flask,render_template,request,flash,g,redirect,url_for
from forms import UserForm
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig

from models import db
from models import Empleados


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404


@app.route("/", methods=['GET', 'POST'])
def index():
    formulario = UserForm(request.form)
    if request.method == 'POST':
        formulario.id.validators = [];

        if formulario.validate():
            print("hola")
            empleado = Empleados(nombre=formulario.nombre.data,
                                 direccion=formulario.direccion.data,
                                 telefono=formulario.telefono.data,
                                 email=formulario.email.data,
                                 sueldo=formulario.sueldo.data)

            formulario.nombre.data = ""
            formulario.direccion.data = ""
            formulario.telefono.data = ""
            formulario.email.data = ""
            formulario.data['sueldo'] = ""

            db.session.add(empleado)
            db.session.commit()

            formulario = UserForm()
        else:
            print("Error en la validación del formulario:", formulario.errors)

    return render_template("index.html", form=formulario)

@app.route("/ABC_Completo", methods=[ "GET", "POST"])
def ABCompleto():
    empleado = Empleados.query.all()
    return render_template("ABC_Completo.html", empleados=empleado)

@app.route("/eliminar", methods=[ "GET", "POST"])
def eliminar():
    formulario = UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        empleado1 = db.session.query(Empleados).filter(Empleados.id == id).first()
        formulario.id.data = request.args.get('id')
        formulario.nombre.data = empleado1.nombre
        formulario.direccion.data = empleado1.direccion
        formulario.telefono.data = empleado1.telefono
        formulario.sueldo.data = empleado1.sueldo
        formulario.email.data = empleado1.email
        
    if request.method == 'POST':
        id = formulario.id.data
        empleado = Empleados.query.get(id)
        db.session.delete(empleado)
        db.session.commit()
        return redirect(url_for('ABCompleto'))

    return render_template("eliminar.html", form=formulario)


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    formulario = UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumno = db.session.query(Empleados).filter(Empleados.id == id).first()
        formulario.id.data = id
        formulario.nombre.data = alumno.nombre
        formulario.direccion.data = alumno.direccion
        formulario.telefono.data = alumno.telefono
        formulario.email.data = alumno.email
        formulario.sueldo.data = alumno.sueldo

    if request.method == 'POST':
        id = formulario.id.data
        alumno = Empleados.query.get(id)
        alumno.nombre = formulario.nombre.data
        alumno.direccion = formulario.direccion.data
        alumno.telefono = formulario.telefono.data
        alumno.email = formulario.email.data
        alumno.sueldo = formulario.sueldo.data
        db.session.commit()
        return redirect(url_for('ABCompleto'))

    return render_template("modificar.html", form=formulario)




if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()