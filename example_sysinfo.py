import sysinfo
import time

dt = sysinfo.DateTime()
sys = sysinfo.System()
net = sysinfo.Network()

while 1:
    sys.clear()
    print '{}'.format('================================================================')
    prtram = '{:7}{:2.0f}{:2}{:2.0f}{:1}'.format('RAM: U:',sys.get_used_ram(),'% F:',sys.get_free_ram(),'%')
    prtos = '{:2}{:22}'.format('OS: ', sys.get_os())
    prtpython = '{:12}{:10}'.format('PYTHON VER: ',sys.get_python_ver())
    print '{}{}{}'.format(prtos,prtpython,prtram)
    print '{}'.format('----------------------------------------------------------------')

    uptime = sys.get_uptime()
    prtuptime='UPTIME: {} DAYS + {:02d}:{:02d}:{:02d}'.format(uptime.days,(uptime.seconds//3600),(uptime.seconds//60)%60,(uptime.seconds)%60)
    print '{:19}{:>45}'.format(dt.now(),prtuptime)
    print '{}'.format('\n')
    net.show_connections()
    print '{}'.format('\n')
    net.show_network()
    print '{}'.format('================================================================')
    time.sleep(1)