
import configparser
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
    # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def print_ip_info():
    hostname = socket.gethostname()
    IPAddr = get_ip() #socket.gethostbyname(hostname)

    print("Computer Name :" + hostname)
    print("Computer IP Address :" + IPAddr)
    print("")
    print("In PIDS software > Devices > <Device name> > IP address to {} see alarms on GUI".format(IPAddr))


def writeMonConfigFile(fileName):
    config = configparser.ConfigParser()
    config['modbus_page'] = {"ipaddr": "192.168.0.7", "pageurl": "192.168.0.7/sernet1.shtml?0", "uname": "admin",
                             "pwd": "admin",
                             "modbusport": "502"}

    config['http_page'] = {"ipaddr": "192.168.0.7", "pageurl": "192.168.0.7/sernet1.shtml?1", "uname": "admin",
                           "pwd": "admin",
                           "token": "/receive?t=123456789", "server": "192.168.0.125"}

    config['misc_page'] = {"ipaddr": "192.168.0.7", "pageurl": "192.168.0.7/misc.shtml", "uname": "admin",
                           "pwd": "admin", "newuname": "hawk",
                           "newpwd": "0195h", "rsttime": "65000"}

    config['dynamic_page'] = {"ipaddr": "192.168.0.7", "pageurl": "192.168.0.7/ipconfig.shtml", "uname": "hawk",
                              "pwd": "0195h", "statip": "110"}

    config['reset_page'] = {"ipaddr": "192.168.0.7", "pageurl": "192.168.0.7/manage.shtml", "uname": "hawk",
                            "pwd": "0195h"}

    config['search_device'] = {"start": "150", "end": "160", "uname": "hawk", "pwd": "0195h", "timeout": "0.3",
                               "network": "192.168.0."}

    config['last_serial'] = {"last_ser": "300"}


    with open(fileName, 'w') as configfile:
            config.write(configfile)

def readMonConfig(fileName):

    mon_config = configparser.ConfigParser()
    try:
        mon_config.read(fileName)

    except:
        print(f'Error: unable to read config file: {fileName}')
        mon_config = -1

    #print(mon_config.sections())

    return mon_config