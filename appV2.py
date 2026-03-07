import nest_asyncio
nest_asyncio.apply()
import streamlit as st
import tempfile
import subprocess
import yt_dlp
import asyncio
from playwright.async_api import async_playwright
import requests
import feedparser
import base64
import os
import json
from bs4 import BeautifulSoup
import uuid

# --- CONFIGURACIÓN ---
GROQ_KEY = st.secrets["GROQ_KEY"]
TG_TOKEN = st.secrets["TELEGRAM_TOKEN"]
TG_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
RSS_URL = "https://el-periodico.com.ar/rss.xml"

st.set_page_config(page_title="Panel El Periódico", layout="wide")

# --- FUNCIONES CORE ---
def get_base64_logo(file_path):
    try:
        with open(file_path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except: return ""

def redactar_copy_custom(titulo, link="", texto=""):
    url = "https://api.groq.com/openai/v1/chat/completions"
    fuente = f"TEXTO DE LA NOTICIA:\n{texto}" if texto else f"TÍTULO: {titulo}"
    prompt = (
        f"Sos editor periodístico de El Periódico de San Francisco, Córdoba. "
        f"Redactá un copy para redes sociales basándote en esta información:\n\n{fuente}\n\n"
        f"Usá solo la información provista, sin inventar datos ni detalles que no estén en la fuente. "
        f"Español argentino directo, sin tiempos compuestos (usá 'fue' no 'ha sido'), "
        f"sin adjetivos valorativos ni sensacionalismo. "
        f"Redactá UN SOLO párrafo si la información no da para más. Solo usá 2 o 3 párrafos si hay información suficiente y distinta para cada uno. NUNCA repitas la misma idea con distintas palabras. "
        f"Al final agregá dos saltos de línea y luego: '👉 Más información en la web de El Periódico. Link en las historias.\n{'  ' + link if link else ''}' "
        f"Sin negritas."
    )
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 500
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        res_json = res.json()
        if res.status_code == 429:
            return "⚠️ Límite de Groq alcanzado. Esperá un momento y volvé a intentar."
        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        else:
            return f"Error API: {res_json.get('error', {}).get('message', 'Desconocido')}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def mejorar_resolucion_imagen(url):
    import re
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
        for tag in soup(['nav', 'footer', 'aside', 'script', 'style', 'header']):
            tag.decompose()
        parrafos = soup.find_all('p')
        texto = ' '.join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)
        return texto[:3000] if len(texto) > 100 else ""
    except:
        return ""

def extraer_datos_rapidos(url):
    """Extrae Título e Imagen Alta Res usando JSON-LD (síncrono y rápido)"""
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        tit = soup.find("meta", property="og:title")
        final_tit = tit["content"].split(" - ")[0].strip() if tit else "Noticia"
        
        img_url = ""
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                images = data.get("image", [])
                if isinstance(images, list) and images:
                    if all(isinstance(x, str) for x in images):
                        img_url = images[0]
                    else:
                        best = max((x for x in images if isinstance(x, dict)), key=lambda x: x.get("width", 0), default=None)
                        if best: img_url = best.get("url", "")
                elif isinstance(images, dict):
                    img_url = images.get("url", "")
                elif isinstance(images, str):
                    img_url = images
                if img_url: break
            except: continue
        
        if not img_url:
            og = soup.find("meta", property="og:image")
            img_url = og["content"] if og else ""
            
        return final_tit, img_url
    except:
        return "Noticia", ""

