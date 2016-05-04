import socket
import sys
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('169.254.20.12', ))

message = (b'*idn?')
bytes = len(message)

bytesent = tcpsock.send(message)

print('sent ', bytesent, ' of', bytes, ' bytes.')


fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

trys = 10

while(trys > 0):
    try:
        msg = s.recv(4096)
    except socket.error, e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            sleep(1)
            print 'No data available'
            continue
        else:
            # a "real" error occurred
            print e
            sys.exit(1)
    else:
        # got a message, do something :)
		print(msg)
	trys = trys - 1