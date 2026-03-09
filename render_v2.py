import base64

RENDER_VERSION = "EL-PERIODICO-DISRUPTIVE-V7"

def logo_html(logo_data: str) -> str:
    if not logo_data: return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'

def global_styles() -> str:
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Barlow+Condensed:wght@700;900&family=Barlow:wght@400;700;800&display=swap');
      * { margin: 0; padding: 0; box-sizing: border-box; }
      .canvas { width: 1080px; height: 1350px; position: relative; overflow: hidden; background: #fff; }
      .brand-logo { position: absolute; bottom: 56px; right: 56px; width: 220px; z-index: 20; }
    </style>
    """

def build_post_html(title, description, image_data, section_label, family, logo_white_data, logo_green_data) -> str:
    title = (title or "").strip()
    # RUTEADOR: Ahora sí separa los mundos
    if family == "deportes_a":
        return build_deportes_a(title, description, image_data, section_label, logo_white_data)
    if family in ["deportes_b", "deportes"]:
        return build_deportes_b(title, description, image_data, section_label, logo_green_data)
    if family == "policiales":
        return build_policiales(title, description, image_data, section_label, logo_white_data)
    return build_general_b(title, description, image_data, section_label, logo_green_data)

def build_deportes_a(title, description, image_data, section_label, logo_data):
    """VARIANTE A: DISRUPTIVA. Estilo Póster, diagonal y Passion One gigante."""
    photo = f"url('{image_data}')" if image_data else "linear-gradient(#1a3b2a, #000)"
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .depa {{ background: #000; font-family: 'Passion One', cursive; }}
          .bg-photo {{ 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.8)), {photo};
            background-size: cover; background-position: center;
          }}
          /* Corte diagonal disruptivo */
          .diagonal-block {{
            position: absolute; bottom: -100px; left: -100px; width: 1300px; height: 700px;
            background: #f37021; transform: rotate(-8deg); z-index: 5;
            display: flex; align-items: center; padding: 100px 150px;
          }}
          .title {{ 
            color: #fff; font-size: 130px; line-height: 0.85; text-transform: uppercase;
            transform: rotate(8deg); /* Compensa la rotación del bloque */
            max-width: 900px; text-shadow: 4px 4px 0px rgba(0,0,0,0.2);
          }}
          .section-chip {{
            position: absolute; top: 56px; left: 56px; background: #fff; color: #f37021;
            padding: 10px 30px; font-family: 'Barlow Condensed'; font-weight: 900; font-size: 35px; z-index: 20;
          }}
        </style>
      </head>
      <body>
        <div class="canvas depa">
          <div class="section-chip">{section_label}</div>
          <div class="bg-photo"></div>
          <div class="diagonal-block"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_deportes_b(title, description, image_data, section_label, logo_data):
    """VARIANTE B: SERVICIO. Base blanca, Barlow y marcador naranja."""
    photo = f"url('{image_data}')" if image_data else "none"
    if ":" in title:
        left, right = title.split(":", 1)
        title_html = f'<span class="marcador">{left.strip()}:</span> {right.strip()}'
    else:
        words = title.split()
        title_html = f'<span class="marcador">{" ".join(words[:3])}</span> {" ".join(words[3:])}' if len(words) >= 3 else f'<span class="marcador">{title}</span>'

    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .depb {{ background: #fff; font-family: 'Barlow', sans-serif; }}
          .photo {{ position: absolute; top: 0; left: 0; width: 100%; height: 800px; background-image: {photo}; background-size: cover; background-position: center; }}
          .content {{ position: absolute; bottom: 0; left: 0; right: 0; height: 550px; padding: 60px 56px; background: #fff; }}
          .title {{ font-size: 80px; color: #1a1a1a; font-weight: 800; line-height: 1.1; }}
          .marcador {{ background: #f37021 !important; color: #fff !important; padding: 2px 12px; display: inline; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
          .accent {{ width: 12px; height: 100px; background: #f37021; float: left; margin-right: 25px; }}
          .section-chip {{ position: absolute; top: 56px; left: 56px; background: #f37021; color: #fff; padding: 8px 24px; font-family: 'Barlow Condensed'; font-weight: 700; font-size: 32px; z-index: 10; text-transform: uppercase; }}
        </style>
      </head>
      <body>
        <div class="canvas depb">
          <div class="section-chip">{section_label}</div>
          <div class="photo"></div>
          <div class="content"><div class="accent"></div><h1 class="title">{title_html}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

# Funciones de soporte para que no rompa el ruteador
def build_general_b(title, description, image_data, section_label, logo_data):
    return build_deportes_b(title, description, image_data, section_label, logo_data).replace("#f37021", "#2d572c")

def build_policiales(title, description, image_data, section_label, logo_data):
    return build_deportes_a(title, description, image_data, section_label, logo_data).replace("#f37021", "#b00")
