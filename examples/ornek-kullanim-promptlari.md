# Örnek Kullanım Promptları (`osmanlica-resmi-evrak`)

## 1. Tek Evrak Derin Diplomatik Okuma + İnteraktif HTML (Mod 1 + Mod 4)
> Bu proje klasöründeki Osmanlıca resmî evrakı (`evrak.jpg`) **üniversite transkripsiyon sistemiyle (TDV İA / TTK)** satır satır oku. Önce diplomatik bölgelere ayır; okuyamadığın veya tereddüt ettiğin kelimeleri asla uydurma, `[...]` veya `[kelime?]` ile işaretleyip 1:1 piksel kesitiyle şerh tablosuna yaz. Hicrî/Rûmî tarihleri `scripts/tarih_cevirici.py` ile kesin Milâdî tarihe çevir. Sonunda kelime kelime (Kubbealtı Lugati bağlantılı), tamlama tamlama ve TDV İslâm Ansiklopedisi kavram notlarıyla birlikte interaktif HTML çalışma kartını bu proje klasörüne kaydet.

## 2. Canlı Chrome DevTools MCP ile BOA / YEK Portal Okuma (Dahili Tarayıcı Yasağı Dahil)
> Bilgisayarımdaki normal Google Chrome tarayıcımda `chrome://inspect/#remote-debugging` ayarını açtım ve `katalog.devletarsivleri.gov.tr` (veya `portal.yek.gov.tr`) sekmesinde incelemek istediğim belgeyi açtım.  
> **ÖNEMLİ:** Antigravity'nin kendi dahili tarayıcısını ASLA açma ("Web Sayfasına Erişim Engellendi" hatası verir); doğrudan `chrome-devtools` MCP ile açık Google Chrome sekmeme bağlan, belgeyi güvenli/sıralı şekilde oku ve tüm 1:1 kanıt kesitleri ile İnteraktif HTML çalışma kartını bu proje klasörüne kaydet.

## 3. Bir Dosya / Gömlek Serisini Kronolojik Özetleme (Mod 2)
> Bu klasördeki 15 adet BOA tahrirat ve mazbata görselini tarih sırasına göre tara. Her belge için fon/tarih (Hicrî-Rûmî-Milâdî), gönderen–muhatap makam, konu özeti ve geçen şahıs/yer/kurum isimlerinden oluşan tek bir kronolojik dizin tablosu çıkar.

## 4. Müsvedde ve Tebyîz Karşılaştırmalı Tahkik (Mod 3)
> Ekteki iki belgeden biri sadâret tezkiresinin müsveddesi, diğeri temize çekilmiş aslıdır. İkisini satır satır karşılaştır; üstü çizilen, sonradan eklenen veya farklılaşan ibareleri kritik aparat (şerh) olarak göster.

## 5. Yalnızca Tamlama ve Kavram Eğitimi (İlahiyat / Tarih / Edebiyat Öğrencileri İçin)
> Bu ferman metnini akademik çeviriyazıyla çıkar, ardından metindeki tüm Arapça ve Farsça tamlamaları (izâfet türleriyle) ayırıp Kubbealtı Lugati ve TDV İslâm Ansiklopedisi bağlantılarıyla interaktif HTML ders notuna dönüştür.

## 6. Çok Sayfalı Defter veya Yazma Eseri 10 Paralel Alt-Ajan (`Subagents`) + Ortak Sözlük (`glossary.md`) ile Okuma/Tercüme (Mod 5)
> Bu proje klasöründeki 100 sayfalık Osmanlıca defteri / Arapça-Osmanlıca el yazması PDF dosyasını paralel alt-ajan orkestrasyonuyla oku ve günümüz Türkçesine aktar:
> 1. Önce sayfaları ayrı görüntülere ayır ve klasörde tüm ajanların ortak okuyacağı bir `glossary.md` (teknik terimler, tamlamalar, şahıs/yer adları ve transkripsiyon ilkeleri sözlüğü) oluştur.
> 2. Sayfaları **10'arlı gruplar halinde paralel alt-ajanlara (`subagent`)** dağıt: aynı anda çalışan 10 ajan kendi sayfasını çevirip/okuyup `sayfalar/sayfa_001.md` ... şeklinde kaydetsin; silik yerleri uydurmayıp `[...]` şerhi düşsün ve yeni terimleri ortak `glossary.md` için raporlasın.
> 3. Tüm sayfalar bittiğinde ayrı bir **Tutarlılık ve Tahkik Editörü Alt-Ajanı** görevlendirerek sayfalar arasındaki terim, özel isim ve üslup birliğini sağla ve tek parça birleşik metni oluştur.
