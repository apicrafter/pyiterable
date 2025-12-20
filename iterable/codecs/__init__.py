from .bz2codec import BZIP2Codec
from .gzipcodec import GZIPCodec
from .lzmacodec import LZMACodec
from .lz4codec import LZ4Codec
from .zipcodec import ZIPCodec
from .zstdcodec import ZSTDCodec 
from .brotlicodec import BrotliCodec
from .snappycodec import SnappyCodec
from .lzocodec import LZOCodec
from .rawcodec import RAWCodec
try:
    from .szipcodec import SZipCodec
except ImportError:
    # py7zr not available
    pass