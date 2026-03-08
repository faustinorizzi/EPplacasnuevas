RENDER_VERSION = "GA-V2-CLEAN-10"

def safe_bg_style(image_data: str, overlay_top: str, overlay_bottom: str, fallback_a: str, fallback_b: str) -> str:
    if image_data:
        return f"background-image: linear-gradient({overlay_top}, {overlay_bottom}), url('{image_data}');"
    return f"background: linear-gradient(135deg, {fallback_a} 0%, {fallback_b} 100%);"


def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'


def build_post_html(title: str, description: str, image_data: str, section_label: str, family: str, logo_white_data: str, logo_green_data: str) -> str:
            title = (title or "").strip()
    description = (description or "").strip()

    if family == "general_b":
        return build_general_b(title, description, image_data, section_label, logo_green_data)
    if family == "deportes":
        return build_deportes(title, description, image_data, section_label, logo_white_data)
    if family == "policiales":
        return build_policiales(title, description, image_data, section_label, logo_white_data)
    return build_general_a(title, description, image_data, section_label, logo_white_data)


def global_styles() -> str:
    return """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Passion+One:wght@400;700;900&family=PT+Sans:wght@400;700&display=swap');

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
        font-family: 'PT Sans', sans-serif;
      }

      .section-chip {
        position: absolute;
        top: 48px;
        left: 56px;
        padding: 12px 22px;
        border-radius: 999px;
        background: rgba(31, 139, 76, .34);
        border: 1px solid rgba(82, 188, 88, .52);
        color: #fff;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: .04em;
        text-transform: uppercase;
        z-index: 6;
        backdrop-filter: blur(4px);
      }

      .title {
        font-family: 'Passion One', sans-serif;
        font-weight: 400;
        line-height: 1.07;
        letter-spacing: 0;
        margin: 0;
      }

      .desc {
        margin: 18px 0 0 0;
        font-size: 27px;
        line-height: 1.32;
        font-weight: 700;
        max-width: 820px;
      }

      .brand-wrap-center {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 50px;
        z-index: 7;
        display: inline-flex;
        align-items: center;
        justify-content: center;
      }

      .brand-logo {
        display: block;
        width: 230px;
        height: auto;
      }

      .accent-bar-center {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 28px;
        z-index: 7;
        border-radius: 2px;
      }
    </style>
    """


def build_general_a(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.07)",
        overlay_bottom="rgba(10,40,20,.68)",
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
              rgba(0,0,0,.08) 0%,
              rgba(0,0,0,0) 38%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .ga .title-wrap {{
            position: absolute;
            left: 56px;
            right: 108px;
            bottom: 196px;
            z-index: 5;
          }}

          .ga .title {{
            font-size: 68px;
            max-width: 840px;
            text-shadow: 0 2px 7px rgba(0,0,0,.16);
          }}

          .ga .brand-logo {{
            width: 228px;
          }}

          .ga .accent-bar-center {{
            width: 190px;
            height: 10px;
            background: #2aa357;
          }}
        </style>
      </head>
      <body>
        <div class="canvas ga">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap-center">{logo_html(logo_data)}</div>
          <div class="accent-bar-center"></div>
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
            background: #f1efea;
            color: #111;
          }}

          .gb .photo {{
            position: absolute;
            top: 0;
            left: 0;
            width: 1080px;
            height: 780px;
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .gb .photo::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,.02), rgba(0,0,0,.10));
          }}

          .gb .panel {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 520px;
            background: #f1efea;
            padding: 46px 56px 34px 56px;
          }}

          .gb .bar {{
            position: absolute;
            left: 56px;
            top: 56px;
            width: 14px;
            height: 118px;
            background: #1f8b4c;
            border-radius: 2px;
          }}

          .gb .inner {{
            margin-left: 34px;
          }}

          .gb .section-chip-inline {{
            display: inline-block;
            padding: 10px 18px;
            border-radius: 999px;
            background: rgba(31, 139, 76, .16);
            border: 1px solid rgba(66, 171, 108, .34);
            color: #1f8b4c;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: .04em;
            text-transform: uppercase;
            margin-bottom: 18px;
          }}

          .gb .title {{
            font-size: 58px;
            font-weight: 400;
            color: #111;
            max-width: 820px;
            line-height: 1.08;
          }}

          .gb .desc {{
    color: #3d3d3d;
    font-size: 25px;
    line-height: 1.34;
    max-width: 790px;
    margin-top: 18px;
}}

          .gb .brand-wrap-center {{
            bottom: 38px;
          }}

          .gb .brand-logo {{
            width: 228px;
          }}

          .gb .accent-bar-center {{
            width: 138px;
            height: 7px;
            background: #1f8b4c;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gb">
          <div class="photo"></div>
          <div class="panel">
            <div class="bar"></div>
            <div class="inner">
              <div class="section-chip-inline">{section_label}</div>
              <h1 class="title">{title}</h1>
              {desc_html}
            </div>
            <div class="brand-wrap-center">{logo_html(logo_data)}</div>
            <div class="accent-bar-center"></div>
          </div>
        </div>
      </body>
    </html>
    """


def build_deportes(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.07)",
        overlay_bottom="rgba(0,0,0,.62)",
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
              rgba(0,0,0,.08) 0%,
              rgba(0,0,0,0) 38%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .dep .title-wrap {{
            position: absolute;
            left: 56px;
            right: 108px;
            bottom: 196px;
            z-index: 5;
          }}

          .dep .title {{
            font-size: 70px;
            max-width: 840px;
            text-shadow: 0 2px 7px rgba(0,0,0,.16);
          }}

          .dep .brand-logo {{
            width: 228px;
          }}

          .dep .accent-bar-center {{
            width: 156px;
            height: 8px;
            background: #c96d2b;
          }}
        </style>
      </head>
      <body>
        <div class="canvas dep">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap-center">{logo_html(logo_data)}</div>
          <div class="accent-bar-center"></div>
        </div>
      </body>
    </html>
    """


def build_policiales(title, description, image_data, section_label, logo_data) -> str:
    bg = safe_bg_style(
        image_data=image_data,
        overlay_top="rgba(0,0,0,.12)",
        overlay_bottom="rgba(0,0,0,.74)",
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
              rgba(0,0,0,.08) 0%,
              rgba(0,0,0,0) 38%
            );
            z-index: 1;
            pointer-events: none;
          }}

          .pol .title-wrap {{
            position: absolute;
            left: 56px;
            right: 112px;
            bottom: 196px;
            z-index: 5;
          }}

          .pol .title {{
            font-size: 64px;
            max-width: 820px;
            text-shadow: 0 2px 7px rgba(0,0,0,.18);
          }}

          .pol .brand-logo {{
            width: 228px;
          }}

          .pol .accent-bar-center {{
            width: 142px;
            height: 6px;
            background: #ffffff;
            opacity: .95;
          }}
        </style>
      </head>
      <body>
        <div class="canvas pol">
          <div class="section-chip">{section_label}</div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          <div class="brand-wrap-center">{logo_html(logo_data)}</div>
          <div class="accent-bar-center"></div>
        </div>
      </body>
    </html>
    """
