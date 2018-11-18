import logging
import csv

from . import processors
from .containers import Hotel


logger = logging.getLogger(__file__)
logging.basicConfig(level='INFO')


FORMAT_PROCESSORS = {
    'yaml': {
        'processor': processors.yaml_format,
        'ext': 'yml',
    },
    'sqlite': {
        'processor': processors.sqlite_format,
        'ext': 'db',
    }
}


def convert(csv_filepath, output_format):
    """Convert data from csv file to the output format."""
    valid_data, invalid_data = [], []

    logger.info('Started processing the csv.')

    with csv_filepath.open(newline='', encoding='utf-8') as f:
        csv_data = (row for row in csv.reader(f) if row)
        next(csv_data)  # skip the header rows

        for row in csv_data:
            hotel = Hotel.from_row(row)
            if hotel.is_valid():
                valid_data.append(hotel.as_dict())
            else:
                invalid_data.append(hotel)

    processor = FORMAT_PROCESSORS[output_format]['processor']
    ext = FORMAT_PROCESSORS[output_format]['ext']

    output_filepath = csv_filepath.parent / 'output.{}'.format(ext)
    processor(valid_data, output_filepath)

    # TODO implement a way to report errors and invalid data
    logger.info('Finish processing the csv. {} hotels converted.'.format(
        len(valid_data)))
