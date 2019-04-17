class Frame:
    def __init__(self, reader, add_frame):
        header = FrameHeader(reader)
        add_frame(str(header))


class FrameHeader(Frame):
    def __init__(self, reader):
        self.skip_to_frame(reader)
        self.reserved = reader.read(1)
        self.set_blocking_strategy(reader.read(1))
        self.set_block_size(reader.binary_read(4))
        self.set_sample_rate(reader.binary_read(4))
        self.set_channel_assignment(reader.binary_read(4))
        self.set_sample_size_in_bits(reader.binary_read(3))

        reader.read(1)

    def skip_to_frame(self, reader):
        sync_code = ''
        while sync_code != '11111111111110':
            if len(sync_code) == 14:
                sync_code = sync_code[1:]
            sync_code += reader.binary_read(1)

    def set_blocking_strategy(self, code):
        strategy = {
            0: 'fixed-blocksize stream; frame header encodes the frame number',
            1: 'variable-blocksize stream; ' +
               'frame header encodes the sample number'
            }
        self.blocking_strategy = strategy[code]

    def set_block_size(self, code):
        sizes = {
            '0000': 'reserved',
            '0001': '192 samples',
            '0010': '576 * (2^(n-2)) samples, i.e. 576/1152/2304/4608',
            '0011': '576 * (2^(n-2)) samples, i.e. 576/1152/2304/4608',
            '0100': '576 * (2^(n-2)) samples, i.e. 576/1152/2304/4608',
            '0101': '576 * (2^(n-2)) samples, i.e. 576/1152/2304/4608',
            '0110': 'get 8 bit (blocksize-1) from end of header',
            '0111': 'get 16 bit (blocksize-1) from end of header',
            '1000': '256 * (2^(n-8)) samples, i.e. ' +
                    '256/512/1024/2048/4096/8192/16384/32768'
        }
        if code not in sizes:
            self.block_size = sizes['1000']
        else:
            self.block_size = sizes[code]

    def set_sample_rate(self, code):
        rates = {
            '0000': 'get from STREAMINFO metadata block',
            '0001': '88.2kHz',
            '0010': '176.4kHz',
            '0011': '192kHz',
            '0100': '8kHz',
            '0101': '16kHz',
            '0110': '22.05kHz',
            '0111': '24kHz',
            '1000': '32kHz',
            '1001': '44.1kHz',
            '1010': '48kHz',
            '1011': '96kHz',
            '1100': 'get 8 bit sample rate (in kHz) from end of header',
            '1101': 'get 16 bit sample rate (in kHz) from end of header',
            '1110': 'get 8 bit sample rate (in tens of Hz) from end of header'
        }
        self.sample_rate = rates[code]

    def set_channel_assignment(self, code):
        dict = {
            '1000': 'left/side stereo: channel 0 is the left channel, ' +
                    'channel 1 is the side(difference) channel',
            '1001': 'right/side stereo: channel 0 is the side(difference) ' +
                    'channel, channel 1 is the right channel',
            '1010': 'mid/side stereo: channel 0 is the mid(average) ' +
                    'channel, channel 1 is the side(difference) channel',
            '1011': 'reserved'
        }
        if code not in dict:
            self.channel_assignment = '{} channels'.format(int(code, base=2))
        else:
            self.channel_assignment = dict[code]

    def set_sample_size_in_bits(self, code):
        sizes = {
            '000': 'get from STREAMINFO metadata block',
            '001': '8 bits per sample',
            '010': '12 bits per sample',
            '011': 'reserved',
            '100': '16 bits per sample',
            '101': '20 bits per sample',
            '110': '24 bits per sample',
            '111': 'reserved'
        }
        self.sample_size_in_bits = sizes[code]

    def __str__(self):
        text = []
        text.append('')
        text.append("-----  HEADER  -----")
        text.append("Blocking strategy: {}".format((self.blocking_strategy)))
        text.append("Block size in inter-channel samples: {}"
                    .format(self.block_size))
        text.append("Sample rate: {}".format(self.sample_rate))
        text.append("Channel assignment: {}".format(self.channel_assignment))
        text.append("Sample size in bits: {}".format(self.sample_size_in_bits))
        text.append('')
        return '\n'.join(text)
