# okerrbench

Simple multiprocessing network benchmarking tool for [okerr](https://okerr.com/) server.

Example usage:
~~~shell script
# warm-up (optional. but first test without warmup could be slow, 2nd test and furhter are OK)
./okerrbench.py --prepare --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 200 -q

# main benchmark
./okerrbench.py -q --test --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 10 --process 20 --shard --seconds 300 
~~~

## Other okerr resources
- [Okerr main website](https://okerr.com/)
- [Okerr-server source code repository](gitlab.com/yaroslaff/okerr-dev/) and [okerr server wiki doc](https://gitlab.com/yaroslaff/okerr-dev/wikis/)
- [Okerr client (okerrupdate) repositoty](https://gitlab.com/yaroslaff/okerrupdate) and [okerrupdate wiki doc](https://gitlab.com/yaroslaff/okerrupdate/wikis/)
- [Okerrbench network server benchmark](https://gitlab.com/yaroslaff/okerrbench)
