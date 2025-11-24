from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import scraper

app = FastAPI()

# CORS Ayarları (React uygulamasının erişebilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "active", "message": "Akıllı Mutfak API v2.0 (Live)"}

@app.get("/api/search")
def search_products(
    lat: float, 
    lon: float, 
    q: Optional[str] = None
):
    """
    Frontend'den gelen konuma göre gerçek zamanlı ürün araması yapar.
    Örnek: /api/search?lat=41.0082&lon=28.9784&q=yumurta
    """
    results = scraper.market_fiyatlari_getir(lat, lon, q)
    return {
        "location": {"lat": lat, "lon": lon},
        "count": len(results),
        "data": results
    }
