#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/applications-module.h"
#include <fstream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("VanetLogger");

std::ofstream logFile;

void ReceivePacket(Ptr<Socket> socket)
{
  Address from;
  Ptr<Packet> packet = socket->RecvFrom(from);
  double now = Simulator::Now().GetSeconds();
  uint32_t size = packet->GetSize();

  logFile << "receive," << now << "," << size << std::endl;
  NS_LOG_INFO("Packet received at " << now << "s, size=" << size);
}

int main(int argc, char *argv[])
{
  LogComponentEnable("VanetLogger", LOG_LEVEL_INFO);
  logFile.open("messages.csv", std::ios::out);
  logFile << "type,timestamp,size\n";

  NodeContainer nodes;
  nodes.Create(3);

  MobilityHelper mobility;
  mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                "MinX", DoubleValue(0.0),
                                "MinY", DoubleValue(0.0),
                                "DeltaX", DoubleValue(10.0),
                                "GridWidth", UintegerValue(3),
                                "LayoutType", StringValue("RowFirst"));
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(nodes);

  WifiHelper wifi;
  wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                               "DataMode", StringValue("DsssRate11Mbps"),
                               "ControlMode", StringValue("DsssRate11Mbps"));
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy;
  phy.SetChannel(channel.Create());

  WifiMacHelper mac;
  mac.SetType("ns3::AdhocWifiMac");
  NetDeviceContainer devices = wifi.Install(phy, mac, nodes);

  InternetStackHelper stack;
  stack.Install(nodes);
  Ipv4AddressHelper address;
  address.SetBase("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = address.Assign(devices);

  for (uint32_t i = 0; i < nodes.GetN(); ++i)
  {
    Ptr<Socket> recvSocket = Socket::CreateSocket(nodes.Get(i), UdpSocketFactory::GetTypeId());
    InetSocketAddress local = InetSocketAddress(Ipv4Address::GetAny(), 9);
    recvSocket->Bind(local);
    recvSocket->SetRecvCallback(MakeCallback(&ReceivePacket));
  }

  // Each node sends a message at staggered times
  for (uint32_t i = 0; i < nodes.GetN(); ++i)
  {
    Ptr<Socket> source = Socket::CreateSocket(nodes.Get(i), UdpSocketFactory::GetTypeId());
    source->SetAllowBroadcast(true);
    InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 9);
    source->Connect(remote);

    Simulator::Schedule(Seconds(2.0 + i), [source, i]() {
      std::string msg = "Vehicle " + std::to_string(i) + " speed=60";
      Ptr<Packet> p = Create<Packet>((uint8_t *)msg.c_str(), msg.length());
      source->Send(p);
      logFile << "send," << Simulator::Now().GetSeconds() << "," << p->GetSize() << std::endl;
      NS_LOG_INFO("Node " << i << " sent packet");
    });
  }

  Simulator::Stop(Seconds(6.0));
  Simulator::Run();
  Simulator::Destroy();
  logFile.close();

  return 0;
}
