"""
Management Command: seed_data
สร้างข้อมูลตัวอย่าง — วัตถุดิบและเมนูอาหารไทย
รัน: python manage.py seed_data
     python manage.py seed_data --clear  (ลบข้อมูลเดิมก่อน)
"""
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient, RecipeStep

# ---------------------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------------------

INGREDIENTS = [
    # โปรตีน
    {'name': 'ไข่',              'category': 'protein'},
    {'name': 'หมูสับ',           'category': 'protein'},
    {'name': 'หมูสไลซ์',         'category': 'protein'},
    {'name': 'ไก่',              'category': 'protein'},
    {'name': 'กุ้ง',             'category': 'protein'},
    {'name': 'เนื้อวัว',          'category': 'protein'},
    {'name': 'ปลา',              'category': 'protein'},
    {'name': 'เต้าหู้',           'category': 'protein'},
    # ข้าวและแป้ง
    {'name': 'ข้าวสวย',          'category': 'grain'},
    {'name': 'เส้นใหญ่',          'category': 'grain'},
    {'name': 'วุ้นเส้น',          'category': 'grain'},
    {'name': 'มาม่า',            'category': 'grain'},
    # ผักและเครื่องเคียง
    {'name': 'กระเทียม',         'category': 'veggie'},
    {'name': 'หัวหอม',           'category': 'veggie'},
    {'name': 'หอมแดง',          'category': 'veggie'},
    {'name': 'ต้นหอม',           'category': 'veggie'},
    {'name': 'พริก',             'category': 'veggie'},
    {'name': 'ผักบุ้ง',          'category': 'veggie'},
    {'name': 'ผักคะน้า',         'category': 'veggie'},
    {'name': 'ผักกาดขาว',       'category': 'veggie'},
    {'name': 'กะหล่ำปลี',        'category': 'veggie'},
    {'name': 'ถั่วฝักยาว',        'category': 'veggie'},
    {'name': 'มะเขือเทศ',        'category': 'veggie'},
    {'name': 'มะละกอเขียว',      'category': 'veggie'},
    {'name': 'เห็ด',             'category': 'veggie'},
    # เครื่องเทศและสมุนไพร
    {'name': 'ใบกะเพรา',        'category': 'spice'},
    {'name': 'ตะไคร้',           'category': 'spice'},
    {'name': 'ใบมะกรูด',         'category': 'spice'},
    {'name': 'ขิง',              'category': 'spice'},
    {'name': 'ผักชี',            'category': 'spice'},
    {'name': 'พริกไทย',          'category': 'spice'},
    # เครื่องปรุงและซอส
    {'name': 'น้ำปลา',           'category': 'sauce'},
    {'name': 'ซีอิ๊วขาว',         'category': 'sauce'},
    {'name': 'ซีอิ๊วดำ',          'category': 'sauce'},
    {'name': 'น้ำมันหอย',        'category': 'sauce'},
    {'name': 'น้ำตาล',           'category': 'sauce'},
    {'name': 'มะนาว',           'category': 'sauce'},
    {'name': 'น้ำมันพืช',        'category': 'sauce'},
    {'name': 'กะทิ',             'category': 'sauce'},
    {'name': 'พริกแกงเขียวหวาน', 'category': 'sauce'},
    {'name': 'เกลือ',            'category': 'sauce'},
    {'name': 'น้ำส้มสายชู',      'category': 'sauce'},
]

