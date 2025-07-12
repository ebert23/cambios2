# Sistema de Gestión de Servicios Automotrices

Este sistema permite gestionar registros de servicios automotrices, incluyendo la importación masiva desde archivos Excel y búsqueda paginada de registros.

## Características

- Registro de servicios automotrices con detalles completos
- Importación masiva desde archivos Excel
- Búsqueda por número de placa
- Visualización paginada (500 registros por página)
- Cálculo automático de totales
- Interfaz responsive y amigable

## Requisitos

- Python 3.11 o superior
- Pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:

En Windows:
```bash
venv\Scripts\activate
```

En Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar la aplicación:
```bash
python app.py
```

2. Abrir el navegador y acceder a:
```
http://localhost:5000
```

## Formato del Archivo Excel para Importación

El archivo Excel debe contener las siguientes columnas:

- **FECHA**: Fecha del servicio (obligatorio)
- **PLACA**: Número de placa del vehículo (obligatorio)
- **CLIENTE**: Nombre del cliente
- **MARCA**: Marca del vehículo
- **MODELO**: Modelo del vehículo
- **KM**: Kilometraje

Columnas de servicios y precios:
- FILTRO DE ACEITE y PRECIO FILTRO ACEITE
- FILTRO DE AIRE y PRECIO FILTRO AIRE
- FILTRO DE PETROLEO y PRECIO FILTRO PETROLEO
- ACEITE DE MOTOR y PRECIO ACEITE MOTOR
- OTROS 1-4 y sus respectivos PRECIO OTROS 1-4

Notas:
- Los nombres de las columnas deben coincidir exactamente
- Los precios deben ser valores numéricos
- La primera fila debe contener los nombres de las columnas