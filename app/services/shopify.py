import httpx
from app.config import settings
from app.utils.logger import get_logger

log = get_logger("shopify")
BASE = f"https://{settings.SHOPIFY_STORE_DOMAIN}/admin/api/{settings.SHOPIFY_ADMIN_API_VERSION}"

def _headers():
    return {"X-Shopify-Access-Token": settings.SHOPIFY_ADMIN_API_KEY}

async def get_products(limit: int = 5):
    url = f"{BASE}/products.json?limit={limit}"
    log.info(f"Shopify GET {url}")
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json().get("products", [])

async def search_product_by_title(q: str, limit: int = 5):
    products = await get_products(limit=50)
    q_norm = q.lower()
    return [p for p in products if q_norm in p["title"].lower()][:limit]
