#!/usr/bin/env bash
set -o errexit

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Creating superuser if not exists..."
python manage.py create_superuser 2>/dev/null || true

echo "==> Seeding equipment catalogue (20 oil & gas items)..."
python manage.py seed_equipment

echo "==> Build complete!"
