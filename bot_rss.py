import os
import json
import asyncio
import requests
import feedparser
import base64
import re
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# --- CONFIG ---
GROQ_KEY = os.environ["GROQ_KEY"]
TG_TOKEN = os.environ["TELEGRAM_TOKEN"]
TG_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
RSS_URL = "https://el-periodico.com.ar/rss.xml"
PUBLICADOS_FILE = "publicados.json"

# --- ESTADO ---
def cargar_publicados():
    if not os.path.exists(PUBLICADOS_FILE): return []
    try:
        with open(PUBLICADOS_FILE, "r") as f: return json.load(f)
    except: return []

def guardar_publicados(ids):
    with open(PUBLICADOS_FILE, "w") as f: json.dump(ids, f)

# --- SCRAPING Y UTILIDADES ---
async def extraer_texto_noticia(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=['--no-sandbox'])
            page = await browser.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(3)
            html = await page.content()
            await browser.close()
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['nav', 'footer', 'aside', 'script', 'style', 'header']): tag.decompose()
        parrafos = soup.find_all('p')
        texto = ' '.join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)
        return texto[:3000] if len(texto) > 100 else ""
    except: return ""

def mejorar_resolucion_imagen(url):
    if not url: return ""
    if 'tadevel-cdn.com' in url:
        url = re.sub(r'/(\d+)\.(webp|jpg|jpeg|png)', r'/1200.\2', url)
    url = re.sub(r'width=\d+', 'width=1200', url)
    url = re.sub(r'height=\d+', 'height=1200', url)
    return url

def imagen_a_base64(url):
    if not url: return None
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if res.status_code == 200:
            ext = 'jpeg'
            ct = res.headers.get('content-type', '')
            if 'png' in ct: ext = 'png'
            elif 'webp' in ct: ext = 'webp'
            b64 = base64.b64encode(res.content).decode()
            return f"data:image/{ext};base64,{b64}"
    except: pass
    return None

def extraer_imagen_jsonld(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        img_url = ""
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                images = data.get("image", [])
                if isinstance(images, list) and images:
                    if all(isinstance(x, str) for x in images): img_url = images[0]
                    else:
                        best = max((x for x in images if isinstance(x, dict)), key=lambda x: x.get("width", 0), default=None)
                        if best: img_url = best.get("url", "")
                elif isinstance(images, dict): img_url = images.get("url", "")
                elif isinstance(images, str): img_url = images
                if img_url: break
            except: continue
        
        if not img_url:
            og = soup.find("meta", property="og:image")
            img_url = og["content"] if og else ""
        return img_url
    except: return ""

# --- GROQ ---
def redactar_copy(titulo, link, texto_noticia=""):
    url = "https://api.groq.com/openai/v1/chat/completions"
    fuente = f"TEXTO DE LA NOTICIA:\n{texto_noticia}" if texto_noticia else f"TÍTULO: {titulo}"
    prompt = (
        f"Sos editor periodístico de El Periódico de San Francisco, Córdoba. "
        f"Redactá un copy para redes sociales basándote en esta información:\n\n{fuente}\n\n"
        f"Usá solo la información provista, sin inventar datos, contexto ni detalles que no estén en la fuente. "
        f"Español argentino directo, sin tiempos compuestos (usá 'fue' no 'ha sido'), "
        f"sin adjetivos valorativos ni sensacionalismo. Hasta 3 párrafos cortos, sin repetir ideas. "
        f"Al final agregá dos saltos de línea y luego: '👉 Más información en la web de El Periódico. Link en las historias.\n{link}' "
        f"Sin negritas."
    )
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 500}
    try:
        res = requests.post(url, json=payload, headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}, timeout=15)
        if res.status_code == 200 and 'choices' in res.json():
            return res.json()['choices'][0]['message']['content']
        return None
    except: return None

# --- PLACAS ---
def get_base64_logo(file_path="logo.png"):
    try:
        with open(file_path, "rb") as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except: return ""

