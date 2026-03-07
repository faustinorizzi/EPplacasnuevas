def section_label(family: str) -> str:
    labels = {
        "general_a": "GENERAL",
        "general_b": "GENERAL",
        "deportes": "DEPORTES",
        "policiales": "POLICIALES",
    }
    return labels.get(family, "GENERAL")


def safe_bg(image_url: str) -> str:
    if image_url:
        return f"background-image: linear-gradient(rgba(0,0,0,.28), rgba(0,0,0,.65)), url('{image_url}');"
    return "background: linear-gradient(135deg, #1a1f1b 0%, #0f120f 100%);"


def build_post_html(title: str, description: str, image_url: str, section: str, family: str, brand: str) -> str:
    title = (title or "").strip()
    description = (description or "").strip()
    label = section_label(family)

    if family == "general_b":
        return build_general_b(title, description, image_url, label, brand)
    if family == "deportes":
        return build_deportes(title, description, image_url, label, brand)
    if family == "policiales":
        return build_policiales(title, description, image_url, label, brand)
    return build_general_a(title, description, image_url, label, brand)


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

      .brand {
        position: absolute;
        left: 56px;
        bottom: 46px;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: .02em;
        z-index: 5;
      }

      .section {
        position: absolute;
        top: 52px;
        left: 56px;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
        z-index: 5;
      }

      .title {
        font-family: 'Passion One', sans-serif;
        line-height: 1.02;
        letter-spacing: .01em;
        margin: 0;
      }

      .desc {
        margin: 18px 0 0 0;
        font-size: 33px;
        line-height: 1.24;
        font-weight: 600;
        max-width: 900px;
      }
    </style>
    """


def build_general_a(title, description, image_url, label, brand) -> str:
    bg = safe_bg(image_url)
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
            right: 56px;
            bottom: 110px;
            z-index: 4;
          }}
          .ga .title {{
            font-size: 92px;
            max-width: 920px;
          }}
          .ga .accent {{
            position: absolute;
            left: 56px;
            bottom: 32px;
            width: 180px;
            height: 10px;
            background: #1f8b4c;
            z-index: 5;
          }}
        </style>
      </head>
      <body>
        <div class="canvas ga">
          <div class="section">{label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand">{brand}</div>
          <div class="accent"></div>
        </div>
      </body>
    </html>
    """


def build_general_b(title, description, image_url, label, brand) -> str:
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gb {{
            background: #f3f2ef;
            color: #111;
          }}
          .gb .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 1080px;
            height: 780px;
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
          }}
          .gb .photo::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,.10), rgba(0,0,0,.28));
          }}
          .gb .section {{
            color: #fff;
          }}
          .gb .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 570px;
            background: #f3f2ef;
            padding: 46px 56px 42px 56px;
          }}
          .gb .bar {{
            width: 18px;
            height: 120px;
            background: #1f8b4c;
            position: absolute;
            left: 56px;
            top: 56px;
          }}
          .gb .inner {{
            margin-left: 42px;
          }}
          .gb .title {{
            font-size: 76px;
            color: #111;
            max-width: 900px;
          }}
          .gb .brand {{
            color: #111;
            bottom: 38px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gb">
          <div class="photo"></div>
          <div class="section">{label}</div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner">
              <h1 class="title">{title}</h1>
              {"<p class='desc'>" + description + "</p>" if description else ""}
            </div>
            <div class="brand">{brand}</div>
          </div>
        </div>
      </body>
    </html>
    """


def build_deportes(title, description, image_url, label, brand) -> str:
    bg = f"background-image: linear-gradient(rgba(0,0,0,.20), rgba(0,0,0,.72)), url('{image_url}');" if image_url else "background: linear-gradient(135deg, #1a1f1b 0%, #0f120f 100%);"

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .dep {{
            color: #fff;
            background-size: cover;
            background-position: center;
            {bg}
          }}
          .dep .title-wrap {{
            position: absolute;
            left: 56px;
            right: 56px;
            bottom: 110px;
            z-index: 4;
          }}
          .dep .title {{
            font-size: 96px;
            max-width: 920px;
          }}
          .dep .accent {{
            position: absolute;
            left: 56px;
            bottom: 32px;
            width: 220px;
            height: 12px;
            background: #c96d2b;
            z-index: 5;
          }}
        </style>
      </head>
      <body>
        <div class="canvas dep">
          <div class="section">{label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand">{brand}</div>
          <div class="accent"></div>
        </div>
      </body>
    </html>
    """


def build_policiales(title, description, image_url, label, brand) -> str:
    bg = f"background-image: linear-gradient(rgba(0,0,0,.30), rgba(0,0,0,.82)), url('{image_url}');" if image_url else "background: linear-gradient(135deg, #171717 0%, #090909 100%);"

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .pol {{
            color: #fff;
            background-size: cover;
            background-position: center;
            {bg}
          }}
          .pol .title-wrap {{
            position: absolute;
            left: 56px;
            right: 56px;
            bottom: 110px;
            z-index: 4;
          }}
          .pol .title {{
            font-size: 90px;
            max-width: 920px;
          }}
          .pol .accent {{
            position: absolute;
            left: 56px;
            bottom: 32px;
            width: 180px;
            height: 8px;
            background: #ffffff;
            opacity: .95;
            z-index: 5;
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="section">{label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand">{brand}</div>
          <div class="accent"></div>
        </div>
      </body>
    </html>
    """