RECIPES = [
    {
        'name':           'ข้าวผัดหมู',
        'description':    'ข้าวผัดหมูสูตรร้านข้าวแกง หอมกระเทียม ไข่ฟู ผัดร้อนๆ อร่อยทุกคำ',
        'cooking_time':   15,
        'difficulty':     'easy',
        'category':       'street',
        'cooking_method': 'stirfry',
        'is_spicy':       False,
        'calories':       450,
        'popularity':     95,
        'ingredients': [
            ('ข้าวสวย',    '2 ถ้วย',       True),
            ('หมูสไลซ์',   '100 กรัม',     True),
            ('ไข่',        '1 ฟอง',        True),
            ('กระเทียม',   '3 กลีบ',       True),
            ('น้ำมันพืช',  '2 ช้อนโต๊ะ',   True),
            ('ซีอิ๊วขาว',  '1 ช้อนโต๊ะ',   True),
            ('น้ำตาล',     '1 ช้อนชา',     True),
            ('ต้นหอม',     '2 ต้น',        False),
        ],
        'steps': [
            'ตั้งกระทะบนไฟกลาง ใส่น้ำมันพืชให้ร้อน',
            'ใส่กระเทียมสับลงผัดให้เหลืองหอม',
            'ใส่หมูสไลซ์ลงผัดให้สุก ปรุงรสด้วยซีอิ๊วขาว',
            'เขี่ยหมูออกด้านข้าง แล้วตอกไข่ลงคนให้เข้ากัน',
            'ใส่ข้าวสวยลงผัดให้เข้ากัน ปรุงรสด้วยน้ำตาล ผัดประมาณ 3–4 นาที จัดใส่จาน โรยต้นหอม',
        ],
    },
    {
        'name':           'ผัดกะเพราหมูสับ',
        'description':    'เมนูขวัญใจชาวไทย หอมกะเพราเข้มข้น เผ็ดร้อนถึงใจ',
        'cooking_time':   10,
        'difficulty':     'easy',
        'category':       'street',
        'cooking_method': 'stirfry',
        'is_spicy':       True,
        'calories':       380,
        'popularity':     98,
        'ingredients': [
            ('หมูสับ',      '200 กรัม',     True),
            ('ใบกะเพรา',   '1 กำมือ',      True),
            ('กระเทียม',   '5 กลีบ',       True),
            ('พริก',       '5 เม็ด',       True),
            ('น้ำปลา',     '1 ช้อนโต๊ะ',   True),
            ('น้ำมันหอย',  '1 ช้อนโต๊ะ',   True),
            ('น้ำตาล',     '1 ช้อนชา',     True),
            ('น้ำมันพืช',  '2 ช้อนโต๊ะ',   True),
            ('ไข่',        '1 ฟอง',        False),
        ],
        'steps': [
            'โขลกกระเทียมและพริกให้ละเอียดพอหยาบ',
            'ตั้งกระทะบนไฟแรง ใส่น้ำมันให้ร้อน ผัดกระเทียมพริกให้หอม',
            'ใส่หมูสับลงผัดให้สุก คนให้ร่วน',
            'ปรุงรสด้วยน้ำปลา น้ำมันหอย น้ำตาล ใส่ใบกะเพราลงผัดให้เข้ากัน เสิร์ฟทันที',
        ],
    },
    {
        'name':           'ไข่เจียว',
        'description':    'ไข่เจียวกรอบนอกนุ่มใน สูตรโบราณใส่น้ำปลา หอมหวนน่ากิน',
        'cooking_time':   5,
        'difficulty':     'easy',
        'category':       'thai',
        'cooking_method': 'fried',
        'is_spicy':       False,
        'calories':       250,
        'popularity':     80,
        'ingredients': [
            ('ไข่',        '3 ฟอง',        True),
            ('น้ำปลา',     '1 ช้อนชา',     True),
            ('น้ำมันพืช',  '3 ช้อนโต๊ะ',   True),
            ('ต้นหอม',     '1 ต้น',        False),
        ],
        'steps': [
            'ตีไข่ในชามให้เข้ากัน ปรุงรสด้วยน้ำปลา',
            'ตั้งกระทะบนไฟกลาง ใส่น้ำมันให้ร้อนจัด',
            'เทไข่ลงกระทะ ปล่อยให้ขอบแห้งก่อนพับ',
            'พลิกกลับเมื่อด้านล่างเหลืองกรอบ เสิร์ฟทันที',
        ],
    },
    {
        'name':           'ต้มจืดหมูสับ',
        'description':    'ซุปใสหวานอร่อยจากกระดูกหมูและผักกาดขาว อาหารอุ่นใจ',
        'cooking_time':   20,
        'difficulty':     'easy',
        'category':       'thai',
        'cooking_method': 'boiled',
        'is_spicy':       False,
        'calories':       200,
        'popularity':     75,
        'ingredients': [
            ('หมูสับ',      '150 กรัม',     True),
            ('ผักกาดขาว',   '200 กรัม',     True),
            ('กระเทียม',   '3 กลีบ',       True),
            ('น้ำปลา',     '2 ช้อนโต๊ะ',   True),
            ('พริกไทย',    '1 ช้อนชา',     True),
            ('ต้นหอม',     '2 ต้น',        False),
        ],
        'steps': [
            'ต้มน้ำในหม้อให้เดือด ใส่กระเทียมบุบและพริกไทยลงไป',
            'ปั้นหมูสับเป็นก้อนเล็กๆ ใส่ลงในน้ำเดือด',
            'พอหมูสุก ใส่ผักกาดขาวลงต้มจนนิ่ม',
            'ปรุงรสด้วยน้ำปลา ชิมรส',
            'ตักใส่ชาม โรยต้นหอมและพริกไทย เสิร์ฟร้อนๆ',
        ],
    },
    {
        'name':           'ผัดกระเทียมหมู',
        'description':    'หมูผัดกระเทียมพริกไทย กลิ่นหอมชวนน้ำลายสอ เมนูง่ายแต่อร่อย',
        'cooking_time':   10,
        'difficulty':     'easy',
        'category':       'street',
        'cooking_method': 'stirfry',
        'is_spicy':       False,
        'calories':       320,
        'popularity':     85,
        'ingredients': [
            ('หมูสไลซ์',   '200 กรัม',     True),
            ('กระเทียม',   '8 กลีบ',       True),
            ('น้ำมันพืช',  '3 ช้อนโต๊ะ',   True),
            ('ซีอิ๊วขาว',  '1 ช้อนโต๊ะ',   True),
            ('พริกไทย',    '1 ช้อนชา',     True),
            ('น้ำตาล',     '1 ช้อนชา',     False),
        ],
        'steps': [
            'บุบกระเทียมให้แตก หั่นหยาบ',
            'ตั้งกระทะบนไฟแรง ใส่น้ำมันให้ร้อน',
            'ผัดกระเทียมจนเหลืองหอม ใส่หมูสไลซ์ลงผัด',
            'ปรุงรสด้วยซีอิ๊วขาว พริกไทย น้ำตาล ผัดให้เข้ากัน เสิร์ฟทันที',
        ],
    },
    {
        'name':           'ผัดผักบุ้งไฟแดง',
        'description':    'ผักบุ้งผัดไฟแรง หอมน้ำมันหอย กรอบอร่อยเคี้ยวเพลิน',
        'cooking_time':   8,
        'difficulty':     'easy',
        'category':       'thai',
        'cooking_method': 'stirfry',
        'is_spicy':       False,
        'calories':       150,
        'popularity':     70,
        'ingredients': [
            ('ผักบุ้ง',    '300 กรัม',     True),
            ('กระเทียม',   '5 กลีบ',       True),
            ('น้ำมันหอย',  '2 ช้อนโต๊ะ',   True),
            ('น้ำปลา',     '1 ช้อนโต๊ะ',   True),
            ('น้ำมันพืช',  '3 ช้อนโต๊ะ',   True),
            ('พริก',       '3 เม็ด',       False),
        ],
        'steps': [
            'บุบกระเทียมและพริก',
            'ตั้งกระทะบนไฟแรงมาก ใส่น้ำมันให้ร้อนจัด',
            'ใส่กระเทียมพริกลงผัดให้หอม ใส่ผักบุ้ง ปรุงรสด้วยน้ำมันหอยและน้ำปลา ผัดเร็วๆ ให้ผักสุกกำลังดี เสิร์ฟทันที',
        ],
    },
    {
        'name':           'ต้มยำกุ้ง',
        'description':    'ต้มยำกุ้งน้ำข้น รสจัดจ้าน เปรี้ยว เผ็ด หอม ครบทุกรส',
        'cooking_time':   25,
        'difficulty':     'medium',
        'category':       'thai',
        'cooking_method': 'boiled',
        'is_spicy':       True,
        'calories':       180,
        'popularity':     90,
        'ingredients': [
            ('กุ้ง',        '300 กรัม',     True),
            ('ตะไคร้',      '2 ต้น',        True),
            ('ใบมะกรูด',    '5 ใบ',         True),
            ('พริก',        '5 เม็ด',       True),
            ('น้ำปลา',      '2 ช้อนโต๊ะ',   True),
            ('มะนาว',       '1 ลูก',        True),
            ('เห็ด',        '100 กรัม',     False),
            ('ผักชี',       '1 ต้น',        False),
        ],
        'steps': [
            'ต้มน้ำในหม้อ ใส่ตะไคร้หั่นท่อน ใบมะกรูด และพริกบุบลงไป',
            'เมื่อน้ำเดือด ใส่กุ้งและเห็ดลงต้ม',
            'พอกุ้งสุก ปรุงรสด้วยน้ำปลา',
            'ปิดไฟ บีบมะนาว ชิมรสให้ครบเปรี้ยวเค็มเผ็ด',
            'ตักใส่ชาม โรยผักชี เสิร์ฟร้อนๆ',
        ],
    },
    {
        'name':           'แกงเขียวหวานไก่',
        'description':    'แกงเขียวหวานสูตรโบราณ กะทิข้น หอมใบมะกรูด เข้มข้นถึงใจ',
        'cooking_time':   30,
        'difficulty':     'medium',
        'category':       'thai',
        'cooking_method': 'soup',
        'is_spicy':       True,
        'calories':       420,
        'popularity':     88,
        'ingredients': [
            ('ไก่',               '300 กรัม',     True),
            ('พริกแกงเขียวหวาน',  '3 ช้อนโต๊ะ',   True),
            ('กะทิ',               '400 มล.',      True),
            ('ใบมะกรูด',           '5 ใบ',         True),
            ('น้ำปลา',             '2 ช้อนโต๊ะ',   True),
            ('น้ำตาล',             '1 ช้อนโต๊ะ',   True),
            ('น้ำมันพืช',          '2 ช้อนโต๊ะ',   True),
        ],
        'steps': [
            'ตั้งกระทะบนไฟกลาง ใส่น้ำมันพืช',
            'ผัดพริกแกงให้หอม ประมาณ 2 นาที',
            'ใส่กะทิครึ่งส่วนลงไป คนให้เข้ากัน',
            'ใส่ไก่ลงผัดให้สุก',
            'เทกะทิที่เหลือลงไป ตามด้วยน้ำ ปรุงรสด้วยน้ำปลาและน้ำตาล',
            'ใส่ใบมะกรูด ต้มไฟอ่อนๆ ประมาณ 10 นาที เสิร์ฟพร้อมข้าวสวย',
        ],
    },
    {
        'name':           'ผัดซีอิ๊วหมู',
        'description':    'ก๋วยเตี๋ยวผัดซีอิ๊วเส้นใหญ่ หอมซีอิ๊วดำ เส้นนุ่ม อร่อยคลาสสิก',
        'cooking_time':   15,
        'difficulty':     'medium',
        'category':       'street',
        'cooking_method': 'stirfry',
        'is_spicy':       False,
        'calories':       520,
        'popularity':     87,
        'ingredients': [
            ('เส้นใหญ่',   '200 กรัม',     True),
            ('หมูสไลซ์',   '150 กรัม',     True),
            ('ผักคะน้า',   '100 กรัม',     True),
            ('ไข่',        '1 ฟอง',        True),
            ('ซีอิ๊วดำ',   '2 ช้อนโต๊ะ',   True),
            ('ซีอิ๊วขาว',  '1 ช้อนโต๊ะ',   True),
            ('น้ำตาล',     '1 ช้อนชา',     True),
            ('น้ำมันพืช',  '3 ช้อนโต๊ะ',   True),
        ],
        'steps': [
            'แช่เส้นใหญ่ในน้ำเย็นให้นิ่ม แยกเส้นออกจากกัน',
            'ตั้งกระทะบนไฟแรง ใส่น้ำมันให้ร้อน',
            'ผัดหมูสไลซ์จนสุก',
            'เขี่ยหมูออก ตอกไข่ลงกระทะ คนพอสุก',
            'ใส่เส้นใหญ่และผักคะน้า ปรุงรสด้วยซีอิ๊วดำ ซีอิ๊วขาว น้ำตาล ผัดให้เข้ากัน เสิร์ฟทันที',
        ],
    },
    {
        'name':           'ส้มตำไทย',
        'description':    'ส้มตำสูตรอีสาน รสจัดจ้าน เปรี้ยวหวานเค็มเผ็ด สดชื่นทุกคำ',
        'cooking_time':   10,
        'difficulty':     'easy',
        'category':       'thai',
        'cooking_method': 'salad',
        'is_spicy':       True,
        'calories':       120,
        'popularity':     82,
        'ingredients': [
            ('มะละกอเขียว', '300 กรัม',     True),
            ('กระเทียม',    '3 กลีบ',       True),
            ('พริก',        '5 เม็ด',       True),
            ('น้ำปลา',      '2 ช้อนโต๊ะ',   True),
            ('มะนาว',       '2 ลูก',        True),
            ('น้ำตาล',      '1 ช้อนโต๊ะ',   True),
            ('ถั่วฝักยาว',  '5 เส้น',       True),
            ('มะเขือเทศ',   '1 ลูก',        True),
        ],
        'steps': [
            'โขลกกระเทียมและพริกในครกให้พอแตก',
            'ใส่ถั่วฝักยาวหั่นท่อน โขลกเบาๆ',
            'ใส่มะเขือเทศหั่น โขลกพอแตก',
            'ใส่มะละกอขูด ปรุงรสด้วยน้ำปลา น้ำตาล มะนาว คลุกให้เข้ากัน ชิมรส เสิร์ฟทันที',
        ],
    },
]


