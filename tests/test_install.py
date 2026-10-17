import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kb_installer',ROOT/'install.py')
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class InstallerSafetyTests(unittest.TestCase):
    def test_manifest_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);(r/'reports').mkdir();(r/'reports/manifest.json').write_text(json.dumps({'files':[{'path':'../escape','sha256':'x'}]}))
            with self.assertRaises(ValueError):installer.verify(r)

    def test_manifest_rejects_modified_package_file(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);(r/'reports').mkdir();(r/'a').write_text('changed');(r/'reports/manifest.json').write_text(json.dumps({'files':[{'path':'a','sha256':'0'*64}]}))
            with self.assertRaises(ValueError):installer.verify(r)

    def test_unsupported_query_does_not_invent_evidence(self):
        sys.path.insert(0,str(ROOT/'tools'))
        import agent
        result=agent.query('quantum zebracorn')
        self.assertEqual(result['status'],'no_evidence')
        self.assertEqual(result['results'],[])

if __name__=='__main__':unittest.main()
