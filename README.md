# okerrbench

Simple multiprocessing benchmarking tool for [okerr](https://okerr.com/) server.

- [Okerr main website](https://okerr.com/)
- [Okerr-server source code repository](gitlab.com/yaroslaff/okerr-dev/) and [okerr server wiki doc](https://gitlab.com/yaroslaff/okerr-dev/wikis/)
- [Okerr client (okerrupdate) repositoty](https://gitlab.com/yaroslaff/okerrupdate) and [okerrupdate wiki doc](https://gitlab.com/yaroslaff/okerrupdate/wikis/)

Example usage:
~~~shell script
# warm-up
./okerrbench.py --prepare --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 200 -q

# main benchmark
./okerrbench.py -q --test --url http://dev.okerr.com/ -i bench -S 'zzz' --indicators 10 --process 20 --shard --seconds 300 
~~~