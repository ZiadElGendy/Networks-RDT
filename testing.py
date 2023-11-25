from sender import *
test_str = "A"

checksum = RDTSender.get_checksum(test_str)

packet = RDTSender.make_pkt('0', "A", 65)

print(RDTSender.is_corrupted(packet))