#=======================================================================================================================
try:
    import psutil
    import datetime
    import os
    import sys
    import platform
    import ipaddress
except Exception, import_err:
    print 'IMPORT LIBS FAILED. ERROR => {}'.format(import_err)
#=======================================================================================================================
class DateTime:
    def __init__(self):
        pass
    #---------------------------------------------------------------------------------
    def now(self):
        return datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    #---------------------------------------------------------------------------------
    def date_now(self):
        return datetime.datetime.now().strftime('%Y.%m.%d')
    #---------------------------------------------------------------------------------
    def time_now(self):
        return datetime.datetime.now().strftime('%H:%M:%S')
#=======================================================================================================================
class System:
    def __init__(self):
        pass
    #---------------------------------------------------------------------------------
    def get_os(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            return 'Linux-%s-%s' % (platform.dist()[0], platform.dist()[1])
        elif sys.platform == "darwin":
            return 'OSX-%s' % platform.mac_ver()[0]
        elif sys.platform == "win32":
            return platform.platform()
        else:
            return 'UNKNOWN'
    #---------------------------------------------------------------------------------
    def get_python_ver(self):
        ver_full = sys.version.split('\n')[0]
        space_pos = ver_full.find(' ')
        return ver_full[0:space_pos]
    #---------------------------------------------------------------------------------
    def get_free_ram(self):
        mem = psutil.virtual_memory()
        free = float(mem.free)/float(mem.total)*100
        return float("{:2.0f}".format(free))
    #---------------------------------------------------------------------------------
    def get_used_ram(self):
        mem = psutil.virtual_memory()
        used = float(mem.used)/float(mem.total)*100
        return float("{0:4.2f}".format(used))
    #---------------------------------------------------------------------------------
    def get_boot_time(self):
        return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y.%m.%d %H:%M:%S")
    #---------------------------------------------------------------------------------
    def get_uptime(self):
        curr_time = datetime.datetime.today()
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        delta = curr_time - boot_time
        #delta_formated = '%s DAYS %.2d:%.2d:%.2d' % (delta.days,delta.seconds//3600,(delta.seconds//60)%60, delta.seconds%60)
        return delta
    #---------------------------------------------------------------------------------
    def clear(self):
        if 'win32' in sys.platform:
            os.system('cls')
        else:
            os.system('clear')
#=======================================================================================================================
class Network:
    def __init__(self):
        System()
        pass
    #---------------------------------------------------------------------------------
    def get_interfaces(self):
        net = psutil.net_if_addrs()
        interfaces = net.keys()
        result = []
        # -------------------------------------------------------------------------------
        if 'win32' in sys.platform: #FOR WINDOWS
            for iface in interfaces:
                obj_len = len(net[iface])
                if obj_len == 1:
                    if net[iface][0].family == 17 or net[iface][0].family == 2:
                        result.append(iface)
                else:
                    if net[iface][1].family == 2:
                        result.append(iface)
        # -------------------------------------------------------------------------------
        elif 'linux' in sys.platform:  # FOR LINUX
            for iface in interfaces:
                result.append(iface)
        #-------------------------------------------------------------------------------
        elif 'darwin' in sys.platform: #FOR MAC OSX
            for iface in interfaces:
                if net[iface][0].family == 2:
                    try:
                        if not '::' in net[iface][1].address:
                            result.append(iface)
                    except Exception:
                        pass
        # -------------------------------------------------------------------------------


        return result
    #---------------------------------------------------------------------------------
    def get_connections(self):

        my_connections = psutil.net_connections()
        conn_len = len(my_connections)
        connections_list = []

        for i in range(0, conn_len):

            if my_connections[i].status == 'ESTABLISHED' and  \
                my_connections[i].laddr[0] <> '0.0.0.0' and \
                (not '::' in my_connections[i].laddr[0] or not '::' in my_connections[i].raddr[0]) and \
                (len(my_connections[i].laddr[0]) <= 16):

                try:
                    conn_loc_address = my_connections[i].laddr[0]
                    conn_loc_port = my_connections[i].laddr[1]
                except Exception:
                    conn_loc_address = 'FAIL'
                    conn_loc_port = 'FAIL'

                try:
                    conn_rem_address = my_connections[i].raddr[0]
                    conn_rem_port = my_connections[i].raddr[1]
                except Exception:
                    conn_rem_address = 'FAIL'
                    conn_rem_port = 'FAIL'

                conn_family = my_connections[i].family
                conn_status = my_connections[i].status

                connections_list.append((conn_loc_address,conn_loc_port,conn_rem_address,conn_rem_port,conn_family,conn_status))

        connections_list.sort()
        return {'LIST': connections_list, 'CONNECTIONS':len(connections_list)}
    #---------------------------------------------------------------------------------
    def get_network(self):

        try:
            net = psutil.net_if_addrs()
        except Exception:
            ip = 'null'
            mac = 'null'
            os = 'null'
            pass

        interfaces = self.get_interfaces()
        ip_list = []
        mac_list = []
        os_list = []
        iface_list =[]

        for iface in interfaces:

            addr1 = 'none'
            addr2 = 'none'
            addr3 = 'none'
            addr4 = 'none'

            iface_str = str(iface)
            iface_data = net[iface_str]


            if len(iface_data) >= 1:
                addr1 = iface_data[0].address

            if len(iface_data) >= 2:
                addr2 = iface_data[1].address

            if len(iface_data) >= 3:
                addr3 = iface_data[2].address

            if len(iface_data) >= 4:
                addr4 = iface_data[3].address

            #--------------------------------
            if 'linux' in sys.platform:
                os = 'Linux'
                try:
                    ip = addr1
                    mac = addr3
                except Exception:
                    ip = 'NOT CONNECTED'
                    mac = addr1
            #--------------------------------
            elif 'darwin' in sys.platform:
                os = 'OSX'
                ip = addr1
                mac = addr2
            #--------------------------------
            elif 'win32' in sys.platform:
                os = 'Windows'
                ip = addr2
                mac = addr1
            #--------------------------------
            if not '00:00:00:00:00:00' in mac:
                ip_list.append(ip)
                mac_list.append(mac)
                os_list.append(os)
                iface_list.append(iface)
            #--------------------------------

        return {'IFACE': iface_list, 'IP': ip_list, 'MAC': mac_list, 'OS': os_list}
    #---------------------------------------------------------------------------------
    def show_network(self):

        print '{}'.format('================================================================')
        print '{:13}{:16}{:22}{:10}'.format('INTERFACE','IP ADDRESS','MAC ADDRESS', 'OS')
        print '{}'.format('----------------------------------------------------------------')

        ifaces = self.get_network()['IFACE']
        ips =  self.get_network()['IP']
        macs = self.get_network()['MAC']
        oss = self.get_network()['OS']

        for n in range(0,len(ifaces)):
            print '{:13}{:16}{:22}{:10}'.format(ifaces[n],ips[n],macs[n],oss[n])
    #---------------------------------------------------------------------------------
    def show_connections(self):
        conn_list = self.get_connections()['LIST']

        print '{}'.format('================================================================')
        print '{:^14}{:^23}{:^27}'.format('CONNECTION','LOCAL','REMOTE')
        print '{}'.format('----------------------------------------------------------------')

        for i in conn_list:

            lst_local = '{:>15} [{:>5}]'.format(i[0],i[1])
            lst_remote = '{:>15} [{:>5}]'.format(i[2],i[3])
            lst_status = i[5]

            print '{:^14}{:>23}{:>27}'.format(lst_status,lst_local,lst_remote)

        print '{}'.format('----------------------------------------------------------------')
        print '{}{}'.format('NUMBER OF CONNECTIONS: ', self.get_connections()['CONNECTIONS'])
        #-----------------------------------------------------------------------------------------
#=======================================================================================================================
