#!/bin/bash

echo "-----------------------------------------------"
echo "ENTRYPOINT BEGIN"
cd pollster

while ! poetry run python manage.py flush --no-input 2>&1; do
	echo "Flusing django manage command"
	sleep 3
done

# Wait for few minute and run db migraiton
poetry run python manage.py makemigrations
while ! poetry run python manage.py migrate 2>&1; do
	echo "!Migration is in progress status"
	sleep 3
done

echo "!Creating superuser"
poetry run python manage.py createsuperuser --noinput

echo "!Seeding"
poetry run python manage.py shell <<EOF
import seeder
seeder.seed_all()
EOF

echo "Django docker is fully configured successfully."
echo "-----------------------------------------------"

# Start the application
exec "$@"
