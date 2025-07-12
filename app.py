import os
from dotenv import load_dotenv # <-- Importa esto
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from datetime import datetime
import pandas as pd

load_dotenv() # <-- Añade esta línea para cargar las variables
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_local')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///servicios.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)
migrate = Migrate(app, db)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cliente = db.Column(db.String(100))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    kilometraje = db.Column(db.Float)
    filtro_aceite = db.Column(db.String(20))
    precio_filtro_aceite = db.Column(db.Float)
    filtro_aire = db.Column(db.String(20))
    precio_filtro_aire = db.Column(db.Float)
    filtro_petroleo = db.Column(db.String(20))
    precio_filtro_petroleo = db.Column(db.Float)
    aceite_motor = db.Column(db.String(50))
    precio_aceite_motor = db.Column(db.Float)
    otros_1 = db.Column(db.String(100))
    precio_otros_1 = db.Column(db.Float)
    otros_2 = db.Column(db.String(100))
    precio_otros_2 = db.Column(db.Float)
    otros_3 = db.Column(db.String(100))
    precio_otros_3 = db.Column(db.Float)
    otros_4 = db.Column(db.String(100))
    precio_otros_4 = db.Column(db.Float)
    total = db.Column(db.Float)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 500
    pagination = Servicio.query.order_by(Servicio.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)
    servicios = pagination.items
    return render_template('index.html', servicios=servicios, pagination=pagination)

@app.route('/buscar')
def buscar():
    placa = request.args.get('placa', '')
    page = request.args.get('page', 1, type=int)
    per_page = 500
    if placa:
        pagination = Servicio.query.filter(Servicio.placa.ilike(f'%{placa}%')).order_by(Servicio.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)
        servicios = pagination.items
    else:
        servicios = []
        pagination = None
    return render_template('index.html', servicios=servicios, pagination=pagination, placa=placa)

@app.route('/servicio/nuevo', methods=['GET', 'POST'])
def nuevo_servicio():
    if request.method == 'POST':
        try:
            servicio = Servicio(
                placa=request.form['placa'],
                fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
                cliente=request.form['cliente'],
                marca=request.form['marca'],
                modelo=request.form['modelo'],
                kilometraje=float(request.form['kilometraje']) if request.form['kilometraje'] else None,
                filtro_aceite=request.form['filtro_aceite'],
                precio_filtro_aceite=float(request.form['precio_filtro_aceite']) if request.form['precio_filtro_aceite'] else None,
                filtro_aire=request.form['filtro_aire'],
                precio_filtro_aire=float(request.form['precio_filtro_aire']) if request.form['precio_filtro_aire'] else None,
                filtro_petroleo=request.form['filtro_petroleo'],
                precio_filtro_petroleo=float(request.form['precio_filtro_petroleo']) if request.form['precio_filtro_petroleo'] else None,
                aceite_motor=request.form['aceite_motor'],
                precio_aceite_motor=float(request.form['precio_aceite_motor']) if request.form['precio_aceite_motor'] else None,
                otros_1=request.form['otros_1'],
                precio_otros_1=float(request.form['precio_otros_1']) if request.form['precio_otros_1'] else None,
                otros_2=request.form['otros_2'],
                precio_otros_2=float(request.form['precio_otros_2']) if request.form['precio_otros_2'] else None,
                otros_3=request.form['otros_3'],
                precio_otros_3=float(request.form['precio_otros_3']) if request.form['precio_otros_3'] else None,
                otros_4=request.form['otros_4'],
                precio_otros_4=float(request.form['precio_otros_4']) if request.form['precio_otros_4'] else None
            )
            
            # Calcular el total
            total = 0
            for attr in ['precio_filtro_aceite', 'precio_filtro_aire', 'precio_filtro_petroleo',
                        'precio_aceite_motor', 'precio_otros_1', 'precio_otros_2',
                        'precio_otros_3', 'precio_otros_4']:
                valor = getattr(servicio, attr)
                if valor is not None:
                    total += valor
            servicio.total = total

            db.session.add(servicio)
            db.session.commit()
            flash('Servicio registrado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al registrar el servicio: {str(e)}', 'danger')
            return redirect(url_for('nuevo_servicio'))
    return render_template('form_servicio.html')

@app.route('/servicio/editar/<int:id>', methods=['GET', 'POST'])
def editar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    if request.method == 'POST':
        try:
            servicio.placa = request.form['placa']
            servicio.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
            servicio.cliente = request.form['cliente']
            servicio.marca = request.form['marca']
            servicio.modelo = request.form['modelo']
            servicio.kilometraje = float(request.form['kilometraje']) if request.form['kilometraje'] else None
            servicio.filtro_aceite = request.form['filtro_aceite']
            servicio.precio_filtro_aceite = float(request.form['precio_filtro_aceite']) if request.form['precio_filtro_aceite'] else None
            servicio.filtro_aire = request.form['filtro_aire']
            servicio.precio_filtro_aire = float(request.form['precio_filtro_aire']) if request.form['precio_filtro_aire'] else None
            servicio.filtro_petroleo = request.form['filtro_petroleo']
            servicio.precio_filtro_petroleo = float(request.form['precio_filtro_petroleo']) if request.form['precio_filtro_petroleo'] else None
            servicio.aceite_motor = request.form['aceite_motor']
            servicio.precio_aceite_motor = float(request.form['precio_aceite_motor']) if request.form['precio_aceite_motor'] else None
            servicio.otros_1 = request.form['otros_1']
            servicio.precio_otros_1 = float(request.form['precio_otros_1']) if request.form['precio_otros_1'] else None
            servicio.otros_2 = request.form['otros_2']
            servicio.precio_otros_2 = float(request.form['precio_otros_2']) if request.form['precio_otros_2'] else None
            servicio.otros_3 = request.form['otros_3']
            servicio.precio_otros_3 = float(request.form['precio_otros_3']) if request.form['precio_otros_3'] else None
            servicio.otros_4 = request.form['otros_4']
            servicio.precio_otros_4 = float(request.form['precio_otros_4']) if request.form['precio_otros_4'] else None

            # Recalcular el total
            total = 0
            for attr in ['precio_filtro_aceite', 'precio_filtro_aire', 'precio_filtro_petroleo',
                        'precio_aceite_motor', 'precio_otros_1', 'precio_otros_2',
                        'precio_otros_3', 'precio_otros_4']:
                valor = getattr(servicio, attr)
                if valor is not None:
                    total += valor
            servicio.total = total

            db.session.commit()
            flash('Servicio actualizado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al actualizar el servicio: {str(e)}', 'danger')
    return render_template('form_servicio.html', servicio=servicio)

