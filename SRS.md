# Software Requirement Specification (SRS)

# Project Name

ThaiCook - Thai Recipe Recommendation Web Application

---

# 1. Introduction

## 1.1 Purpose

ระบบเว็บแอปพลิเคชันสำหรับค้นหาเมนูอาหารไทยจากวัตถุดิบที่ผู้ใช้มีอยู่  
ผู้ใช้สามารถเลือกวัตถุดิบในบ้าน แล้วระบบจะแสดงเมนูอาหารที่สามารถทำได้ พร้อมวิธีทำอย่างละเอียด

ตัวอย่าง:

- มี ไข่ + หมูสับ + ข้าว
  → แนะนำ:
- ข้าวผัดหมู
- ไข่เจียวหมูสับ
- ข้าวไข่ข้นหมู

---

## 1.2 Scope

ระบบรองรับ:

- ค้นหาเมนูอาหารจากวัตถุดิบ
- แสดงรายการเมนูที่ทำได้
- แสดงวัตถุดิบที่ขาด
- ดูรายละเอียดเมนู
- ดูขั้นตอนการทำอาหาร
- ระบบจัดการเมนูสำหรับผู้ดูแลระบบ (Admin)

เน้นอาหารไทยทั่วไป และอาหารตามสั่งในประเทศไทย

---

# 2. Overall Description

## 2.1 Target Users

- ผู้ที่ต้องการทำอาหารที่บ้าน
- นักเรียน / นักศึกษา
- คนทำงาน
- ผู้ที่ไม่รู้ว่าจะทำอะไรกินจากวัตถุดิบที่มี

---

## 2.2 Product Perspective

ระบบเป็น Web Application พัฒนาโดยใช้ Django Framework  
Frontend ใช้ HTML/CSS/Bootstrap หรือ TailwindCSS  
Backend ใช้ Django + PostgreSQL

Deploy บน Render.com

---

# 3. Functional Requirements

## 3.1 User Features

### 3.1.1 Ingredient Selection

ผู้ใช้สามารถ:

- เลือกวัตถุดิบจากรายการ
- ค้นหาวัตถุดิบ
- เพิ่ม/ลบวัตถุดิบที่มี

ตัวอย่างวัตถุดิบ:

- ไข่
- หมูสับ
- กุ้ง
- ข้าว
- กระเทียม
- พริก
- น้ำปลา

---

### 3.1.2 Recipe Recommendation

ระบบต้องสามารถ:

- วิเคราะห์วัตถุดิบที่ผู้ใช้มี
- แสดงเมนูที่สามารถทำได้
- เรียงลำดับตาม:
  - จำนวนวัตถุดิบที่ตรง
  - ความง่าย
  - ความนิยม

ตัวอย่าง:

| Menu         | Match |
| ------------ | ----- |
| ข้าวผัดหมู   | 100%  |
| ผัดกะเพราหมู | 80%   |
| ต้มจืดหมูสับ | 70%   |

---

### 3.1.3 Recipe Detail

เมื่อผู้ใช้กดเข้าเมนูอาหาร:

ระบบจะแสดง:

- รูปอาหาร
- ชื่อเมนู
- ระยะเวลาในการทำ
- ระดับความยาก
- วัตถุดิบทั้งหมด
- วัตถุดิบที่ผู้ใช้ยังขาด
- ขั้นตอนการทำ
- จำนวนแคลอรี่ (optional)

---

### 3.1.4 Search Feature

ผู้ใช้สามารถค้นหา:

- ชื่อเมนูอาหาร
- วัตถุดิบ

---

### 3.1.5 Filter Feature

ผู้ใช้สามารถกรองเมนูตาม:

- อาหารไทย
- อาหารตามสั่ง
- เมนูทอด
- เมนูต้ม
- เมนูผัด
- เมนูเผ็ด
- เมนูง่าย
- ใช้เวลาน้อยกว่า 15 นาที

---

# 4. Admin Features

## 4.1 Recipe Management

Admin สามารถ:

- เพิ่มเมนูอาหาร
- แก้ไขเมนู
- ลบเมนู
- เพิ่มรูปภาพอาหาร
- เพิ่มขั้นตอนการทำ
- เพิ่มวัตถุดิบ

---

## 4.2 Ingredient Management

Admin สามารถ:

- เพิ่มวัตถุดิบใหม่
- แก้ไขวัตถุดิบ
- ลบวัตถุดิบ

---

# 5. Non-functional Requirements

## 5.1 Performance

- หน้าเว็บโหลดไม่เกิน 3 วินาที
- รองรับผู้ใช้งานพร้อมกันอย่างน้อย 100 คน

---

## 5.2 Security

- ใช้ Django Security Middleware
- ป้องกัน SQL Injection
- ใช้ Environment Variables สำหรับ Secret Key

---

## 5.3 Usability

- รองรับมือถือ (Responsive Design)
- UI ใช้งานง่าย
- รองรับภาษาไทย

---

## 5.4 Availability

- Deploy บน Render.com
- ใช้ PostgreSQL Database

---

# 6. System Architecture

## Frontend

- HTML
- CSS
- Bootstrap/TailwindCSS
- JavaScript

## Backend

- Django
- Django ORM

## Database

- PostgreSQL

## Deployment

- GitHub
- Render.com

---

# 7. Database Design

## Tables

### User

- id
- username
- email
- password

### Ingredient

- id
- name

### Recipe

- id
- name
- description
- image
- cooking_time
- difficulty
- category

### RecipeIngredient

- recipe_id
- ingredient_id
- quantity

### RecipeStep

- id
- recipe_id
- step_number
- instruction

---

# 8. Future Improvements

- AI แนะนำเมนูอัตโนมัติ
- AI สร้างสูตรอาหารใหม่
- ระบบ Login ด้วย Google
- Favorite Menu
- Comment & Rating
- Video Cooking Tutorial
- OCR อ่านวัตถุดิบจากรูปภาพ
- Voice Search
- ระบบคำนวณโภชนาการ

---

# 9. Example User Flow

1. ผู้ใช้เปิดเว็บ
2. เลือกวัตถุดิบที่มี
3. กด "ค้นหาเมนู"
4. ระบบแสดงเมนูที่ทำได้
5. ผู้ใช้กดดูรายละเอียดเมนู
6. ระบบแสดงวิธีทำอาหาร

---

# 10. Tech Stack

| Category        | Technology           |
| --------------- | -------------------- |
| Backend         | Django               |
| Database        | PostgreSQL           |
| Frontend        | Bootstrap / Tailwind |
| Deployment      | Render.com           |
| Version Control | Git + GitHub         |

---

# 11. Success Criteria

ระบบถือว่าสำเร็จเมื่อ:

- ผู้ใช้สามารถเลือกวัตถุดิบได้
- ระบบสามารถแนะนำเมนูได้ถูกต้อง
- ผู้ใช้ดูวิธีทำอาหารได้
- Admin เพิ่มเมนูใหม่ได้
- Deploy ใช้งานจริงบน Render.com ได้สำเร็จ
