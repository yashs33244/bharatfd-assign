#!/bin/sh

echo "Waiting for redis..."
while ! nc -z $REDIS_HOST 6379; do
    sleep 1
done
echo "Redis started"

# Apply database migrations
echo "Applying database migrations..."
python backend/manage.py migrate

# Create superuser if DJANGO_SUPERUSER_* env vars are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python backend/manage.py createsuperuser --noinput
fi

# Execute command passed to docker run
exec "$@"