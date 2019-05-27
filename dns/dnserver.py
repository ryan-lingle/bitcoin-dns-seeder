import os
from time import sleep

from dnslib import DNSLabel, QTYPE, RR, dns
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSServer

from db import dns_lookup

TYPE_LOOKUP = {
    'A': (dns.A, QTYPE.A),
    'AAAA': (dns.AAAA, QTYPE.AAAA),
    'CAA': (dns.CAA, QTYPE.CAA),
    'CNAME': (dns.CNAME, QTYPE.CNAME),
    'DNSKEY': (dns.DNSKEY, QTYPE.DNSKEY),
    'MX': (dns.MX, QTYPE.MX),
    'NAPTR': (dns.NAPTR, QTYPE.NAPTR),
    'NS': (dns.NS, QTYPE.NS),
    'PTR': (dns.PTR, QTYPE.PTR),
    'RRSIG': (dns.RRSIG, QTYPE.RRSIG),
    'SOA': (dns.SOA, QTYPE.SOA),
    'SRV': (dns.SRV, QTYPE.SRV),
    'TXT': (dns.TXT, QTYPE.TXT),
    'SPF': (dns.TXT, QTYPE.TXT),
}


class Record:
    def __init__(self, ip):
        self._rname = DNSLabel("seed.convex.city")

        rd_cls, self._rtype = TYPE_LOOKUP["A"]

        self.rr = RR(
            rname=self._rname,
            rtype=self._rtype,
            rdata=rd_cls(ip),
            ttl=300,
        )

    def match(self, q):
        return q.qname == self._rname and (q.qtype == QTYPE.ANY or q.qtype == self._rtype)

    def sub_match(self, q):
        return self._rtype == QTYPE.SOA and q.qname.matchSuffix(self._rname)

    def __str__(self):
        return str(self.rr)


class Resolver():

    def resolve(self, request, handler):
        type_name = QTYPE[request.q.qtype]
        reply = request.reply()
        for record in [Record(row["ip"]) for row in dns_lookup()]:
            if record.match(request.q):
                reply.add_answer(record.rr)

        if reply.rr:
            print('found zone for %s[%s], %d replies', request.q.qname, type_name, len(reply.rr))
            return reply

        print('no local zone found, proxying %s[%s]', request.q.qname, type_name)
        return reply

if __name__ == '__main__':
    port = int(os.getenv('PORT', 53))
    resolver = Resolver()
    udp_server = DNSServer(resolver, port=port)
    tcp_server = DNSServer(resolver, port=port, tcp=True)

    print('starting DNS server on port %d', port)
    udp_server.start_thread()
    tcp_server.start_thread()

    try:
        while udp_server.isAlive():
            sleep(1)
    except KeyboardInterrupt:
        pass
