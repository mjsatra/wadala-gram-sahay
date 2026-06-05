from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "wadala_secret"

def init_db():

    conn = sqlite3.connect("contacts.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS contacts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        category TEXT,

        name_en TEXT,

        name_gu TEXT,

        phone TEXT,

        area_en TEXT,

        area_gu TEXT

    )

    """)

    conn.commit()

    conn.close()

def get_contacts():

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            category,
            name_en,
            name_gu,
            phone,
            area_en,
            area_gu
        FROM contacts
    """)

    rows = cursor.fetchall()

    conn.close()

    contacts = {}

    for row in rows:

        category = row[1]

        person = {
            "id": row[0],
            "name_en": row[2],
            "name_gu": row[3],
            "phone": row[4],
            "area_en": row[5],
            "area_gu": row[6]
        }

        if category not in contacts:
            contacts[category] = []

        contacts[category].append(person)

    for category in contacts:

        contacts[category].sort(
            key=lambda x: x["name_en"].lower()
        )

    return contacts

def gujarati_number(number):

    eng = "0123456789"
    guj = "૦૧૨૩૪૫૬૭૮૯"

    table = str.maketrans(eng, guj)

    return str(number).translate(table)

# Sample Data
services = {
    "Plumber": [],
    "Electrician": [],
    "Carpenter": [],
    "Maid": [],
    "Doctor": [],
    "Ambulance": [],
    "Auto - Taxi": [],
    "Grocery Shop": [],
    "Milkman": [],
    "Water Supplier": [],
    "Internet/WiFi": [],
    "AC Repair": [],
    "Mobile Repair": [],
    "Bike Mechanic": [],
    "Temple Committee": [],
    "Help Line": [],
    "Security Guard": [],
    "School": [],
    "Blood Donor": [],
    "Gas Service": [],
    "Bhohanshala": [],
    "Vegetable Seller": [],
    "Tuffan Car": []

}

active_categories = [

   
    "Milkman",
    "Water Supplier",
    "Vegetable Seller",
    "Bhohanshala",
    "Grocery Shop",
    "Plumber",
    "Electrician",
    "Carpenter",
    "Auto - Taxi",
    "Tuffan Car",
    "Doctor",
    "Help Line"    
]

icons = {

    "Plumber": "🔧",
    "Electrician": "⚡",
    "Carpenter": "🔨",
    "Maid": "🧹",
    "Doctor": "🩺",
    "Ambulance": "🚑",
    "Auto - Taxi": "🚕",
    "Grocery Shop": "🛒",
    "Milkman": "🥛",
    "Water Supplier": "💧",
    "Internet/WiFi": "📶",
    "AC Repair": "❄️",
    "Mobile Repair": "📱",
    "Bike Mechanic": "🏍️",
    "Temple Committee": "🛕",
    "Help Line": "☎️",
    "Security Guard": "🛡️",
    "School": "🏫",
    "Blood Donor": "🩸",
    "Gas Service": "🔥",
    "Bhohanshala": "🍽️" ,
    "Vegetable Seller": "🌿",
    "Tuffan Car": "🚐"
}


