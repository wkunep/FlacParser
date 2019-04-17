from collections import namedtuple


class MetaDataBlock:
    def __init__(self, reader, add_metadata_block):
        while True:
            header = MetaDataBlockHeader(reader)
            BlockType = header.get_type()
            block = BlockType(reader, header.get_length())
            add_metadata_block(str(header), str(block))
            if header.is_end:
                break


class MetaDataBlockHeader(MetaDataBlock):
    def __init__(self, reader):
        self.block_types = {
            0: MetaDataBlockStreamInfo,
            1: MetaDataBlockPadding,
            2: MetaDataBlockApplication,
            3: MetaDataBlockSeektable,
            4: MetaDataBlockVorbisComment,
            5: MetaDataBlockCuesheet,
            6: MetaDataBlockPicture
        }
        self._flag = reader.read(1)
        self._type = reader.read(7)
        self._metadata_length_in_bytes = reader.read(24)
        self.is_end = self._flag

    def get_type(self):
        return self.block_types[self._type]

    def get_length(self):
        return self._metadata_length_in_bytes

    def __str__(self):
        text = []
        text.append('')
        text.append("----------  HEADER  ----------")
        text.append("Block Type: {}".format(self.get_type().__name__))
        text.append("Length of metadata: {} bytes".format(self.get_length()))
        text.append('')
        return '\n'.join(text)


