RENDER_VERSION = "GA-V2-CLEAN-02"


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
    description = (description or "").strip()

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
        font-size: 22px;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
        z-index: 6;
      }

      .title {
        font-family: 'Passion One', sans-serif;
        font-weight: 400;
        line-height: 1.08;
        letter-spacing: 0;
        margin: 0;
      }

      .desc {
        margin: 18px 0 0 0;
        font-size: 27px;
        line-height: 1.32;
        font-weight: 600;
        max-width: 820px;
      }

      .brand-wrap {
        position: absolute;
        left: 56px;
        bottom: 42px;
        z-index: 7;
        display: inline-flex;
        align-items: center;
      }

      .brand-logo {
        display: block;
        width: 198px;
        height: auto;
      }

      .accent-bar {
        position: absolute;
        left: 56px;
        bottom: 22px;
        z-index: 7;
        border-radius: 2px;
      }
    </style>
    """


def build_general_a(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.07)",
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

          .ga::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to top,
              rgba(0,0,0,.12) 0%,
              rgba(0,0,0,0) 34%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .ga .section {{
            color: #fff;
            text-shadow: 0 1px 2px rgba(0,0,0,.18);
          }}

          .ga .title-wrap {{
            position: absolute;
            left: 56px;
            right: 122px;
            bottom: 188px;
            z-index: 5;
          }}

          .ga .title {{
            font-size: 62px;
            max-width: 790px;
            text-shadow: 0 2px 7px rgba(0,0,0,.16);
          }}

          .ga .brand-logo {{
            width: 198px;
          }}

          .ga .accent-bar {{
            width: 165px;
            height: 7px;
            background: #1f8b4c;
          }}
        </style>
      </head>
      <body>
        <div class="canvas ga">
          <div class="section">{section_label}</div>
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
    photo_style = f"background-image: url('{image_data}');" if image_data else "background: linear-gradient(135deg, #273126 0%, #1a2119 100%);"
    desc_html = f"<p class='desc'>{description}</p>" if description else ""

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
            height: 742px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .gb .photo::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,.05), rgba(0,0,0,.16));
          }}

          .gb .section {{
            color: #fff;
            text-shadow: 0 1px 2px rgba(0,0,0,.20);
          }}

          .gb .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 608px;
            background: #f3f2ef;
            padding: 52px 56px 48px 56px;
          }}

          .gb .bar {{
            width: 12px;
            height: 104px;
            background: #1f8b4c;
            position: absolute;
            left: 56px;
            top: 58px;
            border-radius: 2px;
          }}

          .gb .inner {{
            margin-left: 32px;
          }}

          .gb .title {{
            font-size: 55px;
            font-weight: 400;
            color: #111;
            max-width: 820px;
            line-height: 1.09;
          }}

          .gb .desc {{
            color: #3a3a3a;
            font-size: 23px;
            line-height: 1.34;
            max-width: 790px;
            margin-top: 18px;
          }}

          .gb .brand-logo {{
            width: 198px;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gb">
          <div class="photo"></div>
          <div class="section">{section_label}</div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner">
              <h1 class="title">{title}</h1>
              {desc_html}
            </div>
            <div class="brand-wrap">{logo_html(logo_data)}</div>
          </div>
        </div>
      </body>
    </html>
    """


def build_deportes(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.07)",
        overlay_bottom="rgba(0,0,0,.64)",
        fallback_a="#1f221d",
        fallback_b="#0f100c",
    )

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

          .dep::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to top,
              rgba(0,0,0,.12) 0%,
              rgba(0,0,0,0) 34%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .dep .title-wrap {{
            position: absolute;
            left: 56px;
            right: 116px;
            bottom: 188px;
            z-index: 5;
          }}

          .dep .title {{
            font-size: 64px;
            max-width: 805px;
            text-shadow: 0 2px 7px rgba(0,0,0,.16);
          }}

          .dep .brand-logo {{
            width: 198px;
          }}

          .dep .accent-bar {{
            width: 178px;
            height: 8px;
            background: #c96d2b;
          }}
        </style>
      </head>
      <body>
        <div class="canvas dep">
          <div class="section">{section_label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap">{logo_html(logo_data)}</div>
          <div class="accent-bar"></div>
        </div>
      </body>
    </html>
    """


def build_policiales(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.12)",
        overlay_bottom="rgba(0,0,0,.76)",
        fallback_a="#171717",
        fallback_b="#090909",
    )

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

          .pol::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
              to top,
              rgba(0,0,0,.10) 0%,
              rgba(0,0,0,0) 34%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .pol .title-wrap {{
            position: absolute;
            left: 56px;
            right: 122px;
            bottom: 188px;
            z-index: 5;
          }}

          .pol .title {{
            font-size: 60px;
            max-width: 790px;
            text-shadow: 0 2px 7px rgba(0,0,0,.18);
          }}

          .pol .brand-logo {{
            width: 198px;
          }}

          .pol .accent-bar {{
            width: 160px;
            height: 6px;
            background: #ffffff;
            opacity: .95;
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="section">{section_label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap">{logo_html(logo_data)}</div>
          <div class="accent-bar"></div>
        </div>
      </body>
    </html>
    """
