import streamlit as st
from pathlib import Path
from playwright.sync_api import sync_playwright
import tempfile
import os

st.set_page_config(page_title="CONTROL TEST V3", layout="wide")

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


st.title("CONTROL TEST V3")
st.caption("Si esto no cambia visualmente, no estás viendo esta app/archivo")

html = """
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {
    margin: 0;
    padding: 0;
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #111;
    font-family: Arial, sans-serif;
  }
  .canvas {
    width: 1080px;
    height: 1350px;
    background: linear-gradient(180deg, #ff0033 0%, #111111 100%);
    color: white;
    position: relative;
  }
  .badge {
    position: absolute;
    top: 60px;
    left: 60px;
    background: yellow;
    color: black;
    font-weight: bold;
    padding: 14px 22px;
    font-size: 36px;
    border-radius: 16px;
  }
  .title {
    position: absolute;
    left: 60px;
    right: 60px;
    top: 260px;
    font-size: 64px;
    line-height: 1.1;
    font-weight: 900;
  }
  .footer {
    position: absolute;
    left: 60px;
    bottom: 80px;
    font-size: 42px;
    font-weight: bold;
    color: #00ff88;
  }
</style>
</head>
<body>
  <div class="canvas">
    <div class="badge">CONTROL TEST V3</div>
    <div class="title">
      ESTA PLACA DEBE VERSE TOTALMENTE DISTINTA.<br><br>
      FONDO ROJO, ETIQUETA AMARILLA Y ESTE TEXTO.
    </div>
    <div class="footer">SI VES LA PLACA ANTERIOR, ESTA APP NO ES LA CORRECTA</div>
  </div>
</body>
</html>
"""

png_bytes = html_to_png_bytes(html)

st.image(png_bytes, use_container_width=True)
st.download_button(
    "Descargar PNG de prueba",
    data=png_bytes,
    file_name="control_test_v3.png",
    mime="image/png",
)
