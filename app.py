from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

# ==========================================
# SEMANA 11: Clave secreta para seguridad CSRF
# ==========================================
app.config['SECRET_KEY'] = 'clave_secreta_ritmo_y_folklore_2026'

# ==========================================
# SEMANA 11: Definición de Formularios Flask-WTF
# ==========================================
class SolicitudForm(FlaskForm):
    nombre = StringField('Nombre del Postulante', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=4, message="El nombre debe tener al menos 4 caracteres")
    ])
    categoria = SelectField('Categoría de Taller', choices=[
        ('', 'Seleccione una opción...'),
        ('Cursos Permanentes', 'Cursos Permanentes'),
        ('Vacacionales', 'Vacacionales'),
        ('Montajes Coreográficos', 'Montajes Coreográficos'),
        ('Contrataciones', 'Contrataciones')
    ], validators=[DataRequired(message="Debe seleccionar una categoría válida")])
    descripcion = TextAreaField('Observación / Descripción', validators=[
        DataRequired(message="La observación es obligatoria"),
        Length(min=10, message="La observación debe tener al menos 10 caracteres")
    ])
    submit = SubmitField('Agregar a la Lista')

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(message="Ingrese su nombre")])
    email = StringField('Correo Electrónico', validators=[DataRequired(message="Ingrese su correo"), Email(message="Correo no válido")])
    asunto = StringField('Asunto', validators=[DataRequired(message="Ingrese el asunto")])
    mensaje = TextAreaField('Mensaje o Consulta', validators=[DataRequired(message="Ingrese su mensaje")])
    submit = SubmitField('Enviar Formulario')

# ==========================================
# SEMANA 10: Datos dinámicos (Arreglos / Colecciones)
# ==========================================
solicitudes_db = [
    {
        "id": 1,
        "nombre": "Carlos Tipán",
        "categoria": "Cursos Permanentes",
        "descripcion": "Nivel principiante, requiere horario vespertino."
    },
    {
        "id": 2,
        "nombre": "María Morales",
        "categoria": "Vacacionales",
        "descripcion": "Taller intensivo de expresión dancística y ritmo."
    }
]

servicios_db = [
    {"icono": "🎭", "titulo": "Cursos Permanentes", "desc": "Clases continuas de danza folklórica tradicional para todas las edades.", "color": "text-danger"},
    {"icono": "☀️", "titulo": "Vacacionales", "desc": "Talleres intensivos de expresión dancística, ritmo y coordinación corporal.", "color": "text-warning"},
    {"icono": "🎉", "titulo": "Contrataciones", "desc": "Presentaciones artísticas coreográficas para pregones de fiestas y eventos.", "color": "text-success"},
    {"icono": "🗺️", "titulo": "Montajes", "desc": "Diseño y producción de coreografías exclusivas para instituciones públicas o privadas.", "color": "text-primary"}
]

# ==========================================
# SEMANA 9 & 11: Rutas y Métodos GET/POST
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    form_reg = SolicitudForm()
    form_contacto = ContactoForm()

    # Procesamiento con validación Flask-WTF (Semana 11)
    if form_reg.validate_on_submit() and 'btn_registro' in request.form:
        nuevo_id = len(solicitudes_db) + 1
        nuevo_registro = {
            "id": nuevo_id,
            "nombre": form_reg.nombre.data,
            "categoria": form_reg.categoria.data,
            "descripcion": form_reg.descripcion.data
        }
        solicitudes_db.append(nuevo_registro)
        flash('¡Solicitud registrada con éxito!', 'success')
        return redirect(url_for('index') + '#registro-estudiantes')

    return render_template(
        'index.html',
        form_reg=form_reg,
        form_contacto=form_contacto,
        solicitudes=solicitudes_db,
        servicios=servicios_db,
        total_registros=len(solicitudes_db)
    )

if __name__ == '__main__':
    app.run(debug=True)