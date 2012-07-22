import unicodedata


class Word(object):
    """
    """
    def __init__(self, input):
        self.original = input
        self.decoded = input.decode('utf-8', 'ignore')
        self.normalized = ''.join(
            (c for c in unicodedata.normalize('NFD', self.decoded)
            if unicodedata.category(c) != 'Mn'))
        self.upper = self.normalized.upper()
        self.length = len(self.upper)
        self.prepad = "--"
        self.start_index = len(self.prepad)
        self.end_index = self.start_index + self.length - 1
        self.postpad = "------"
        # so we can index beyond the begining and end of the input string
        self.buffer = self.prepad + self.upper + self.postpad

    @property
    def is_slavo_germanic(self):
        return (
            self.upper.find('W') > -1
            or self.upper.find('K') > -1
            or self.upper.find('CZ') > -1
            or self.upper.find('WITZ') > -1)

    def get_letters(self, start=0, end=None):
        if not end:
            end = start + 1
        start = self.start_index + start
        end = self.start_index + end
        return self.buffer[start:end]
