from sys import exit

try:
    from metaDataBlock import MetaDataBlock
    from frame import Frame
except ImportError as exception:
    exit("Some program module not found: {}".format(exception))


class BitReader:
    def __init__(self, data_in_bytes):
        self.data = data_in_bytes
        self.position = 0
        self.unpacked_bits = ""
        self.is_end = False

    def read_bytes(self, count):
        next_bytes = self.data[self.position:self.position + count]
        self.position += count
        return next_bytes

    def read(self, count):
        if count <= 0:
            return 0
        binary = self.binary_read(count)
        return int(binary, base=2)

    def binary_read(self, count):
        if count <= 0:
            return ""
        bits = self.unpacked_bits[:count]
        self.unpacked_bits = self.unpacked_bits[count:]
        count -= len(bits)
        while count > 0:
            next_byte = self.unpack_byte(self.data[self.position])
            self.position += 1
            next_bits = next_byte[:count]
            bits += next_bits
            if len(next_bits) < 8:
                self.unpacked_bits = next_byte[count:]
                break
            count -= 8
        return bits

    def unpack_byte(self, byte):
        return bin(byte)[2:].zfill(8)

    def skip(self, count):
        self.read(count)


class FlacParser:
    def __init__(self, data, pattern):
        self.reader = BitReader(data)
        self.pattern = pattern

    def parse(self):
        self.reader.skip(32)
        self.metadata_block = MetaDataBlock(self.reader,
                                            self.pattern.add_metadata_block)
        self.frame = Frame(self.reader, self.pattern.add_frame)
