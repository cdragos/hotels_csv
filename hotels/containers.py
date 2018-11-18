import re
from collections import OrderedDict

from attr import Factory, attrib, attrs


uri_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@attrs(slots=True)
class Hotel(object):

    name = attrib(converter=str.strip)
    address = attrib(converter=str.strip)
    stars = attrib(converter=str.strip)
    contact = attrib(converter=str.strip)
    phone = attrib(converter=str.strip)
    uri = attrib(converter=str.strip)

    errors = attrib(default=Factory(list))

    @classmethod
    def from_row(cls, row):
        name, address, stars, contact, phone, uri = row
        return cls(name, address, stars, contact, phone, uri)

    def is_valid(self):
        return len(self.errors) == 0

    def as_dict(self):
        data = OrderedDict([
            ('name', self.name),
            ('address', self.address),
            ('stars', self.stars),
            ('contact', self.contact),
            ('phone', self.phone),
            ('uri', self.uri)
        ])
        if self.errors:
            data['errors'] = self.errors
        return data

    @name.validator
    def validate_name(self, attribute, value):
        try:
            value.encode('utf-8')
        except UnicodeEncodeError:
            self.errors.append('Name is not UTF-8 valid.')

    @uri.validator
    def validate_uri(self, attribute, value):
        if not re.match(uri_regex, value):
            self.errors.append(
                'URI value: "{}"" is not a valid url.'.format(value))

    @stars.validator
    def validate_stars(self, attribute, value):
        try:
            self.stars = int(value)
        except (ValueError, TypeError):
            self.errors.append(
                'Stars value: "{}"" is not a valid integer.'.format(value))
            return

        if not 0 <= self.stars <= 5:
            self.errors.append(
                'Stars value: "{}"" should be between 0 and 5.'.format(value))
