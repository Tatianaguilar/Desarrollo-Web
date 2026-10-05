import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

# ==========================================
# SEMANA 11: Clave secreta para seguridad CSRF
# ==========================================
app.config['SECRET_KEY'] = 'clave_secreta_ritmo_y_folklore_2026'

# ==========================================
# SEMANA 12: Configuración y conexión SQLite
# ==========================================
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'academia.db')

def init_db():
    """Prepara las tablas principales de la Academia Ritmo y Folklore."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Activar las relaciones entre tablas
    cursor.execute("PRAGMA foreign_keys = ON")

    # ==========================================
    # TABLA 1: USUARIOS
    # ==========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            telefono TEXT,
            categoria TEXT,
            rol TEXT NOT NULL DEFAULT 'alumno'
        )
    ''')

    # ==========================================
    # TABLA 2: SOLICITUDES
    # ==========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # ==========================================
    # TABLA 3: HORARIOS
    # ==========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            dia TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            cupos INTEGER NOT NULL DEFAULT 20
        )
    ''')

    # ==========================================
    # COMPATIBILIDAD CON LA TABLA EXISTENTE
    # ==========================================
    cursor.execute("PRAGMA table_info(solicitudes)")
    columnas = [columna[1] for columna in cursor.fetchall()]

    if 'usuario_id' not in columnas:
        cursor.execute('''
            ALTER TABLE solicitudes
            ADD COLUMN usuario_id INTEGER
        ''')

    conn.commit()
    conn.close()
    # Inicializar la base de datos al arrancar
init_db()
    # ==========================================
# USUARIO ADMINISTRADOR
# ==========================================
def crear_usuario_admin():
    """Crea el usuario administrador si todavía no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE usuario = ?",
        ("admin",)
    )

    usuario_existente = cursor.fetchone()

    if usuario_existente is None:
        password_hash = generate_password_hash("admin123")

        cursor.execute('''
            INSERT INTO usuarios
            (nombre, usuario, password, email, telefono, categoria, rol)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Administrador",
            "admin",
            password_hash,
            "admin@ritmoyfolklore.com",
            "",
            "",
            "admin"
        ))

        conn.commit()

    conn.close()


# Crear administrador automáticamente
crear_usuario_admin()

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
# SEMANA 10: Datos dinámicos de Servicios
# ==========================================
servicios_db = [
    {"icono": "🎭", "titulo": "Cursos Permanentes", "desc": "Clases continuas de danza folklórica tradicional para todas las edades.", "color": "text-danger"},
    {"icono": "☀️", "titulo": "Vacacionales", "desc": "Talleres intensivos de expresión dancística, ritmo y coordinación corporal.", "color": "text-warning"},
    {"icono": "🎉", "titulo": "Contrataciones", "desc": "Presentaciones artísticas coreográficas para pregones de fiestas y eventos.", "color": "text-success"},
    {"icono": "🗺️", "titulo": "Montajes", "desc": "Diseño y producción de coreografías exclusivas para instituciones públicas o privadas.", "color": "text-primary"}
]

# ==========================================
# SEMANA 9, 11 & 12: Rutas y Métodos GET/POST con SQLite
# ==========================================
# ==========================================
# LOGIN DEL SISTEMA
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT id, nombre, usuario, password, rol
            FROM usuarios
            WHERE usuario = ?
            ''',
            (usuario,)
        )

        usuario_db = cursor.fetchone()
        conn.close()

        if usuario_db and check_password_hash(usuario_db[3], password):

            session['usuario_id'] = usuario_db[0]
            session['nombre_usuario'] = usuario_db[1]
            session['usuario'] = usuario_db[2]
            session['rol'] = usuario_db[4]

            flash('¡Bienvenido al sistema, ' + usuario_db[1] + '!', 'success')

            return redirect(url_for('index'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')


# ==========================================
# CERRAR SESIÓN
# ==========================================
@app.route('/logout')
def logout():

    session.clear()

    flash('Sesión cerrada correctamente.', 'info')

    return redirect(url_for('login'))


# ==========================================
# SEMANA 9, 11 & 12: Rutas y Métodos GET/POST con SQLite
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    form_reg = SolicitudForm()
    form_contacto = ContactoForm()

    # --- SEMANA 12: Procesar formulario e INSERTAR en SQLite ---
    if form_reg.validate_on_submit() and 'btn_registro' in request.form:
        nombre = form_reg.nombre.data
        categoria = form_reg.categoria.data
        descripcion = form_reg.descripcion.data

        # Guardar en la base de datos de SQLite con consulta parametrizada
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO solicitudes (nombre, categoria, descripcion) VALUES (?, ?, ?)",
            (nombre, categoria, descripcion)
        )
        conn.commit()
        conn.close()

        flash('¡Solicitud registrada con éxito en la base de datos!', 'success')
        return redirect(url_for('index') + '#registro-estudiantes')

    # --- SEMANA 12: Consultar registros con SELECT desde SQLite ---
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, categoria, descripcion FROM solicitudes")
    filas = cursor.fetchall()
    conn.close()

    # Formatear filas recuperadas para la plantilla Jinja2
    solicitudes_db = []
    for fila in filas:
        solicitudes_db.append({
            "id": fila[0],
            "nombre": fila[1],
            "categoria": fila[2],
            "descripcion": fila[3]
        })

    return render_template(
        'index.html',
        form_reg=form_reg,
        form_contacto=form_contacto,
        solicitudes=solicitudes_db,
        servicios=servicios_db,
        total_registros=len(solicitudes_db)
    )
# ==========================================
# RUTAS DE ACCIONES: Eliminar Registro de SQLite
# ==========================================
@app.route('/eliminar/<int:id_solicitud>', methods=['POST'])
def eliminar_solicitud(id_solicitud):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM solicitudes WHERE id = ?", (id_solicitud,))
    conn.commit()
    conn.close()

    flash('¡Solicitud eliminada con éxito!', 'warning')
    return redirect(url_for('index') + '#registro-estudiantes')

if __name__ == '__main__':
    app.run(debug=True)