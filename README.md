# okerrbench

Simple multiprocessing network benchmarking tool for [okerr](https://okerr.com/) server.

Example usage:
~~~shell script
# warm-up (optional. but first test without warmup could be slow, 2nd test and furhter are OK)
./okerrbench.py --prepare --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 200 -q

# main benchmark
./okerrbench.py -q --test --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 10 --process 20 --shard --seconds 300 
~~~

# Other okerr resources
- [Okerr main website](https://okerr.com/)
- [Okerr-server source code repository](https://github.com/yaroslaff/okerr-dev/) 
- [Okerr client (okerrupdate) repositoty](https://github.com/yaroslaff/okerrupdate) and [okerrupdate documentation](https://okerrupdate.readthedocs.io/)
- [Okerrbench network server benchmark](https://github.com/yaroslaff/okerrbench)
- [Okerr custom status page](https://github.com/yaroslaff/okerr-status)
- [Okerr JS-powered static status page](https://github.com/yaroslaff/okerrstatusjs)
- [Okerr network sensor](https://github.com/yaroslaff/sensor)

