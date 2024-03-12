from flask import Flask,render_template,request,flash,g,redirect,url_for,session
from forms import UserForm,PizzaForm
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from datetime import datetime
import time
from flask import request


from models import db
from models import Empleados,Pizzas


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

pedidos = []


@app.route("/", methods=['GET', 'POST'])
def index():
    formulario = UserForm(request.form)
    if request.method == 'POST':
        formulario.id.validators = [];

        if formulario.validate():
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
        empleado = db.session.query(Empleados).filter(Empleados.id == id).first()
        formulario.id.data = id
        formulario.nombre.data = empleado.nombre
        formulario.direccion.data = empleado.direccion
        formulario.telefono.data = empleado.telefono
        formulario.email.data = empleado.email
        formulario.sueldo.data = empleado.sueldo

    if request.method == 'POST':
        id = formulario.id.data
        empleado = Empleados.query.get(id)
        empleado.nombre = formulario.nombre.data
        empleado.direccion = formulario.direccion.data
        empleado.telefono = formulario.telefono.data
        empleado.email = formulario.email.data
        empleado.sueldo = formulario.sueldo.data
        db.session.commit()
        return redirect(url_for('ABCompleto'))

    return render_template("modificar.html", form=formulario)



@app.route("/pizzas", methods=['GET', 'POST'])
def pizzas():
    formulario = PizzaForm(request.form)
    ventas = Pizzas.query.all()
    ventas_total = sum(venta.total for venta in ventas)

    if request.method == 'POST':
        formulario.id.validators = [];
        formulario.fechaCompra.validators = [];
        formulario.total.validators = [];
        

        if formulario.validate():
            precios_base = {
                'Chica': 40,
                'Mediana': 80,
                'Grande': 120
            }

            ingredientes_str = ', '.join(formulario.ingredientes.data)
            precio_base_pizza = precios_base.get(formulario.tamanioPizza.data)
            precio_ingredientes = len(ingredientes_str.split(', ')) * 10
            total = (precio_base_pizza + precio_ingredientes) * int(formulario.cantidadPizzas.data)

            pizza = Pizzas(nombreCliente=formulario.nombreCliente.data,
                               direccion=formulario.direccion.data,
                               telefono=formulario.telefono.data,
                               fechaCompra= formulario.fechaCompra.data,
                               tamanioPizza=formulario.tamanioPizza.data,
                               ingredientes=ingredientes_str,
                               cantidadPizzas=formulario.cantidadPizzas.data,
                               total=total)
            
            pedidos.append(pizza)
            
            
        else:
            print("Error en la validación del formulario:", formulario.errors)
    

    if request.method == "POST" and "meses" in request.form:
        mes = request.form.get("meses")
        ventas = Pizzas.query.filter(db.extract('month', Pizzas.fechaCompra) == mes).all()
        ventas_total = sum(venta.total for venta in ventas)
            
    if request.method == "POST" and "dias" in request.form:
        dia = request.form.get("dias")  # Convertir la cadena a entero
        print(dia)
        ventas = Pizzas.query.filter(Pizzas.diaSemana == dia).all()
        ventas_total = sum(venta.total for venta in ventas)

    return render_template("pizza.html", form=formulario, pizzas=pedidos,ventas = ventas, ventas_total = ventas_total)

