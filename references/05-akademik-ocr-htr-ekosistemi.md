# 05 — Akademik AI OCR / HTR Ekosistemi ve Hibrit İş Akışı

Büyük ölçekli belge serilerinde (ör. yüzlerce sayfalık matbu/el yazması koleksiyonlar) multimodal yapay zekâ okumasını akademik HTR/OCR araçlarıyla birleştirmek doğruluk ve hız sağlar.

---

## 1. Türkiye Üniversite ve Akademik Projeleri

- **Vesiqari** *(Boğaziçi Üni. & İTÜ Teknopark & TÜBİTAK BİGG)*: Osmanlı Türkçesi belgeleri ve matbu eserleri yapay zekâ tabanlı OCR/HTR ile Latin harflerine aktarma ve arşiv içi arama platformu.
- **Osmanlica.com** *(İstanbul Üniversitesi-Cerrahpaşa — Doç. Dr. Atakan Kurt & Dr. İshak Dölek, TÜBİTAK 1512 & KOSGEB)*: 3 aşamalı boru hattı (*OCR/HTR → Alfabe/Transkripsiyon → Günümüz Türkçesine Çeviri*).
- **Akis Projesi** *(Sabancı Üni. Prof. Dr. Berrin Yanıkoğlu + İstanbul Medeniyet Üni. + Viyana Üni., TÜBİTAK)*: Matbu ve arşiv metinlerinin yapay zekâ ile Latin alfabesine aktarımı.
- **OTA-BOUN / HisTR** *(Boğaziçi Üniversitesi)*: Tarihsel Türkçe ve Osmanlıca NLP kıyaslama veri setleri.

---

## 2. Uluslararası Açık Kaynak ve Akademik HTR/OCR Ekosistemi

| Araç / Repo | Ne İşe Yarar? | Hibrit Kullanım Senaryosu |
| :--- | :--- | :--- |
| **OpenITI / Kraken / eScriptorium** (`OpenITI/ocr_with_kraken_public`, `OpenITI/arabic_script_ocr_models`) | Açık kaynak satır bölütleyici ve Arap harfli HTR/OCR motoru. | Yüzlerce sayfalık matbu/nesih metinlerde ilk ham metni yerel olarak çıkarıp bu Skill ile diplomatik düzeltme + şerh yapmak. |
| **OpenITI MAKHZAN** (`OttomanNLP/OpenITI-MAKHZAN-Ottoman-Lines`) | Açık erişimli satır düzeyi Osmanlıca HTR veri seti. | Kendi yerel Kraken/TrOCR modelini eğitmek isteyen araştırmacılar için temel eğitim seti. |
| **`YusufByn/htr-ottoman`** (Zenodo DOI `10.5281/zenodo.23502722`) | OpenITI MAKHZAN üzerinde ince ayarlı Osmanlıca nesih Kraken modeli. | Nesih el yazmalarında ön transkripsiyon üretmek. |
| **Transkribus (READ-COOP)** (`OttomanTurkish_generic`, `Ottoman Fatwa Manuscript`, `OttomanTurkish_Print_1/v2`) | Freiburg Üni. MultiHTR ve Digital Ottoman Corpora kamu modelleri. | Çok sayfalı fetva/yazma/gazete koleksiyonlarında ön okuma çıkarıp bu Skill ile TDV İA transkripsiyonuna ve HTML çalışma kartına dönüştürmek. |
| **`umute642-boop/RikaOCR`** & **`Ottoman-NLP/ottominer-public`** | Rik'a OCR ve tarihî Osmanlıca PDF yerleşim/metin madenciliği araçları. | 19. yüzyıl resmî Rik'a evraklarında deneysel satır çıkarımı. |
| **`gusta-bib/ottoman-htr`** *(Usta, Alpoğlu & Günaydın, 2026; DOI: `10.21203/rs.3.rs-10418926/v1`)* | `Qwen2.5-VL-3B` tabanlı ince ayarlı Osmanlıca HTR modelleri (*Azra 1/2*) ve `ي/ى/ی` – `ك/ک/ڭ` Unicode eşitleme protokolü. | Küçük 3B modellerin tek başına harf hata oranı yüksek olduğundan (*Rik'a %21,9 CER; Nesih %35,5 CER; DBNet satır bölütleme %19,5 kesinlik*) doğrudan arşiv okumasında birincil büyük multimodal modelin yerine kullanılmaz; ancak makaledeki **kanonik Ye/Kef Unicode normalizasyonu** ve **Şer'iyye sicili kalıp imlâ kuralları** (`şuhûdü'l-hâl`, `ڭ` Sağır Kef, `غروش`) bu becerinin sözlük ve arama katmanına entegre edilmiştir. |
| **`cdliai/ottoman-ner`** | Osmanlı Türkçesi Varlık İsmi Tanıma (şahıs, yer, kurum). | Seri/dosya okuma modunda (Mod 2) otomatik dizin çıkarımı. |

---

## 3. Önerilen Hibrit Akış

1. **1–10 Evraklık Derin Diplomatik Çalışma:** Doğrudan bu Skill (`scripts/evrak_bolge_kesici.py` + multimodal yüksek çözünürlüklü satır okuması + 1:1 şerh kesitleri + `tarih_cevirici.py` + `sozluk_ve_html_uretici.py`).
2. **50–1000+ Sayfalık Koleksiyon / Defter Serisi:** Önce **Kraken / eScriptorium** veya **Transkribus** ile ham satır dökümü alınır; ardından kritik belgeler ve şüpheli satırlar bu Skill'in **1:1 kesit + TDV İA/Kubbealtı doğrulama + şerh** boru hattından geçirilir.
