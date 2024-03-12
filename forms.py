from wtforms import validators,Form,StringField,IntegerField,EmailField,TelField,FloatField,DateField,RadioField,SelectMultipleField,widgets

class UserForm(Form):
    id = IntegerField('id',[validators.number_range(min=1, max=20, message='Valor no válido')])
    nombre = StringField("nombre",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=20,message='El minimo es 4 y el máximo es 10'),
    ])
    direccion = StringField("direccion",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=20,message='El minimo es 4 y el máximo es 10')
    ])
    telefono = TelField("telefono",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=10,max=10,message='El minimo es 4 y el máximo es 10'),
    ])
    email = EmailField("email",[
        validators.Email(message='Ingrese un email válido!')
    ])
    sueldo = FloatField("sueldo",[
        validators.DataRequired(message='Ingrese un sueldo!'),
    ])

class PizzaForm(Form):
    id = IntegerField('id',[validators.number_range(min=1, max=20, message='Valor no válido')])
    nombreCliente = StringField("Nombre de Cliente",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=20,message='El minimo es 4 y el máximo es 10'),
    ])
    direccion = StringField("Direccion",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4,max=20,message='El minimo es 4 y el máximo es 10')
    ])
    telefono = TelField("Telefono",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=10,max=10,message='El minimo es y el máximo es 10'),
    ])
    fechaCompra = DateField("Fecha de Compra",[
        validators.DataRequired(message='El campo es requerido.'),
    ])
    tamanioPizza = RadioField("Tamaño de Pizza",
                            choices=[("Chica", "Chica $40"), 
                                     ("Mediana", "Mediana $80"), 
                                     ("Grande", "Grande $120")],
                            validators=[
                                validators.DataRequired(message='Seleccione un tamaño.'),
                            ])
    ingredientes = SelectMultipleField("Ingredientes",
                            choices=[("Jamon", "Jamon $10"), 
                                     ("Piña", "Piña $10"), 
                                     ("Champiñones", "Champiñones $10")],
                            widget=widgets.ListWidget(prefix_label=False),
                            option_widget=widgets.CheckboxInput(),
                            validators=[
                                validators.DataRequired(message='Seleccione al menos un ingrediente.'),
                            ])

    cantidadPizzas = TelField("Num. de Pizzas.",[
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=1,max=10,message='El minimo es 1 y el máximo es 10'),
    ])

    total = FloatField('Total',default=0)