translations = {

    "en": {

        "title": "Vadala Gram Sahay",

        "Plumber": "Plumber",
        "Electrician": "Electrician",
        "Carpenter": "Carpenter",
        "Maid": "Maid",
        "Doctor": "Doctor",
        "Ambulance": "Ambulance",
        "Auto - Taxi": "Auto - Taxi",
        "Grocery Shop": "Grocery Shop",
        "Milkman": "Milkman",
        "Water Supplier": "Water Supplier",
        "Internet/WiFi": "Internet/WiFi",
        "AC Repair": "AC Repair",
        "Mobile Repair": "Mobile Repair",
        "Bike Mechanic": "Bike Mechanic",
        "Temple Committee": "Temple Committee",
        "Help Line": "Help Line",
        "Security Guard": "Security Guard",
        "School": "School",
        "Blood Donor": "Blood Donor",
        "Gas Service": "Gas Service",
        "Bhohanshala": "Bhojanshala" ,
        "Vegetable Seller": "Vegetable Seller",
        "Tuffan Car": "Tuffan Car"
    },

    "gu": {

        "title": "વડાલા ગ્રામ સહાય",

        "Plumber": "પ્લમ્બર",
        "Electrician": "ઇલેક્ટ્રિશિયન",
        "Carpenter": "સુથાર",
        "Maid": "કામવાળી",
        "Doctor": "ડોક્ટર",
        "Ambulance": "એમ્બ્યુલન્સ",
        "Auto - Taxi": "રિક્ષા - ટેક્સી",
        "Grocery Shop": "કરિયાણું",
        "Milkman": "દૂધવાળા",
        "Water Supplier": "પાણી સપ્લાયર",
        "Internet/WiFi": "વાઈફાઈ",
        "AC Repair": "AC રિપેર",
        "Mobile Repair": "મોબાઈલ રિપેર",
        "Bike Mechanic": "બાઈક મિકેનિક",
        "Temple Committee": "મંદિર કમિટી",
        "Help Line": "હેલ્પલાઇન",
        "Security Guard": "સિક્યુરિટી",
        "School": "શાળા",
        "Blood Donor": "બ્લડ ડોનર",
        "Gas Service": "ગેસ સેવા",
        "Bhohanshala": "ભોજનસાળા",
        "Vegetable Seller": "શાકવાળા",
        "Tuffan Car": "તુફાન ગાડી"
    }
}


@app.route("/")
def home():

    lang = request.args.get("lang", "en")

    categories = active_categories

    return render_template(
        "index.html",
        categories=categories,
        t=translations[lang],
        lang=lang,
        icons=icons
    )


@app.route("/category/<name>")
def category(name):

    lang = request.args.get("lang", "en")

    contacts = get_contacts()

    people = contacts.get(name, [])

    return render_template(
        "category.html",
        category=name,
        people=people,
        lang=lang,
        gujarati_number=gujarati_number,
        t=translations[lang]
    )

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect("/login")

    contacts = get_contacts()

    categories = active_categories

    total_contacts = 0

    for category in contacts:
        total_contacts += len(contacts[category])

    return render_template(
        "admin.html",
        categories=categories,
        services=contacts,
        total_contacts=total_contacts
    )

@app.route("/save_contact", methods=["POST"])
def save_contact():

    conn = sqlite3.connect("contacts.db")

    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM contacts

        WHERE phone = ?
        AND category = ?

    """, (

        request.form["phone"],
        request.form["category"]

    ))

    existing_contact = cursor.fetchone()

    if existing_contact:

        conn.close()

        return redirect("/admin?duplicate=1")

    cursor.execute("""

    INSERT INTO contacts (

        category,
        name_en,
        name_gu,
        phone,
        area_en,
        area_gu

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        request.form["category"],
        request.form["name_en"],
        request.form["name_gu"],
        request.form["phone"],
        request.form["area_en"],
        request.form["area_gu"]

    ))

    conn.commit()

    conn.close()

    return redirect("/admin?saved=1")
    
@app.route("/update_contact", methods=["POST"])
def update_contact():

    conn = sqlite3.connect("contacts.db")

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE contacts

    SET

        category = ?,
        name_en = ?,
        name_gu = ?,
        phone = ?,
        area_en = ?,
        area_gu = ?

    WHERE id = ?

    """, (

        request.form["category"],
        request.form["name_en"],
        request.form["name_gu"],
        request.form["phone"],
        request.form["area_en"],
        request.form["area_gu"],
        request.form["contact_id"]

    ))

    conn.commit()
    conn.close()

    return redirect("/admin?updated=1")

@app.route("/delete_contact", methods=["POST"])
def delete_contact():

    conn = sqlite3.connect("contacts.db")

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM contacts

        WHERE id = ?

    """, (

        request.form["contact_id"],

    ))

    conn.commit()

    conn.close()

    return redirect("/admin?deleted=1")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form["password"]

        if password == "1234":

            session["admin"] = True

            return redirect("/admin")

        else:

            return render_template(
                "login.html",
                error="Wrong Password"
            )

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)