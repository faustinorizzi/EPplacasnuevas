RENDER_VERSION = "GENERAL-A-PROTOTYPES-01"

def logo_html(logo_data: str) -> str:
    if not logo_data:
        return ""
    return f'<img src="{logo_data}" alt="El Periódico" class="brand-logo" />'


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
        z-index: 50;
      }
    </style>
    """


def build_general_experiment(
    variant: str,
    title: str,
    image_data: str,
    logo_white_data: str,
) -> str:
    title = (title or "").strip()

    if variant == "general_a_corte":
        return build_general_a_corte(title, image_data, logo_white_data)

    if variant == "general_a_doble":
        return build_general_a_doble(title, image_data, logo_white_data)

    return build_general_a_base(title, image_data, logo_white_data)


def build_general_a_base(title: str, image_data: str, logo_data: str) -> str:
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #2d572c 0%, #183624 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background:
              linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0%,
                rgba(0, 0, 0, 0.02) 48%,
                rgba(13, 48, 30, 0.30) 64%,
                rgba(16, 58, 36, 0.88) 82%,
                rgba(16, 58, 36, 0.96) 100%
              );
            z-index: 5;
          }}

          .base {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 300px;
            background: linear-gradient(
              to top,
              rgba(16, 58, 36, 0.98) 0%,
              rgba(16, 58, 36, 0.88) 54%,
              rgba(16, 58, 36, 0.00) 100%
            );
            z-index: 8;
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
          <div class="base"></div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_corte(title: str, image_data: str, logo_data: str) -> str:
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #2d572c 0%, #183624 100%);"
    )

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background:
              linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0%,
                rgba(0, 0, 0, 0.03) 48%,
                rgba(10, 38, 24, 0.26) 64%,
                rgba(13, 48, 30, 0.80) 82%,
                rgba(13, 48, 30, 0.92) 100%
              );
            z-index: 5;
          }}

          .base {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 320px;
            background: #17452e;
            clip-path: polygon(0 24%, 100% 8%, 100% 100%, 0 100%);
            z-index: 10;
          }}

          .cut-mark {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 318px;
            height: 10px;
            background: #2d6a47;
            z-index: 11;
            clip-path: polygon(0 100%, 100% 0, 100% 100%, 0 100%);
            opacity: 0.9;
          }}

          .title-wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 248px;
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
          <div class="base"></div>
          <div class="cut-mark"></div>
          <div class="title-wrap">
            <h1 class="title">{title}</h1>
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """


def build_general_a_doble(title: str, image_data: str, logo_data: str) -> str:
    photo_style = (
        f"background-image: url('{image_data}');"
        if image_data
        else "background: linear-gradient(135deg, #2d572c 0%, #183624 100%);"
    )

    words = title.split()
    if len(words) >= 5:
        split_at = max(2, len(words) // 2)
        line1 = " ".join(words[:split_at])
        line2 = " ".join(words[split_at:])
    else:
        line1 = title
        line2 = ""

    second_line_html = f'<div class="title-secondary">{line2}</div>' if line2 else ""

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {global_styles()}
        <style>
          .gena {{
            {photo_style}
            background-size: cover;
            background-position: center;
          }}

          .overlay {{
            position: absolute;
            inset: 0;
            background:
              linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0) 0%,
                rgba(0, 0, 0, 0.02) 46%,
                rgba(12, 44, 28, 0.24) 60%,
                rgba(16, 58, 36, 0.86) 82%,
                rgba(16, 58, 36, 0.95) 100%
              );
            z-index: 5;
          }}

          .base {{
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 300px;
            background: linear-gradient(
              to top,
              rgba(16, 58, 36, 0.98) 0%,
              rgba(16, 58, 36, 0.88) 54%,
              rgba(16, 58, 36, 0.00) 100%
            );
            z-index: 8;
          }}

          .title-wrap {{
            position: absolute;
            left: 92px;
            right: 92px;
            bottom: 248px;
            z-index: 20;
          }}

          .title-primary {{
            font-family: 'Passion One', cursive;
            font-size: 48px;
            line-height: 0.98;
            color: #dff2e7;
          }}

          .title-secondary {{
            margin-top: 8px;
            font-family: 'Passion One', cursive;
            font-size: 70px;
            line-height: 0.92;
            color: #fff;
          }}
        </style>
      </head>
      <body>
        <div class="canvas gena">
          <div class="overlay"></div>
          <div class="base"></div>
          <div class="title-wrap">
            <div class="title-primary">{line1}</div>
            {second_line_html}
          </div>
          {logo_html(logo_data)}
        </div>
      </body>
    </html>
    """
