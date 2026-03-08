RENDER_VERSION = "GA-V2-INNOVATOR-01 - GEMINI"

def safe_bg_style(image_data: str, overlay_top: str, overlay_bottom: str, fallback_a: str, fallback_b: str) -> str:
    if image_data:
        return f"background-image: linear-gradient({overlay_top}, {overlay_bottom}), url('{image_data}');"
    return f"background: linear-gradient(135deg, {fallback_a} 0%, {fallback_b} 100%);"

def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'

def global_styles() -> str:
    """Estilos base con Passion One (identidad impreso) y Barlow (limpieza)."""
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Barlow+Condensed:wght@700;900&family=Barlow:wght@400;700&display=swap');
      
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { background: #eee; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
      
      .canvas {
        width: 1080px;
        height: 1350px;
        position: relative;
        overflow: hidden;
        background: #fff;
        font-family: 'Passion One', cursive;
      }

      .section-chip {
        position: absolute;
        top: 56px;
        left: 56px;
        background: #2d572c; /* Verde El Periódico */
        color: #fff;
        padding: 8px 24px;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700;
        font-size: 32px;
        text-transform: uppercase;
        z-index: 10;
      }

      .brand-logo {
        position: absolute;
        bottom: 56px;
        right: 56px;
        width: 220px;
        height: auto;
        z-index: 10;
      }
      
      .title {
        line-height: 0.9;
        text-transform: uppercase;
      }
    </style>
    """

def build_post_html(
    title: str,
    description: str,
    image_data: str,
    section_label: str,
    family: str,
    logo_white_data: str,
    logo_green_data: str,
) -> str:
    title = (title or "").strip()
    
    # Ruteo de familias
    if family == "deportes_a":
        return build_deportes_a(title, image_data, section_label, logo_green_data)
    if family == "deportes_b" or family == "deportes":
        return build_deportes_b(title, image_data, section_label, logo_green_data)
    if family == "portada_mate":
        # Esta se llama manualmente pasando un título con pipe '|' para dividir bloques
        return build_portada_mate(title, image_data, section_label, logo_green_data)
    if family == "general_b":
        return build_general_b(title, image_data, section_label, logo_green_data)
    if family == "policiales":
        return build_policiales(title, image_data, section_label, logo_white_data)
    
    # Default: General A
    return build_general_a(title, image_data, section_label, logo_green_data)

def build_deportes_a(title, image_data, section_label, logo_data):
    """VARIANTE A: Diagonal + Bloque Sólido Verde. Passion One Blanca."""
    bg = safe_bg_style(image_data, "transparent", "transparent", "#1a3b2a", "#1a3b2a")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .dep-a {{ {bg} background-size: cover; background-position: center; }}
          .footer-block {{
            position: absolute; bottom: 0; left: 0; width: 100%;
            background: #1a3b2a; padding: 120px 56px 180px 56px;
            clip-path: polygon(0 18%, 100% 0, 100% 100%, 0 100%); z-index: 5;
          }}
          .title {{ font-size: 110px; color: #fff; max-width: 950px; }}
          .section-chip {{ top: auto; bottom: 560px; background: #f37021; }} /* Naranja disruptivo */
        </style>
      </head>
      <body>
        <div class="canvas dep-a">
          <div class="section-chip">{section_label}</div>
          <div class="footer-block"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_deportes(title, description, image_data, section_label, logo_data) -> str:
    photo_style = f"background-image: url('{image_data}');" if image_data else "background: linear-gradient(135deg, #273126 0%, #1a2119 100%);"

    raw_title = (title or "").strip()
    title_html = raw_title

    # Lógica de detección para el resaltado
    if ":" in raw_title:
        left, right = raw_title.split(":", 1)
        if left.strip():
            title_html = f'<span class="title-highlight">{left.strip()}:</span> {right.strip()}'
    else:
        words = raw_title.split()
        if len(words) >= 4:
            # Resalta las primeras 3 palabras si no hay ":"
            title_html = f'<span class="title-highlight">{" ".join(words[:3])}</span> {" ".join(words[3:])}'

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .depb {{
            background: #efede8;
            color: #111;
          }}

          .depb .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 1080px;
            height: 760px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .depb .photo::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,.03), rgba(0,0,0,.15));
          }}

          .depb .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 480px; /* Un poco más alto para dar aire al bloque */
            background: #efede8;
            padding: 40px 56px;
          }}

          .depb .bar {{
            position: absolute;
            left: 56px;
            top: 40px;
            width: 14px;
            height: 140px;
            background: #f37021; /* Naranja disruptivo de El Periódico */
            border-radius: 2px;
          }}

          .depb .inner {{
            margin-left: 34px;
          }}

          .depb .title {{
            font-size: 72px;
            font-weight: 400;
            color: #111;
            max-width: 880px;
            line-height: 1.2; /* Ajustado para que el highlight no se encime */
          }}

          /* EL RESALTADO TIPO MARCADOR */
          .depb .title-highlight {{
            background-color: #f37021; /* Fondo naranja sólido */
            color: #ffffff;            /* Texto blanco sobre el fondo */
            padding: 4px 15px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
            display: inline;
          }}

          .depb .brand-wrap-center {{
            bottom: 40px;
          }}

          .depb .brand-logo {{
            width: 228px;
          }}

          .depb .accent-bar-center {{
            width: 138px;
            height: 7px;
            background: #1f8b4c;
          }}
        </style>
      </head>
      <body>
        <div class="canvas depb">
          <div class="photo"></div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner">
              <h1 class="title">{title_html}</h1>
            </div>
            <div class="brand-wrap-center">{logo_html(logo_data)}</div>
            <div class="accent-bar-center"></div>
          </div>
        </div>
      </body>
    </html>
    """

def build_portada_mate(title, image_data, section_label, logo_data):
    """DIVERGENTE: Estilo Mate/Streaming. Títulos asimétricos."""
    # Soporta dividir título con '|' para tamaños distintos
    parts = title.split('|')
    main_text = parts[0]
    sub_text = parts[1] if len(parts) > 1 else ""
    
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.2)", "rgba(0,0,0,0.7)", "#2d572c", "#000")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .mate {{ {bg} background-size: cover; background-position: center; display: flex; flex-direction: column; justify-content: flex-end; padding: 56px; }}
          .text-container {{ position: relative; z-index: 5; }}
          .main-t {{ font-size: 160px; color: #fff; margin-bottom: -10px; }}
          .sub-t {{ font-size: 80px; color: #f37021; background: rgba(0,0,0,0.8); display: inline-block; padding: 0 15px; }}
          .section-chip {{ background: #fff; color: #2d572c; font-family: 'Barlow', sans-serif; font-weight: 800; }}
        </style>
      </head>
      <body>
        <div class="canvas mate">
          <div class="section-chip">{section_label}</div>
          <div class="text-container">
            <div class="main-t">{main_text}</div>
            {f'<div class="sub-t">{sub_text}</div>' if sub_text else ''}
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_general_a(title, image_data, section_label, logo_data):
    """GENERAL A: La voz líder con Passion One."""
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.1)", "rgba(0,0,0,0.85)", "#2d572c", "#1a331b")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .gen-a {{ {bg} background-size: cover; background-position: center; }}
          .title-wrap {{ position: absolute; bottom: 200px; left: 56px; right: 56px; z-index: 5; }}
          .title {{ font-size: 105px; color: #fff; text-shadow: 0 5px 20px rgba(0,0,0,0.4); }}
        </style>
      </head>
      <body>
        <div class="canvas gen-a">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_general_b(title, image_data, section_label, logo_data):
    """GENERAL B: Cercanía. Mantenemos Barlow para balancear la modernidad."""
    bg = safe_bg_style(image_data, "rgba(255,255,255,0.8)", "rgba(255,255,255,0.95)", "#fff", "#eee")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .gen-b {{ {bg} background-size: cover; background-position: center; font-family: 'Barlow', sans-serif; }}
          .content-wrap {{ position: absolute; bottom: 180px; left: 56px; right: 56px; display: flex; gap: 24px; z-index: 5; }}
          .accent-bar {{ width: 12px; background: #2d572c; flex-shrink: 0; }}
          .title {{ font-size: 78px; color: #1a1a1a; font-weight: 800; line-height: 1; text-transform: none; }}
        </style>
      </head>
      <body>
        <div class="canvas gen-b">
          <div class="section-chip">{section_label}</div>
          <div class="content-wrap">
            <div class="accent-bar"></div><h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """

def build_policiales(title, image_data, section_label, logo_data):
    """POLICIALES: Seriedad y peso."""
    bg = safe_bg_style(image_data, "rgba(0,0,0,0.3)", "rgba(0,0,0,0.9)", "#000", "#222")
    return f"""
    <html>
      <head><meta charset="utf-8">{global_styles()}
        <style>
          .pol {{ {bg} background-size: cover; background-position: center; }}
          .title-wrap {{ position: absolute; left: 56px; right: 100px; bottom: 200px; z-index: 5; }}
          .title {{ font-size: 85px; color: #fff; }}
          .section-chip {{ background: #b00; }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
