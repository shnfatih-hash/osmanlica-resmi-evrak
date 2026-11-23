---
name: osmanlica-resmi-evrak
description: Osmanlıca resmî evrak ve arşiv belgelerini (Ferman, Berat, İrade, Arz Tezkiresi, Arz-ı Hâl, Tahrirat, Mazbata, Buyuruldu, Hüccet, İlam, Telgrafname, Vakfiye) üniversitelerde geçerli İA/TTK/İSAM transkripsiyon sistemiyle satır satır okuma; çözülemeyen/silik kısımlara 1:1 piksel kesitli şerh (kritik aparat) düşme; Hicrî/Rûmî tarih dönüşümü, kelime kelime ve tamlama çözümlemeli interaktif HTML çıktısı üretme ve Kubbealtı Lugati (lugatim.com) ile TDV İslâm Ansiklopedisi (islamansiklopedisi.org.tr) atıflı diplomatik analiz becerisi. Kullanıcı Osmanlıca evrak, ferman, berat, irade, tapu, hüccet, tahrirat, mazbata, arz-ı hâl, matbu veya el yazması belge okuma, transkripsiyon, sadeleştirme veya diplomatik inceleme istediğinde etkinleştirin.
---

# Osmanlıca Resmî Evrak, Diplomatik ve Paleografya Okuma Becerisi

Bu beceri, Osmanlı Türkçesi ile kaleme alınmış resmî evrak ve arşiv belgelerini **diplomatik anatomisi**, **üniversite düzeyinde akademik transkripsiyon (TDV İA / TTK / İSAM)**, **1:1 piksel kesit kanıtı**, **şerh (kritik aparat)** ve **kelime/tamlama çözümlemeli interaktif HTML** standartlarıyla okumak için tasarlanmıştır.

---

## 1. Çalışma Yöntemleri (Kullanıcıya Sunulacak 4 Mod)

Kullanıcı belge(ler) paylaştığında veya talep ilettiğinde amacına uygun modu seçer (belirtilmemişse varsayılan olarak **Mod 1 + Mod 4** birlikte sunulur):

1. **Mod 1 — Tek Evrak Derin Diplomatik Okuma:** Bir belgenin tüm rükünlerini (davet, tuğra/başlık, elkab, nakil/iblâğ, hüküm/talep, tarih, imza/mühür, derkenar/hâmiş/buyuruldu) tespit ederek 3 katmanlı çıktı (*Künye + Akademik Transkripsiyon + Günümüz Türkçesi & Şerhler*) üretir.
2. **Mod 2 — Seri / Dosya İnceleme ve Kronolojik İndeks:** Bir klasördeki birden fazla evrakı (ör. BOA dosya/gömlek serisi) tarih sırasına göre dizip her belge için özet künye, gönderen–alıcı matrisi ve şahıs/yer/kurum dizini çıkarır.
3. **Mod 3 — Karşılaştırmalı Tahkik (Müsvedde / Tebyîz / Suret):** Aynı belgenin müsvedde (taslak), tebyîz (temize çekilmiş asıl) veya suret nüshalarını satır satır karşılaştırıp nüsha farklarını aparat olarak gösterir.
4. **Mod 4 — İnteraktif HTML Çalışma Sayfası (Kelime & Tamlama Çözümlemeli):**
   - Sol/üst bölümde belge künyesi ve 1:1 kritik bölge kesitleri,
   - Satır satır **Akademik Transkripsiyon** ↔ **Günümüz Türkçesi**,
   - **Kelime Kelime Çözümleme (Müfredât)** tablosu (Osmanlıca, çeviriyazı, köken, anlam, Kubbealtı `lugatim.com` doğrulama linki),
   - **Tamlamalar ve Kalıp İfadeler (Terkîbât)** tablosu (Farsça/Arapça izâfet türü, yapısal çözümleme, anlam),
   - **Kurumsal ve Tarihsel Kavramlar (TDV İA Atıflı)** bölümü (`islamansiklopedisi.org.tr` madde bağlantıları ve kısa diplomatik notlar),
   - **Şerh / Aparat (Çözülemeyen ve Şüpheli Yerler)** paneli.

