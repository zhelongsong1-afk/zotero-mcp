import unittest
from unittest.mock import patch,Mock
from zotero_agent import mcp_reader as reader


class MCPBoundaryTests(unittest.TestCase):
    def test_title_search_returns_authors_and_stored_doi(self):
        zotero = Mock()
        zotero.items.return_value = [{'key': 'FAKEKEY1', 'data': {
            'title': 'Sample Robot Paper',
            'DOI': '10.1234/example',
            'creators': [
                {'creatorType': 'author', 'firstName': 'A.', 'lastName': 'Author'},
                {'creatorType': 'author', 'name': 'Robotics Group'},
                {'creatorType': 'editor', 'name': 'E. Editor'},
            ],
        }}]
        with patch.object(reader, 'Zotero', return_value=zotero):
            result = reader.search_papers('robot paper')
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['papers'][0]['title'], 'Sample Robot Paper')
        self.assertEqual(result['papers'][0]['authors'], ['A. Author', 'Robotics Group'])
        self.assertEqual(result['papers'][0]['doi'], '10.1234/example')

    def test_arbitrary_path_is_rejected(self):
        with patch.object(reader,'Zotero') as z:
            with self.assertRaises(ValueError):reader.resolve('../private/config.json')
            z.assert_not_called()

    def test_attachment_must_belong_to_selected_paper(self):
        z=Mock()
        z.items.return_value=[{'key':'FAKEKEY1','data':{'title':'Fictional'}}]
        z.children.return_value=[{'key':'PDFKEY01','data':{'contentType':'application/pdf'}}]
        with patch.object(reader,'Zotero',return_value=z):
            with self.assertRaises(ValueError):reader.resolve('FAKEKEY1','OTHERPDF')
            z.pdf.assert_not_called()

    def test_oversized_range_is_rejected_before_io(self):
        with patch.object(reader,'resolve') as resolve:
            with self.assertRaises(ValueError):reader.read_pdf_pages('FAKEKEY1',1,20)
            resolve.assert_not_called()