@app.route('/modificarPizza/<int:index>', methods=['GET', 'POST'])
def modificarPedido(index):
    formulario = PizzaForm(request.form)

    if request.method == 'GET':
        # Obtener el pedido correspondiente al índice proporcionado
        pedido = pedidos[index]
        
        # Llenar el formulario con los datos del pedido
        formulario.id.data = index
        formulario.nombreCliente.data = pedido.nombreCliente
        formulario.direccion.data = pedido.direccion
        formulario.telefono.data = pedido.telefono
        formulario.ingredientes.data = pedido.ingredientes
        formulario.tamanioPizza.data = pedido.tamanioPizza
        formulario.cantidadPizzas.data = pedido.cantidadPizzas
        formulario.fechaCompra.data = pedido.fechaCompra
        
        # Renderizar el template con el formulario y el pedido
        return render_template("modificarPizza.html", indice=index,  form=formulario, pedido=pedido)
    
    elif request.method == 'POST':
        precios_base = {
                'Chica': 40,
                'Mediana': 80,
                'Grande': 120
            }
        
        ingredientes_str = ', '.join(formulario.ingredientes.data)
        precio_base_pizza = precios_base.get(formulario.tamanioPizza.data)
        precio_ingredientes = len(ingredientes_str.split(', ')) * 10
        total = (precio_base_pizza + precio_ingredientes) * int(formulario.cantidadPizzas.data)
        fecha_compra_str = request.form['fechaCompra']
        fecha_compra = datetime.strptime(fecha_compra_str, '%Y-%m-%d')

        pedidos[index].nombreCliente = request.form['nombreCliente']
        pedidos[index].direccion = request.form['direccion']
        pedidos[index].telefono = request.form['telefono']
        pedidos[index].ingredientes = request.form['ingredientes']
        pedidos[index].tamanioPizza = request.form['tamanioPizza']
        pedidos[index].cantidadPizzas = request.form['cantidadPizzas']
        pedidos[index].fechaCompra = fecha_compra
        pedidos[index].total = total


        return redirect(url_for('pizzas'))


@app.route('/eliminarPizzaLista/<int:index>', methods=['GET', 'POST'])
def eliminarPedido(index):
    pedidos.pop(index)
    return redirect(url_for('pizzas'))


@app.route('/terminar', methods=['GET', 'POST'])
def terminar():
    ventas_total = sum(pizza.total for pizza in pedidos)
    flash("El total es de: ${}, ¿Desea confirmar el pedido?".format(ventas_total))
    formulario = PizzaForm()
    return redirect(url_for('pizzas'))

@app.route('/cancelar', methods=['GET', 'POST'])
def cancelar():
    pedidos.clear()
    flash("El pedido se ha cancelado")
    return redirect(url_for('pizzas'))

@app.route('/guardarPedido', methods=['GET', 'POST'])
def guardarPedido():
    global pedidos  # Declarar 'pedidos' como global

    try:
        # Calcula el total de todas las pizzas una vez
        total_todas_las_pizzas = sum(pedido.total for pedido in pedidos)

        # Elimina todos los pedidos excepto el primero
        if len(pedidos) > 1:
            pedidos = pedidos[:1]

        # Actualiza el total del primer pedido con el total calculado
        pedidos[0].total = total_todas_las_pizzas
        
        # Obtén la fecha de compra del pedido
        fecha_compra = pedidos[0].fechaCompra

        # Obtén el día de la semana correspondiente a la fecha de compra (lunes = 0, martes = 1, ..., domingo = 6)
        dia_semana = fecha_compra.weekday()

        # Asigna el día de la semana al pedido
        pedidos[0].diaSemana = dia_semana

        # Agrega el pedido restante con el total calculado a la sesión de la base de datos
        db.session.add(pedidos[0])

        # Guarda los cambios en la base de datos
        db.session.commit()

        # Limpia la lista de pedidos
        pedidos.clear()

        # Muestra un mensaje de éxito
        flash("Pedido realizado correctamente.")

        # Redirige a la página de pizzas
        return redirect(url_for('pizzas'))

    except Exception as e:
        # En caso de error, revierte los cambios en la base de datos y muestra un mensaje de error
        db.session.rollback()
        flash("Error al guardar pedidos en la base de datos: {}".format(str(e)))
        return redirect(url_for('pizzas'))


@app.route("/eliminarPizza", methods=[ "GET", "POST"])
def eliminarPizza():
    formulario = PizzaForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        pizza1 = db.session.query(Pizzas).filter(Pizzas.id == id).first()
        formulario.id.data = request.args.get('id')
        formulario.nombreCliente.data = pizza1.nombreCliente
        formulario.direccion.data = pizza1.direccion
        formulario.telefono.data = pizza1.telefono
        formulario.ingredientes.data = pizza1.ingredientes
        formulario.tamanioPizza.data = pizza1.tamanioPizza
        formulario.cantidadPizzas.data = pizza1.cantidadPizzas
        
    if request.method == 'POST':
        id = formulario.id.data
        pizza = Pizzas.query.get(id)
        db.session.delete(pizza)
        db.session.commit()
        return redirect(url_for('pizzas'))

    return render_template("eliminarPizza.html", form=formulario)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()