---

## 2. Transkripsiyon Sistemi (Üniversite Standardı: TDV İA / TTK / İSAM)

Okuma çıktısında iki düzey desteklenir; kullanıcı aksini istemedikçe **Düzey A (Tam Akademik)** esas alınır:

- **Düzey A — Tam Akademik Çeviriyazı (İSAM / TDV İA / TTK):**
  - Uzun ünlüler: `â, î, û` (`Â, Î, Û`)
  - Noktalı/çizgili ünsüzler: `s̱` (ث), `ḥ` (ح), `ḫ` (خ), `ẕ` (ذ), `ṣ` (ص), `ż / ḍ` (ض), `ṭ` (ط), `ẓ` (ظ), `ġ` (غ), `ḳ` (ق), `ñ` (ڭ)
  - Ayn ve Hemze: `‘` (ع — U+2018) ve `’` (ء — U+2019)
  - İzâfet ve tamlama kuralları: `fermân-ı hümâyûn`, `irâde-i seniyye`, `bi’l-cümle`, `fi’l-aṣl`, `‘ale’l-‘umûm`, `bi-emri’llâh`.
- **Düzey B — Sadeleştirilmiş Akademik (Yayın/Genel Okur):**
  - Uzun ünlüler (`â, î, û`) ve gerekli yerde ayn/hemze korunur; alt noktalı ünsüzler sadeleştirilir (`h, s, z, t, g, k, n`).

> Ayrıntılı harf karşılıkları, izâfet kuralları ve örnekler için: [references/03-transkripsiyon-elkab-ve-serh-sistemi.md](references/03-transkripsiyon-elkab-ve-serh-sistemi.md)

---

## 3. Altın Kural: Sıfır Halüsinasyon ve Şerh (Kritik Aparat) Protokolü

Osmanlıca el yazması okumasında **tahmin uydurmak kesinlikle yasaktır.** Okunamayan, silik, yırtık, mürekkep dağılmış veya birden fazla okunuşa açık her nokta şu standart akademik işaretlerle gösterilir ve **numaralı Şerh (Aparat) Tablosu**'nda açıklanır:

| İşaret | Anlamı | Şerh Zorunluluğu |
| :--- | :--- | :--- |
| `[...]` | Yırtık, kopuk veya tamamen okunamayan kısım (tahmini uzunlukla: `[... 1 kelime silik]`) | Zorunlu — 1:1 kesit + neden okunamadığı |
| `[kelime?]` | Bağlam ve harf iskeleti güçlü ama kesinleşmemiş okunuş | Zorunlu — 1:1 kesit + alternatif okunuş adayları + sözlük notu |
| `[ek]` | Belgede yazılmamış ama diplomatik formül veya anlam gereği araştırmacının tamamladığı unsur | Zorunlu — neden tamamlandığı |
| `(!)` | Belgede kâtip/müstensih tarafından açık imlâ hatasıyla yazılmış kelime (`sic`) | Zorunlu — belgedeki imlâ ve doğru biçimi |

**Kanıt Seviyeleri:**
- **Kesin (A):** Harf iskeleti, noktalama, diplomatik bağlam ve sözlük doğrulaması tam uyumlu.
- **Güçlü İhtimal (B):** Bir iki nokta/diş silik ama diplomatik kalıp ve bağlam yüksek olasılıkla destekliyor (`[kelime?]` + şerh).
- **Çözülemedi (C):** 1:1 kesit alınmasına rağmen net okunamıyor (`[...]` + şerh; uzman gözüyle yeniden kontrol önerilir).

---

## 4. Altı Aşamalı Okuma İş Akışı

