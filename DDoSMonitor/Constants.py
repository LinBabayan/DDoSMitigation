from enum import Enum, auto
from scapy.all import IP, IPv6
from scapy.layers.l2 import Ether
from scapy.all import IP, IPv6, TCP, UDP, ICMP, ARP 
from scapy.layers.l2 import Ether, ARP

class ParsedDataColumnNames:
    column_time = 'timestamp'
    column_protocol_N = "protocol_N"
    column_protocol = "protocol"
    column_length = "length"
    column_src_ip = "src_ip"
    column_dst_ip = "dst_ip"
    column_src_port = "src_port"
    column_dst_port = "dst_port"

class Mode(Enum):
    Undefined = auto()
    REALTIME_DETECTION = auto()
    MODEL_TRAINING = auto()

class Models(Enum):
    VolumeBased = "VolumeBasedAttackModel.pkl"
    ProtocolBased = "ProtocolBasedAttackModel.pkl" 
    VolumeBasedByProtocol = "VolumeBasedByProtocolAttackModel.pkl" 
    ProtocolBasedByProtocol = "ProtocolBasedByProtocolAttackModel.pkl"

proto_name_unknown ="Unknown"
proto_N_unknown =9999

class NetProtocol(object): 
    def __init__(self):
        #protocol name on protocol number.
        self._protocol_name_by_number = { 1:    "ICMP"      ,
                                          6:    "TCP"       ,
                                          17:   "UDP"       ,
                                          50:   "ESP"       ,
                                          51:   "AH"        ,
                                          47:   "GRE"       ,
                                          58:   "ICMPv6"    ,
                                          2000:   'Dot3'      ,
                                          2001:   'Dot3(CDP)' ,
                                          2002:   'Dot3(VTP)' ,
                                          2003:   'Dot3(DTP)' ,
                                          2004:   'Dot3(PAgP)',
                                          2005:   'Dot3(UDLD)',
                                          2050:   'ARP',

                                          0x8847: 'MPLS(unicast)'  ,
                                          0x8848: 'MPLS(multicast)',
                                          0x88cc: 'LLDP'           ,
                                          0x8100: 'VLAN'           ,
                                          proto_N_unknown: proto_name_unknown
                                        }                          

        self._protocol_number_by_name =  { "ICMP": 1,
                                            "TCP": 6,
                                           "HTTP": 6, #80
                                          "HTTPS": 6, #443
                                            "FTP": 6, #20, 21
                                            "SSH": 6, #22
                                           "SMTP": 6, #22
                                            "SSH": 6, #25
                                           "POP3": 6, #110
                                           "IMAP": 6, #143
                                            "RDP": 6, #3389

                                            "UDP": 17,
                                           "DHCP": 17,
                                            "DNS": 17, #53
                                           "MDNS": 17, #5353
                                           "DHCP": 17, #67 (server), 68 (client)
                                           "TFTP": 17, #69
                                           "SNMP": 17, #161, 162
                                            "NTP": 17, #161, 162
                                         "Syslog": 17, #17 or 6	UDP/TCP	514
                                           "NBNS": 17, #137

                                            "ESP": 50,
                                             "AH": 51,
                                            "GRE": 47,
                                         "ICMPv6": 58,

                                         'Dot3'           : 2000,
                                         'Dot3(CDP)'      : 2001,   #cisco ?
                                         'Dot3(VTP)'      : 2002,
                                         'Dot3(DTP)'      : 2003,
                                         'Dot3(PAgP)'     : 2004,
                                         'Dot3(UDLD)'     : 2005,

                                         'ARP'            : 2050,   #Address Resolution Protocol (ARP)

                                         'MPLS(unicast)'  : 0x8847,	#MPLS (Multiprotocol Label Switching) unicast
                                         'MPLS(multicast)': 0x8848,	#MPLS multicast	MPLS multicast
                                         'LLDP'           : 0x88cc,	#Link Layer Discovery Protocol (LLDP)
                                         'VLAN'           : 0x8100,	#VLAN IEEE 802.1Q Virtual LAN (VLAN)

                                          proto_name_unknown: proto_N_unknown,
                                        }

    def get_protocol_name(self, pkt):
        if IP in pkt:
            proto_num = pkt[IP].proto
        elif IPv6 in pkt:
            proto_num = pkt[IPv6].nh
        else:
            return proto_name_unknown

        return self._protocol_name_by_number.get(proto_num, str(proto_num))   # default to number as string if not found

    def get_proto_info(self, pkt):
        proto_num = proto_N_unknown
        src_ip = None
        dst_ip = None
        src_port = None
        dst_port = None

        if pkt.haslayer(IP):
            proto_num = pkt[IP].proto
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

        elif pkt.haslayer(IPv6):
            proto_num = pkt[IPv6].nh
            src_ip = pkt[IPv6].src
            dst_ip = pkt[IPv6].dst

        elif pkt.haslayer(ARP):
            proto_num = 2050  
            src_ip = pkt[ARP].psrc
            dst_ip = pkt[ARP].pdst

        elif pkt.haslayer('Dot3'):
            if pkt.haslayer(IP):
                proto_num = pkt[IP].proto
            else:
                if pkt.haslayer('CDP'):
                    proto_num = 2001
                elif pkt.haslayer('LLC'):
                    proto_num = 2001
                elif pkt.haslayer('VTP'):
                    proto_num = 2002
                elif pkt.haslayer('DTP'):
                     proto_num = 2003
                elif pkt.haslayer('PAgP'):
                     proto_num = 2004
                elif pkt.haslayer('UDLD'):
                    proto_num = 2005
                else:
                    proto_num = 2000

        elif pkt.haslayer(Ether):
            proto_num = pkt[Ether].type  

        if pkt.haslayer(TCP):
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
        elif pkt.haslayer(UDP):
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport

        proto_name = self._protocol_name_by_number.get(proto_num, str(proto_num))
        return (proto_num, proto_name, src_ip, dst_ip, src_port, dst_port)

net_protocol = NetProtocol()
