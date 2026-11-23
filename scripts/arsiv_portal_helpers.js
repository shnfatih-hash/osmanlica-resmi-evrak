/**
 * arsiv_portal_helpers.js
 * Chrome DevTools MCP `evaluate_script` için salt-okunur ve WAF dostu yardımcı işlevler.
 * Desteklenen portallar:
 *  - katalog.devletarsivleri.gov.tr (BOA / BCA)
 *  - portal.yek.gov.tr (Türkiye Yazma Eserler Kurumu)
 *  - lugatim.com (Kubbealtı Lugati — canlı tekil kelime doğrulama)
 *  - islamansiklopedisi.org.tr (TDV İslâm Ansiklopedisi — canlı tekil madde özeti)
 *
 * GÜVENLİK KURALI:
 *  - Asla paralel toplu istek (Promise.all) atmaz.
 *  - Hiçbir giriş/CAPTCHA/yetki duvarını atlamaz; oturum açma daima kullanıcıya aittir.
 */

// 1) Devlet Arşivleri Kataloğu (katalog.devletarsivleri.gov.tr) sonuç tablosunu okuma
export function readDabSearchResults() {
  const rows = Array.from(document.querySelectorAll("table tbody tr"));
  return rows.map((tr, i) => {
    const cells = Array.from(tr.querySelectorAll("td")).map(td => td.innerText.trim());
    return { index: i + 1, cells };
  }).filter(r => r.cells.length > 0);
}

// 2) YEK Portal (portal.yek.gov.tr/works/detail/...) künye alanlarını okuma
export function readYekWorkMetadata() {
  const title = document.querySelector("h1, h2, .work-title")?.innerText?.trim() || document.title;
  const rows = Array.from(document.querySelectorAll("tr, .detail-row, dl > div")).map(el => el.innerText.trim()).filter(Boolean);
  return { url: location.href, title, metadata_lines: rows.slice(0, 40) };
}

// 3) Kubbealtı Lugati (lugatim.com/s/...) tekil kelime anlam özeti (canlı doğrulama için)
export function readLugatimEntry() {
  const heading = document.querySelector("h1, h2, .word-title")?.innerText?.trim() || "";
  const meanings = Array.from(document.querySelectorAll("p, li, .meaning")).map(e => e.innerText.trim()).filter(t => t.length > 2).slice(0, 12);
  return { url: location.href, heading, meanings };
}

// 4) TDV İslâm Ansiklopedisi (islamansiklopedisi.org.tr/...) madde başlığı ve ilk paragraf atfı
export function readTdvIaEntry() {
  const heading = document.querySelector("h1")?.innerText?.trim() || document.title;
  const author = document.querySelector(".author, .maddemüellifi, [class*='author']")?.innerText?.trim() || "";
  const firstParagraphs = Array.from(document.querySelectorAll("article p, .madde-metin p, main p"))
    .map(p => p.innerText.trim())
    .filter(t => t.length > 40)
    .slice(0, 2);
  return { url: location.href, heading, author, lead_summary_only: firstParagraphs };
}