class MetaDataBlockStreamInfo(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        self.minimum_block_size_in_samples = reader.read(16)
        self.maximum_block_size_in_samples = reader.read(16)
        self.minimum_frame_size_in_bytes = reader.read(24)
        self.maximum_frame_size_in_bytes = reader.read(24)
        self.sample_rate_in_Hz = reader.read(20)
        self.number_of_channels = reader.read(3)
        self.bits_per_sample = reader.read(5)
        self.number_samples_in_stream = reader.read(36)
        self.md5_signature = hex(reader.read(128))[2:]

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        text.append("The minimum block size in samples in the stream: {}".
                    format(self.minimum_block_size_in_samples))
        text.append('The maximum block size in samples in the stream: {}'.
                    format(self.maximum_block_size_in_samples))
        text.append('The minimum frame size in bytes in the stream: {}'.
                    format(self.minimum_frame_size_in_bytes))
        text.append('The maximum frame size in bytes in the stream: {}'.
                    format(self.maximum_frame_size_in_bytes))
        text.append('Sample rate in Hz: {}'.
                    format(self.sample_rate_in_Hz))
        text.append('The number of channels: {}'.
                    format(self.number_of_channels))
        text.append('Number bits per sample: {}'.
                    format(self.bits_per_sample))
        text.append('The number of samples in the stream: {}'.
                    format(self.number_samples_in_stream))
        text.append('MD5 signature of the unencoded audio data: {}'.
                    format(self.md5_signature))
        text.append('')
        return '\n'.join(text)


class MetaDataBlockPadding(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        self.size = size_in_bytes
        reader.binary_read(size_in_bytes * 8)

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        text.append("Padding: {} bytes".format(self.size))
        text.append('')
        return '\n'.join(text)


class MetaDataBlockApplication(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        self.id = reader.read(32)
        self.size = size_in_bytes
        reader.binary_read((size_in_bytes - 4) * 8)

    def __str__(self):
        text = []
        text.append("-----  METADATABLOCK  -----")
        text.append("Id: {}".format(self.id))
        text.append('')
        return '\n'.join(text)


class MetaDataBlockSeektable(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        self.SeekPoint = namedtuple('SeekPoint', (
            'sample_number', 'offset_in_bytes', 'number_of_samples'))
        self.seek_points = []
        for i in range(int(size_in_bytes / 18)):
            self.seek_points.append(self.SeekPoint(
                reader.read(64), reader.read(64), reader.read(16)))

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        for point in self.seek_points:
            text.append('|----  SeekPoint  ----|')
            text.append("Sample number of first sample " +
                        "in the target frame: {}".
                        format(point.sample_number))
            text.append("Offset in bytes: {}".
                        format(point.offset_in_bytes))
            text.append("Number of samples in the target frame: {}".
                        format(point.number_of_samples))
            text.append('')
        return '\n'.join(text)


class MetaDataBlockVorbisComment(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        temp = reader.read(size_in_bytes * 8)
        self.comment = temp.to_bytes(
            (temp.bit_length() + 7) // 8, 'big').decode('utf-8')

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        text.append(self.comment)
        text.append('')
        return '\n'.join(text)


class MetaDataBlockCuesheet(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        temp = reader.read(128*8)
        self.media_catalog_number = temp.to_bytes(
            (temp.bit_length() + 7) // 8, 'big').decode()
        self.number_lead_samples = reader.read(64)
        self.flag = reader.read(1)
        self.reserved = reader.read(7+258*8)
        self.number_tracks = reader.read(8)
        self.cuesheet_tracks = []
        self.CuesheetTrack = namedtuple('CuesheetTrack', (
            'track_offset', 'track_number', 'write_code', 'track_type',
            'pre_emphasis_flag', 'reserved', 'number_track_index_points',
            'track_index_points'))
        for i in range(self.number_tracks):
            track_offset = reader.read(64)
            track_number = reader.read(8)
            write_code = reader.read(12*8)
            track_type = reader.read(1)
            pre_emphasis_flag = reader.read(1)
            reserved = reader.read(6+13*8)
            number_track_index_points = reader.read(8)
            track_index_points = []
            CuesheetTrackIndex = namedtuple('CuesheetTrackIndex', (
                'offset', 'index_point_number', 'reserved'))
            for j in range(number_track_index_points):
                track_index_points.append(CuesheetTrackIndex(
                    reader.read(64), reader.read(8), reader.read(3*8)))
            self.cuesheet_tracks.append(self.CuesheetTrack(
                track_offset, track_number, write_code, track_type,
                pre_emphasis_flag, reserved, number_track_index_points,
                track_index_points))

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        text.append("Media catalog number: {}".
                    format(self.media_catalog_number))
        text.append("The number of lead-in samples: {}".
                    format(self.number_lead_samples))
        text.append("1 if the CUESHEET corresponds to a Compact Disc, " +
                    "else 0: {}".
                    format(self.flag))
        text.append("The number of tracks: {}".
                    format(self.number_tracks))
        for track in self.cuesheet_tracks:
            text.append("|----  CUESHEET TRACK  ----|")
            text.append("Track offset in samples, relative to the beginning " +
                        "of the FLAC audio stream: {}".
                        format(track.track_offset))
            text.append("Track_number: {}".
                        format(track.track_number))
            text.append("Track ISRC: {}".
                        format(track.write_code))
            text.append("The track type: {}".
                        format(track.track_type))
            text.append("The pre-emphasis flag: {}".
                        format(track.pre_emphasis_flag))
            text.append("The number of track index points: {}".
                        format(track.number_track_index_points))
            text.append('')
            for track_index in track.track_index_points:
                text.append("||---  CUESHEET_TRACK_INDEX  ---||")
                text.append("Offset in samples, relative to the track " +
                            "offset, of the index point: {}".
                            format(track_index.offset))
                text.append("The index point number: {}".
                            format(track_index.index_point_number))
                text.append('')
            text.append('')
        text.append('')
        return '\n'.join(text)


class MetaDataBlockPicture(MetaDataBlock):
    def __init__(self, reader, size_in_bytes):
        self.picture_type = reader.read(32)
        self.mime_length = reader.read(32)
        temp = reader.read(self.mime_length * 8)
        self.mime_string = temp.to_bytes(
            (temp.bit_length() + 7) // 8, 'big').decode()
        self.length_of_description = reader.read(32)
        temp = reader.read(self.length_of_description * 8)
        self.description_of_picture = temp.to_bytes(
            (temp.bit_length() + 7) // 8, 'big').decode('utf-8')
        self.picture_width_in_pixels = reader.read(32)
        self.picture_height_in_pixels = reader.read(32)
        self.color_depth_in_bits_per_pixel = reader.read(32)
        self.color_number = reader.read(32)
        self.picture_data_length = reader.read(32)
        self.picture_data = reader.read_bytes(self.picture_data_length)

        with open('picture.png', 'wb') as f:
            f.write(self.picture_data)

    def get_picture_type(self):
        picture_types = {
            0: "Other",
            1: "32x32 pixels 'file icon' (PNG only)",
            2: "Other file icon",
            3: "Cover (front)",
            4: "Cover (back)",
            5: "Leaflet page",
            6: "Media (e.g. label side of CD",
            7: "Lead artist/lead performer/solist",
            8: "Artist/performer",
            9: "Conductor",
            10: "Band/Orchestra",
            11: "Composer",
            12: "Lyricist/text writer",
            13: "Recording Location",
            14: "During recording",
            15: "During perfomance",
            16: "Movie/video screen capture",
            17: "A bright coloured fish",
            18: "Illustration",
            19: "Band/artist logotype",
            20: "Publisher/Studio logotype"
            }
        return picture_types[self.picture_type]

    def __str__(self):
        text = []
        text.append("-----  METADATA BLOCK  -----")
        text.append("The picture type according to the ID3v2 APIC frame: " +
                    "{} - {}".
                    format(self.picture_type, self.get_picture_type()))
        text.append("The length of the MIME type string in bytes: {}".
                    format(self.mime_length))
        text.append("The MIME type string: {}".
                    format(self.mime_string))
        text.append("The length of the description string in bytes: {}".
                    format(self.length_of_description))
        text.append("The description of the picture, in UTF-8: {}".
                    format(self.description_of_picture))
        text.append("The width of the picture in pixels: {}".
                    format(self.picture_width_in_pixels))
        text.append("The height of the picture in pixels: {}".
                    format(self.picture_height_in_pixels))
        text.append("The color depth of the picture in bits-per-pixel: {}".
                    format(self.color_depth_in_bits_per_pixel))
        text.append("For indexed-color pictures (e.g. GIF), " +
                    "the number of colors used, " +
                    "or 0 for non-indexed pictures: {}".
                    format(self.color_number))
        text.append("The length of the picture data in bytes: {}".
                    format(self.picture_data_length))
        text.append('')
        return '\n'.join(text)
