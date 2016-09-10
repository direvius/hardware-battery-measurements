# hardware-battery-measurements
Измерение потребления батарейки телефоном - arduino-way.  
  
Как использовать:  
1. Скомпилить.  
2. Подключить arduino к USB порту  
3. Запустить serial-reader. 

    
Usage of serial-reader:  
  -device string  
        USB device file (default "/dev/cu.wchusbserial1410")  
  -samples int  
        number of samples to acquire (default 30000)  
  -skip int  
        number of samples to skip (workaround to avoid dirty buffer) (default 500)  
  
  
$ serial-reader -device /dev/cu.wchusbserial1420 -samples 900000  
 1472476706.982795 1435.55  
 1472476706.982903 1040.04  
 1472476706.982911 908.20  
 1472476706.982915 952.15  
 1472476706.991034 869.14  
 1472476706.991091 1113.28  
 1472476706.991102 1059.57  
