import tempfile
import unittest
from pathlib import Path
import fitz
from zotero_agent.reading_export import page_text


class ReadingExportTests(unittest.TestCase):
    def test_physical_page_numbers_and_range(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'fictional.pdf'
            with fitz.open() as doc:
                for value in ['First sample','Second sample']:
                    doc.new_page().insert_text((50,50),value)
                doc.save(path)
            data=page_text(path,2,2)
            self.assertEqual(data['total_pages'],2)
            self.assertEqual(data['pages'][0]['page'],2)
            self.assertIn('Second sample',data['pages'][0]['text'])
            with self.assertRaises(ValueError):page_text(path,0,2)
