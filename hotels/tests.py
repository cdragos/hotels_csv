from collections import OrderedDict
from contextlib import contextmanager
from pathlib import Path, PurePath
from unittest import TestCase, mock
from tempfile import mkstemp

from hotels import models, processors


@contextmanager
def filepath_mock(data):
    file_mock = mock.Mock()
    file_open_magic_mock = mock.MagicMock()
    file_mock.open.return_value = file_open_magic_mock
    file_open_magic_mock.__enter__.return_value = data
    file_mock.parent = PurePath('_parent')
    yield file_mock


class ImporterTests(TestCase):

    @mock.patch('hotels.processors.yaml_format')
    def test_import_data(self, mock_yaml_format):
        from hotels.converter import convert

        data = [
            'name,address,stars,contact,phone,uri',
            ',,,,,',
            'Name 1,Address 1,5,Contact 1,Phone 1,http://www.example.com',
            ',,,,,',
            'Name 2,Address 2,7,Contact 2,Phone 2,http://www.example.com']

        with filepath_mock(data) as mock:
            resp = convert(mock, 'yaml')
            self.assertIsNone(resp)

        valid_data = OrderedDict([
            ('name', 'Name 1'),
            ('address', 'Address 1'),
            ('stars', 5),
            ('contact', 'Contact 1'),
            ('phone', 'Phone 1'),
            ('uri', 'http://www.example.com')])

        mock_yaml_format.assert_called_once_with(
            [valid_data], PurePath('_parent/output.yml'))

    def test_yaml_processor(self):
        items = [{
            'name': 'Name 1',
            'address': 'Address 1',
            'stars': 5,
            'contact': 'Contact 1',
            'phone': 'Phone 1',
            'uri': 'Uri 1',
        }]

        fd, path = mkstemp()
        filepath = Path(path)
        try:
            processors.yaml_format(items, filepath)
            data = filepath.read_text()
            self.assertTrue(data)
            self.assertIn('Address 1', data)
        finally:
            filepath.unlink()

    def test_sqlite_processor(self):
        items = [{
            'name': 'Name 1',
            'address': 'Address 1',
            'stars': 5,
            'contact': 'Contact 1',
            'phone': 'Phone 1',
            'uri': 'Uri 1',
        }]

        fd, path = mkstemp()
        filepath = Path(path)
        try:
            processors.sqlite_format(items, filepath)
            qs = models.Hotel.select().filter(
                name='Name 1', address='Address 1', stars=5, contact='Contact 1',
                phone='Phone 1', uri='Uri 1')
            self.assertTrue(qs.exists())
        finally:
            filepath.unlink()
