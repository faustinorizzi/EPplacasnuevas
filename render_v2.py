RENDER_VERSION = "GENERAL-A-LAB-03"
GENERAL_A_EXPERIMENT_MODE = "top_band"  # classic | top_band | bottom_band | side_left | superblock | double_level | hybrid_strip


def logo_html(logo_data: str, extra_class: str = "") -> str:
    if not logo_data:
        return ""
    klass = f"brand-logo {extra_class}".strip()
    return f'<img src="{logo_data}" alt="El Periódico" class="{klass}" />'


def global_styles() -> str:
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=Barlow+Condensed:wght@400;600;700;900&display=swap');

      * { margin: 0; padding: 0; box-sizing: border-box; }

      body {
        background: #e9e9e9;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
      }

      .canvas {
        width: 1080px;
        height: 1350px;
        position: relative;
        overflow: hidden;
        background: #fff;
      }

      .brand-logo {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 108px;
        width: 220px;
        height: auto;
        z-index: 60;
      }

      .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 30px;
        font-weight: 800;
        line-height: 1;
        letter-spacing: 0.3px;
        text-transform: uppercase;
      }

      .deck {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 26px;
        line-height: 1.18;
        font-weight: 600;
        color: #505050;
      }
    </style>
    """


def show_deck(description: str, max_chars: int = 150) -> bool:
    text = (description or "").strip()
    return bool(text) and len(text) <= max_chars


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
    description = (description or "").strip()

    if family == "deportes_a":
        return build_deportes_a(title, description, image_data, section_label, logo_white_data)

    if family == "deportes_b":
        return build_deportes_b(title, description, image_data, section_label, logo_green_data)

    if family == "general_b":
        return build_general_b(title, description, image_data, section_label, logo_green_data)

    if family == "general_a1":
        return build_general_a1(title, description, image_data, section_label, logo_green_data)

    if family == "policiales":
        return build_policiales(title, description, image_data, section_label, logo_white_data)

    return build_general_a(title, description, image_data, section_label, logo_white_data)


def build_general_a(title, description, image_data, section_label, logo_data):
    mode = GENERAL_A_EXPERIMENT_MODE

    if mode == "top_band":
        return build_general_a_top_band(title, image_data, logo_data)
    if mode == "bottom_band":
        return build_general_a_bottom_band(title, image_data, logo_data)
    if mode == "side_left":
        return build_general_a_side_left(title, image_data, logo_data)
    if mode == "superblock":
        return build_general_a_superblock(title, image_data, logo_data)
    if mode == "double_level":
        return build_general_a_double_level(title, image_data, logo_data)
    if mode == "hybrid_strip":
        return build_general_a_hybrid_strip(title, image_data, logo_data)

    return build_general_a_classic(title, image_data, logo_data)


def photo_style(image_data: str) -> str:
    if image_data:
        return f"background-image: url('{image_data}');"
    return "background: linear-gradient(135deg, #2d572c 0%, #183624 100%);"


def build_general_a_classic(title, image_data, logo_data):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0) 0%,
              rgba(0,0,0,0.02) 48%,
              rgba(13,48,30,0.30) 64%,
              rgba(16,58,36,0.88) 82%,
              rgba(16,58,36,0.96) 100%
            );
          }}
          .title-wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 250px;
            z-index: 20;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            line-height: 0.96;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="overlay"></div>
          <div class="title-wrap"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_top_band(title, image_data, logo_data):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .veil {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.12) 0%, rgba(0,0,0,0.08) 100%);
          }}
          .band {{
            position: absolute;
            left: 0;
            right: 0;
            top: 120px;
            min-height: 250px;
            background: rgba(18, 71, 43, 0.94);
            padding: 44px 92px 42px 92px;
            z-index: 20;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 66px;
            line-height: 0.95;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="veil"></div>
          <div class="band"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_bottom_band(title, image_data, logo_data):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .band {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            min-height: 430px;
            background: rgba(18, 71, 43, 0.95);
            padding: 66px 92px 170px 92px;
            z-index: 20;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 68px;
            line-height: 0.95;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="band"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_side_left(title, image_data, logo_data):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .veil {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, rgba(8,28,18,0.20) 0%, rgba(8,28,18,0.03) 60%, rgba(8,28,18,0.00) 100%);
          }}
          .col {{
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            width: 420px;
            background: rgba(18, 71, 43, 0.94);
            padding: 120px 42px 170px 42px;
            z-index: 20;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 66px;
            line-height: 0.94;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="veil"></div>
          <div class="col"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_superblock(title, image_data, logo_data):
    words = title.split()
    if len(words) >= 5:
        lead = " ".join(words[:3])
        rest = " ".join(words[3:])
    else:
        lead = title
        rest = ""

    rest_html = f'<div class="rest">{rest}</div>' if rest else ""

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0.00) 0%,
              rgba(0,0,0,0.06) 52%,
              rgba(10,36,23,0.48) 78%,
              rgba(10,36,23,0.86) 100%
            );
          }}
          .wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 248px;
            z-index: 20;
          }}
          .lead {{
            display: inline;
            font-family: 'Passion One', cursive;
            font-size: 66px;
            line-height: 0.95;
            color: #fff;
            background: rgba(109,179,63,0.96);
            padding: 4px 12px 2px 12px;
            box-decoration-break: clone;
            -webkit-box-decoration-break: clone;
          }}
          .rest {{
            margin-top: 8px;
            font-family: 'Passion One', cursive;
            font-size: 66px;
            line-height: 0.95;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="overlay"></div>
          <div class="wrap">
            <div class="lead">{lead}</div>
            {rest_html}
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_double_level(title, image_data, logo_data):
    words = title.split()
    if len(words) >= 5:
        cut = max(2, len(words) // 2)
        line1 = " ".join(words[:cut])
        line2 = " ".join(words[cut:])
    else:
        line1 = title
        line2 = ""

    line2_html = f'<div class="l2">{line2}</div>' if line2 else ""

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0.00) 0%,
              rgba(0,0,0,0.04) 48%,
              rgba(13,48,30,0.28) 68%,
              rgba(16,58,36,0.88) 84%,
              rgba(16,58,36,0.96) 100%
            );
          }}
          .wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 248px;
            z-index: 20;
          }}
          .l1 {{
            font-family: 'Passion One', cursive;
            font-size: 46px;
            line-height: 0.98;
            color: #dff2e7;
          }}
          .l2 {{
            margin-top: 8px;
            font-family: 'Passion One', cursive;
            font-size: 74px;
            line-height: 0.90;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="overlay"></div>
          <div class="wrap">
            <div class="l1">{line1}</div>
            {line2_html}
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_hybrid_strip(title, image_data, logo_data):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .veil {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to bottom,
              rgba(0,0,0,0.00) 0%,
              rgba(0,0,0,0.04) 50%,
              rgba(8,28,18,0.20) 70%,
              rgba(8,28,18,0.55) 100%
            );
          }}
          .strip {{
            position: absolute;
            left: 56px;
            right: 56px;
            bottom: 248px;
            background: rgba(18,71,43,0.88);
            padding: 30px 36px 28px 36px;
            z-index: 20;
            border-left: 14px solid #6DB33F;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 64px;
            line-height: 0.95;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="veil"></div>
          <div class="strip"><h1 class="title">{title}</h1></div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a1(title, description, image_data, section_label, logo_data):
    return build_general_a_classic(title, image_data, logo_data)


def build_general_b(title, description, image_data, section_label, logo_data):
    deck_html = f'<div class="deck">{description}</div>' if show_deck(description) else ""
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .genb {{
            background: #f5f2ec;
          }}
          .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 760px;
            {photo_style(image_data)}
            background-size: cover;
            background-position: center;
          }}
          .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 590px;
            background: #f5f2ec;
            padding: 54px 56px 178px 56px;
          }}
          .inner {{
            position: relative;
            margin-left: 92px;
            margin-right: 92px;
          }}
          .section-label {{
            color: #2d572c;
            margin-bottom: 18px;
          }}
          .accent {{
            position: absolute;
            left: -28px;
            top: 66px;
            width: 14px;
            height: 140px;
            background: #2d572c;
          }}
          .title {{
            font-family: 'Passion One', cursive;
            font-size: 60px;
            line-height: 1.00;
            color: #141414;
          }}
          .deck {{
            margin-top: 24px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas genb">
          <div class="photo"></div>
          <div class="panel">
            <div class="inner">
              <div class="accent"></div>
              <div class="section-label">{section_label}</div>
              <h1 class="title">{title}</h1>
              {deck_html}
            </div>
            {logo_html(logo_data)}
          </div>
        </div>
      </body>
    </html>
    """


def build_deportes_a(title, description, image_data, section_label_unused, logo_data):
    return build_general_a_classic(title.upper(), image_data, logo_data)


def build_deportes_b(title, description, image_data, section_label_unused, logo_data):
    return build_general_b(title, description, image_data, "", logo_data)


def build_policiales(title, description, image_data, section_label, logo_data):
    return build_general_a_classic(title, image_data, logo_data)
