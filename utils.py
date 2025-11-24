# Bu dosya ürünleri analiz edip kategori ve besin değeri atar.
# Gerçek bir AI modeli yerine kural tabanlı (heuristic) hızlı bir motor yazdım.

def urun_analiz_et(isim):
    isim = isim.lower()
    
    # Varsayılan Değerler
    etiketler = []
    kategori = "Diğer"
    kalori = 0  # Ortalama 100g/ml için
    
    # 1. Kategori ve Kalori Analizi
    if any(x in isim for x in ["yumurta"]):
        kategori = "Protein"
        etiketler.extend(["keto", "vegetarian", "gluten_free"])
        kalori = 155
    elif any(x in isim for x in ["tavuk", "piliç", "kanat", "göğüs", "bonfile"]):
        kategori = "Protein"
        etiketler.extend(["keto", "paleo", "gluten_free"])
        kalori = 165
    elif any(x in isim for x in ["kıyma", "dana", "köfte", "sucuk", "salam"]):
        kategori = "Protein"
        etiketler.extend(["keto", "paleo"])
        kalori = 250
    elif any(x in isim for x in ["süt", "yoğurt", "ayran", "kefir", "peynir", "labne"]):
        kategori = "Protein"
        etiketler.extend(["vegetarian", "gluten_free"])
        if "vegan" not in isim: etiketler.append("dairy") # Alerjen
        kalori = 60
    elif any(x in isim for x in ["makarna", "erişte", "mantı"]):
        kategori = "Karb"
        etiketler.extend(["vegan"])
        if "glutensiz" not in isim: etiketler.append("gluten") # Alerjen
        kalori = 350
    elif any(x in isim for x in ["pirinç", "bulgur", "mercimek", "nohut", "fasulye"]):
        kategori = "Karb"
        etiketler.extend(["vegan", "gluten_free"])
        kalori = 130
    elif any(x in isim for x in ["domates", "salatalık", "biber", "patlıcan", "kabak", "soğan", "patates", "maydanoz", "marul"]):
        kategori = "Sebze"
        etiketler.extend(["vegan", "keto", "paleo", "gluten_free"])
        kalori = 30
    elif any(x in isim for x in ["elma", "muz", "portakal", "çilek", "karpuz", "üzüm"]):
        kategori = "Meyve"
        etiketler.extend(["vegan", "paleo", "gluten_free"])
        kalori = 50
    elif any(x in isim for x in ["yağ", "zeytinyağı", "ayçiçek"]):
        kategori = "Temel"
        etiketler.extend(["vegan", "keto", "gluten_free"])
        kalori = 880
    elif any(x in isim for x in ["su", "soda", "meyve suyu", "kola", "gazoz"]):
        kategori = "İçecek"
        etiketler.extend(["vegan", "gluten_free"])
        kalori = 40
        
    return {
        "category": kategori,
        "tags": etiketler,
        "calorie": kalori
    }