class Command(BaseCommand):
    help = 'สร้างข้อมูลตัวอย่างวัตถุดิบและเมนูอาหารไทย'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='ลบข้อมูลเดิมทั้งหมดก่อนสร้างใหม่',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  กำลังลบข้อมูลเดิม...')
            RecipeStep.objects.all().delete()
            RecipeIngredient.objects.all().delete()
            Recipe.objects.all().delete()
            Ingredient.objects.all().delete()
            self.stdout.write(self.style.WARNING('ลบข้อมูลเดิมเรียบร้อย'))

        # ---- สร้างวัตถุดิบ ----
        self.stdout.write('\n🥩 กำลังสร้างวัตถุดิบ...')
        ingredient_map: dict[str, Ingredient] = {}

        for data in INGREDIENTS:
            obj, created = Ingredient.objects.get_or_create(
                name=data['name'],
                defaults={'category': data['category']},
            )
            ingredient_map[obj.name] = obj
            status = 'สร้างใหม่' if created else 'มีอยู่แล้ว'
            self.stdout.write(f'  {"✅" if created else "⏭️ "} {obj.name} ({status})')

        self.stdout.write(self.style.SUCCESS(f'\nสร้างวัตถุดิบครบ {len(ingredient_map)} รายการ'))

        # ---- สร้างเมนู ----
        self.stdout.write('\n🍜 กำลังสร้างเมนูอาหาร...')

        for recipe_data in RECIPES:
            recipe, created = Recipe.objects.get_or_create(
                name=recipe_data['name'],
                defaults={
                    'description':    recipe_data['description'],
                    'cooking_time':   recipe_data['cooking_time'],
                    'difficulty':     recipe_data['difficulty'],
                    'category':       recipe_data['category'],
                    'cooking_method': recipe_data['cooking_method'],
                    'is_spicy':       recipe_data['is_spicy'],
                    'calories':       recipe_data.get('calories'),
                    'popularity':     recipe_data['popularity'],
                    'is_active':      True,
                },
            )

            if created:
                # เพิ่มวัตถุดิบ
                for ing_name, quantity, is_required in recipe_data['ingredients']:
                    if ing_name in ingredient_map:
                        RecipeIngredient.objects.get_or_create(
                            recipe=recipe,
                            ingredient=ingredient_map[ing_name],
                            defaults={
                                'quantity':    quantity,
                                'is_required': is_required,
                            },
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠️  ไม่พบวัตถุดิบ: {ing_name}')
                        )

                # เพิ่มขั้นตอน
                for idx, instruction in enumerate(recipe_data['steps'], start=1):
                    RecipeStep.objects.get_or_create(
                        recipe=recipe,
                        step_number=idx,
                        defaults={'instruction': instruction},
                    )

                self.stdout.write(f'  ✅ สร้างเมนู: {recipe.name}')
            else:
                self.stdout.write(f'  ⏭️  มีอยู่แล้ว: {recipe.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 เสร็จสิ้น! สร้างข้อมูลครบทั้งหมด\n'
                f'   วัตถุดิบ: {Ingredient.objects.count()} รายการ\n'
                f'   เมนูอาหาร: {Recipe.objects.count()} เมนู\n'
            )
        )
