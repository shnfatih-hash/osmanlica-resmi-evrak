#!/usr/bin/env python3
"""
sozluk_ve_html_uretici.py — Osmanlıca Resmî Evrak İnteraktif HTML Çalışma Kartı Üreticisi

Girdi JSON dosyasından:
  - Arşiv ve Diplomatik Künye
  - Satır Satır Akademik (TDV İA / TTK) ↔ Sadeleştirilmiş Transkripsiyon ↔ Günümüz Türkçesi
  - Kelime Kelime Çözümleme (Müfredât) + Kubbealtı Lugati (lugatim.com) doğrulama bağlantıları
  - Tamlamalar ve Kalıp İfadeler (Terkîbât) çözümleme tablosu
  - Kurumsal & Tarihsel Kavramlar (TDV İslâm Ansiklopedisi — islamansiklopedisi.org.tr atıflı)
  - Çözülemeyen / Şüpheli Yerler Şerh (Kritik Aparat) Paneli
üreten bağımsız, yazdırılabilir, aranabilir tek dosya HTML çıktısı oluşturur.

Kullanım:
  python sozluk_ve_html_uretici.py evrak_verisi.json --out evrak_calisma_karti.html
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

HARAKAT_AND_CTRL_RE = re.compile(r"[\u064B-\u065F\u0670\u0640\u200C\u200D]")


def normalize_ottoman_unicode(text: str | None) -> str:
    """
    Osmanlıca/Arapça metinlerdeki Ye (ي/ى/ی), Kef (ك/ک/گ/ڭ) ve ZWNJ/hareke
    farklarını kanonik olarak eşitler (karşılaştırma ve sözlük araması için).
    """
    if not text:
        return ""
    s = HARAKAT_AND_CTRL_RE.sub("", str(text))
    return (
        s.replace("\u064a", "\u06cc")
        .replace("\u0649", "\u06cc")
        .replace("\u0643", "\u06a9")
        .replace("\u06af", "\u06a9")
        .replace("\u06ad", "\u06a9")
    )


def esc(text: str | None) -> str:
    return html.escape(str(text or ""), quote=True)


def lugatim_url(word: str) -> str:
    return f"https://lugatim.com/s/{quote(word.strip())}"


def tdv_ia_url(term: str, slug: str | None = None) -> str:
    if slug and slug.strip():
        return f"https://islamansiklopedisi.org.tr/{quote(slug.strip())}"
    return f"https://islamansiklopedisi.org.tr/arama/?q={quote(term.strip())}"


def build_html(data: dict) -> str:
    meta = data.get("kunye", {})
    title = meta.get("baslik", "Osmanlıca Resmî Evrak Diplomatik Çalışma Kartı")
    satirlar = data.get("satirlar", [])
    kelimeler = data.get("kelimeler", [])
    tamlamalar = data.get("tamlamalar", [])
    tdv_kavramlar = data.get("tdv_ia_kavramlar", [])
    serhler = data.get("serhler", [])
    ozet = data.get("ozet", "")

    kunye_rows = ""
    kunye_fields = [
        ("Arşiv / Fon Künyesi", meta.get("arsiv_kunyesi")),
        ("Belge Türü", meta.get("belge_turu")),
        ("Hat Türü", meta.get("hat_turu")),
        ("Gönderen Makam / Kişi", meta.get("gonderen")),
        ("Muhatap Makam / Kişi", meta.get("muhatap")),
        ("Hicrî / Rûmî Tarih", meta.get("orijinal_tarih")),
        ("Milâdî Karşılık", meta.get("miladi_tarih")),
        ("Transkripsiyon Standardı", meta.get("transkripsiyon_standardi", "TDV İA / TTK / İSAM")),
    ]
    for label, val in kunye_fields:
        if val:
            kunye_rows += f"<tr><th>{esc(label)}</th><td>{esc(val)}</td></tr>\n"

    satir_html = ""
    for s in satirlar:
        no = esc(s.get("no", ""))
        bolge = esc(s.get("bolge", "Gövde"))
        osm = esc(s.get("osmanlica", ""))
        akd = esc(s.get("akademik", ""))
        sade = esc(s.get("sadelestirilmis", akd))
        tr = esc(s.get("gunumuz_turkcesi", ""))
        kesit = s.get("kesit_gorsel")
        kesit_tag = (
            f'<div class="crop-box"><img src="{esc(kesit)}" alt="Satır {no} 1:1 kesit" loading="lazy"></div>'
            if kesit
            else ""
        )
        satir_html += f"""
        <article class="line-card">
          <div class="line-head">
            <span class="badge">Satır {no}</span>
            <span class="badge subtle">{bolge}</span>
          </div>
          {kesit_tag}
          {f'<p class="osm-text" dir="rtl" lang="ota">{osm}</p>' if osm else ''}
          <p class="tr-academic" data-mode="academic">{akd}</p>
          <p class="tr-simple hidden" data-mode="simple">{sade}</p>
          <p class="tr-modern"><strong>Günümüz Türkçesi:</strong> {tr}</p>
        </article>
        """

    kelime_rows = ""
    for k in kelimeler:
        sorgu = k.get("lugatim_sorgu") or k.get("sade") or k.get("transkripsiyon", "")
        kelime_rows += f"""
        <tr class="filter-row">
          <td class="osm-cell" dir="rtl" lang="ota">{esc(k.get("osmanlica", ""))}</td>
          <td><strong>{esc(k.get("transkripsiyon", ""))}</strong></td>
          <td><span class="tag">{esc(k.get("koken", "-"))}</span></td>
          <td>{esc(k.get("anlam", ""))}</td>
          <td>{esc(k.get("satir", "-"))}</td>
          <td><a class="ext-link" href="{lugatim_url(sorgu)}" target="_blank" rel="noopener">Kubbealtı ↗</a></td>
        </tr>
        """

    tamlama_rows = ""
    for t in tamlamalar:
        slug = t.get("tdv_ia_slug")
        terim = t.get("sade") or t.get("transkripsiyon", "")
        tamlama_rows += f"""
        <tr class="filter-row">
          <td class="osm-cell" dir="rtl" lang="ota">{esc(t.get("osmanlica", ""))}</td>
          <td><strong>{esc(t.get("transkripsiyon", ""))}</strong></td>
          <td><span class="tag gold">{esc(t.get("tur", ""))}</span></td>
          <td>{esc(t.get("cozumleme", ""))}</td>
          <td>{esc(t.get("gunumuz_turkcesi", ""))}</td>
          <td>
            <a class="ext-link" href="{lugatim_url(terim)}" target="_blank" rel="noopener">Lugat ↗</a>
            <a class="ext-link ia" href="{tdv_ia_url(terim, slug)}" target="_blank" rel="noopener">TDV İA ↗</a>
          </td>
        </tr>
        """

    tdv_cards = ""
    for c in tdv_kavramlar:
        madde = c.get("madde", "")
        slug = c.get("slug")
        tdv_cards += f"""
        <div class="ia-card">
          <div class="ia-head">
            <h4>{esc(madde)}</h4>
            <a class="ext-link ia" href="{tdv_ia_url(madde, slug)}" target="_blank" rel="noopener">TDV İslâm Ansiklopedisi'nde Aç ↗</a>
          </div>
          <p>{esc(c.get("aciklama", ""))}</p>
          {f'<p class="muted"><strong>Belgedeki Bağlamı:</strong> {esc(c.get("belge_baglami"))}</p>' if c.get("belge_baglami") else ''}
        </div>
        """

    serh_rows = ""
    for sh in serhler:
        durum = esc(sh.get("kanit_seviyesi", "B"))
        kesit = sh.get("kesit_gorsel")
        kesit_cell = (
            f'<img class="mini-crop" src="{esc(kesit)}" alt="Şerh {esc(sh.get("no"))}">'
            if kesit
            else "—"
        )
        serh_rows += f"""
        <tr>
          <td><strong>[{esc(sh.get("no", ""))}]</strong></td>
          <td>Satır {esc(sh.get("satir", "-"))}</td>
          <td><code>{esc(sh.get("ibare", ""))}</code></td>
          <td><span class="tag warn">{durum}</span></td>
          <td>{esc(sh.get("aciklama", ""))}</td>
          <td>{esc(sh.get("alternatifler", "-"))}</td>
          <td>{kesit_cell}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<style>
  :root {{
    --bg: #f8f5ee; --card: #ffffff; --ink: #1e242b; --muted: #5c6670;
    --accent: #7a2e2e; --gold: #9a6b2f; --ia: #1f5c4e; --border: #e2dac9;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: "Segoe UI", "Noto Sans", system-ui, sans-serif;
    background: var(--bg); color: var(--ink); line-height: 1.65;
  }}
  header {{
    background: linear-gradient(135deg, #1b2838 0%, #2c3e50 100%);
    color: #fdfbf7; padding: 28px 24px; border-bottom: 4px solid var(--gold);
  }}
  header .wrap, main.wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 18px; }}
  header h1 {{ margin: 0 0 6px; font-family: Georgia, serif; font-size: 1.7rem; font-weight: 600; }}
  header p {{ margin: 0; opacity: .88; font-size: .95rem; }}
  .toolbar {{
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between;
    margin: 20px 0 14px; padding: 12px 16px; background: var(--card);
    border: 1px solid var(--border); border-radius: 10px;
  }}
  .tabs {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .tab-btn, .mode-btn {{
    border: 1px solid var(--border); background: #faf7f0; color: var(--ink);
    padding: 7px 13px; border-radius: 7px; cursor: pointer; font-size: .88rem; font-weight: 600;
  }}
  .tab-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
  .mode-btn.active {{ background: var(--ia); color: #fff; border-color: var(--ia); }}
  .panel {{ display: none; }}
  .panel.active {{ display: block; }}
  .card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 2px 6px rgba(0,0,0,.03);
  }}
  h2 {{ margin: 0 0 12px; font-family: Georgia, serif; color: var(--accent); font-size: 1.25rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
  th, td {{ padding: 9px 11px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
  th {{ background: #f3ede0; color: #362e23; font-weight: 600; }}
  .line-card {{
    background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--gold);
    border-radius: 8px; padding: 14px 16px; margin-bottom: 12px;
  }}
  .line-head {{ display: flex; gap: 8px; margin-bottom: 8px; }}
  .badge {{ background: var(--accent); color: #fff; padding: 2px 9px; border-radius: 99px; font-size: .78rem; font-weight: 600; }}
  .badge.subtle {{ background: #ece5d5; color: #4a3f30; }}
  .osm-text, .osm-cell {{
    font-family: "Amiri", "Traditional Arabic", "Scheherazade New", serif;
    font-size: 1.38rem; line-height: 1.8; color: #161b22;
  }}
  .tr-academic, .tr-simple {{ font-family: "Gentium Plus", Georgia, serif; font-size: 1.06rem; margin: 6px 0; }}
  .tr-modern {{ margin: 6px 0 0; color: #2b3540; font-size: .95rem; }}
  .hidden {{ display: none; }}
  .tag {{ display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: .78rem; background: #edf2f7; color: #2d3748; }}
  .tag.gold {{ background: #f9eedb; color: #7a5219; }}
  .tag.warn {{ background: #fde8e8; color: #9b1c1c; }}
  .ext-link {{
    display: inline-block; padding: 3px 8px; border-radius: 5px; text-decoration: none;
    font-size: .8rem; font-weight: 600; background: #f3ece0; color: var(--gold); border: 1px solid #e2d2b5;
  }}
  .ext-link.ia {{ background: #e6f4f0; color: var(--ia); border-color: #b7dfd4; }}
  .search-input {{
    width: 100%; max-width: 360px; padding: 8px 12px; margin-bottom: 12px;
    border: 1px solid var(--border); border-radius: 7px; font-size: .92rem;
  }}
  .ia-card {{ border: 1px solid #cce3dc; background: #f7fcfa; border-radius: 8px; padding: 14px 16px; margin-bottom: 10px; }}
  .ia-head {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between; }}
  .ia-head h4 {{ margin: 0; color: var(--ia); font-size: 1.05rem; }}
  .muted {{ color: var(--muted); font-size: .9rem; }}
  .crop-box img {{ max-width: 100%; border: 1px solid var(--border); border-radius: 6px; margin-bottom: 8px; }}
  .mini-crop {{ max-width: 160px; border: 1px solid var(--border); border-radius: 4px; }}
  @media print {{
    .toolbar, .search-input {{ display: none !important; }}
    .panel {{ display: block !important; page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>{esc(title)}</h1>
    <p>Üniversite Transkripsiyon Standardı (TDV İA / TTK / İSAM) • Kelime &amp; Tamlama Çözümlemesi • Şerhli Diplomatik Çalışma Kartı</p>
  </div>
</header>

<main class="wrap">
  <section class="card" style="margin-top:18px;">
    <h2>Arşiv ve Diplomatik Künye</h2>
    <table>{kunye_rows}</table>
    {f'<p style="margin-top:12px;"><strong>Belge Özeti:</strong> {esc(ozet)}</p>' if ozet else ''}
  </section>

  <div class="toolbar">
    <div class="tabs">
      <button class="tab-btn active" onclick="openTab('tab-satir', this)">Satır Satır Okuma ({len(satirlar)})</button>
      <button class="tab-btn" onclick="openTab('tab-kelime', this)">Kelime Kelime ({len(kelimeler)})</button>
      <button class="tab-btn" onclick="openTab('tab-tamlama', this)">Tamlamalar ({len(tamlamalar)})</button>
      <button class="tab-btn" onclick="openTab('tab-tdv', this)">TDV İA Kavramlar ({len(tdv_kavramlar)})</button>
      <button class="tab-btn" onclick="openTab('tab-serh', this)">Şerh &amp; Aparat ({len(serhler)})</button>
    </div>
    <div>
      <button class="mode-btn active" id="btn-academic" onclick="setMode('academic')">Tam Akademik (İA/TTK)</button>
      <button class="mode-btn" id="btn-simple" onclick="setMode('simple')">Sadeleştirilmiş</button>
    </div>
  </div>

  <section id="tab-satir" class="panel active">
    {satir_html or '<div class="card">Satır verisi eklenmemiş.</div>'}
  </section>

  <section id="tab-kelime" class="panel card">
    <h2>Kelime Kelime Çözümleme (Müfredât)</h2>
    <input class="search-input" type="search" placeholder="Kelime, köken veya anlam ara..." oninput="filterTable('tbl-kelime', this.value)">
    <table id="tbl-kelime">
      <thead><tr><th>Osmanlıca</th><th>Çeviriyazı</th><th>Köken</th><th>Anlam</th><th>Satır</th><th>Sözlük</th></tr></thead>
      <tbody>{kelime_rows or '<tr><td colspan="6">Kelime kaydı yok.</td></tr>'}</tbody>
    </table>
  </section>

  <section id="tab-tamlama" class="panel card">
    <h2>Tamlamalar ve Kalıp İfadeler (Terkîbât)</h2>
    <input class="search-input" type="search" placeholder="Tamlama veya tür ara..." oninput="filterTable('tbl-tamlama', this.value)">
    <table id="tbl-tamlama">
      <thead><tr><th>Osmanlıca</th><th>Çeviriyazı</th><th>Tamlama Türü</th><th>Yapısal Çözümleme</th><th>Günümüz Türkçesi</th><th>Doğrulama</th></tr></thead>
      <tbody>{tamlama_rows or '<tr><td colspan="6">Tamlama kaydı yok.</td></tr>'}</tbody>
    </table>
  </section>

  <section id="tab-tdv" class="panel card">
    <h2>Kurumsal ve Tarihsel Kavramlar (TDV İslâm Ansiklopedisi Atıflı)</h2>
    {tdv_cards or '<p class="muted">TDV İA kavram kaydı eklenmemiş.</p>'}
  </section>

  <section id="tab-serh" class="panel card">
    <h2>Şerh ve Kritik Aparat (Çözülemeyen / Şüpheli Yerler)</h2>
    <table>
      <thead><tr><th>No</th><th>Konum</th><th>Metindeki İbare</th><th>Kanıt</th><th>Şerh / Gerekçe</th><th>Alternatif Okunuşlar</th><th>1:1 Kesit</th></tr></thead>
      <tbody>{serh_rows or '<tr><td colspan="7">Çözülemeyen veya şüpheli ibare bulunmamaktadır.</td></tr>'}</tbody>
    </table>
  </section>
</main>

<script>
function openTab(id, btn) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}}
function setMode(mode) {{
  document.querySelectorAll('[data-mode="academic"]').forEach(el => el.classList.toggle('hidden', mode !== 'academic'));
  document.querySelectorAll('[data-mode="simple"]').forEach(el => el.classList.toggle('hidden', mode !== 'simple'));
  document.getElementById('btn-academic').classList.toggle('active', mode === 'academic');
  document.getElementById('btn-simple').classList.toggle('active', mode === 'simple');
}}
function normOsm(str) {{
  return (str || '').toLowerCase()
    .replace(/[\u064B-\u065F\u0670\u0640\u200C\u200D]/g, '')
    .replace(/[\u064a\u0649]/g, '\u06cc')
    .replace(/[\u0643\u06af\u06ad]/g, '\u06a9')
    .replace(/[â]/g, 'a').replace(/[î]/g, 'i').replace(/[û]/g, 'u');
}}
function filterTable(tableId, query) {{
  const q = normOsm(query.trim());
  document.querySelectorAll('#' + tableId + ' tbody tr.filter-row').forEach(tr => {{
    tr.style.display = normOsm(tr.innerText).includes(q) ? '' : 'none';
  }});
}}
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Osmanlıca resmî evrak JSON analizinden kelime/tamlama/şerhli İnteraktif HTML üretir."
    )
    parser.add_argument("input_json", help="Yapılandırılmış evrak okuma JSON dosyası")
    parser.add_argument("--out", required=True, help="Çıktı HTML dosya yolu")
    args = parser.parse_args()

    src = Path(args.input_json).resolve()
    data = json.loads(src.read_text(encoding="utf-8"))
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_html(data), encoding="utf-8")
    print(f"İnteraktif HTML çalışma kartı oluşturuldu: {out}")


if __name__ == "__main__":
    main()