async def generar_placas(titulo, bg_img, sid="default"):
    os.system("playwright install chromium")
    logo_data = get_base64_logo("logo.png")
    bg_style = f"background: url('{bg_img}') no-repeat center center; background-size: cover;" if bg_img else "background: #1a1a1a;"

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        
        h_feed = f"""
        <html><head><style>@font-face {{ font-family: 'ArialNova'; src: url('ArialNova-Bold.ttf') format('truetype'); font-weight: 700; }}</style></head>
        <style>
            body {{ margin: 0; padding: 0; font-family: 'ArialNova', sans-serif; }}
            .canvas {{ width: 1080px; height: 1350px; {bg_style} display: flex; flex-direction: column; justify-content: flex-end; }}
            .overlay {{ background: linear-gradient(to top, rgba(14,100,46,0.9) 0%, rgba(14,100,46,0.7) 35%, transparent 100%); padding: 110px 90px; color: white; }}
            h1 {{ font-size: 46pt; margin: 0 0 55px 0; line-height: 1.0; font-weight: 700; letter-spacing: 0.5px; text-shadow: 2px 2px 12px rgba(0,0,0,0.9), 0px 0px 20px rgba(0,0,0,0.7); }}
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

        p_f = await browser.new_page(viewport={'width': 1080, 'height': 1350}); await p_f.set_content(h_feed); await asyncio.sleep(2); await p_f.screenshot(path=f"FEED_{sid}.jpg")
        p_s = await browser.new_page(viewport={'width': 1080, 'height': 1920}); await p_s.set_content(h_story); await asyncio.sleep(2); await p_s.screenshot(path=f"STORY_{sid}.jpg")
        await browser.close()

def enviar_telegram(copy_texto, sid="default"):
    lineas = copy_texto.strip().split('\n')
    ultima = lineas[-1] if lineas else ''
    es_link = ultima.startswith('http')
    if es_link:
        cuerpo = '\n'.join(lineas[:-1])
        pie = '\n' + ultima
    else:
        cuerpo = copy_texto
        pie = ''
    cuerpo = cuerpo.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    limite = 1024 - len(pie)
    if len(cuerpo) > limite: cuerpo = cuerpo[:limite - 3] + '...'
    copy_final = cuerpo + pie

    feed_path = f"FEED_{sid}.jpg"
    story_path = f"STORY_{sid}.jpg"
    media = [{"type": "photo", "media": "attach://f", "caption": copy_final, "parse_mode": "HTML"}, {"type": "photo", "media": "attach://s"}]
    try:
        with open(feed_path, "rb") as f, open(story_path, "rb") as s:
            res = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMediaGroup", data={"chat_id": TG_CHAT_ID, "media": json.dumps(media)}, files={"f": f, "s": s}, timeout=30)
        if res.status_code == 200 and res.json().get("ok"): st.success("✅ Enviado.")
        else: st.error(f"❌ Error Telegram: {res.json().get('description', 'sin detalle')}")
    except Exception as e: st.error(f"❌ Error: {str(e)}")

# --- FUNCIONES VIDEO ---
async def generar_portada_video(titulo, frame_path):
    logo_data = get_base64_logo("logo.png")
    img_b64 = ""
    try:
        with open(frame_path, "rb") as f:
            img_b64 = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    except: pass

    html = f"""
    <html><head><style>@font-face {{ font-family: 'ArialNova'; src: url('ArialNova-Bold.ttf') format('truetype'); font-weight: 700; }}</style></head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'ArialNova', sans-serif; }}
        .canvas {{ width: 1080px; height: 1920px; background: url('{img_b64}') no-repeat center center; background-size: cover; display: flex; flex-direction: column; justify-content: flex-end; }}
        .overlay {{ background: linear-gradient(to top, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.6) 45%, transparent 100%); padding: 90px 80px 280px 80px; }}
        h1 {{ font-size: 58pt; font-weight: 700; line-height: 1.2; color: white; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 60px; }}
        h1 span {{ background: #0e642e; padding: 0px 6px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
        .logo-row {{ display: flex; align-items: center; justify-content: space-between; border-top: 2px solid rgba(255,255,255,0.3); padding-top: 30px; }}
        .logo-img {{ height: 50px; filter: brightness(0) invert(1); }}
        .play-icon {{ width: 90px; height: 90px; border: 3px solid white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; color: white; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); }}
        .play-wrapper {{ position: relative; width: 90px; height: 90px; }}
    </style>
    <body>
    <div class='canvas'><div class='overlay'><h1><span>{titulo}</span></h1><div class='logo-row'><img src='{logo_data}' class='logo-img'><div class='play-wrapper'><div class='play-icon'>▶</div></div></div></div></div>
    </body></html>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920})
        await page.set_content(html); await asyncio.sleep(2); await page.screenshot(path="PORTADA_VIDEO.jpg"); await browser.close()

