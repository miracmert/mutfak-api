import requests
import sqlite3
import json
from datetime import datetime

# --- AYARLAR ---
DB_NAME = "mutfak.db"

def veritabani_kur():
    """Veritabanını ve tabloyu oluşturur"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Eğer tablo yoksa oluştur, varsa dokunma
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT,
            fiyat REAL,
            market TEXT,
            marka TEXT,
            resim TEXT,
            tarih TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Veritabanı kontrol edildi.")

def veri_cek(aranacak_kelime):
    print(f"\n📡 '{aranacak_kelime}' için güncel fiyatlar taranıyor...")
    
    url = "https://api.marketfiyati.org.tr/api/v2/search"
    
    # Senin çalışan sihirli anahtarın
    payload = {
        "keywords": aranacak_kelime,
        "pages": 0,
        "size": 50, # 50 ürün çekelim
        "latitude": 40.9908760778212,
        "longitude": 28.8752998883946,
        "distance": 1,
        "depots": [
            "sok-614", "sok-7188", "bim-H819", "sok-7169", "sok-698", 
            "a101-0457", "sok-2972", "a101-G635", "tarim_kredi-7390", 
            "migros-5675", "migros-3863", "a101-0089", "bim-H817", 
            "a101-H233", "bim-H823", "migros-6404", "migros-7137", 
            "a101-0181", "bim-J829", "bim-H822", "carrefour-3002"
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            veri = response.json()
            
            # Attığın veriye göre ürünler 'content' listesinin içinde
            if "content" in veri:
                urun_listesi = veri["content"]
            else:
                print("⚠️ Uyarı: Ürün listesi bulunamadı.")
                return

            print(f"📥 Toplam {len(urun_listesi)} ürün bulundu. İşleniyor...")
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            sayac = 0
            for urun in urun_listesi:
                # 1. Ürün Adını Alıyoruz
                isim = urun.get("title", "İsimsiz Ürün")
                
                # 2. Marka ve Resim
                marka = urun.get("brand", "")
                resim = urun.get("imageUrl", "")

                # 3. FİYAT KISMI (EN ÖNEMLİ YER)
                # Fiyat 'productDepotInfoList' içindeki ilk elemandadır.
                fiyat = 0
                market = "Bilinmiyor"
                
                depo_bilgisi = urun.get("productDepotInfoList", [])
                
                if len(depo_bilgisi) > 0:
                    # Listenin ilk elemanını al
                    detay = depo_bilgisi[0] 
                    fiyat = detay.get("price", 0)
                    market = detay.get("marketAdi", "Genel")
                
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M")

                # Sadece fiyatı 0 olmayanları kaydedelim
                if fiyat > 0:
                    cursor.execute("""
                        INSERT INTO urunler (isim, fiyat, market, marka, resim, tarih) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (isim, fiyat, market, marka, resim, tarih))
                    
                    sayac += 1
                    # Ekrana havalı bir çıktı verelim
                    print(f"   🛒 {market.upper()}: {isim[:30]}... -> {fiyat} TL")
            
            conn.commit()
            conn.close()
            print(f"\n✅ BAŞARILI! Toplam {sayac} adet güncel fiyat veritabanına eklendi.")
            
        else:
            print(f"❌ Site hatası: {response.status_code}")

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")

# --- PROGRAM BAŞLIYOR ---
if __name__ == "__main__":
    veritabani_kur()
    
    # Şimdi gerçek bir alışveriş listesi tarayalım
    aramalar = ["yumurta", "süt", "peynir", "yoğurt"]
    
    for urun in aramalar:
        veri_cek(urun)