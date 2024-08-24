#include <core.p4>
#include <v1model.p4>
const bit<16> TYPE_IPV4=0x0800;
const bit<8> IP_PROTO_REQUEST=150;
const bit<8> IP_PROTO_RESPONSE=151;
const bit<9> CPU_PORT=5;
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16>   ether_type;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    bit<32> src_addr;
    bit<32> dst_addr;
}

header request_t{
    bit<8> deviceid;
    bit <32> dst_addr;
}

header response_t{
    bit<7> deviceid;
    bit<32> dst_addr;
    bit<9> port;
}

struct headers{
    ethernet_t         ethernet;
    ipv4_t             ipv4;
    request_t          request;
    response_t         response;
}

struct metadata {
    
}

parser MyParser(
            packet_in pkt,
            out headers hdr,
            inout metadata meta,
            inout standard_metadata_t standard_metadata
){
    state start{
        transition parse_ethernet;
    }

    state parse_ethernet{
        pkt.extract(hdr.ethernet);
        transition parse_ipv4;
    }

    state parse_ipv4{
        pkt.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            150: parse_request;
            151:parse_response;
            default: accept;
        }
    }

    state parse_request{
        pkt.extract(hdr.request);
        transition accept;
    }

    state parse_response{
        pkt.extract(hdr.response);
        transition accept;
    }
}

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}  

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata)
{
    action drop(){
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(bit<9> port){
        standard_metadata.egress_spec = port;
    }

    table ipv4_lpm{
        key={
            hdr.ipv4.dst_addr: exact;
        }
        actions={
            ipv4_forward;
            drop;
        }
        size = 1024;
        default_action = drop;
    }

    apply{
        if(hdr.ipv4.protocol!=150){
            ipv4_lpm.apply();
        }else if(hdr.ipv4.protocol==150){
            standard_metadata.egress_spec=CPU_PORT;
        }
    }
}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata){
        apply{}
}

control MyComputeChecksum(inout headers  hdr, inout metadata meta){
    apply{}
}

control MyDeparser(packet_out packet, in headers hdr){
    apply{
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.request);
        packet.emit(hdr.response);
    }
}

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;