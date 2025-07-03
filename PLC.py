import pymcprotocol
class PLC:
    def __init__(self,IP,PORT):
        '''
        IP string format ie IP = "192.168.3.250"
        Port is an integer ie PORT = 1026
        '''
        self.IP = IP
        self.PORT=PORT
        #connection error increments until a threshold is reached then reset and reconnect.
        self.connection_error = 0
        
        #connect to the PLC
        self.pymc3e = pymcprotocol.Type3E()
        try:
            self.pymc3e.connect(self.IP, self.PORT)
        except:
            print("Error in connection!!")
        else:
            print("successful connnection")
            
    def reconnect(self):
        self.connection_error = 0
        #connection error increments until a threshold is reached then reset and reconnect.
        self.connection_error = 0
        #connect to the PLC
        self.pymc3e = pymcprotocol.Type3E()
        try:
            self.pymc3e.connect(self.IP, self.PORT)
        except:
            print("Error in connection!!")
        else:
            print("successful connnection")
        
    def connect(self,IP,PORT):
        #connect to the PLC
        self.pymc3e = pymcprotocol.Type3E()
        try:
            self.pymc3e.connect(self.IP, self.PORT)
        except:
            print("Error in connection!!")
        else:
            print("successful connnection")
            
    def read_word_value(self,value):
        '''
        value is a string ie value="D306"
        used only for word units
        '''
        try:
            word=self.pymc3e.batchread_wordunits(headdevice=value,readsize=1)
        except:
            self.connection_error +=1
            return 0
        else:
            return word[0]
        
    
    def read_double_value(self,value):
        '''
        value is a string ie value="D306"
        used only for word units
        '''
        try:
            word_values, dword_values = self.pymc3e.randomread(word_devices = ["D1"],dword_devices=[value])
        except:
            self.connection_error +=1
            return 0
        else:
            return dword_values[0]
        
    def read_binary_value(self,value):       
        '''
        value is a string ie value="M306"
        used only for binary units
        '''
        try:
            bit = self.pymc3e.batchread_bitunits(headdevice=value,readsize=2)
        except:
            self.connection_error +=1
            print("error read")
            return 1
        else:
            return bit[0]

    def read_input_value(self):       
        '''
        value is a string ie value="M306"
        used only for binary units
        '''
        try:
            bits = self.pymc3e.batchread_bitunits(headdevice="X000",readsize=180)
        except:
            self.connection_error +=1
            return [1]*180
        else:
            #print(bits)
            return bits

    def check_connect(self):
        if self.connection_error>10:
            print("Number of read failures happened over limit")
            #there is a connection error lets reconnect
            self.reconnect()
            self.connection_error=0
            
        return 0

    
    def read_m_bits(self,start,amount):
        '''
        read from start device ie start="M23"
        read amount bits from start eg if start ="M23" and amount=3 return M23,M24,M25
        '''
        try:
            M = self.pymc3e.batchread_bitunits(headdevice=start,readsize=amount)
        except:
            self.connection_error +=1
            return [-1]*amount
        else:
            return M        
