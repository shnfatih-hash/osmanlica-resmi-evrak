#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugging Face Spaces Canlı Web Aracı — Osmanlıca Resmî Evrak, Diplomatik ve Paleografya AI Skill
"""

from __future__ import annotations

import datetime
import html
import json
import tempfile
from pathlib import Path
from PIL import Image

import gradio as gr

from scripts.sozluk_ve_html_uretici import build_html
from scripts.tarih_cevirici import (
    HICRI_AY_ADLARI,
    HICRI_AYLAR,
    RUMI_AY_ADLARI,
    RUMI_AYLAR,
    TTK_URL,
    format_tr,
    gregorian_to_jdn,
    hijri_to_jdn,
    jdn_to_gregorian,
    jdn_to_hijri,
    jdn_to_rumi,
    julian_to_jdn,
    parse_hicri_day,
)

ROOT = Path(__file__).resolve().parent
SAMPLE_JSON_PATH = ROOT / "examples" / "ornek_evrak_verisi.json"

SUPPORT_BANNER_HTML = """
<div style="background: linear-gradient(135deg, #4a1c1c 0%, #2c3e50 100%); color: #fff; padding: 20px 24px; border-radius: 12px; border-bottom: 4px solid #ffdd00; margin-bottom: 14px;">
  <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px;">
    <div>
      <h2 style="margin: 0 0 6px; font-size: 1.45rem; color: #fff;">🖋️ Osmanlıca Resmî Evrak, Diplomatik ve Paleografya AI Skill</h2>
      <p style="margin: 0; opacity: 0.92; font-size: 0.95rem;">
        TDV İA / TTK transkripsiyon standardı, 1:1 piksel şerh aparatı, Kubbealtı &amp; TDV İA bağlantılı İnteraktif HTML çalışma kartı üreticisi.
      </p>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
      <a href="https://buymeacoffee.com/shnfatih8" target="_blank" rel="noopener"
         style="background: #FFDD00; color: #111; font-weight: 700; padding: 9px 16px; border-radius: 8px; text-decoration: none; font-size: 0.92rem; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
        ☕ Bir Kahve Ismarla (Buy Me a Coffee)
      </a>
      <a href="https://github.com/sponsors/shnfatih-hash" target="_blank" rel="noopener"
         style="background: #ea4aaa; color: #fff; font-weight: 700; padding: 9px 16px; border-radius: 8px; text-decoration: none; font-size: 0.92rem;">
        💖 GitHub Sponsors
      </a>
      <a href="https://github.com/shnfatih-hash/osmanlica-resmi-evrak" target="_blank" rel="noopener"
         style="background: #24292f; color: #fff; font-weight: 600; padding: 9px 14px; border-radius: 8px; text-decoration: none; font-size: 0.9rem; border: 1px solid #57606a;">
        ⭐ GitHub Deposu
      </a>
    </div>
  </div>
