from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Bu ayar, ileride yapacağımız mobil uygulamanın 
# bu API'ye erişmesine izin verir (Güvenlik kilidini açar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def baglanti_kur():
    conn = sqlite3.connect('mutfak.db')
    conn.row_factory = sqlite3.Row # Verileri sözlük gibi (isim: süt) almak için
    return conn

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Mutfak Asistanı API Yayında! 🚀"}

# 1. Tüm Ürünleri Listele
@app.get("/urunler")
def urunleri_getir():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urunler ORDER BY fiyat ASC")
    urunler = cursor.fetchall()
    conn.close()
    return {"data": urunler}

# 2. Arama Yap (Örn: /ara/yumurta)
@app.get("/ara/{kelime}")
def urun_ara(kelime: str):
    conn = baglanti_kur()
    cursor = conn.cursor()
    # SQL içinde arama yapıyoruz (% işareti 'içinde geçen' demek)
    cursor.execute("SELECT * FROM urunler WHERE isim LIKE ? ORDER BY fiyat ASC", ('%' + kelime + '%',))
    sonuclar = cursor.fetchall()
    conn.close()
    return {"sonuc_sayisi": len(sonuclar), "data": sonuclar}