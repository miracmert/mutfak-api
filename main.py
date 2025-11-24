from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import scraper  # scraper.py dosyasını içe aktarıyoruz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def baglanti_kur():
    conn = sqlite3.connect('mutfak.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Mutfak Asistanı API Yayında! 🚀"}

@app.get("/urunler")
def urunleri_getir():
    # Veritabanı yoksa oluştur (İlk kurulum için)
    scraper.veritabani_kur()
    
    conn = baglanti_kur()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM urunler ORDER BY fiyat ASC")
        urunler = cursor.fetchall()
        return {"data": urunler}
    except sqlite3.OperationalError:
        return {"data": [], "mesaj": "Veritabanı boş, önce /guncelle adresine gidin."}
    finally:
        conn.close()

# Bu endpoint sunucudaki scraper'ı tetikler
@app.get("/guncelle")
def verileri_guncelle(background_tasks: BackgroundTasks):
    def gorev():
        print("Veri güncelleme başladı...")
        scraper.veritabani_kur()
        # Temel ürünleri tara
        liste = ["yumurta", "süt", "peynir", "yoğurt", "yağ", "makarna", "tavuk", "ekmek"]
        for urun in liste:
            scraper.veri_cek(urun)
        print("Veri güncelleme tamamlandı.")

    background_tasks.add_task(gorev)
    return {"mesaj": "Veri güncelleme işlemi arka planda başlatıldı. 1-2 dakika sürebilir."}
