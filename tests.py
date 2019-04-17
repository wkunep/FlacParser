import unittest

from metaDataBlock import MetaDataBlock, MetaDataBlockHeader, \
    MetaDataBlockApplication, MetaDataBlockCuesheet, \
    MetaDataBlockPadding, MetaDataBlockPicture, MetaDataBlockSeektable, \
    MetaDataBlockStreamInfo, MetaDataBlockVorbisComment
from frame import Frame, FrameHeader
from flacExtractor import FlacParser, BitReader
from pattern import Pattern


class TestFlacParser(unittest.TestCase):
    def test_MetaDataBlockHeader(self):
        data = b'\x82\x00\x00\x00'
        block = MetaDataBlockHeader(BitReader(data))
        self.assertEqual(str(block).replace('\n', ''),
                         '----------  HEADER  ----------'
                         'Block Type: MetaDataBlockApplication'
                         'Length of metadata: 0 bytes')

    def test_MetaDataBlockStreamInfo(self):
        data = b'\x12\x00\x12\x00\x00\x00\x0f\x005>\n\xc4B\xf0\x00R\xb6' \
               b'\xe4"\xa4\xa7\x981\xca\x08\xe9:\\b\x8a\x83\xd4Dg'
        block = MetaDataBlockStreamInfo(BitReader(data), 34)
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  METADATA BLOCK  -----'
                         'The minimum block size in samples ' +
                         'in the stream: 4608'
                         'The maximum block size in samples ' +
                         'in the stream: 4608'
                         'The minimum frame size in bytes in the stream: 15'
                         'The maximum frame size in bytes in the stream: 13630'
                         'Sample rate in Hz: 44100'
                         'The number of channels: 1'
                         'Number bits per sample: 15'
                         'The number of samples in the stream: 5420772'
                         'MD5 signature of the unencoded audio ' +
                         'data: 22a4a79831ca08e93a5c628a83d44467')

    def test_MetaDataBlockPadding(self):
        data = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        block = MetaDataBlockPadding(BitReader(data), 8)
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  METADATA BLOCK  -----'
                         'Padding: 8 bytes')

    def test_MetaDataBlockSeektable(self):
        data = b'\x00\x00\x00\x00\x00\x00\x00\x01\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x80'
        block = MetaDataBlockSeektable(BitReader(data), 18)
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  METADATA BLOCK  -----'
                         '|----  SeekPoint  ----|'
                         'Sample number of first sample in the target frame: 1'
                         'Offset in bytes: 0'
                         'Number of samples in the target frame: 128')

    def test_MetaDataBlockCuesheet(self):
        self.maxDiff = None
        data = b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a\x7a' \
               b'\x7a\x7a' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x02' \
               b'\x03\x04\x05\x06\x07\x08\x09\x01\x01\x80\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00' \
               b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        block = MetaDataBlockCuesheet(BitReader(data), 432)
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  METADATA BLOCK  -----'
                         'Media catalog number: zzzzzzzzzzzzzzzzzzzzz' +
                         'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz' +
                         'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
                         'zzzzzzzzzzzzzzzzzzzzz'
                         'The number of lead-in samples: 0'
                         '1 if the CUESHEET corresponds to a Compact Disc, ' +
                         'else 0: 1'
                         'The number of tracks: 1'
                         '|----  CUESHEET TRACK  ----|'
                         'Track offset in samples, relative to the ' +
                         'beginning of the FLAC audio stream: 0'
                         'Track_number: 1'
                         'Track ISRC: 1218426182456967898398977'
                         'The track type: 1'
                         'The pre-emphasis flag: 0'
                         'The number of track index points: 1'
                         '||---  CUESHEET_TRACK_INDEX  ---||'
                         'Offset in samples, relative to the track offset, ' +
                         'of the index point: 0'
                         'The index point number: 1')

    def test_MetaDataBlockPicture(self):
        self.maxDiff = None
        data = b'\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               b'\x80\x80\x00\x00\x80\x80\x00\x00\xff\xff' \
               b'\x00\x00\x80\x08\x00\x00\x00\x00'
        block = MetaDataBlockPicture(BitReader(data), 36)
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  METADATA BLOCK  -----'
                         'The picture type according to the ID3v2 APIC ' +
                         'frame: 4 - Cover (back)'
                         'The length of the MIME type string in bytes: 0'
                         'The MIME type string: '
                         'The length of the description string in bytes: 0'
                         'The description of the picture, in UTF-8: '
                         'The width of the picture in pixels: 32896'
                         'The height of the picture in pixels: 32896'
                         'The color depth of the picture in ' +
                         'bits-per-pixel: 65535'
                         'For indexed-color pictures (e.g. GIF), '
                         'the number of colors used, ' +
                         'or 0 for non-indexed pictures: 32776'
                         'The length of the picture data in bytes: 0')

    def test_FrameHeader(self):
        self.maxDiff = None
        data = b'\xf1\xff\xf9\x18\x98'
        block = FrameHeader(BitReader(data))
        self.assertEqual(str(block).replace('\n', ''),
                         '-----  HEADER  -----'
                         'Blocking strategy: variable-blocksize stream; ' +
                         'frame header encodes the sample number'
                         'Block size in inter-channel samples: 192 samples'
                         'Sample rate: 32kHz'
                         'Channel assignment: right/side stereo: ' +
                         'channel 0 is the side(difference) channel, '
                         'channel 1 is the right channel'
                         'Sample size in bits: 16 bits per sample')

    def test_pattern_add_metadata_block(self):
        pattern = Pattern('input', 'output')
        pattern.add_metadata_block('header', 'data')
        self.assertEqual(pattern.get_output_string().replace('\n', ''),
                         'header'
                         'data'
                         '_____________________________________')

    def test_pattern_add_frame(self):
        pattern = Pattern('input', 'output')
        pattern.add_frame('header')
        self.assertEqual(pattern.get_output_string().replace('\n', ''),
                         '==========  FRAME  =========='
                         'header')


if __name__ == "__main__":
    unittest.main()
