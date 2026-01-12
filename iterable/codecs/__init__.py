# Core codecs (always available)
from .bz2codec import BZIP2Codec
from .gzipcodec import GZIPCodec
from .lzmacodec import LZMACodec
from .rawcodec import RAWCodec
from .zipcodec import ZIPCodec

# Optional codecs - import conditionally
try:
    from .brotlicodec import BrotliCodec
except ImportError:
    # brotli_file not available
    pass

try:
    from .lz4codec import LZ4Codec
except ImportError:
    # lz4 not available
    pass

try:
    from .lzocodec import LZOCodec
except ImportError:
    # python-lzo not available
    pass

try:
    from .snappycodec import SnappyCodec
except ImportError:
    # python-snappy not available
    pass

try:
    from .zstdcodec import ZSTDCodec
except ImportError:
    # zstandard not available
    pass

try:
    from .szipcodec import SZipCodec
except ImportError:
    # py7zr not available
    pass