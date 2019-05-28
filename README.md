Bitcoin DNS Seeder
==================

This project includes a Crawler that collects informatiom from all nodes in the Bitcoin Protocol. 
The DNS portion of the repository utilizes the IP Addresses found by the Crawler to build a dynamic Nameserver
that is capable of providing 25 randomly selected IP's of well connected nodes. Such a Nameserver is used by
Bitcoin-Core for the DNS Seeding portion of the node initialization. 

My personal DNS Seeder can be found at seed.convex.city. I have a [fork of bitcoin-core here](https://github.com/ryan-lingle/bitcoin-dns)
that utilizes this DNS Seeder rather than the standard Core Developer supplied seeders.

Check out the seeder by using one of the following commands:
```
host seed.convex.city
```
```
dig seed.convex.city
```
