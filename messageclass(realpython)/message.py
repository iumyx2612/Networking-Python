import json
import struct
import io
import sys

# Need to encode and decode data to/from utf-8 encoding
# -----------------------------------------------------
def json_decode(json_bytes, encoding='utf-8'):
    json_str = json_bytes.decode(encoding) # to string
    obj = json.loads(json_str) # to dict
    return obj


def json_encode(obj, encoding='utf-8'):
    return json.dumps(obj, ensure_ascii=False).encode(encoding) # dict -> string -> bytes
# -----------------------------------------------------


# Message class, decode then read json data, writing json data then encode
# 1. Init the class with buffer
# 2. Decode data to get the content
# or
# 3. Encode data to utf-8 encoding to ready to send
class Message():
    def __init__(self, data, addr=None):
        self.addr = addr
        self.buffer = data # bytes or string
        self.len_proto_header = 4
        self.json_header = None
        self.len_json_header = 0
        self.content = None

    # Process data when received
    # ------------------------------------------------------------------------------------------------
    # process proto header to get length of json header
    def process_protoheader(self):
        if len(self.buffer) >= self.len_proto_header:
            self.len_json_header = struct.unpack("!I", self.buffer[:self.len_proto_header]) # unpack from in_buffer
            self.len_json_header = self.len_json_header[0] # unpack return a tuple -> take the first value
            self.buffer = self.buffer[self.len_proto_header:] # remove the proto header bytes from buffer


    # process json header to get information about content
    def process_jsonheader(self):
        if len(self.buffer) > self.len_json_header:
            self.json_header = json_decode(
                self.buffer[:self.len_json_header], 'utf-8'
            )
            self.buffer = self.buffer[self.len_json_header:]
            for reqhdr in (
                    "byteorder", # self-explanatory
                    "content-length", # length of content in bytes
                    "content-type", # type of content in payload (text/json or binary)
                    "content-encoding", # encoding used by content (utf-8 or binary)
            ):
                if reqhdr not in self.json_header:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    # process the content
    def process_request(self):
        content_length = self.json_header["content-length"]
        if not len(self.buffer) >= content_length:
            return
        data = self.buffer[:content_length]
        self.buffer = self.buffer[content_length:]
        if self.json_header["content-type"] == "json":
            encoding = self.json_header["content-encoding"]
            self.content = json_decode(data, encoding=encoding)
            print(f'Received request {repr(self.content)} from {self.addr}')
        elif self.json_header["content-type"] == "text":
            encoding = self.json_header["content-encoding"]
            self.content = data.decode(encoding)
            print(f'Received text {self.content} from {self.addr}')
        else:
            self.content = data
            print(f'Received {self.json_header["content-encoding"]} request from {self.addr}')

    def handle_receive(self):
        self.process_protoheader()
        self.process_jsonheader()
        self.process_request()
    # ------------------------------------------------------------------------------------------------


    # Process data to send
    # ------------------------------------------------------------------------------------------------
    def create_byte_data(self, content_type="text"):
        content_bytes = bytearray(self.buffer, encoding='utf-8')
        self.json_header = {
            "byteorder": sys.byteorder,
            "content-length": len(content_bytes),
            "content-type": content_type,
            "content-encoding": 'utf-8'
        }
        json_header_bytes = json_encode(self.json_header)
        proto_header = struct.pack("!I", len(json_header_bytes))
        message = proto_header + json_header_bytes + content_bytes
        return message
    # ------------------------------------------------------------------------------------------------