### Aşama 1 — Görüntü Envanteri ve Bölge Ayırma
- Kullanıcı `.jpg / .png / .tif / .pdf / .zip` verdiğinde `scripts/evrak_bolge_kesici.py` ile belgeyi incele:
  1. Görüntü boyutlarını ve çözünürlüğünü kaydet.
  2. Belgeyi diplomatik okuma bölgelerine böl: **üst başlık/davet/tuğra**, **gövde satır şeritleri** (örtüşmeli yatay bantlar), **sağ/sol derkenar (hâmiş) ve buyuruldu alanları**, **alt imza ve mühür bölgesi**.
  3. Küçültülmüş tam sayfa görüntüsüne bakarak tek seferde hüküm verme; her satırı yüksek çözünürlüklü şeritten oku.

### Aşama 2 — Diplomatik ve Paleografik Kimlik Tespiti
- [references/01-diplomatik-belge-turleri.md](references/01-diplomatik-belge-turleri.md) ve [references/02-hat-turleri-ve-paleografya.md](references/02-hat-turleri-ve-paleografya.md) rehberlerine göre belirle:
  - **Belge Türü:** Ferman, Berat, İrade-i Seniyye, Arz Tezkiresi, Arz-ı Hâl, Tahrirat, Mazbata, Şukka, Buyuruldu, Hüccet/İlam, Telgrafname, Vakfiye, Matbu Evrak.
  - **Hat Türü:** Rik'a, Divânî / Celî Divânî, Nesih, Ta'lik (Nesta'lik), Siyakat, Matbu.
  - **Rükün Akışı:** Davet (`Hû`) → Başlık/Elkab → Nakil/İblâğ → Talep/Hüküm → Tarih → İmza/Mühür → Derkenar/Hâmiş/Buyuruldu.

### Aşama 3 — Satır Satır Okuma ve 1:1 Kesit Doğrulaması
- Metni satır numaralarıyla (`[Satır 1]`, `[Satır 2]`, ...) çıkar.
- Şahıs adları, yer adları, rakamlar/tarihler, mühür metinleri ve tereddütlü her kelime için `scripts/evrak_bolge_kesici.py crop` ile **1:1 piksel kesiti** al ve görsel olarak yeniden denetle.

### Aşama 4 — Tarih Dönüşümü (Hicrî / Rûmî → Milâdî)
- Belgedeki tüm Hicrî Kamerî ve Rûmî Malî tarihleri (ve ay kısaltmalarını: `M, S, Ra, R, Ca, C, B, Ş, N, L, Za, Z`) **asla zihinden tahmin etmeden** `scripts/tarih_cevirici.py` ile kesin Milâdî karşılığına çevir.

### Aşama 5 — Sözlük ve TDV İslâm Ansiklopedisi Doğrulaması
- [references/04-sozluk-tdv-ia-dogrulama.md](references/04-sozluk-tdv-ia-dogrulama.md) kurallarını uygula:
  - **Kelime ve Tamlama Kontrolü:** Nadir kelimeler ve Arapça/Farsça tamlamalar için **Kubbealtı Lugati (`https://lugatim.com/s/<kelime>`)** ve kamu malı **Kâmûs-ı Türkî / Redhouse** referanslarını doğrula.
  - **Kurumsal & Tarihsel Kavramlar (TDV İA):** Belgede geçen vergi, rütbe, kalem/daire, hukuk veya diplomatik terimler için **TDV İslâm Ansiklopedisi (`https://islamansiklopedisi.org.tr/`)** maddelerine atıf vererek özgün kısa şerh notu düş (*telif gereği toplu metin kopyalanmaz; kısa özet + madde adı ve URL atfı verilir*).

### Aşama 6 — Çıktı Üretimi (Markdown + İnteraktif HTML)
- Kullanıcıya hem temiz Markdown raporu hem de `scripts/sozluk_ve_html_uretici.py` ile üretilmiş **kelime kelime ve tamlama çözümlemeli, şerhli, Kubbealtı ve TDV İA bağlantılı İnteraktif HTML** çalışma sayfasını sun.

---

## 5. Resmî Portallar ve Chrome DevTools MCP Entegrasyonu

Bu beceri, yerel dosya/klasör okumasının yanı sıra kullanıcının açık Google Chrome oturumuna **Chrome DevTools MCP** (`chrome-devtools-mcp --autoConnect`) üzerinden bağlanarak aşağıdaki resmî portallarda doğrudan tarama ve doğrulama yapabilir:

| Portal | Resmî Adres | Kullanım Amacı |
| :--- | :--- | :--- |
| **Devlet Arşivleri Kataloğu (BOA / BCA)** | `https://katalog.devletarsivleri.gov.tr` | Resmî evrak (Ferman, İrade, Sadâret Mektûbî, Dâhiliye, Hâriciye vb.) arama, künye okuma, güvenli sıralı önizleme |
| **Türkiye Yazma Eserler Kurumu (YEK Portal)** | `https://portal.yek.gov.tr` | Yazma ve nadir matbu eser künyesi, nüsha tespiti, çevrim içi varak görüntüleme |
| **Kubbealtı Lugati** | `https://lugatim.com` | Tekil şüpheli kelime ve tamlama doğrulama (toplu kazıma yapılmaz) |
| **TDV İslâm Ansiklopedisi** | `https://islamansiklopedisi.org.tr` | Kurumsal, hukukî, malî ve diplomatik terimler için canlı madde atfı ve kısa özgün şerh |
| **TTK Tarih Çevirme Kılavuzu** | `https://www.ttk.gov.tr/tarih-cevirme-kilavuzu/` | Yerel `scripts/tarih_cevirici.py` çıktısının resmî çevrimiçi çapraz doğrulaması |

### Chrome DevTools MCP Güvenlik ve Oturum Kuralları
1. **Kullanıcı Girişi & CAPTCHA:** e-Devlet, BOA veya YEK Portal girişlerini ve varsa CAPTCHA doğrulamalarını daima **kullanıcı kendi tarayıcısında** yapar; ajan asla şifre istemez ve güvenlik duvarlarını aşmaya çalışmaz.
2. **WAF Koruması:** `katalog.devletarsivleri.gov.tr` ve `portal.yek.gov.tr` üzerinde asla paralel toplu istek (`Promise.all`) atılmaz; sayfalar tek tek, aralarında en az `1800 ms` bekleme bırakarak incelenir (`scripts/arsiv_portal_helpers.js`). `HTTP 418 / 429` görülürse derhâl durulur.
3. **Bağlantı Kurulumu:** Google Chrome'da yeni sekmede `chrome://inspect/#remote-debugging` açılıp **"Enable remote debugging"** kutucuğu işaretlenir; MCP yapılandırmasında `npx -y chrome-devtools-mcp@latest --autoConnect` kullanılır.

---

## 6. Araçlar ve Referanslar Dizini

- **Referanslar:**
  - `references/01-diplomatik-belge-turleri.md`
  - `references/02-hat-turleri-ve-paleografya.md`
  - `references/03-transkripsiyon-elkab-ve-serh-sistemi.md`
  - `references/04-sozluk-tdv-ia-dogrulama.md`
  - `references/05-akademik-ocr-htr-ekosistemi.md`
- **Python & Tarayıcı Araçları (`scripts/`):**
  - `scripts/evrak_bolge_kesici.py` — Envanter, diplomatik bölge/satır şeridi ayırma ve 1:1 piksel kesit aracı.
  - `scripts/tarih_cevirici.py` — Modern 3 yönlü Hicrî ↔ Rûmî ↔ Milâdî tarih çevirici (`--json` + TTK doğrulama bağlantısı).
  - `scripts/sozluk_ve_html_uretici.py` — JSON analiz dosyasından kelime kelime & tamlama çözümlemeli, şerhli, Kubbealtı ve TDV İA bağlantılı interaktif HTML üretici.
  - `scripts/arsiv_portal_helpers.js` — Chrome DevTools MCP için salt-okunur ve WAF dostu portal okuyucu işlevleri (BOA, YEK, Kubbealtı, TDV İA).
- **Örnekler:**
  - `examples/ornek-kullanim-promptlari.md`
