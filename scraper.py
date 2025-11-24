import requests
import json
from datetime import datetime
from utils import urun_analiz_et

def market_fiyatlari_getir(lat, lon, arama_terimi=""):
    """
    Belirtilen konum ve arama terimine göre canlı market verisi çeker.
    Eğer arama_terimi boşsa, temel gıdaları tarar.
    """
    
    url = "https://api.marketfiyati.org.tr/api/v2/search"
    
    # Eğer özel bir arama yoksa 'temel' kelimesiyle genel tarama yapalım
    keyword = arama_terimi if arama_terimi else "süt yumurta ekmek"
    
    payload = {
        "keywords": keyword,
        "pages": 0,
        "size": 100, # Daha fazla ürün
        "latitude": float(lat),
        "longitude": float(lon),
        "distance": 2, # 2 km çapındaki marketler
        "depots": [] # Boş bırakarak çevredeki tüm marketleri hedefliyoruz
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    print(f"📡 İstek atılıyor: {keyword} @ {lat}, {lon}")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            raw_products = data.get("content", [])
            
            processed_products = []
            
            for item in raw_products:
                # Fiyat ve Market Bilgisi
                depot_info = item.get("productDepotInfoList", [])
                if not depot_info: continue
                
                # En uygun fiyatı bul
                best_price_info = min(depot_info, key=lambda x: x.get("price", 999999))
                
                name = item.get("title", "Ürün")
                price = best_price_info.get("price", 0)
                market = best_price_info.get("marketAdi", "Yerel Market")
                image = item.get("imageUrl", "")
                
                # Yapay Zeka ile Etiketle (Utils.py)
                analiz = urun_analiz_et(name)
                
                product_obj = {
                    "id": item.get("id"),
                    "name": name,
                    "price": price,
                    "unit": item.get("unitCode", "adet"),
                    "store": market,
                    "image": image,
                    "category": analiz["category"],
                    "calorie": analiz["calorie"],
                    "tags": analiz["tags"],
                    "basePrice": price # Frontend uyumluluğu için
                }
                
                processed_products.append(product_obj)
                
            print(f"✅ {len(processed_products)} ürün bulundu ve işlendi.")
            return processed_products
            
        else:
            print(f"❌ API Hatası: {response.status_code}")
            return []

    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")
        return []