@app.route('/servicio/eliminar/<int:id>')
def eliminar_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    try:
        db.session.delete(servicio)
        db.session.commit()
        flash('Servicio eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el servicio: {str(e)}', 'danger')
    return redirect(url_for('index'))

@app.route('/importar', methods=['GET', 'POST'])
def importar_excel():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        try:
            df = pd.read_excel(file)
            # Verificar si existen las columnas requeridas
            columnas_requeridas = ['FECHA', 'PLACA']
            for columna in columnas_requeridas:
                if columna not in df.columns:
                    raise ValueError(f'La columna {columna} no existe en el archivo Excel')

            for _, row in df.iterrows():
                try:
                    # Manejo específico de la fecha
                    fecha_raw = row['FECHA']
                    if pd.isna(fecha_raw):
                        raise ValueError('La fecha no puede estar vacía')
                    
                    try:
                        fecha = pd.to_datetime(fecha_raw).date()
                    except Exception as fecha_error:
                        raise ValueError(f'Error al procesar la fecha "{fecha_raw}": {str(fecha_error)}')

                    servicio = Servicio(
                        placa=str(row['PLACA']) if pd.notna(row['PLACA']) else None,
                        fecha=fecha,
                        cliente=str(row['CLIENTE']) if pd.notna(row.get('CLIENTE')) else None,
                        marca=str(row['MARCA']) if pd.notna(row.get('MARCA')) else None,
                        modelo=str(row['MODELO']) if pd.notna(row.get('MODELO')) else None,
                        kilometraje=float(row['KM']) if pd.notna(row.get('KM')) else None,
                        filtro_aceite=str(row['FILTRO DE ACEITE']) if pd.notna(row.get('FILTRO DE ACEITE')) else None,
                        precio_filtro_aceite=float(row['PRECIO FILTRO ACEITE']) if pd.notna(row.get('PRECIO FILTRO ACEITE')) else None,
                        filtro_aire=str(row['FILTRO DE AIRE']) if pd.notna(row.get('FILTRO DE AIRE')) else None,
                        precio_filtro_aire=float(row['PRECIO FILTRO AIRE']) if pd.notna(row.get('PRECIO FILTRO AIRE')) else None,
                        filtro_petroleo=str(row['FILTRO DE PETROLEO']) if pd.notna(row.get('FILTRO DE PETROLEO')) else None,
                        precio_filtro_petroleo=float(row['PRECIO FILTRO PETROLEO']) if pd.notna(row.get('PRECIO FILTRO PETROLEO')) else None,
                        aceite_motor=str(row['ACEITE MOTOR']) if pd.notna(row.get('ACEITE MOTOR')) else None,
                        precio_aceite_motor=float(row['PRECIO ACEITE MOTOR']) if pd.notna(row.get('PRECIO ACEITE MOTOR')) else None,
                        otros_1=str(row['OTROS 1']) if pd.notna(row.get('OTROS 1')) else None,
                        precio_otros_1=float(row['PRECIO OTROS 1']) if pd.notna(row.get('PRECIO OTROS 1')) else None,
                        otros_2=str(row['OTROS 2']) if pd.notna(row.get('OTROS 2')) else None,
                        precio_otros_2=float(row['PRECIO OTROS 2']) if pd.notna(row.get('PRECIO OTROS 2')) else None,
                        otros_3=str(row['OTROS 3']) if pd.notna(row.get('OTROS 3')) else None,
                        precio_otros_3=float(row['PRECIO OTROS 3']) if pd.notna(row.get('PRECIO OTROS 3')) else None,
                        otros_4=str(row['OTROS 4']) if pd.notna(row.get('OTROS 4')) else None,
                        precio_otros_4=float(row['PRECIO OTROS 4']) if pd.notna(row.get('PRECIO OTROS 4')) else None
                    )

                    # Calcular el total
                    total = 0
                    for attr in ['precio_filtro_aceite', 'precio_filtro_aire', 'precio_filtro_petroleo',
                                'precio_aceite_motor', 'precio_otros_1', 'precio_otros_2',
                                'precio_otros_3', 'precio_otros_4']:
                        valor = getattr(servicio, attr)
                        if valor is not None:
                            total += valor
                    servicio.total = total
                    
                    db.session.add(servicio)
                except Exception as row_error:
                    db.session.rollback()
                    raise ValueError(f'Error en la fila {_ + 2}: {str(row_error)}')
            
            db.session.commit()
            flash('Datos importados exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al importar datos: {str(e)}', 'danger')
        
        return redirect(url_for('index'))
    
    return render_template('importar.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)