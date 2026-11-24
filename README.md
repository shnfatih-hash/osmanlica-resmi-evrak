# Osmanlıca Resmî Evrak, Diplomatik ve Paleografya AI Skill

Osmanlı Türkçesi ile kaleme alınmış resmî evrak ve arşiv belgelerini (**Ferman, Berat, İrade-i Seniyye, Arz Tezkiresi, Arz-ı Hâl, Tahrirat, Mazbata, Buyuruldu, Hüccet/İlam, Telgrafname, Vakfiye**) üniversitelerde geçerli **TDV İA / TTK / İSAM transkripsiyon sistemiyle** satır satır okuyan, çözülemeyen kısımlara **1:1 piksel kesitli şerh (kritik aparat)** düşen, **Hicrî/Rûmî tarih dönüşümü** yapan ve **kelime kelime + tamlama çözümlemeli interaktif HTML** çalışma sayfası üreten açık kaynaklı yapay zekâ becerisi (*Agent Skill*).

> **Kardeş Proje:** Aile ve soy kütüğü defterleri (`NFS.d`, `ML.VRD.TMT.d`, `TT.d`) için geliştirilmiş kardeş beceri: [`devlet-arsivleri-soykutugu`](https://github.com/shnfatih-hash/devlet-arsivleri-soykutugu)

---

## Temel Özellikler

1. **Üniversite Transkripsiyon Standardı (TDV İA / TTK / İSAM):**
   - `â, î, û`, `ḥ, ḫ, ṣ, ż/ḍ, ṭ, ẓ, ġ, ḳ, ñ, s̱, ẕ` ve `‘` (ayn) / `’` (hemze) işaretleriyle tam akademik çeviriyazı + isteğe bağlı sadeleştirilmiş yayın modu.
2. **Sıfır Halüsinasyon & Numaralı Şerh (Aparat) Sistemi:**
   - Okunamayan veya tereddütlü her kelime `[...]`, `[kelime?]`, `[ek]`, `(!)` işaretleriyle belirtilir ve 1:1 piksel kesitiyle şerh tablosuna alınır.
3. **4 Farklı Çalışma Yöntemi:**
   - Tek Evrak Derin Diplomatik Okuma
   - Seri / Dosya İnceleme ve Kronolojik İndeks
   - Karşılaştırmalı Tahkik (Müsvedde / Tebyîz / Suret)
   - İnteraktif HTML Çalışma Kartı (Kelime Kelime & Tamlama Çözümlemeli)
4. **Sözlük ve TDV İslâm Ansiklopedisi Entegrasyonu (Telif Dostu):**
   - Her kelime için **Kubbealtı Lugati (`lugatim.com`)** doğrulama bağlantısı ve kamu malı **Kâmûs-ı Türkî / Redhouse** referansı.
   - Kurumsal, hukukî, malî ve diplomatik kavramlar için **TDV İslâm Ansiklopedisi (`islamansiklopedisi.org.tr`)** madde bağlantıları ve atıflı kısa şerhler.
5. **Yerleşik Python Yardımcı Araçları:**
   - `scripts/evrak_bolge_kesici.py` — Belgeyi diplomatik bölgelere ve yatay satır şeritlerine böler, 1:1 piksel kanıt kesiti alır (zip-slip ve zip bombası korumalı).
   - `scripts/tarih_cevirici.py` — Hicrî Kamerî ve Rûmî Malî tarihleri (Osmanlıca ay kısaltmaları dahil) kesin Milâdî tarihe çevirir.
   - `scripts/sozluk_ve_html_uretici.py` — JSON okuma verisinden aranabilir, kelime/tamlama/şerh sekmeli interaktif HTML çalışma sayfası üretir.

---

## Hızlı Kurulum ve Chrome DevTools MCP Ayarı

### 1. Python Bağımlılığı
```bash
# Python 3.8+ gereklidir
pip install Pillow
```

### 2. Skill Paketini Kurma
Skill klasörünü kullandığınız AI ajan aracının `skills` dizinine kopyalayın:
- **Antigravity / Gemini:** `~/.gemini/config/skills/osmanlica-resmi-evrak/`
- **Claude Code:** `~/.claude/skills/osmanlica-resmi-evrak/`

### 3. Chrome DevTools MCP Ayarı (BOA, YEK Portal, Kubbealtı, TDV İA Canlı Erişim)
Açık Google Chrome oturumunuzda **Devlet Arşivleri (`katalog.devletarsivleri.gov.tr`)**, **YEK Portal (`portal.yek.gov.tr`)**, **Kubbealtı Lugati (`lugatim.com`)**, **TDV İslâm Ansiklopedisi (`islamansiklopedisi.org.tr`)** ve **TTK Tarih Çevirme Kılavuzu (`ttk.gov.tr/tarih-cevirme-kilavuzu`)** ile doğrudan çalışmak için:

1. MCP yapılandırma dosyanıza (`mcp_config.json` / `.mcp.json`) şu bloğu ekleyin:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--autoConnect"]
    }
  }
}
```
2. Google Chrome'da yeni sekmede `chrome://inspect/#remote-debugging` adresine gidip **"Enable remote debugging"** kutucuğunu işaretleyin.
3. Kendi hesabınızla BOA veya YEK Portal'a giriş yaptıktan sonra ajana doğrudan *"açık sekmedeki evrakı oku"* demeniz yeterlidir.

---

## Python Araçlarını Doğrudan Kullanma

```bash
# 1) Belge envanteri ve yatay satır şeritlerine bölme
python scripts/evrak_bolge_kesici.py split evrak.jpg --bands 6 --out ./bolgeler

# 2) Belirli bir kelime/mühür için 1:1 piksel kesiti
python scripts/evrak_bolge_kesici.py crop evrak.jpg --box 120,450,900,620 --scale 2 --out ./kesit_muhur.png

# 3) 3 Yönlü Modern Tarih Çevirici (Hicrî ↔ Rûmî ↔ Milâdî + --json)
python scripts/tarih_cevirici.py hicri 10 C 1143
python scripts/tarih_cevirici.py rumi 21 Kanunuevvel 1311
python scripts/tarih_cevirici.py miladi 1896-02-07 --json

# 4) Kelime/tamlama çözümlemeli İnteraktif HTML üretimi
python scripts/sozluk_ve_html_uretici.py ornek_evrak.json --out evrak_calisma_karti.html
```

---

## ♥ Projeye Gönüllü Destek

Bu proje tamamen ücretsiz ve açık kaynaklıdır; herkesin özgürce kullanımına açık kalacaktır. Çalışmayı faydalı bulduysanız ve yeni Osmanlı arşivi, yazma eser ve dijital beşerî bilimler AI Skill'lerinin geliştirilmesine gönüllü olarak katkıda bulunmak isterseniz bir kahve ısmarlayarak veya GitHub Sponsors üzerinden destek olabilirsiniz:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Bir%20Kahve%20Ismarla-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/shnfatih8)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Projeye%20Destek%20Ol-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/shnfatih-hash)

---

## Lisans

MIT Lisansı — bkz. [LICENSE](LICENSE).
