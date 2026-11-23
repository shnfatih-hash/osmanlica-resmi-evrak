#!/usr/bin/env python3
"""
evrak_bolge_kesici.py — Osmanlıca Resmî Evrak Diplomatik Bölge Ayırma ve 1:1 Kesit Aracı

Alt komutlar:
  inventory <girdi_klasoru>
  split     <evrak_gorseli> --bands 6 --out <cikti_klasoru>
  crop      <evrak_gorseli> --box x1,y1,x2,y2 --scale 2 --out <kesit.png>

Gereksinim: Python 3.8+ ve Pillow (`pip install Pillow`)
"""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("Hata: Pillow yüklü değil. Kurmak için: pip install Pillow\n")
    sys.exit(1)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
MAX_ZIP_UNCOMPRESSED_BYTES = 4 * 1024 ** 3  # 4 GB zip bombası koruması
MAX_ZIP_MEMBERS = 5000


def extract_zips_safely(input_dir: Path, extract_root: Path) -> list[Path]:
    """Klasördeki .zip arşivlerini zip-slip ve zip-bomb korumasıyla açar."""
    found: list[Path] = []
    for root, _, files in os.walk(input_dir):
        for fname in sorted(files):
            fpath = Path(root) / fname
            ext = fpath.suffix.lower()
            if ext in IMAGE_EXTS:
                found.append(fpath)
            elif ext == ".zip":
                target = extract_root / fpath.stem
                if not target.exists():
                    target.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(fpath, "r") as zf:
                        members = zf.infolist()
                        total_size = sum(m.file_size for m in members)
                        if len(members) > MAX_ZIP_MEMBERS or total_size > MAX_ZIP_UNCOMPRESSED_BYTES:
                            raise ValueError(
                                f"Arşiv güvenlik sınırını aşıyor ({len(members)} dosya, {total_size} bayt): {fpath.name}"
                            )
                        base = target.resolve()
                        for member in members:
                            dest = (target / member.filename).resolve()
                            if os.path.commonpath([str(base), str(dest)]) != str(base):
                                raise ValueError(f"Güvensiz zip yolu reddedildi: {member.filename}")
                            zf.extract(member, target)
                for zroot, _, zfiles in os.walk(target):
                    for zf_name in sorted(zfiles):
                        zp = Path(zroot) / zf_name
                        if zp.suffix.lower() in IMAGE_EXTS:
                            found.append(zp)
    return sorted(set(found))


def cmd_inventory(args: argparse.Namespace) -> None:
    input_dir = Path(args.input_dir).resolve()
    if not input_dir.exists():
        sys.stderr.write(f"Hata: Klasör bulunamadı: {input_dir}\n")
        sys.exit(1)
    extract_root = input_dir / "_acilan_evraklar"
    images = extract_zips_safely(input_dir, extract_root)
    print(f"Toplam görüntü sayısı: {len(images)}\n")
    print(f"{'No':<4} {'Genişlik':>8} {'Yükseklik':>9}  Dosya")
    print("-" * 74)
    for idx, img_path in enumerate(images, 1):
        try:
            with Image.open(img_path) as im:
                w, h = im.size
        except Exception as exc:
            print(f"{idx:<4} {'HATA':>8} {'-':>9}  {img_path} ({exc})")
            continue
        rel = img_path.relative_to(input_dir) if input_dir in img_path.parents else img_path
        print(f"{idx:<4} {w:>8} {h:>9}  {rel}")


def cmd_split(args: argparse.Namespace) -> None:
    src = Path(args.image).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    with Image.open(src) as im:
        w, h = im.size
        # 1. Üst başlık / davet (Hû) / tuğra / antet (%22)
        im.crop((0, 0, w, int(h * 0.22))).save(out_dir / f"{stem}_00_ust_baslik.png")

        # 2. Sağ derkenar / hâmiş / buyuruldu şeridi (sağ %30)
        im.crop((int(w * 0.70), 0, w, h)).save(out_dir / f"{stem}_98_sag_derkenar.png")

        # 3. Alt imza ve mühür bölgesi (alt %24)
        im.crop((0, int(h * 0.76), w, h)).save(out_dir / f"{stem}_99_alt_muhur_imza.png")

        # 4. Örtüşmeli yatay okuma şeritleri (gövde satırları için)
        bands = max(1, int(args.bands))
        overlap = int((h / bands) * 0.14)
        for i in range(bands):
            y1 = max(0, int(h * i / bands) - overlap)
            y2 = min(h, int(h * (i + 1) / bands) + overlap)
            im.crop((0, y1, w, y2)).save(out_dir / f"{stem}_satir_band_{i + 1:02d}.png")

    print(f"Evrak diplomatik bölgelere ayrıldı ({w}x{h} px, {bands} satır bandı): {out_dir}")


def cmd_crop(args: argparse.Namespace) -> None:
    src = Path(args.image).resolve()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    parts = [int(v.strip()) for v in args.box.split(",")]
    if len(parts) != 4:
        sys.stderr.write("Hata: --box formatı x1,y1,x2,y2 olmalıdır.\n")
        sys.exit(1)
    x1, y1, x2, y2 = parts

    with Image.open(src) as im:
        w, h = im.size
        box = (max(0, x1), max(0, y1), min(w, x2), min(h, y2))
        cropped = im.crop(box)
        if args.scale and args.scale > 1:
            cw, ch = cropped.size
            cropped = cropped.resize((int(cw * args.scale), int(ch * args.scale)), Image.NEAREST)
        cropped.save(out)
    print(f"1:1 kanıt kesiti kaydedildi {box} (ölçek {args.scale}x): {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Osmanlıca resmî evrak diplomatik bölge ayırma ve 1:1 piksel kesit aracı."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_inv = sub.add_parser("inventory", help="Klasördeki .zip ve görüntü dosyalarını güvenli biçimde listeler.")
    p_inv.add_argument("input_dir", help="Evrak görsellerini veya .zip dosyalarını içeren klasör")
    p_inv.set_defaults(func=cmd_inventory)

    p_spl = sub.add_parser("split", help="Evrakı başlık, derkenar, mühür ve yatay satır bantlarına ayırır.")
    p_spl.add_argument("image", help="Kaynak evrak görseli")
    p_spl.add_argument("--bands", type=int, default=6, help="Yatay okuma şeridi sayısı (varsayılan: 6)")
    p_spl.add_argument("--out", default="./evrak_bolgeler", help="Çıktı klasörü")
    p_spl.set_defaults(func=cmd_split)

    p_crp = sub.add_parser("crop", help="Şüpheli kelime, tarih veya mühürden 1:1 piksel kesiti alır.")
    p_crp.add_argument("image", help="Kaynak evrak görseli")
    p_crp.add_argument("--box", required=True, help="Piksel koordinatları: x1,y1,x2,y2")
    p_crp.add_argument("--scale", type=float, default=1.0, help="Büyütme katsayısı (1 veya 2, NEAREST)")
    p_crp.add_argument("--out", required=True, help="Çıktı PNG dosya yolu")
    p_crp.set_defaults(func=cmd_crop)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
