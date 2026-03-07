import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path
from playwright.sync_api import sync_playwright
import tempfile
import os
import base64

from rules_v2 import infer_section_from_url, choose_family, display_section_label
from render_v2 import build_post_html


st.set_page_config(page_title="El Periódico - Placas V2", layout="wide")


def file_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    mime = "image/png"
    if p.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def image_url_to_base64(url: str) -> str:
    if not url:
        return ""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "").lower()
    if "jpeg" in content_type or "jpg" in content_type:
        mime = "image/jpeg"
    elif "png" in content_type:
        mime = "image/png"
    elif "webp" in content_type:
        mime = "image/webp"
    else:
        mime = "image/jpeg"

    encoded = base64.b64encode(resp.content).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def fetch_article_data(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    def get_meta(prop=None, name=None):
        if prop:
            tag = soup.find("meta", attrs={"property": prop})
            if tag and tag.get("content"):
                return tag["content"].strip()
        if name:
            tag = soup.find("meta", attrs={"name": name})
            if tag and tag.get("content"):
                return tag["content"].strip()
        return ""

    title = get_meta(prop="og:title") or (soup.title.get_text(strip=True) if soup.title else "")
    description = get_meta(prop="og:description") or get_meta(name="description")
    image_url = get_meta(prop="og:image")

    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else "Sin título"

    raw_section = infer_section_from_url(url)
    visible_section = display_section_label(url)

    image_data = ""
    if image_url:
        try:
            image_data = image_url_to_base64(image_url)
        except Exception:
            image_data = ""

    return {
        "url": url,
        "title": title,
        "description": description,
        "image_url": image_url,
        "image_data": image_data,
        "section": raw_section,
        "section_label": visible_section,
    }


def html_to_png_bytes(html: str, width: int = 1080, height: int = 1350) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = Path(tmpdir) / "preview.html"
        img_path = Path(tmpdir) / "preview.png"

        html_path.write_text(html, encoding="utf-8")

        chromium_candidates = [
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]

        chromium_path = next((p for p in chromium_candidates if os.path.exists(p)), None)

        with sync_playwright() as p:
            launch_args = {
                "headless": True,
                "args": [
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ],
            }

            if chromium_path:
                browser = p.chromium.launch(executable_path=chromium_path, **launch_args)
            else:
                browser = p.chromium.launch(**launch_args)

            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1
            )

            page.goto(html_path.as_uri(), wait_until="load")
            page.screenshot(path=str(img_path), full_page=True)
            browser.close()

        return img_path.read_bytes()


st.title("El Periódico · Placas V2")
st.caption("Laboratorio de diseño separado del sistema productivo")

with st.form("url_form"):
    url = st.text_input(
        "Pegá la URL de una nota",
        placeholder="https://el-periodico.com.ar/local/..."
    )
    submitted = st.form_submit_button("Generar preview")

if submitted:
    if not url.strip():
        st.error("Pegá una URL primero.")
        st.stop()

    try:
        article = fetch_article_data(url.strip())

        family = choose_family(
            section=article["section"],
            title=article["title"],
            description=article["description"],
        )

        logo_data = file_to_base64("logo.png")

        html = build_post_html(
            title=article["title"],
            description=article["description"],
            image_data=article["image_data"],
            section_label=article["section_label"],
            family=family,
            logo_data=logo_data,
        )

        png_bytes = html_to_png_bytes(html)

        col1, col2 = st.columns([1.1, 0.9])

        with col1:
            st.subheader("Preview")
            st.image(png_bytes, use_container_width=True)

        with col2:
            st.subheader("Datos detectados")
            st.write(f"**Sección visible:** {article['section_label']}")
            st.write(f"**Familia asignada:** {family}")
            st.write(f"**Título:** {article['title']}")
            st.write(f"**Descripción:** {article['description'] or '—'}")
            st.write(f"**Imagen encontrada:** {'Sí' if article['image_url'] else 'No'}")
            st.write(f"**Imagen embebida:** {'Sí' if article['image_data'] else 'No'}")
            st.write(f"**Logo encontrado:** {'Sí' if logo_data else 'No'}")

            st.download_button(
                "Descargar PNG",
                data=png_bytes,
                file_name="placa_v2.png",
                mime="image/png",
            )

            with st.expander("Ver HTML generado"):
                st.code(html, language="html")

    except Exception as e:
        st.error(f"Error al generar la placa: {e}")
