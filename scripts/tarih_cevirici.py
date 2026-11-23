#!/usr/bin/env python3
"""
tarih_cevirici.py (v2.0) — Modern 3 Yönlü Osmanlıca Tarih Çevirici
(Hicrî Kamerî ↔ Rûmî Malî ↔ Milâdî Gregoryen)

Kullanım:
  python tarih_cevirici.py hicri 10 C 1143
  python tarih_cevirici.py hicri gurre M 1243 --json
  python tarih_cevirici.py rumi 21 Kanunuevvel 1311
  python tarih_cevirici.py miladi 1896-02-07

Özellikler:
  - Tüm Osmanlıca Hicrî ay kısaltmaları (M, S, Ra, R, Ca, C, B, Ş, N, L, Za, Z)
  - Gurre, Evâ'il, Evâsıt, Evâhir, Selh aralık çözümlemesi
  - 1 Mart 1333 (1917) Rûmî Takvim Islahı öncesi/sonrası tam Jülyen/Gregoryen hesabı
  - Üç takvimi (Milâdî, Hicrî, Rûmî) birlikte gösterir + TTK doğrulama bağlantısı + --json desteği
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys

TTK_URL = "https://www.ttk.gov.tr/tarih-cevirme-kilavuzu/"

HICRI_AY_ADLARI = [
    "", "Muharrem", "Safer", "Rebîülevvel", "Rebîülâhir",
    "Cemâziyelevvel", "Cemâziyelâhir", "Receb", "Şa‘bân",
    "Ramazân", "Şevvâl", "Zilkade", "Zilhicce",
]

HICRI_AYLAR = {
    "m": 1, "muharrem": 1, "1": 1,
    "s": 2, "safer": 2, "2": 2,
    "ra": 3, "rebiulevvel": 3, "rebîülevvel": 3, "3": 3,
    "r": 4, "rebiulahir": 4, "rebîülâhir": 4, "4": 4,
    "ca": 5, "cemaziyelevvel": 5, "cemâziyelevvel": 5, "5": 5,
    "c": 6, "cemaziyelahir": 6, "cemâziyelâhir": 6, "6": 6,
    "b": 7, "receb": 7, "recep": 7, "7": 7,
    "ş": 8, "saban": 8, "şaban": 8, "şa'ban": 8, "şa‘bân": 8, "8": 8,
    "n": 9, "ramazan": 9, "ramazân": 9, "9": 9,
    "l": 10, "sevval": 10, "şevval": 10, "şevvâl": 10, "10": 10,
    "za": 11, "zilkade": 11, "11": 11,
    "z": 12, "zilhicce": 12, "12": 12,
}

RUMI_AY_ADLARI = {
    1: "Kânûn-ı S̱ânî (Ocak)", 2: "Şubat", 3: "Mart", 4: "Nisan",
    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
    9: "Eylül", 10: "Teşrîn-i Evvel (Ekim)", 11: "Teşrîn-i S̱ânî (Kasım)", 12: "Kânûn-ı Evvel (Aralık)",
}

RUMI_AYLAR = {
    "mart": 3, "3": 3, "nisan": 4, "4": 4, "mayis": 5, "mayıs": 5, "5": 5,
    "haziran": 6, "6": 6, "temmuz": 7, "7": 7, "agustos": 8, "ağustos": 8, "8": 8,
    "eylul": 9, "eylül": 9, "9": 9,
    "tesrinievvel": 10, "teşrinievvel": 10, "ekim": 10, "10": 10,
    "tesrinisani": 11, "teşrinisani": 11, "kasim": 11, "kasım": 11, "11": 11,
    "kanunuevvel": 12, "kânûnuevvel": 12, "kanunievvel": 12, "aralik": 12, "aralık": 12, "12": 12,
    "kanunusani": 1, "kânûnusânî": 1, "kanunisani": 1, "ocak": 1, "1": 1,
    "subat": 2, "şubat": 2, "2": 2,
}

TR_AYLAR = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
]
TR_GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def hijri_to_jdn(year: int, month: int, day: int) -> int:
    return (
        day
        + (295001 * (month - 1) + 9900) // 10000
        + (year - 1) * 354
        + (3 + 11 * year) // 30
        + 1948439
    )


def jdn_to_hijri(jdn: int) -> tuple[int, int, int]:
    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    month = (24 * l) // 709
    day = l - (709 * month) // 24
    year = 30 * n + j - 30
    return year, month, day


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def jdn_to_gregorian(jdn: int) -> datetime.date:
    a = jdn + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    return datetime.date(year, month, day)


def julian_to_jdn(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083


def jdn_to_julian(jdn: int) -> tuple[int, int, int]:
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + (m // 10)
    return year, month, day


def jdn_to_rumi(jdn: int) -> str:
    dt = jdn_to_gregorian(jdn)
    if dt < datetime.date(1840, 3, 13):
        return "Uygulanmaz (Rûmî takvim 13 Mart 1840'ta resmen yürürlüğe girdi)"
    if dt < datetime.date(1917, 3, 1):
        jy, jm, jd = jdn_to_julian(jdn)
        ry = jy - (585 if jm in (1, 2) else 584)
        return f"R. {jd} {RUMI_AY_ADLARI[jm]} {ry}"
    ry = dt.year - 584
    return f"R. {dt.day} {RUMI_AY_ADLARI[dt.month]} {ry}"


def format_tr(dt: datetime.date) -> str:
    return f"{dt.day} {TR_AYLAR[dt.month]} {dt.year} {TR_GUNLER[dt.weekday()]} ({dt.isoformat()})"


def parse_hicri_day(raw: str) -> tuple[int, int, str]:
    key = raw.strip().lower().replace("'", "").replace("’", "")
    if key in ("gurre", "gurre-i"):
        return 1, 1, "Gurre (1)"
    if key in ("evail", "evâil", "evâ’il"):
        return 1, 10, "Evâ’il (1–10)"
    if key in ("evasit", "evâsıt", "evasıt"):
        return 11, 20, "Evâsıt (11–20)"
    if key in ("evahir", "evâhir"):
        return 21, 30, "Evâhir (21–30)"
    if key in ("selh", "selḫ"):
        return 29, 30, "Selh (29/30)"
    d = int(key)
    if not 1 <= d <= 30:
        raise ValueError("Hicrî gün 1–30 arasında olmalıdır.")
    return d, d, str(d)


def emit(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for k, v in payload.items():
        print(f"{k:<12}: {v}")


def cmd_hicri(args: argparse.Namespace) -> None:
    ay_key = args.month.strip().lower()
    if ay_key not in HICRI_AYLAR:
        sys.stderr.write(f"Hata: Tanınmayan Hicrî ay/kısaltma: {args.month}\n")
        sys.exit(1)
    m = HICRI_AYLAR[ay_key]
    d1, d2, label = parse_hicri_day(args.day)
    j1 = hijri_to_jdn(args.year, m, d1)
    dt1 = jdn_to_gregorian(j1)
    if d1 == d2:
        miladi = format_tr(dt1)
        rumi = jdn_to_rumi(j1)
    else:
        j2 = hijri_to_jdn(args.year, m, d2)
        miladi = f"{format_tr(dt1)} — {format_tr(jdn_to_gregorian(j2))}"
        rumi = f"{jdn_to_rumi(j1)} — {jdn_to_rumi(j2)}"
    emit({
        "Girdi": f"H. {label} {HICRI_AY_ADLARI[m]} {args.year}",
        "Milâdî": miladi,
        "Rûmî": rumi,
        "Not": "Hilâl rü’yeti farkı nedeniyle Hicrî dönüşümde ±1 gün sapma olabilir.",
        "TTK_Kontrol": TTK_URL,
    }, args.json)


def cmd_rumi(args: argparse.Namespace) -> None:
    ay_key = args.month.strip().lower()
    if ay_key not in RUMI_AYLAR:
        sys.stderr.write(f"Hata: Tanınmayan Rûmî ay: {args.month}\n")
        sys.exit(1)
    m = RUMI_AYLAR[ay_key]
    if args.year < 1333 or (args.year == 1333 and m in (1, 2)):
        jy = args.year + (585 if m in (1, 2) else 584)
        jdn = julian_to_jdn(jy, m, args.day)
        not_str = "1917 öncesi Jülyen esaslı Rûmî takvim (+12/+13 gün farkı uygulandı)."
    else:
        dt_g = datetime.date(args.year + 584, m, args.day)
        jdn = gregorian_to_jdn(dt_g.year, dt_g.month, dt_g.day)
        not_str = "1 Mart 1333 (1917) sonrası Gregoryen gün/ay eşitlenmiş Rûmî takvim."
    dt = jdn_to_gregorian(jdn)
    hy, hm, hd = jdn_to_hijri(jdn)
    emit({
        "Girdi": f"R. {args.day} {RUMI_AY_ADLARI[m]} {args.year}",
        "Milâdî": format_tr(dt),
        "Hicrî": f"H. {hd} {HICRI_AY_ADLARI[hm]} {hy}",
        "Not": not_str,
        "TTK_Kontrol": TTK_URL,
    }, args.json)


def cmd_miladi(args: argparse.Namespace) -> None:
    dt = datetime.date.fromisoformat(args.iso_date.strip())
    jdn = gregorian_to_jdn(dt.year, dt.month, dt.day)
    hy, hm, hd = jdn_to_hijri(jdn)
    emit({
        "Girdi": format_tr(dt),
        "Hicrî": f"H. {hd} {HICRI_AY_ADLARI[hm]} {hy}",
        "Rûmî": jdn_to_rumi(jdn),
        "Not": "Hicrî karşılıkta hilâl rü’yeti nedeniyle ±1 gün sapma olabilir.",
        "TTK_Kontrol": TTK_URL,
    }, args.json)


def main() -> None:
    parser = argparse.ArgumentParser(description="3 yönlü Osmanlıca tarih çevirici (Hicrî ↔ Rûmî ↔ Milâdî).")
    sub = parser.add_subparsers(dest="calendar", required=True)

    p_h = sub.add_parser("hicri", help="Hicrî Kamerî → Milâdî & Rûmî")
    p_h.add_argument("day", help="Gün (1-30) veya gurre/evail/evasit/evahir/selh")
    p_h.add_argument("month", help="Ay adı veya arşiv kısaltması (M, S, Ra, R, Ca, C, B, Ş, N, L, Za, Z)")
    p_h.add_argument("year", type=int, help="Hicrî yıl")
    p_h.add_argument("--json", action="store_true", help="JSON formatında çıktı üretir")
    p_h.set_defaults(func=cmd_hicri)

    p_r = sub.add_parser("rumi", help="Rûmî Malî → Milâdî & Hicrî")
    p_r.add_argument("day", type=int, help="Gün (1-31)")
    p_r.add_argument("month", help="Rûmî ay adı")
    p_r.add_argument("year", type=int, help="Rûmî yıl")
    p_r.add_argument("--json", action="store_true", help="JSON formatında çıktı üretir")
    p_r.set_defaults(func=cmd_rumi)

    p_m = sub.add_parser("miladi", help="Milâdî (YYYY-AA-GG) → Hicrî & Rûmî")
    p_m.add_argument("iso_date", help="Milâdî tarih (örn. 1896-02-07)")
    p_m.add_argument("--json", action="store_true", help="JSON formatında çıktı üretir")
    p_m.set_defaults(func=cmd_miladi)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
