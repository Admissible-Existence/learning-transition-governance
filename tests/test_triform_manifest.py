import json
import unittest
from pathlib import Path
from tools.validate_triform_manifest import validate

ROOT=Path(__file__).resolve().parents[1]

class TriFormManifestTests(unittest.TestCase):
    def test_manifest_valid(self):
        data=json.loads((ROOT/'formalism/triform-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual([], validate(data))

    def test_authority_promotion_fails(self):
        data=json.loads((ROOT/'formalism/triform-manifest.json').read_text(encoding='utf-8'))
        data['authority_effect']=True
        self.assertIn('authority_effect', validate(data))

    def test_identity_capture_fails(self):
        data=json.loads((ROOT/'formalism/triform-manifest.json').read_text(encoding='utf-8'))
        data['identity_capture']=True
        self.assertIn('identity_capture', validate(data))

    def test_principle_gap_fails(self):
        data=json.loads((ROOT/'formalism/triform-manifest.json').read_text(encoding='utf-8'))
        data['principles']=data['principles'][:-1]
        self.assertTrue(any(x.startswith('principle_ids:') for x in validate(data)))

if __name__=='__main__': unittest.main()