async def generar_placas(titulo, bg_img):
    logo_data = get_base64_logo()
    bg_style = f"background: url('{bg_img}') no-repeat center center; background-size: cover;" if bg_img else "background: #1a1a1a;"

    h_feed = f"""
    <html><head><style>@font-face {{ font-family: 'ArialNova'; src: url('ArialNova-Bold.ttf') format('truetype'); font-weight: 700; }}</style></head>
    <style>
        body {{ margin: 0; padding: 0; font-family: 'ArialNova', sans-serif; }}
        .canvas {{ width: 1080px; height: 1350px; {bg_style} display: flex; flex-direction: column; justify-content: flex-end; }}
        .overlay {{ background: linear-gradient(to top, rgba(14,100,46,0.9) 0%, rgba(14,100,46,0.7) 35%, transparent 100%); padding: 110px 90px; color: white; }}
        h1 {{ font-size: 48pt; margin: 0 0 55px 0; line-height: 1.0; font-weight: 700; letter-spacing: 0.5px; text-shadow: 2px 2px 12px rgba(0,0,0,0.9), 0px 0px 20px rgba(0,0,0,0.7); }}
        .logo-container {{ text-align: center; width: 100%; }}
        .logo-img {{ height: 58px; filter: brightness(0) invert(1); }}
    </style>
    <body><div class='canvas'><div class='overlay'><h1>{titulo}</h1><div class='logo-container'><img src='{logo_data}' class='logo-img'></div></div></div></body></html>
    """

    h_story = f"""
    <html><head><link href='https://fonts.googleapis.com/css2?family=PT+Serif:wght@700&display=swap' rel='stylesheet'></head>
    <style>
        body {{ margin: 0; padding: 0; background: white; font-family: 'PT Serif', serif; }}
        .wrapper {{ width: 1080px; height: 1920px; display: block; padding-top: 200px; }}
        .header-logo {{ height: 83px; display: block; margin-left: 24px; margin-bottom: 36px; }}
        .image-frame {{ width: 900px; height: 800px; margin: 0 auto; {bg_style} border-radius: 30px; }}
        .text-container {{ width: 900px; margin: 35px auto 0 auto; display: flex; flex-direction: column; }}
        h1 {{ font-size: 46pt; line-height: 1.0; color: #1a1a1a; margin: 0; padding-bottom: 30px; font-weight: 400; }}
        .footer {{ border-top: 3px solid #333333; width: 60%; margin: 30px auto 0 auto; padding-top: 30px; text-align: center; font-size: 45px; font-family: sans-serif; color: #333; }}
        .green-arrow {{ color: #0e642e; font-size: 55px; }}
    </style>
    <body><div class='wrapper'><img src='{logo_data}' class='header-logo'><div class='image-frame'></div><div class='text-container'><h1>{titulo}</h1><div class='footer'>Leé más <span class='green-arrow'>▼</span></div></div></div></body></html>
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        p_f = await browser.new_page(viewport={'width': 1080, 'height': 1350}); await p_f.set_content(h_feed); await asyncio.sleep(2); await p_f.screenshot(path="FEED.jpg")
        p_s = await browser.new_page(viewport={'width': 1080, 'height': 1920}); await p_s.set_content(h_story); await asyncio.sleep(2); await p_s.screenshot(path="STORY.jpg")
        await browser.close()

# --- TELEGRAM ---
def enviar_telegram(copy_texto):
    media = [{"type": "photo", "media": "attach://f", "caption": copy_texto, "parse_mode": "HTML"}, {"type": "photo", "media": "attach://s"}]
    try:
        with open("FEED.jpg", "rb") as f, open("STORY.jpg", "rb") as s:
            res = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMediaGroup", data={"chat_id": TG_CHAT_ID, "media": json.dumps(media)}, files={"f": f, "s": s}, timeout=30)
        if res.status_code == 200 and res.json().get("ok"):
            print(f"✅ Enviado: {copy_texto[:60]}...")
            return True
        else:
            print(f"❌ Error Telegram: {res.json().get('description', 'sin detalle')}")
            return False
    except Exception as e:
        print(f"❌ Excepción al enviar: {str(e)}")
        return False

# --- MAIN ---
async def main():
    publicados = cargar_publicados()
    feed = feedparser.parse(RSS_URL)
    if not feed.entries: return

    nuevos = 0
    for entry in feed.entries[:10]:
        entry_id = getattr(entry, 'id', entry.link)
        if entry_id in publicados: continue

        titulo, link = entry.title, entry.link
        if any(p in link.lower() for p in ["necrologicas", "quiniela-de-cordoba-hoy"]):
            publicados.append(entry_id); continue

        print(f"Nueva noticia: {titulo}")

        # Extracción de imagen robusta
        img_url_raw = entry.enclosures[0].url if hasattr(entry, 'enclosures') and entry.enclosures else extraer_imagen_jsonld(link)
        if not img_url_raw:
            print(f"Sin imagen para: {titulo}, saltando.")
            publicados.append(entry_id); continue

        img_b64 = imagen_a_base64(mejorar_resolucion_imagen(img_url_raw)) or imagen_a_base64(img_url_raw)
        final_fondo = img_b64 if img_b64 else img_url_raw

        await generar_placas(titulo, final_fondo)
        texto_noticia = await extraer_texto_noticia(link)

        copy = redactar_copy(titulo, link, texto_noticia) or f"{titulo}\n\n🔗 {link}"
        partes = copy.rsplit(link, 1)
        cuerpo = partes[0] if len(partes) > 1 else copy
        cuerpo = cuerpo.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        pie = f"\n{link}"
        limite = 1024 - len(pie)
        if len(cuerpo) > limite: cuerpo = cuerpo[:limite - 3] + '...'
        copy_final = cuerpo + pie

        if enviar_telegram(copy_final):
            publicados.append(entry_id)
            nuevos += 1
        await asyncio.sleep(5)

    guardar_publicados(publicados[-50:])
    print(f"Proceso terminado. Nuevas publicadas: {nuevos}")

if __name__ == "__main__":
    asyncio.run(main())
