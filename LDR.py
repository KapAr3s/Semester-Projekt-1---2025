from machine import I2C, Pin
import time

class I2C_ADS_LDR:
    
    def __init__(self,address, channels):
        self.channels = channels
        self.address = address
        self._w = bytearray(1) # ADS expects 1 byte format
        self._r = bytearray(1) # Also we don't allocate new
                #byte each time but reuse the same
        self.readings = []
        self.turn = False
        self.curent_avg = []
        self.last_instructs = []
        
        for _ in channels:
            self.readings.append([100,100,100])
            
            
        self.sensor_values = [0]*len(channels)

        self.tsStart = time.ticks_ms()

        self.i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400_000)
        
    def _ctrl_byte(self, ch, single_ended=True, pd_bits=0b01):
        #This function creates control byte for ADS
        if not 0 <= ch <=7:
            raise ValueError("Channel must be within 0-7")
        #Checks that channel requested is valid

        if single_ended:
            cmd = 0b1 << 7
        else:
            cmd = 0b0 << 7

        """This sets MSB to either 1 or 0 depending, if we want single_ended or differential input.
        we tpically want single_ended to the resulting cmd will look like 1000_0000 at this point"""


        cmd |= (ch & 0b111) << 4

        """This adds channel bits to our command from position 6 -> 4, using a bitwise OR to merge
        if the channel is 3 for example the cmd will now look like 1011_0000""" 
        
        cmd |= (pd_bits & 0b11) << 2
        
        """This adds power down bits to our command from position 3 -> 2, using a bitwise OR to merge
        if pd_bits is 01 for example the cmd will now look like 1011_0100"""

        return cmd
    
    
    def read_one(self, ch):
        try:
            self._w[0] = self._ctrl_byte(ch)
            self.i2c.writeto(self.address, self._w)
            self.i2c.readfrom_into(self.address,self._r)
            return self._r[0]
        except OSError:
            return None
    
    def read_all(self):
        sensor_values = []
        for ch in self.channels:
            sensor_values.append(self.read_one(ch))
        self.sensor_values = sensor_values
        return sensor_values

