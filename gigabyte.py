from __future__ import annotations
import usb.core
import sys
from time import sleep


class GCC:
    def __init__(self) -> None:
        self.VID = 0x2109
        self.PID = 0x8883
        self.dev: usb.Device | None = None
        self.delay = 100 / 1000 # 100ms delay
        self.reattach = False
    
    def __enter__(self):
        self.dev: usb.Device | None = usb.core.find(idVendor=self.VID, idProduct=self.PID)
        
        if self.dev is None:
            raise ValueError('Not found!')
            sys.exit(1)
        
        self.reattach = False
        if sys.platform != "win32" and self.dev.is_kernel_driver_active(0):
            self.reattach = True
            self.dev.detach_kernel_driver(0)
        
        self.dev.set_configuration(1)
        
        return self

    def __exit__(self, type, value, traceback):
        if self.reattach:
            self.dev.detach_kernel_driver(0)

    def write(self, brightness_percent):
        bmRequestType = 0x40
        bmRequest = 178
        wValue = 0x00
        wIndex = 0x00
        wdata = bytearray([0x6e, 0x51, 0x81 + len(bytearray(brightness_percent)), 0x03, 0x10, 0x00, brightness_percent]) 
        self.dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, wdata)
        sleep(self.delay)
    
    def transition(self, _from: int, _to: int):
        for x in range(_from, _to + 1, 5):
            self.write(x)

    
if __name__ == "__main__":
    if not len(sys.argv) > 1:
        sys.exit(-1)
    
    with GCC() as gcc:
        # print(gcc.dev)
        # breakpoint()
        # gcc.write(int(sys.argv[1])) # 0-100
        for _ in range(4):
            gcc.transition(0,100)
            sleep(0.1)
            gcc.transition(100,0)