def procesar_video(video_path, titulo, segundos_titulo):
    from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    
    clip = VideoFileClip(video_path)
    w, h = clip.size
    ratio_916 = 9 / 16
    if abs((w/h) - ratio_916) > 0.05:
        if (w/h) > ratio_916:
            nw = int(h * ratio_916)
            clip = clip.crop(x1=(w//2 - nw//2), x2=(w//2 + nw//2))
        else:
            nh = int(w / ratio_916)
            clip = clip.crop(y1=(h//2 - nh//2), y2=(h//2 + nh//2))
        w, h = clip.size

    dur_overlay = clip.duration if segundos_titulo == 0 else min(segundos_titulo, clip.duration)
    OW, OH = 1080, 1920
    overlay_img = Image.new("RGBA", (OW, OH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_img)
    grad_h = int(OH * 0.45)
    for i in range(grad_h):
        draw.rectangle([0, OH - grad_h + i, OW, OH - grad_h + i + 1], fill=(14, 100, 46, int(210 * (i / grad_h))))

    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except: font = ImageFont.load_default()

    lineas, linea_actual = [], ""
    for palabra in titulo.split():
        test = f"{linea_actual} {palabra}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] > OW - 120:
            if linea_actual: lineas.append(linea_actual)
            linea_actual = palabra
        else: linea_actual = test
    if linea_actual: lineas.append(linea_actual)
    texto_completo = "\n".join(lineas)
    
    bbox = draw.multiline_textbbox((0, 0), texto_completo, font=font, spacing=6)
    y_texto = OH - grad_h + (grad_h - (bbox[3] - bbox[1])) // 2 - 40
    draw.multiline_text((62, y_texto + 3), texto_completo, font=font, fill=(0, 0, 0, 180), spacing=6)
    draw.multiline_text((60, y_texto), texto_completo, font=font, fill=(255, 255, 255, 255), spacing=6)

    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo_h = int(OH * 0.04)
        logo = logo.resize((int(logo_h * (logo.width / logo.height)), logo_h), Image.LANCZOS)
        r, g, b, a = logo.split()
        logo_blanco = Image.merge("RGBA", (Image.new("L", logo.size, 255), Image.new("L", logo.size, 255), Image.new("L", logo.size, 255), a))
        overlay_img.paste(logo_blanco, ((OW - logo_blanco.width) // 2, OH - int(OH * 0.06)), logo_blanco)
    except: pass

    overlay_clip = ImageClip(np.array(overlay_img.resize((w, h), Image.LANCZOS)), ismask=False).set_duration(dur_overlay)
    video_final = CompositeVideoClip([clip, overlay_clip])
    video_final.write_videofile("VIDEO_FINAL.mp4", codec="libx264", audio_codec="aac", verbose=False, logger=None)
    clip.close()
    return "VIDEO_FINAL.mp4"

def enviar_video_telegram(video_path, portada_path, caption):
    with open(portada_path, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto", data={"chat_id": TG_CHAT_ID, "caption": caption}, files={"photo": f})
    with open(video_path, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendVideo", data={"chat_id": TG_CHAT_ID}, files={"video": f})

def descargar_video_url(url):
    output_path = f"/tmp/video_{uuid.uuid4().hex[:8]}.mp4"
    try:
        with yt_dlp.YoutubeDL({'outtmpl': output_path, 'format': 'mp4/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'quiet': True, 'no_warnings': True, 'merge_output_format': 'mp4'}) as ydl: ydl.download([url])
        return output_path if os.path.exists(output_path) else None
    except: return None

# --- INTERFAZ ---
if "gen_id" not in st.session_state: st.session_state.gen_id = 0
if "session_id" not in st.session_state: st.session_state.session_id = uuid.uuid4().hex[:8]
sid = st.session_state.session_id

t2, t3, t4 = st.tabs(["📝 Link / RSS", "📤 Carga Manual", "🎬 Video"])

with t2:
    url_input = st.text_input("Link de la noticia:")
    if st.button("Generar desde Link"):
        with st.spinner("Procesando noticia..."):
            final_tit, img_url_raw = extraer_datos_rapidos(url_input)
            img_b64 = imagen_a_base64(mejorar_resolucion_imagen(img_url_raw)) or imagen_a_base64(img_url_raw)
            final_fondo = img_b64 if img_b64 else img_url_raw

            loop = asyncio.get_event_loop()
            texto_noticia = loop.run_until_complete(extraer_texto_noticia(url_input))
            loop.run_until_complete(generar_placas(final_tit, final_fondo, sid))
            
            st.session_state.copy_final = redactar_copy_custom(final_tit, url_input, texto_noticia)
            st.session_state.gen_id += 1
            st.rerun()

    st.divider()
    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        opciones = {e.title: e for e in feed.entries[:10]}
        seleccion = st.selectbox("Noticias RSS:", list(opciones.keys()))
        if st.button("Generar desde RSS"):
            noticia = opciones[seleccion]
            img_rss_raw = noticia.enclosures[0].url if 'enclosures' in noticia else ""
            img_b64 = imagen_a_base64(mejorar_resolucion_imagen(img_rss_raw)) or imagen_a_base64(img_rss_raw)
            final_fondo = img_b64 if img_b64 else img_rss_raw

            loop = asyncio.get_event_loop()
            loop.run_until_complete(generar_placas(noticia.title, final_fondo, sid))
            texto_noticia = loop.run_until_complete(extraer_texto_noticia(noticia.link))
            
            st.session_state.copy_final = redactar_copy_custom(noticia.title, noticia.link, texto_noticia)
            st.session_state.gen_id += 1
            st.rerun()

    if os.path.exists(f"FEED_{sid}.jpg"):
        st.divider(); col1, col2 = st.columns(2)
        with col1: st.image(f"FEED_{sid}.jpg"); st.image(f"STORY_{sid}.jpg")
        with col2:
            copy_ready = st.text_area("Editar Copy:", value=st.session_state.get("copy_final", ""), height=300, key=f"copy_area_{st.session_state.gen_id}")
            if st.button("📤 Enviar"): enviar_telegram(copy_ready, sid)

with t3:
    st.header("Generación Manual")
    with st.form("manual_v25_form"):
        titulo_m = st.text_input("Título de la placa:")
        foto_m = st.file_uploader("Foto:", type=["jpg", "png", "jpeg"])
        modo_copy = st.radio("Método de Copy:", ["Manual", "IA con instrucciones"])
        texto_m = st.text_area("Tu copy (si es manual):")
        instruccion_m = st.text_input("Instrucción para la IA:")
        submit_m = st.form_submit_button("🎨 Generar Todo")

    if submit_m and foto_m:
        b64_img = f"data:image/jpeg;base64,{base64.b64encode(foto_m.read()).decode()}"
        st.session_state.copy_final = redactar_copy_custom(titulo_m, instruccion_m) if modo_copy == "IA con instrucciones" else texto_m
        asyncio.run(generar_placas(titulo_m, b64_img, sid))
        st.session_state.gen_id += 1
        st.rerun()

    if os.path.exists(f"FEED_{sid}.jpg"):
        st.divider(); c1, c2 = st.columns(2)
        with c1: st.image(f"FEED_{sid}.jpg"); st.image(f"STORY_{sid}.jpg")
        with c2:
            c_m = st.text_area("Confirmar Copy:", value=st.session_state.get("copy_final", ""), height=300, key=f"man_area_{st.session_state.gen_id}")
            if st.button("📤 Enviar Manual"): enviar_telegram(c_m, sid)

with t4:
    st.header("🎬 Generación de Video")
    with st.form("video_form"):
        titulo_v = st.text_input("Título del video:")
        url_video = st.text_input("Link del video (Twitter, Instagram, YouTube, etc.):")
        video_file = st.file_uploader("O subí el archivo:", type=["mp4", "mov", "avi"])
        segundos_v = st.number_input("Segundos que dura el título (0 = todo el video):", min_value=0, max_value=90, value=0, step=1)
        submit_v = st.form_submit_button("🎬 Procesar Video")

    if submit_v and titulo_v and (video_file or url_video):
        with st.spinner("Procesando video..."):
            if url_video:
                tmp_path = descargar_video_url(url_video)
                if not tmp_path: st.error("No se pudo descargar el video. Verificá el link."); st.stop()
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(video_file.read()); tmp_path = tmp.name

            frame_path = "FRAME_PORTADA.jpg"
            subprocess.run(["ffmpeg", "-y", "-i", tmp_path, "-vframes", "1", "-q:v", "2", frame_path], capture_output=True)
            asyncio.run(generar_portada_video(titulo_v, frame_path))
            video_output = procesar_video(tmp_path, titulo_v, int(segundos_v))

        st.success("✅ Video procesado"); col1, col2 = st.columns(2)
        with col1: st.image("PORTADA_VIDEO.jpg", caption="Portada")
        with col2: st.video(video_output)
        
        caption_v = st.text_area("Caption para Telegram:", height=100, key="caption_video")
        if st.button("📤 Enviar Video a Telegram"):
            enviar_video_telegram(video_output, "PORTADA_VIDEO.jpg", caption_v)
            st.success("✅ Enviado a Telegram")
