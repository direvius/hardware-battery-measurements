# hardware-battery-measurements
Измерение потребления батарейки телефоном - arduino-way.  
  

Как использовать:  
1. Скомпилить.  
2. Подключить arduino к USB порту  
3. Запустить serial-reader. 
  
```
$ serial-reader -device /dev/cu.wchusbserial1420 -samples 900000

 1472476706.982795 1435.55  
 1472476706.982903 1040.04  
 1472476706.982911 908.20  
 1472476706.982915 952.15  
 1472476706.991034 869.14  
 1472476706.991091 1113.28  
 1472476706.991102 1059.57
```
help почитать так: `serial-reader -h`
```
$ ./serial-reader -h
Usage of ./serial-reader:
  -device string
        USB device file (default "/dev/cu.wchusbserial1410")
  -samples int
        number of samples to acquire (default 30000)
  -skip int
        number of samples to skip (workaround to avoid dirty buffer) (default 500)
```
$ ./ser.go
=======
>>>>>>> c8f53d708c4cb7971cbaa001cd1f7e581c946f9a
 1472476706.982795 1435.55  
 1472476706.982903 1040.04  
 1472476706.982911 908.20  
 1472476706.982915 952.15  
 1472476706.991034 869.14  
 1472476706.991091 1113.28  
 1472476706.991102 1059.57  
<<<<<<< HEAD
```

Известные проблемы:  
1. Буферизуется вывод/попадает мусор в начало лога. В исходниках есть грязных хак, бросающий на пол первые значения. Т.е. в начале не собирается около секунды.
=======
>>>>>>> c8f53d708c4cb7971cbaa001cd1f7e581c946f9a
