class Pattern:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.output_data = []

    def add_metadata_block(self, header, data):
        self.output_data.append(header)
        self.output_data.append(data)
        self.output_data.append('_____________________________________')

    def add_frame(self, header):
        self.output_data.append('==========  FRAME  ==========')
        self.output_data.append(header)

    def write(self):
        with open(self.output, 'w') as f:
            f.write(self.get_output_string())

    def get_output_string(self):
        return '\n'.join(self.output_data)
