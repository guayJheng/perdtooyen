# เปิดตู้เย็น (PerdTooYen)

แอปพลิเคชันค้นหาเมนูอาหารไทยจากวัตถุดิบที่มีอยู่ในบ้านของคุณ พัฒนาด้วย Django framework และ Clean Architecture

## 🚀 ฟีเจอร์หลัก
- ค้นหาเมนูอาหารจากวัตถุดิบที่คุณมีในตู้เย็น
- ดูรายละเอียดเมนู วิธีทำ แคลอรี่ และวัตถุดิบที่จำเป็น
- ฟิลเตอร์ค้นหาอาหารตามระดับความยาก เวลาที่ใช้ และหมวดหมู่

## 📁 โครงสร้างโปรเจกต์ (Project Structure)
```
perdtooyen/
├── apps/               # โฟลเดอร์รวมแอปของ Django ทั้งหมด
│   ├── ingredients/    # จัดการข้อมูลวัตถุดิบ
│   ├── recipes/        # จัดการข้อมูลเมนูอาหาร
│   └── recommendations/# ระบบคำนวณจับคู่วัตถุดิบและแนะนำเมนู
├── config/             # ตั้งค่าหลักของ Django โปรเจกต์
├── static/             # ไฟล์ CSS, JS และรูปภาพ
├── templates/          # ไฟล์ HTML ของเว็บไซต์
├── requirements.txt    # รวมรายชื่อ Library ที่ใช้
└── manage.py           # ตัวจัดการระบบ Django
```

## 🛠️ วิธีการติดตั้งและการใช้งานเบื้องต้น (Installation)

1. สร้าง Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

2. ติดตั้ง Library
```bash
pip install -r requirements.txt
```

3. สร้างฐานข้อมูลและนำเข้าข้อมูลตัวอย่าง (Seed Data)
```bash
python manage.py migrate
python manage.py seed_data
```

4. รันเซิร์ฟเวอร์
```bash
python manage.py runserver
```
เข้าใช้งานได้ที่ http://127.0.0.1:8000/
