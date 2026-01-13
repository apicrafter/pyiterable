import binascii

import pytest

from iterable.datatypes.pcap import PCAPIterable
from iterable.helpers.detect import open_iterable

try:
    import dpkt  # noqa: F401

    HAS_DPKT = True
except ImportError:
    HAS_DPKT = False

# Minimal PCAP file hex dump (Global Header + 1 Packet)
# Global Header: Magic(a1b2c3d4), Major(2), Minor(4), Zone(0), SigFigs(0), SnapLen(65535), Net(1=Ethernet)
# Packet Header: TS_sec, TS_usec, InclLen(14), OrigLen(14)
# Packet Data: 14 bytes (Ethernet frame)
PCAP_HEX = (
    "d4c3b2a1020004000000000000000000ffff000001000000"  # Global Header
    "5d2e20500e240c000e0000000e000000"  # Packet Header
    "0000000000000000000000000800"  # Packet Data (dst, src, type)
)


@pytest.fixture
def pcap_file(tmp_path):
    p = tmp_path / "test.pcap"
    p.write_bytes(binascii.unhexlify(PCAP_HEX))
    return str(p)


@pytest.mark.skipif(not HAS_DPKT, reason="dpkt not installed")
class TestPCAP:
    def test_read_pcap(self, pcap_file):
        with open_iterable(pcap_file) as source:
            assert isinstance(source, PCAPIterable)
            records = list(source)
            assert len(records) == 1
            assert "timestamp" in records[0]
            assert "data" in records[0]
            assert len(records[0]["data"]) == 14

    def test_read_via_class(self, pcap_file):
        source = PCAPIterable(pcap_file)
        records = list(source)
        source.close()
        assert len(records) == 1

    def test_detection(self, pcap_file):
        from iterable.helpers.detect import detect_file_type

        res = detect_file_type(pcap_file)
        assert res["success"]
        assert res["datatype"] == PCAPIterable

    def test_not_installed(self):
        if not HAS_DPKT:
            with pytest.raises(ImportError, match="dpkt is required"):
                PCAPIterable("dummy.pcap")
