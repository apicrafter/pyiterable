from .brotlicodec import BrotliCodec
from .bz2codec import BZIP2Codec
from .gzipcodec import GZIPCodec
from .lz4codec import LZ4Codec
from .lzmacodec import LZMACodec
from .lzocodec import LZOCodec
from .rawcodec import RAWCodec
from .snappycodec import SnappyCodec
from .zipcodec import ZIPCodec
from .zstdcodec import ZSTDCodec

try:
    from .szipcodec import SZipCodec
except ImportError:
    # py7zr not available
    pass