from header_definition import *
from scapy.packet import Raw
def deal_packet_for_simple_switch(packet):
    """普通交换机解析域内控制器发过来的response包.

    Args:
        packet: 对应普通交换机的控制平面接收到的response包
    
    Returns:
        dict: 从response包中解析出来的信息
    """
    response_header=response_t(bytes(packet[Raw]))
    deviceid=response_header.deviceid
    dst_addr=response_header.dst_addr
    port=response_header.port
    dst_port_mac=response_header.dst_port_mac
    return  {"deviceid":deviceid,"dst_addr":dst_addr,"port":port,"dst_port_mac":dst_port_mac}


def deal_packet_for_controller_switch(packet):
    """控制交换机解析发过来的request包.

    Args:
        packet: 对应控制交换机的控制平面接收到的request包
    
    Returns:
        dict: 从request包中解析出来的信息
    """
    request_header=request_t(bytes(packet[Raw]))
    deviceid=request_header.deviceid
    dst_addr=request_header.dst_addr
    return {"deviceid": deviceid,"dst_addr":dst_addr}


def make_a_response_packet(deviceid,dst_addr,port,dst_port_mac,ipv4):
    """控制交换机控制平面构造response数据包发送给对应普通交换机.

    Args:
        deviceid(int): response包目的交换机的deviceid
        dst_addr(str): response包的response头部的dst_addr
        port(int): response包的response头部的port
        dst_port_mac(str): response包的response头部的dst_port_mac
        ipv4(str): response包的ipv4头部中的dst_addr
    
    Returns:
        packet: 打包好的完整response包
    """
    packet=Ether()/IP(dst=ipv4,proto=151)/\
    response_t(deviceid=deviceid,dst_addr=dst_addr,port=port,dst_port_mac=dst_port_mac)
    return packet


