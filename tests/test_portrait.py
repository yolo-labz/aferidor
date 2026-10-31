#!/usr/bin/env python3
"""Small, offline regression check for the cast-to-portrait transformation."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
P = runpy.run_path(str(ROOT / "docs/assets/source/portrait.py"))


class PortraitTest(unittest.TestCase):
    def test_fixture_and_reflow(self):
        blocks = P["recorded_blocks"]()
        self.assertEqual(len(blocks), 5)
        self.assertIn("REFUSED", " ".join(blocks[-1]))
        table = "\n".join(P["reflow"](blocks[2]))
        for text in ("mediana R$ 7,90 / L", "mediana R$ 8,32 / L", "MANTER:", "5.1%", "8%", "<- atual"):
            self.assertIn(text, table)
        screen = "\n".join(P["reflow"](blocks[1]))
        self.assertIn("R$ 7,49", screen)
        self.assertNotIn("(360,193)", screen)
        # Reflow must preserve all words of the refusal, not replace real output.
        self.assertEqual(" ".join(P["reflow"](blocks[4])).split(), " ".join(blocks[4]).split())

    def test_every_scene_has_large_fixed_disclosure(self):
        wanted = ["VITRINE LOCAL DE DEMONSTRAÇÃO", "NÃO É IFOOD NEM APP DE ENTREGA",
                  "aferidor-fone é experimental"]
        for i, block in enumerate(P["recorded_blocks"]()):
            lines = P["reflow"](block)
            svg = ET.fromstring(P["scene_svg"](i, lines))
            texts = svg.findall("{http://www.w3.org/2000/svg}text")
            self.assertEqual([t.text for t in texts[:3]], wanted)
            self.assertEqual([int(t.attrib["y"]) for t in texts[:3]], [82, 150, 224])
            self.assertTrue(all(int(t.attrib["font-size"]) >= 36 for t in texts[:3]))
            self.assertTrue(all(len(line) <= 41 for line in lines))
            self.assertLessEqual(628 + (len(lines) - 1) * 50, 1628)

    def test_fails_closed_on_fixture_or_layout_drift(self):
        with self.assertRaises(ValueError):
            P["reflow"](["x" * 42])
        with self.assertRaises(ValueError):
            P["reflow"](["line"] * 22)
        with self.assertRaises(ValueError):
            P["reflow"](["atacarejo-online  unexpected table"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.cast"
            for output in ("$ unknown command\n", "\x1b]unknown"):
                path.write_text(json.dumps({"version": 3}) + "\n" + json.dumps([0, "o", output]))
                with self.assertRaises(ValueError):
                    P["recorded_blocks"](path)


if __name__ == "__main__":
    unittest.main()
