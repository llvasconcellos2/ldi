import re
import random
from pathlib import Path

rip_dir = Path(__file__).parent / "rip"
thumb_dir = rip_dir / "imagens" / "thumb"

thumb_files = [f.name for f in thumb_dir.iterdir() if f.suffix.lower() == ".jpg"]
if not thumb_files:
    raise RuntimeError(f"No JPG files found in {thumb_dir}")

pattern = re.compile(
    r'<span\b[^>]*>[\s]*Imagem\s+n\xE3o\s+dispon\xEDvel[\s]*</span\s*>',
    re.DOTALL,
)


def build_replacement(thumb_name: str) -> str:
    main_name = thumb_name[6:] if thumb_name.startswith("thumb_") else thumb_name
    return (
        "<a\n"
        '  href="#"\n'
        f"  onClick=\"void window.open('imagens/{main_name}', '_blank', 'width=440,height=365,status=no,resizable=yes,top=20,left=80');\"\n"
        f'  ><img border="0" src="imagens/thumb/{thumb_name}"\n'
        "/></a>"
    )


total = 0
for html_file in sorted(rip_dir.rglob("*.html")):
    content = html_file.read_text(encoding="utf-8", errors="replace")
    matches = pattern.findall(content)
    if not matches:
        continue
    new_content = pattern.sub(lambda _: build_replacement(random.choice(thumb_files)), content)
    html_file.write_text(new_content, encoding="utf-8")
    total += len(matches)
    print(f"  {html_file.relative_to(rip_dir.parent)}: {len(matches)} replacement(s)")

print(f"\nDone. Total replacements: {total}")
