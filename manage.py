#!/usr/bin/env python
from pathlib import Path

import click

from hotels import converter


@click.group()
def cli():
    pass


def validate_file(ctx, param, value):
    """Validate that the filepath is in csv format."""
    filepath = Path(value)
    if not filepath.suffix == '.csv':
        raise click.BadParameter('File needs to be a csv.')
    return filepath


def validate_output_format(ctx, param, value):
    """Validate that the output format is supported."""
    if value not in converter.FORMAT_PROCESSORS:
        raise click.BadParameter('Output format not supported.')
    return value


@cli.command()
@click.argument('csv_filepath', type=click.Path(exists=True),
                callback=validate_file)
@click.option('--output_format', default='yaml', help='Output format.',
              callback=validate_output_format)
def convert(csv_filepath, output_format):
    converter.convert(csv_filepath, output_format)


if __name__ == '__main__':
    cli()
