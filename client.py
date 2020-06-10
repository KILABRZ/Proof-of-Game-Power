from scapy.all import *
from scapy.layers.http import  HTTP, HTTPRequest

srcIP = '127.0.0.1'
desIP = '127.0.0.1'
srcPort = 1234
desPort = 8000

load_layer('http')
req = IP(src=srcIP, dst=desIP) / TCP(sport=srcPort, dport=desPort) / HTTP() / HTTPRequest(
	Connection=b'keep-alive',
	Cache_Control=b'no-cache',
	Upgrade_Insecure_Requests=b'1',
	Accept=b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	Accept_Encoding=b'gzip, defalte, br',
	Host = b'localhost:8000') 

req.show()
send(req)