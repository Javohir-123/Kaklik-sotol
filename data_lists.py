# Barcha kategoriyalar va ularning ichidagi bo'limlar shu yerda saqlanadi.
# Kengaytirish kerak bo'lsa faqat shu faylni tahrirlash kifoya.

CATEGORIES = {
    "parrandalar": {
        "title": "🐔 Parrandalar",
        "items": {
            "tovuq": "🐔 Tovuq",
            "xoroz": "🐓 Xo'roz",
            "joja": "🐤 Jo'ja",
            "kaklik": "🦃 Kaklik",
            "bedana": "🐦 Bedana",
            "kurka": "🦃 Kurka",
            "ordak": "🦆 O'rdak",
            "goz": "🦢 G'oz",
            "boshqa_parranda": "➕ Boshqa parranda",
        }
    },
    "qora_mol": {
        "title": "🐄 Qora mol",
        "items": {
            "sigir": "🐄 Sigir",
            "buzoq": "🐮 Buzoq",
            "buqa": "🐂 Buqa",
            "ho'kiz": "🐃 Ho'kiz",
            "boshqa_mol": "➕ Boshqa",
        }
    },
    "qoy": {
        "title": "🐑 Qo'y",
        "items": {
            "qoy": "🐑 Qo'y (urg'ochi)",
            "qochqor": "🐏 Qo'chqor",
            "qozi": "🐑 Qo'zi",
            "echki": "🐐 Echki",
            "boshqa_qoy": "➕ Boshqa",
        }
    },
    "ot": {
        "title": "🐎 Ot",
        "items": {
            "ot": "🐎 Ot (erkak)",
            "biya": "🐴 Biya (urg'ochi)",
            "toy": "🐴 Toy",
            "eshak": "🫏 Eshak",
            "boshqa_ot": "➕ Boshqa",
        }
    },
    "mashina": {
        "title": "🚗 Mashina",
        "items": {
            "yengil": "🚗 Yengil avtomobil",
            "yuk": "🚚 Yuk mashinasi",
            "avtobus": "🚌 Avtobus",
            "moto": "🏍 Mototsikl",
            "traktor": "🚜 Traktor / qishloq texnikasi",
            "boshqa_mashina": "➕ Boshqa",
        }
    },
    "boshqa_hayvon": {
        "title": "🐾 Boshqa hayvonlar",
        "items": {
            "it": "🐕 It",
            "mushuk": "🐈 Mushuk",
            "quyon": "🐇 Quyon",
            "baliq": "🐟 Baliq (akvarium)",
            "asalari": "🐝 Asalari (ari oilasi)",
            "boshqa": "➕ Boshqa",
        }
    },
}

# Jins tanlash uchun
GENDERS = ["Erkak", "Urg'ochi", "Aniqlanmagan"]

# Qaysi kategoriyalarda "jinsi" so'raladi (faqat jonli mavjudotlar uchun).
# Mashina va shunga o'xshash jonsiz narsalar uchun jins so'ralmaydi.
CATEGORIES_WITH_GENDER = {"parrandalar", "qora_mol", "qoy", "ot", "boshqa_hayvon"}

# Ish e'lonlari turlari
JOB_TYPES = {
    "ish_berish": "🧑‍💼 Ish berish (xodim kerak)",
    "ishlash": "👷 Ishlash (ish qidiryapman)",
}

# O'zbekiston viloyatlari (ish e'lonlari uchun)
REGIONS = {
    "toshkent_shahar": "🏙 Toshkent shahri",
    "toshkent_viloyat": "Toshkent viloyati",
    "andijon": "Andijon",
    "fargona": "Farg'ona",
    "namangan": "Namangan",
    "samarqand": "Samarqand",
    "buxoro": "Buxoro",
    "navoiy": "Navoiy",
    "qashqadaryo": "Qashqadaryo",
    "surxondaryo": "Surxondaryo",
    "jizzax": "Jizzax",
    "sirdaryo": "Sirdaryo",
    "xorazm": "Xorazm",
    "qoraqalpogiston": "Qoraqalpog'iston",
}

