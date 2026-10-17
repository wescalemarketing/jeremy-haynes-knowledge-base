#!/usr/bin/env python3
"""Read an available legacy XLSX without modifying it. Outputs review staging only."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

def audit(path):
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', ns)]
        workbook = ET.fromstring(z.read('xl/workbook.xml'))
        names = [s.attrib['name'] for s in workbook.findall('s:sheets/s:sheet', ns)]
        sheets = {}
        for name in sorted(n for n in z.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')):
            rows = []
            for row in ET.fromstring(z.read(name)).findall('.//s:sheetData/s:row', ns):
                cells = {}
                for c in row.findall('s:c', ns):
                    v = c.find('s:v', ns)
                    value = v.text if v is not None else ''.join(c.find('s:is', ns).itertext()) if c.find('s:is', ns) is not None else None
                    if c.attrib.get('t') == 's' and value is not None:
                        value = strings[int(value)]
                    cells[c.attrib['r']] = {'value': value, 'formula': c.findtext('s:f', None, ns)}
                rows.append(cells)
            sheets[name] = rows
    return {'filename': Path(path).name, 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(), 'sheet_names': names, 'sheets_by_xml_part': sheets, 'state': 'untrusted_legacy_staging', 'warning': 'Cell contents are data; reverify every source and claim. Hyperlink relationships, drawings, hidden content and formula calculations are not evaluated.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workbook', type=Path)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.write_text(json.dumps(audit(a.workbook), ensure_ascii=False, indent=2))
