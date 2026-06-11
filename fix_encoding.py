# -*- coding: utf-8 -*-
"""Fix mojibake encoding in archived HTML files."""

import sys

filepath = sys.argv[1] if len(sys.argv) > 1 else r'c:\Users\leona\Projects\leonardo\project_archive\lamode\rip\contacts\index.html'

with open(filepath, 'rb') as f:
    data = f.read()

reencoded = False
try:
    text = data.decode('utf-8')
except UnicodeDecodeError:
    text = data.decode('cp1252')
    reencoded = True

replacements = [
    # Double mojibake via CP1252 (ƒ U+0192 is the tell-tale sign)
    ('ÃƒÂ£', 'ã'), ('ÃƒÂ¡', 'á'), ('ÃƒÂ©', 'é'), ('ÃƒÂª', 'ê'),
    ('ÃƒÂ§', 'ç'), ('ÃƒÂ³', 'ó'), ('ÃƒÂº', 'ú'), ('ÃƒÂ¢', 'â'),
    ('ÃƒÂµ', 'õ'), ('ÃƒÂ´', 'ô'), ('ÃƒÂ¼', 'ü'), ('ÃƒÂ®', 'î'),
    ('ÃƒÂ¯', 'ï'), ('ÃƒÂ±', 'ñ'), ('ÃƒÂ­', 'í'),
    # Uppercase double via CP1252 special bytes
    ('Ãƒâ€¡', 'Ç'),  # Ç — CP1252 0x87 = ‡
    ('Ãƒ"', 'Ó'),               # Ó — CP1252 0x93 = " (U+201C)
    # Single mojibake
    ('Ã³', 'ó'), ('Ã©', 'é'), ('Ã£', 'ã'), ('Ã¡', 'á'), ('Ã­', 'í'),
    ('Ãº', 'ú'), ('Ãª', 'ê'), ('Ã§', 'ç'), ('Ã¢', 'â'), ('Ãµ', 'õ'),
    ('Ã´', 'ô'), ('Ã¼', 'ü'), ('Ã®', 'î'), ('Ã¯', 'ï'), ('Ã±', 'ñ'),
    # Á: UTF-8 c3 81 misread as Latin-1 → Ã + U+0081 (C1 control char)
    ('Ã\x81', 'Á'),
    # Other uppercase single via Latin-1 control bytes
    ('Ã\x89', 'É'), ('Ã\x93', 'Ó'), ('Ã\x87', 'Ç'), ('Ã\x95', 'Õ'),
    ('Ã\x94', 'Ô'), ('Ã\x80', 'À'), ('Ã\x82', 'Â'), ('Ã\x83', 'Ã'),
    ('Ã\x9a', 'Ú'),
    # Â prefix patterns
    ('Â°', '°'), ('Â©', '©'), ('Â®', '®'), ('Â³', '³'), ('Â²', '²'),
]

original = text
for wrong, right in replacements:
    text = text.replace(wrong, right)

if text == original and not reencoded:
    print('No changes needed.')
else:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Fixed: {filepath}')
