#!/usr/bin/env python
"""
Script para configurar MySQL en Railway automáticamente.
Este script parsea la DATABASE_URL de Railway y configura las variables de MySQL.
"""

import os
import re
from urllib.parse import urlparse

def setup_mysql_from_database_url():
    """
    Configura las variables de entorno de MySQL desde DATABASE_URL de Railway.
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("No se encontró DATABASE_URL. Usando configuración por defecto.")
        return
    
    # Parsear la URL de la base de datos
    parsed = urlparse(database_url)
    
    # Extraer componentes
    username = parsed.username
    password = parsed.password
    hostname = parsed.hostname
    port = parsed.port or 3306
    database = parsed.path.lstrip('/')
    
    # Configurar variables de entorno
    os.environ['MYSQL_DATABASE'] = database
    os.environ['MYSQL_USER'] = username
    os.environ['MYSQL_PASSWORD'] = password
    os.environ['MYSQL_HOST'] = hostname
    os.environ['MYSQL_PORT'] = str(port)
    
    print(f"MySQL configurado:")
    print(f"  Database: {database}")
    print(f"  User: {username}")
    print(f"  Host: {hostname}")
    print(f"  Port: {port}")

if __name__ == '__main__':
    setup_mysql_from_database_url() 