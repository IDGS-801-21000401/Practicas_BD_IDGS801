from flask import Flask,render_template,request,flash,g
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

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()