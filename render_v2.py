RENDER_VERSION = "GA-V2-TEST-01"


def safe_bg_style(image_data: str, overlay_top: str, overlay_bottom: str, fallback_a: str, fallback_b: str) -> str:
    if image_data:
        return f"background-image: linear-gradient({overlay_top}, {overlay_bottom}), url('{image_data}');"
    return f"background: linear-gradient(135deg, {fallback_a} 0%, {fallback_b} 100%);"


def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'


def build_post_html(title: str, description: str, image_data: str, section_label: str, family: str, logo_data: str) -> str:
    title = (title or "").strip()

    if family == "general_b":
        return build_general_b(title, description, image_data, section_label, logo_data)
    if family == "deportes":
        return build_deportes(title, description, image_data, section_label, logo_data)
    if family == "policiales":
        return build_policiales(title, description, image_data, section_label, logo_data)
    return build_general_a(title, description, image_data, section_label, logo_data)


def global_styles() -> str:
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Inter:wght@400;600;700;800&display=swap');

      * { box-sizing: border-box; }
      html, body {
        margin: 0;
        padding: 0;
        width: 1080px;
        height: 1350px;
        overflow: hidden;
        background: #111;
      }
      .canvas {
        width: 1080px;
        height: 1350px;
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
      }
      .section {
        position: absolute;
        top: 54px;
        left: 56px;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: .05em;
        text-transform: uppercase;
        z-index: 6;
      }
      .title {
        font-family: 'Passion One', sans-serif;
        line-height: 1.08;
        letter-spacing: 0;
        margin: 0;
      }
      .brand-wrap {
        position: absolute;
        left: 56px;
        bottom: 42px;
        z-index: 7;
      }
      .brand-logo {
        display: block;
        width: 200px;
        height: auto;
      }
      .accent-bar {
        position: absolute;
        left: 56px;
        bottom: 22px;
        z-index: 7;
        border-radius: 2px;
      }
      .test-chip {
        position: absolute;
        top: 54px;
        right: 56px;
        z-index: 8;
        background: #ff0033;
        color: white;
        padding: 10px 16px;
        border-radius: 999px;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: .04em;
      }
    </style>
    """


def build_general_a(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.10)",
        overlay_bottom="rgba(0,0,0,.62)",
        fallback_a="#1a1f1b",
        fallback_b="#0f120f",
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .ga {{
            color: #fff;
            background-size: cover;
            background-position: center;
            {bg}
          }}
          .ga .title-wrap {{
            position: absolute;
            left: 56px;
            right: 90px;
            bottom: 190px;
            z-index: 5;
          }}
          .ga .title {{
            font-size: 64px;
            max-width: 860px;
            text-shadow: 0 2px 8px rgba(0,0,0,.22);
          }}
          .ga .accent-bar {{
            width: 240px;
            height: 16px;
            background: #ff0033;
          }}
        </style>
      </head>
      <body>
        <div class="canvas ga">
          <div class="section">{section_label}</div>
          <div class="test-chip">{RENDER_VERSION}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap">{logo_html(logo_data)}</div>
          <div class="accent-bar"></div>
        </div>
      </body>
    </html>
    """


def build_general_b(title, description, image_data, section_label, logo_data) -> str:
    return build_general_a(title, description, image_data, section_label, logo_data)


def build_deportes(title, description, image_data, section_label, logo_data) -> str:
    return build_general_a(title, description, image_data, section_label, logo_data)


def build_policiales(title, description, image_data, section_label, logo_data) -> str:
    return build_general_a(title, description, image_data, section_label, logo_data)