</div>
"""


def render_evrak_html(json_text: str):
    try:
        data = json.loads(json_text)
        rendered = build_html(data)
        escaped_srcdoc = html.escape(rendered, quote=True)
        iframe = (
            f'<iframe srcdoc="{escaped_srcdoc}" '
            f'style="width:100%; height:640px; border:1px solid #dfd6c5; border-radius:10px; background:#f8f5ee;"></iframe>'
        )
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_evrak_calisma_karti.html", mode="w", encoding="utf-8")
        tmp.write(rendered)
        tmp.close()
        return iframe, tmp.name
    except Exception as exc:
        return f"<div style='color:#9b1c1c; padding:12px;'><strong>JSON Hatası:</strong> {html.escape(str(exc))}</div>", None


def diplomatic_regions_and_crop(img: Image.Image | None, x1: float, y1: float, x2: float, y2: float, scale: float):
    if img is None:
        return None, None, None, None
    im = img.convert("RGB")
    w, h = im.size
    top_heading = im.crop((0, 0, w, int(h * 0.22)))
    right_margin = im.crop((int(w * 0.70), 0, w, h))
    bottom_seal = im.crop((0, int(h * 0.76), w, h))

    bx1, bx2 = sorted([int(x1 * w), int(x2 * w)])
    by1, by2 = sorted([int(y1 * h), int(y2 * h)])
    crop = im.crop((bx1, by1, max(bx1 + 10, min(w, bx2)), max(by1 + 10, min(h, by2))))
    if scale > 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.Resampling.NEAREST)
    return top_heading, right_margin, bottom_seal, crop


def convert_date(cal_type: str, day_str: str, month_str: str, year_val: int) -> str:
    try:
        year = int(year_val)
        if cal_type == "Hicrî Kamerî":
            m = HICRI_AYLAR[month_str.split(" ")[0].strip().lower()]
            d1, d2, label = parse_hicri_day(day_str)
            j1 = hijri_to_jdn(year, m, d1)
            dt1 = jdn_to_gregorian(j1)
            miladi = format_tr(dt1) if d1 == d2 else f"{format_tr(dt1)} — {format_tr(jdn_to_gregorian(hijri_to_jdn(year, m, d2)))}"
            return (
                f"- **Girdi:** H. {label} {HICRI_AY_ADLARI[m]} {year}\n"
                f"- **Milâdî:** {miladi}\n"
                f"- **Rûmî:** {jdn_to_rumi(j1)}\n"
                f"- **Doğrulama:** [TTK Tarih Çevirme Kılavuzu]({TTK_URL})"
            )
        if cal_type == "Rûmî Malî":
            d = int(day_str.strip())
            m = RUMI_AYLAR[month_str.split(" ")[0].strip().lower()]
            if year < 1333 or (year == 1333 and m in (1, 2)):
                jdn = julian_to_jdn(year + (585 if m in (1, 2) else 584), m, d)
            else:
                dt_g = datetime.date(year + 584, m, d)
                jdn = gregorian_to_jdn(dt_g.year, dt_g.month, dt_g.day)
            dt = jdn_to_gregorian(jdn)
            hy, hm, hd = jdn_to_hijri(jdn)
            return (
                f"- **Girdi:** R. {d} {RUMI_AY_ADLARI[m]} {year}\n"
                f"- **Milâdî:** {format_tr(dt)}\n"
                f"- **Hicrî:** H. {hd} {HICRI_AY_ADLARI[hm]} {hy}\n"
                f"- **Doğrulama:** [TTK Tarih Çevirme Kılavuzu]({TTK_URL})"
            )
        d = int(day_str.strip())
        m = int(month_str.split(" ")[0].strip())
        dt = datetime.date(year, m, d)
        jdn = gregorian_to_jdn(dt.year, dt.month, dt.day)
        hy, hm, hd = jdn_to_hijri(jdn)
        return (
            f"- **Girdi (Milâdî):** {format_tr(dt)}\n"
            f"- **Hicrî:** H. {hd} {HICRI_AY_ADLARI[hm]} {hy}\n"
            f"- **Rûmî:** {jdn_to_rumi(jdn)}\n"
            f"- **Doğrulama:** [TTK Tarih Çevirme Kılavuzu]({TTK_URL})"
        )
    except Exception as exc:
        return f"**Hata:** `{exc}`"


def build_ui() -> gr.Blocks:
    sample_json = SAMPLE_JSON_PATH.read_text(encoding="utf-8") if SAMPLE_JSON_PATH.exists() else "{}"
    prompts_md = (
        (ROOT / "examples" / "ornek-kullanim-promptlari.md").read_text(encoding="utf-8")
        if (ROOT / "examples" / "ornek-kullanim-promptlari.md").exists()
        else ""
    )
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    if readme_text.startswith("---"):
        parts = readme_text.split("---", 2)
        if len(parts) == 3:
            readme_text = parts[2].strip()

    initial_iframe, _ = render_evrak_html(sample_json)

    with gr.Blocks(title="Osmanlıca Resmî Evrak & Paleografya AI Skill") as demo:
        gr.HTML(SUPPORT_BANNER_HTML)

        with gr.Tabs():
            with gr.Tab("🗂️ Canlı İnteraktif HTML Çalışma Kartı (Örnek Yüklü)"):
                gr.Markdown(
                    "Aşağıdaki örnek *Sadâret Arz Tezkiresi & İrâde-i Seniyye* JSON analizini düzenleyip veya kendi evrak JSON çıktınızı yapıştırıp **Kubbealtı Lugati** ve **TDV İslâm Ansiklopedisi** bağlantılı etkileşimli çalışma kartını anında üretebilirsiniz."
                )
                btn_render = gr.Button("✨ İnteraktif HTML Kartı Üret & İndirmeye Hazırla", variant="primary")
                html_preview = gr.HTML(value=initial_iframe)
                with gr.Row():
                    json_editor = gr.Code(value=sample_json, language="json", label="Evrak Analiz JSON Verisi", lines=16)
                    dl_html = gr.File(label="Tek Dosya İnteraktif HTML İndir")
                btn_render.click(render_evrak_html, inputs=json_editor, outputs=[html_preview, dl_html])

            with gr.Tab("✂️ Diplomatik Bölge & 1:1 Mühür/İbare Kesiti"):
                gr.Markdown(
                    "Bir Osmanlıca evrak görseli yükleyin; araç otomatik olarak **Üst Başlık/Tuğra**, **Sağ Derkenar/Hâmiş**, **Alt Mühür/İmza** bölgelerini ve seçtiğiniz koordinatın **1:1 piksel kesitini** çıkarır."
                )
                with gr.Row():
                    evrak_img = gr.Image(type="pil", label="Osmanlıca Evrak Görseli (.jpg / .png)")
                    with gr.Column():
                        cx1 = gr.Slider(0.0, 1.0, value=0.20, step=0.01, label="Sol (x1)")
                        cy1 = gr.Slider(0.0, 1.0, value=0.75, step=0.01, label="Üst (y1)")
                        cx2 = gr.Slider(0.0, 1.0, value=0.60, step=0.01, label="Sağ (x2)")
                        cy2 = gr.Slider(0.0, 1.0, value=0.95, step=0.01, label="Alt (y2)")
                        cscale = gr.Slider(1.0, 3.0, value=2.0, step=0.5, label="Piksel Büyütme (NEAREST)")
                        btn_split = gr.Button("Diplomatik Bölgelere Ayır & Kesit Al", variant="primary")
                with gr.Row():
                    o_top = gr.Image(label="Üst Başlık / Davet / Tuğra (%22)")
                    o_margin = gr.Image(label="Sağ Derkenar / Buyuruldu (%30)")
                    o_seal = gr.Image(label="Alt İmza & Mühür (%24)")
                o_crop = gr.Image(label="Seçili Bölge 1:1 Piksel Kanıt Kesiti")
                btn_split.click(
                    diplomatic_regions_and_crop,
                    inputs=[evrak_img, cx1, cy1, cx2, cy2, cscale],
                    outputs=[o_top, o_margin, o_seal, o_crop],
                )

            with gr.Tab("🗓️ 3 Yönlü Osmanlıca Tarih Çevirici"):
                with gr.Row():
                    c_cal = gr.Dropdown(["Hicrî Kamerî", "Rûmî Malî", "Milâdî"], value="Hicrî Kamerî", label="Kaynak Takvim")
                    c_day = gr.Textbox(value="15", label="Gün veya gurre / evail / evasit / evahir / selh")
                    c_mon = gr.Textbox(value="Ş", label="Ay veya Kısaltma (M, S, Ra, R, Ca, C, B, Ş, N, L, Za, Z)")
                    c_yr = gr.Number(value=1278, precision=0, label="Yıl")
                btn_dt = gr.Button("Tarihi Çevir", variant="primary")
                out_dt = gr.Markdown()
                btn_dt.click(convert_date, inputs=[c_cal, c_day, c_mon, c_yr], outputs=out_dt)

            with gr.Tab("✍️ Hazır Promptlar & Kurulum Rehberi"):
                gr.Markdown(prompts_md + "\n\n---\n\n" + readme_text)

        gr.HTML(
            """
            <div style="text-align: center; margin-top: 18px; padding: 14px; background: #faf7f0; border: 1px solid #e2dac9; border-radius: 10px;">
              <strong>Projeyi faydalı buldunuz mu?</strong> Açık kaynaklı Osmanlı paleografyası ve dijital beşerî bilimler AI araçlarına destek olmak için:
              <a href="https://buymeacoffee.com/shnfatih8" target="_blank" style="margin-left:8px; font-weight:700; color:#7a5200;">☕ Buy Me a Coffee (shnfatih8)</a> •
              <a href="https://github.com/sponsors/shnfatih-hash" target="_blank" style="margin-left:6px; font-weight:700; color:#b82578;">💖 GitHub Sponsors</a>
            </div>
            """
        )
    return demo


if __name__ == "__main__":
    app = build_ui()
    app.launch()