# Har bir viloyat/hudud ichidagi tumanlar (shaharlar).
# Foydalanuvchi viloyatni tanlagach, shu ro'yxatdan tuman tanlaydi.
DISTRICTS = {
    "toshkent_shahar": [
        "Bektemir", "Chilonzor", "Yakkasaroy", "Mirzo Ulug'bek", "Mirobod",
        "Olmazor", "Sergeli", "Shayxontohur", "Uchtepa", "Yashnobod", "Yunusobod", "Yangihayot",
    ],
    "toshkent_viloyat": [
        "Bekobod", "Bo'ka", "Bo'stonliq", "Chinoz", "Ohangaron", "Oqqo'rg'on",
        "Parkent", "Piskent", "Qibray", "Quyichirchiq", "Toshkent tumani",
        "O'rtachirchiq", "Yangiyo'l", "Zangiota", "Yuqorichirchiq",
    ],
    "andijon": [
        "Andijon shahri", "Andijon tumani", "Asaka", "Baliqchi", "Bo'z", "Buloqboshi",
        "Izboskan", "Jalaquduq", "Xo'jaobod", "Qo'rg'ontepa", "Marhamat",
        "Oltinko'l", "Paxtaobod", "Shahrixon", "Ulug'nor", "Xonobod",
    ],
    "fargona": [
        "Farg'ona shahri", "Marg'ilon", "Qo'qon", "Farg'ona tumani", "Bag'dod", "Beshariq",
        "Buvayda", "Dang'ara", "Furqat", "Oltiariq", "Quva", "Quvasoy", "Rishton",
        "So'x", "Toshloq", "O'zbekiston", "Uchko'prik", "Yozyovon",
    ],
    "namangan": [
        "Namangan shahri", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Namangan tumani",
        "Norin", "Pop", "To'raqo'rg'on", "Uchqo'rg'on", "Uychi", "Yangiqo'rg'on",
    ],
    "samarqand": [
        "Samarqand shahri", "Bulung'ur", "Ishtixon", "Jomboy", "Kattaqo'rg'on", "Kattaqo'rg'on shahri",
        "Narpay", "Nurobod", "Oqdaryo", "Payariq", "Paxtachi", "Pastdarg'om",
        "Qo'shrabot", "Samarqand tumani", "Toyloq", "Urgut",
    ],
    "buxoro": [
        "Buxoro shahri", "Buxoro tumani", "G'ijduvon", "Jondor", "Kogon", "Kogon tumani",
        "Olot", "Peshku", "Qorako'l", "Qorovulbozor", "Romitan", "Shofirkon", "Vobkent",
    ],
    "navoiy": [
        "Navoiy shahri", "Zarafshon", "Karmana", "Konimex", "Navbahor", "Nurota",
        "Qiziltepa", "Tomdi", "Uchquduq", "Xatirchi",
    ],
    "qashqadaryo": [
        "Qarshi shahri", "Koson", "Kasbi", "Kitob", "Chiroqchi", "Dehqonobod",
        "G'uzor", "Mirishkor", "Muborak", "Nishon", "Qamashi", "Qarshi tumani",
        "Shahrisabz", "Yakkabog'",
    ],
    "surxondaryo": [
        "Termiz shahri", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo'rg'on",
        "Muzrabot", "Oltinsoy", "Qiziriq", "Qumqo'rg'on", "Sariosiyo",
        "Sherobod", "Sho'rchi", "Termiz tumani", "Uzun",
    ],
    "jizzax": [
        "Jizzax shahri", "Arnasoy", "Baxmal", "Do'stlik", "Forish", "G'allaorol",
        "Sharof Rashidov", "Yangiobod", "Zafarobod", "Zarbdor", "Zomin", "Mirzacho'l", "Paxtakor",
    ],
    "sirdaryo": [
        "Guliston shahri", "Boyovut", "Guliston tumani", "Mirzaobod", "Oqoltin",
        "Sardoba", "Sayxunobod", "Sirdaryo", "Xovos", "Yangiyer", "Shirin",
    ],
    "xorazm": [
        "Urganch shahri", "Bog'ot", "Gurlan", "Xiva", "Xonqa", "Qo'shko'pir",
        "Shovot", "Urganch tumani", "Yangiariq", "Yangibozor", "Tuproqqal'a",
    ],
    "qoraqalpogiston": [
        "Nukus shahri", "Amudaryo", "Beruniy", "Chimboy", "Ellikqal'a", "Kegeyli",
        "Mo'ynoq", "Nukus tumani", "Qanliko'l", "Qorao'zak", "Qo'ng'irot",
        "Shumanay", "Taxtako'pir", "To'rtko'l", "Xo'jayli",
    ],
}


def get_category_title(cat_key: str) -> str:
    return CATEGORIES.get(cat_key, {}).get("title", cat_key)


def get_item_title(cat_key: str, item_key: str) -> str:
    return CATEGORIES.get(cat_key, {}).get("items", {}).get(item_key, item_key)
