#!/usr/bin/env python3
"""Build the static repository viewer; accepts a verified repository URL when live."""
import argparse
import json
from pathlib import Path
import shutil
from kb import ROOT, read_jsonl

def build(out, repository_url=None):
    out.mkdir(parents=True, exist_ok=True)
    data={'videos':json.loads((ROOT/'data/video-catalog.json').read_text()),'claims':read_jsonl(ROOT/'data/claims.jsonl'),'sources':read_jsonl(ROOT/'data/sources.jsonl'),'repository_url':repository_url}
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    (out/'index.html').write_text((ROOT/'web/template.html').read_text().replace('__LIBRARY_DATA__',payload))
    for name in ('AGENT_START.md','SKILL.md'):
        shutil.copyfile(ROOT/name,out/name)
    shutil.copyfile(ROOT/'reports/COVERAGE.md',out/'COVERAGE.md')
    (out/'data').mkdir(exist_ok=True)
    for name in ('sources.jsonl','claims.jsonl','frameworks.json','video-relations.json','video-catalog.json'):
        shutil.copyfile(ROOT/'data'/name,out/'data'/name)
    return {'directory':str(out),'videos':265,'notes':len(data['claims'])}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);p.add_argument('--repository-url');a=p.parse_args();print(json.dumps(build(a.out,a.repository_url)))
