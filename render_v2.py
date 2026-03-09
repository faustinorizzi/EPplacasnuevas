import base64

RENDER_VERSION = "EL-PERIODICO-V8-UNIFICADO"

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
    family_key = family.lower().strip()
    if family_key == "deportes_a":
        return build_deportes_a(title, section_label, image_data, logo_white_data)
    return build_deportes_b(title, section_label, image_data, logo_green_data)

def build_deportes_a(title, section_label, image_data, logo_data):
    """VARIANTE A: IMPACTO DISRUPTIVO (DIAGONAL)"""
    photo = f"url('{image_data}')" if image_data else "linear-gradient(#1a3b2a, #000)"
    return f"""
    <html><head><meta charset="utf-8">{global_styles()}
    <style>
      .c_a {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: #000; font-family: 'Passion One', cursive; }}
      .bg_a {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.7)), {photo}; background-size: cover; background-position: center; }}
      .diag {{ position: absolute; bottom: -100px; left: -150px; width: 1450px; height: 700px; background: #f37021; transform: rotate(-7deg); z-index: 5; display: flex; align-items: center; padding-left: 200px; }}
      .t_a {{ color: #fff; font-size: 130px; line-height: 0.9; text-transform: uppercase; transform: rotate(7deg); max-width: 900px; }}
      .chip_a {{ position: absolute; top: 56px; left: 56px; background: #fff; color: #f37021; padding: 10px 30px; font-family: 'Barlow Condensed'; font-weight: 900; font-size: 35px; z-index: 20; }}
    </style></head>
    <body><div class="c_a"><div class="chip_a">{section_label}</div><div class="bg_a"></div><div class="diag"><h1 class="t_a">{title}</h1></div>{logo_html(logo_data)}</div></body></html>
    """

def build_deportes_b(title, section_label, image_data, logo_data):
    """VARIANTE B: SERVICIO LIMPIO (MARCADOR)"""
    photo = f"url('{image_data}')" if image_data else "none"
    words = title.split()
    t_html = f'<span class="m">{" ".join(words[:3])}</span> {" ".join(words[3:])}' if len(words) >= 3 else f'<span class="m">{title}</span>'
    return f"""
    <html><head><meta charset="utf-8">{global_styles()}
    <style>
      .c_b {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: #fff; font-family: 'Barlow', sans-serif; }}
      .ph_b {{ position: absolute; top: 0; left: 0; width: 100%; height: 800px; background-image: {photo}; background-size: cover; background-position: center; }}
      .cont {{ position: absolute; bottom: 0; left: 0; right: 0; height: 550px; padding: 60px 56px; background: #fff; }}
      .t_b {{ font-size: 85px; color: #111; font-weight: 800; line-height: 1.1; }}
      .m {{ background: #f37021; color: #fff; padding: 2px 12px; display: inline; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
      .acc {{ width: 12px; height: 100px; background: #f37021; float: left; margin-right: 25px; }}
      .chip_b {{ position: absolute; top: 56px; left: 56px; background: #f37021; color: #fff; padding: 8px 24px; font-family: 'Barlow Condensed'; font-weight: 700; font-size: 32px; z-index: 10; }}
    </style></head>
    <body><div class="c_b"><div class="chip_b">{section_label}</div><div class="ph_b"></div><div class="cont"><div class="acc"></div><h1 class="t_b">{t_html}</h1></div>{logo_html(logo_data)}</div></body></html>
    """
