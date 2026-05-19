#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "🌱 Seeding initial data..."
python manage.py seed_data

echo "👑 Creating superuser (if not exists)..."
# ต้องตั้งค่าตัวแปรแวดล้อม (Environment Variables) ใน Render ชื่อ DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
python manage.py createsuperuser --noinput || true

echo "✅ Build completed successfully!"
