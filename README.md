---
title: Osmanlıca Resmî Evrak, Diplomatik & Paleografya AI Skill
emoji: 🖋️
colorFrom: red
colorTo: yellow
sdk: static
pinned: true
license: mit
short_description: TDV İA/TTK transkripsiyon, 1:1 şerh ve interaktif HTML aracı
---

# Osmanlıca Resmî Evrak, Diplomatik ve Paleografya AI Skill (`osmanlica-resmi-evrak`)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Bir%20Kahve%20Ismarla-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/shnfatih8)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Projeye%20Destek%20Ol-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/shnfatih-hash)
[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Canlı%20Web%20Aracı-FFD21E?style=for-the-badge)](https://huggingface.co/spaces/sahanfatih/osmanlica-resmi-evrak)
[![GitHub Repo](https://img.shields.io/badge/GitHub-shnfatih--hash%2Fosmanlica--resmi--evrak-181717?style=for-the-badge&logo=github)](https://github.com/shnfatih-hash/osmanlica-resmi-evrak)

Osmanlı Türkçesi ile kaleme alınmış resmî evrak ve arşiv belgelerini (**Ferman, Berat, İrade-i Seniyye, Arz Tezkiresi, Arz-ı Hâl, Tahrirat, Mazbata, Buyuruldu, Hüccet/İlam, Telgrafname, Vakfiye**) üniversitelerde geçerli **TDV İA / TTK / İSAM transkripsiyon sistemiyle** satır satır okuyan, çözülemeyen kısımlara **1:1 piksel kesitli şerh (kritik aparat)** düşen, **3 yönlü Hicrî/Rûmî/Milâdî tarih dönüşümü** yapan ve **kelime kelime + tamlama çözümlemeli interaktif HTML** çalışma sayfası üreten açık kaynaklı yapay zekâ becerisi (*Agent Skill* + *Canlı Web Aracı*).

> **Kardeş Projeler:**  
> - Aile ve soy kütüğü defterleri (`NFS.d`, `ML.VRD.TMT.d`, `MŞH.ŞSC.d`, `MAD.d`, `TT.d`) için: **[`shnfatih-hash/devlet-arsivleri-soykutugu`](https://github.com/shnfatih-hash/devlet-arsivleri-soykutugu)**  
> - Çok sayfalı Arapça/Osmanlıca/Farsça yazma eserlerin 10'lu paralel alt-ajan ve ortak sözlükle tercümesi için: **[`shnfatih-hash/yazma-eser-paralel-tercume`](https://github.com/shnfatih-hash/yazma-eser-paralel-tercume)**

---

## Temel Özellikler

1. **Üniversite Transkripsiyon Standardı (TDV İA / TTK / İSAM):**
   - `â, î, û`, `ḥ, ḫ, ṣ, ż/ḍ, ṭ, ẓ, ġ, ḳ, ñ, s̱, ẕ` ve `‘` (ayn) / `’` (hemze) işaretleriyle tam akademik çeviriyazı + isteğe bağlı sadeleştirilmiş yayın modu.
2. **Sıfır Kayıp, Sıfır Halüsinasyon & Numaralı Şerh (Aparat) Sistemi:**
   - Elkab, dua, vakfiye şartları, *şuhûdü'l-hâl* ve Arapça/Farsça mülemma ibareler *"zaten Türkçe / klasik formül"* diyerek özetlenmez; kenar `sahh` tashihleri ait olduğu cümleye işlenir, derkenar/buyuruldu notları ilgili paragrafın hemen altında sunulur.
   - Okunamayan veya tereddütlü her kelime `[...]`, `[kelime?]`, `[ek]`, `(!)` işaretleriyle belirtilir ve 1:1 piksel kesitiyle şerh tablosuna alınır.
3. **5 Farklı Çalışma Yöntemi:**
   - **Mod 1:** Tek Evrak Derin Diplomatik Okuma
   - **Mod 2:** Seri / Dosya İnceleme ve Kronolojik İndeks
   - **Mod 3:** Karşılaştırmalı Tahkik (Müsvedde / Tebyîz / Suret)
   - **Mod 4:** İnteraktif HTML Çalışma Kartı (Kelime Kelime & Tamlama Çözümlemeli)
   - **Mod 5:** Çok Sayfalı Defter / Yazma Eserde **10 Paralel Alt-Ajan (`Subagents`) + Ortak Sözlük (`glossary.md`) + Tutarlılık Editörü** Orkestrasyonu
4. **Sözlük ve TDV İslâm Ansiklopedisi Entegrasyonu (Telif Dostu):**
   - Her kelime için **Kubbealtı Lugati (`lugatim.com`)** doğrulama bağlantısı ve kamu malı **Kâmûs-ı Türkî / Redhouse** referansı.
   - Kurumsal, hukukî, malî ve diplomatik kavramlar için **TDV İslâm Ansiklopedisi (`islamansiklopedisi.org.tr`)** madde bağlantıları ve atıflı kısa şerhler.
5. **Yerleşik Python Yardımcı Araçları & Canlı Gradio Arayüzü:**
   - `scripts/evrak_bolge_kesici.py` — Belgeyi diplomatik bölgelere ve yatay satır şeritlerine böler, 1:1 piksel kanıt kesiti alır (zip-slip ve zip bombası korumalı).
   - `scripts/tarih_cevirici.py` — Hicrî Kamerî, Rûmî Malî ve Milâdî tarihleri (Osmanlıca ay kısaltmaları ve *gurre/evâil/evâsıt/evâhir/selh* dahil) 3 yönlü çevirir.
   - `scripts/sozluk_ve_html_uretici.py` — JSON okuma verisinden aranabilir, kelime/tamlama/şerh sekmeli interaktif HTML çalışma sayfası üretir.

---

## Hızlı Kurulum, Proje Klasörü ve Chrome DevTools MCP Ayarı

### 1. Özel Proje Klasörü ve Python Bağımlılığı
Masaüstünüzde belgeleriniz için ayrı bir çalışma klasörü (ör. `Osmanlica_Evrak_Inceleme`) açıp Antigravity'de **`Open Folder`** ile açın; böylece tüm 1:1 satır kesitleri ve üretilen İnteraktif HTML çalışma kartları düzenli olarak bu klasöre kaydedilir.
```bash
# Python 3.8+ gereklidir
pip install Pillow
```

### 2. Skill Paketini Tek Komutla Kurma
```powershell
# Windows (PowerShell) — Google Antigravity
git clone https://github.com/shnfatih-hash/osmanlica-resmi-evrak.git "$HOME\.gemini\config\skills\osmanlica-resmi-evrak"
```
```bash
# macOS / Linux — Google Antigravity veya Claude Code
git clone https://github.com/shnfatih-hash/osmanlica-resmi-evrak.git ~/.gemini/config/skills/osmanlica-resmi-evrak
git clone https://github.com/shnfatih-hash/osmanlica-resmi-evrak.git ~/.claude/skills/osmanlica-resmi-evrak
```

### 3. Chrome DevTools MCP Ayarı ve ⚠️ `"Web Sayfasına Erişim Engellendi"` Hatasının Çözümü
Açık Google Chrome oturumunuzda **Devlet Arşivleri (`katalog.devletarsivleri.gov.tr`)**, **YEK Portal (`portal.yek.gov.tr`)**, **Kubbealtı Lugati (`lugatim.com`)**, **TDV İslâm Ansiklopedisi (`islamansiklopedisi.org.tr`)** ve **TTK Tarih Çevirme Kılavuzu (`ttk.gov.tr/tarih-cevirme-kilavuzu`)** ile doğrudan çalışmak için:

1. MCP yapılandırma dosyanıza (`~/.gemini/config/mcp_config.json` / `.mcp.json`) şu bloğu ekleyin:
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
2. Bilgisayarınızdaki **normal Google Chrome** tarayıcısında yeni sekmede `chrome://inspect/#remote-debugging` adresine gidip **"Enable remote debugging"** kutucuğunu işaretleyin.
3. Kendi hesabınızla BOA veya YEK Portal'a **normal Google Chrome üzerinden** giriş yapın.

> **⚠️ Önemli Sorun Giderme (`Web Sayfasına Erişim Engellendi`):**  
> Antigravity'nin sağ paneldeki **kendi yerleşik tarayıcısı (*built-in browser*)** Devlet Arşivleri güvenlik duvarı tarafından engellenir. Eğer bu ekranı görürseniz yerleşik tarayıcıyı kapatın, normal Google Chrome'u açıp e-Devlet/BOA girişinizi oradan yapın ve Antigravity'ye *"Kendi dahili tarayıcını açma; doğrudan **Chrome DevTools MCP** ile açık Google Chrome sekmeme bağlan"* deyin. Dilerseniz belgeleri normal Chrome'dan indirip klasöre atarak hiç MCP olmadan da okutabilirsiniz.

---

## Çok Sayfalı Defter ve El Yazmalarında Paralel Alt-Ajan (`Subagents`) İş Akışı

Elinizde 50–100+ sayfalık bir şer'iyye sicili, mühimme defteri veya Arapça/Osmanlıca el yazması PDF olduğunda **Mod 5** ile:
1. Ana sohbet oturumu koordinatör olur ve proje klasöründe ortak bir **`glossary.md`** (terimler, elkab ve özel isimler sözlüğü) başlatır.
2. **10 paralel alt-ajan** aynı anda farklı sayfaları (`sayfa_001.md` ... `sayfa_010.md`) çevirip/transkribe edip kaydeder.
3. Tüm sayfalar bitince bir **Tutarlılık ve Tahkik Editörü Ajanı** tüm sayfalar arasındaki terim ve üslup birliğini sağlar. *(Hazır prompt için bkz. [`examples/ornek-kullanim-promptlari.md`](./examples/ornek-kullanim-promptlari.md) — Şablon 6).*

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
python scripts/sozluk_ve_html_uretici.py examples/ornek_evrak_verisi.json --out evrak_calisma_karti.html
```

---

## 🤝 Soru Sor, Terim Ekle ve Katkıda Bulun

Kod veya Git bilmeden de aşağıdaki hazır formlarla teknik soru sorabilir, yeni diplomatik kalıp/elkab/TDV İA terimi veya prompt önerisi paylaşabilirsiniz (ayrıntılar: [CONTRIBUTING.md](CONTRIBUTING.md)):

- ❓ **[Teknik Soru & Kurulum Desteği](https://github.com/shnfatih-hash/osmanlica-resmi-evrak/issues/new?template=01-soru-ve-teknik-destek.yml)**
- 📖 **[Yeni Diplomatik Terim, Elkab veya Tamlama Katkısı](https://github.com/shnfatih-hash/osmanlica-resmi-evrak/issues/new?template=02-terim-ve-sozluk-katkisi.yml)**
- 💡 **[Yeni Prompt veya Özellik Önerisi](https://github.com/shnfatih-hash/osmanlica-resmi-evrak/issues/new?template=03-prompt-ve-yontem-onerisi.yml)**
- 🐛 **[Hata Bildirimi](https://github.com/shnfatih-hash/osmanlica-resmi-evrak/issues/new?template=04-hata-bildirimi.yml)** • 💬 **[Hugging Face Topluluk](https://huggingface.co/spaces/sahanfatih/osmanlica-resmi-evrak/discussions)**

---

## ♥ Projeye Gönüllü Destek

Bu proje tamamen ücretsiz ve açık kaynaklıdır; herkesin özgürce kullanımına açık kalacaktır. Çalışmayı faydalı bulduysanız ve yeni Osmanlı arşivi, yazma eser ve dijital beşerî bilimler AI Skill'lerinin geliştirilmesine gönüllü olarak katkıda bulunmak isterseniz bir kahve ısmarlayarak veya GitHub Sponsors üzerinden destek olabilirsiniz:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Bir%20Kahve%20Ismarla-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/shnfatih8)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Projeye%20Destek%20Ol-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/shnfatih-hash)

---

## Lisans

MIT Lisansı — bkz. [LICENSE](LICENSE).
