import time
import esp
esp.osdebug(None)

def open_and_create_file(file,data=''):
    import uos
    files = uos.listdir('')
    del uos
    if not file in files:
        f = open(file,'w')
        f.write(data)
        f.close()
    f = open(file,'r')
    return(f)

class wlan():
    def __init__(self):
        import network
        self.nw = network
        self.load_wlan_config()
        self.start_station()

    def load_wlan_config(self):
        f = open_and_create_file('wifi.txt','SSID\r\nPassword')
        f_split = f.read().replace('\n','\r').replace('\r\r','\r').split('\r')
        f.close()
        self.sta_name = f_split[0]
        self.sta_passwd = f_split[1]
        del f_split

    def start_station(self):
        wlan = self.nw.WLAN(self.nw.STA_IF)
        wlan.active(True)
        print('Connecting to network...')
        wlan.connect(self.sta_name, self.sta_passwd)
        start = time.time()
        while wlan.isconnected()==False and start+30>time.time():
            time.sleep(2)
        if wlan.isconnected()==True:
            print('network config:', wlan.ifconfig())
        if wlan.isconnected()==False:
            wlan.active(False)
            self.broken_wlan_sta()

    def broken_wlan_sta(self):
        print('Failed to connect to WiFi AP, starting fallback.')
        ap = self.nw.WLAN(self.nw.AP_IF)
        ap.config(essid='WeMoS-AP',channel=11)
        ap.config(max_clients=10)
        ap.active(True)



def main():
    wlan()
    import webrepl
    webrepl.start(password='1234')

if __name__=='__main__':
    main()
