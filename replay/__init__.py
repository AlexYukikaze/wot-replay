__author__ = 'Alexander "Yukikaze" Putin'
__email__ = 'yukikaze (at) modxvm.com'

import struct


class Replay(object):
    def __init__(self, raw_data):
        self._raw_data = raw_data
        self._blocks = []
        self._magic, block_count = struct.unpack('II', raw_data[:8])  # unpack 2 uint
        self._last_block_end = self.__read_blocks(block_count)

    @classmethod
    def from_file(cls, path):
        stream = open(path, 'rb')
        data = stream.read()
        stream.close()
        return cls(data)

    @property
    def block_count(self):
        return len(self._blocks)

    @property
    def magic(self):
        return self._magic

    @property
    def blocks(self):
        return self._blocks[:]

    @property
    def match_start(self):
        return self._blocks[0]

    @property
    def battle_result(self):
        return self._blocks[1]

    def add_block(self, data):
        self._blocks.append(data)

    def remove_block(self, i):
        self._blocks.remove(i)

    def to_string(self):
        import json
        result = struct.pack('II', self._magic, len(self._blocks))
        for block in self._blocks:
            json_string = json.dumps(block)
            length = len(json_string)
            result += struct.pack('I', length)
            result += json_string
        result += self._raw_data[self._last_block_end:]
        return result

    def to_file(self, path):
        stream = open(path, 'wb')
        data = self.to_string()
        stream.write(data)
        stream.close()

    def save(self, path):
        self.to_file(path)

    def __read_blocks(self, count):
        import json
        pos = 8
        for i in xrange(0, count):
            size = struct.unpack('I', self._raw_data[pos: pos + 4])[0]
            start = pos + 4
            end = pos + 4 + size
            json_string = self._raw_data[start: end]
            json_object = json.loads(json_string)
            self._blocks += json_object,
            pos = end
        return pos


def load(file_name):
    return Replay.from_file(file_name)
