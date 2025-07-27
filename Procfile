web: python manage.py runserver 0.0.0.0:$PORT
release: python setup_mysql.py && python manage.py collectstatic --noinput && python manage.py migrate 