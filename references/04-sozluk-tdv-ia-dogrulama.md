# 04 — Sözlükler ve TDV İslâm Ansiklopedisi (TDV İA) Doğrulama Protokolü

Osmanlıca resmî evrak okumasında yalnızca harf çözmek yetmez; kelimenin **dönemsel anlamı** ve bürokratik kavramın **kurumsal-tarihsel arka planı** da doğrulanmalıdır.

---

## 1. Sözlük Katmanı (Kelime ve Tamlama Doğrulama)

| Kaynak | Erişim / Telif Durumu | Kullanım Amacı |
| :--- | :--- | :--- |
| **Kubbealtı Lugati** (`https://lugatim.com`) | Vakıf telifli — **toplu kazıma yapılmaz**, canlı arama linki ve atıf olarak kullanılır. | Osmanlıca kelimelerin Türkçe kullanım nüansları, tamlama örnekleri ve köken kontrolü. URL kalıbı: `https://lugatim.com/s/<kelime>` |
| **Şemseddin Sami — *Kâmûs-ı Türkî* (1901)** | Kamu malı | 19.–20. yüzyıl geç dönem Osmanlı Türkçesi kelimelerinin otoriter imlâ ve anlam kontrolü. |
| **Sir James Redhouse — *Turkish and English Lexicon* (1890)** | Kamu malı | Nadir bürokratik, askerî ve hukukî terimlerin çapraz doğrulaması. |
| **Ferit Devellioğlu — *Osmanlıca-Türkçe Ansiklopedik Lûgat*** | Yayınevi telifli | Standart transkripsiyon ve Arapça/Farsça terkiplerin akademik kontrolü. |
| **Mehmet Zeki Pakalın — *Osmanlı Tarih Deyimleri ve Terimleri Sözlüğü*** | Klasik başvuru eseri | Vergi, makam, rütbe, unvan ve saray/taşra deyimlerinin anlamı. |

---

## 2. TDV İslâm Ansiklopedisi (`islamansiklopedisi.org.tr`) Entegrasyonu

**Türkiye Diyanet Vakfı İslâm Ansiklopedisi (TDV İA)**, Osmanlı kurumları, hukuku, maliyesi, diplomatik belgeleri ve tarihî coğrafyası için en güvenilir Türkçe akademik başvuru kaynağıdır.

### Telif Haklarına Tam Saygılı 3 Katmanlı Entegrasyon Modeli

1. **Otomatik Madde & Arama Bağlantısı (HTML + Markdown):**
   - `scripts/sozluk_ve_html_uretici.py`, belgede geçen her kurumsal/diplomatik kavram için otomatik olarak:
     - Doğrudan madde linki (biliniyorsa: `https://islamansiklopedisi.org.tr/<slug>`),
     - Arama linki (`https://islamansiklopedisi.org.tr/arama/?q=<terim>`)
     üretir.
2. **Canlı Anlamlandırma ve Kısa Özgün Şerh (Ajan Araştırması):**
   - Belgede kritik bir kurum, vergi, rütbe veya hukuk terimi geçtiğinde (ör. *Avârız, Buyuruldu, İrâde-i Seniyye, Meclis-i Vâlâ, Mütesellim, Salyâne, Temettuat, Tekâlif-i Örfiyye, Kethüda, Tımar, Zeamet, Şühûdü’l-hâl*), yapay zekâ ajanı web arama veya kullanıcının açık tarayıcı oturumu üzerinden ilgili TDV İA maddesine başvurarak **kopyala-yapıştır yapmadan 2–3 cümlelik özgün akademik şerh** yazar ve madde başlığı + URL atfı ekler.
3. **Kavram Haritası (Sık Karşılaşılan TDV İA Maddeleri):**
   - **Belgeler:** `ferman`, `berat`, `irade-i-seniyye`, `buyuruldu`, `tezkire`, `mazbata`, `arzuhal`, `huccet`, `ilam`, `vakfiye`, `muhimme-defteri`, `seriyye-sicilleri`
   - **Kurum & Görevliler:** `babiali`, `sadaret`, `meclis-i-vala-yi-ahkam-i-adliyye`, `sura-yi-devlet`, `defterhane`, `kadi`, `mutesellim`, `kethuda`, `ayan`, `muhtar`
   - **Vergi & Maliye:** `avariz`, `osr`, `temettuat`, `cizye`, `iltizam`, `mukataa`, `timar`, `zeamet`, `tekalif-i-orfiyye`

---

## 3. Kelime & Tamlama Çıkarma Standardı (HTML Çalışma Kartı İçin)

Her evrak çözümlemesinde şu iki ayrı liste hazırlanır:
1. **Müfredât (Kelime Kelime Liste):**
   - `osmanlica` (Arap harfli), `transkripsiyon` (TDV İA), `koken` (Arapça / Farsça / Türkçe), `anlam`, `satir_no`, `lugatim_sorgu`.
2. **Terkîbât (Tamlamalar ve Kalıp İfadeler):**
   - `osmanlica`, `transkripsiyon`, `tur` (*Farsça isim tamlaması*, *Farsça sıfat tamlaması*, *Arapça harf-i tarifli terkip*, *Diplomatik kalıp*), `cozumleme` (unsur unsur ayırma), `gunumuz_turkcesi`, `tdv_ia_slug` (varsa).
