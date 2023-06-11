import sqlite3
import random
import string
import qrcode
from PIL import Image

conn = sqlite3.connect('guests.sqlite3')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS guests
             (id INTEGER PRIMARY KEY, code TEXT, first_name TEXT, last_name TEXT, family TEXT, checked BOOLEAN DEFAULT False)''')

def generate_code():
    code = ''.join(random.choices(string.digits, k=12))
    c.execute("SELECT COUNT(*) FROM guests WHERE code=?", (code,))
    count = c.fetchone()[0]
    if count == 0:
        return code
    else:
        return generate_code()


def generate_qr_code(name, family_list):
    code = generate_code()
    family = ', '.join(family_list) if family_list else None
    c.execute("INSERT INTO guests (code, first_name, last_name, family, checked) VALUES (?, ?, ?, ?, ?)", (code, first_name, last_name, family, False))
    conn.commit()

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{name}.png")


name = input("Enter guest's full name: ")
try:
    first_name, last_name = name.split()
except ValueError:
    print('Please insert full name separated by space(i.e Girumsew Bezabeh)')
    quit()
family_str = input(
    "Enter family member names separated by comma (leave blank if none): ")
family_list = [f.strip() for f in family_str.split(',') if f.strip()]

generate_qr_code(name, family_list)

conn.close()
