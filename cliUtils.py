# cliUtil
# Version 0.1 Patch 4
# Ryan Sharp - 4/28/16

""" CLI Utility for pinging hosts. """

from subprocess import run


def Ping(host, packets=1, timeout=10, IncludeBadIP=True):
    """Pings 'host' IP Address with 'packets' packets and waits for 'timeout' milliseconds for a reply.
    Returns dict [IP]:reachable. If IncludeBadIP is False, Returns only reachable IPs as dict"""

    print('\nPing Called.\n')
    
    if(not isinstance(host,list) or len(host) == 0):
        print('There were no valid entries in the address list.\n')
        return None
    args = "ping -n %d -w %d" % (packets,timeout)
    print('Testing Reachability of hosts...\nUsing args: %s\n' % (args))
    Rdict = {}
    if(IncludeBadIP):
        print('Including all addresses...\n')
        for h in host:
            req = '%s %s' % (args,h,)
            # print(req)
            print('Trying %s...' % (h),end='')
            result = run(req,shell=True).returncode
            if(result is 0):
                print('\t Reachable.')
                Rdict[h] = True
            else:
                print('\t Unreachable.')
                Rdict[h] = False
    else:
        print('Including only reachable addresses...\n')
        for h in host:
            req = '%s %s' % (args,h,)
            # print(req)
            print('Trying %s...' % (h),end='')
            result = run(req,shell=True).returncode
            if(result is 0):
                print('\t Reachable.')
                Rdict[h] = True
            else:
                print('\t Unreachable.')

    print('\nPing Done.')
    return Rdict

if __name__ == "__main__":
    import sys

    print('\n****************************')
    print('Trying to run test script: Ping\nWith arguments: %s...\n' % (sys.argv[1:]))

    Rdict = Ping(sys.argv[1:])
    print('\n',Rdict)
        
    


