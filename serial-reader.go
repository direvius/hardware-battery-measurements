package main

import (
    "log"

    "bufio"
    "fmt"
    "github.com/tarm/serial"
    "time"
)

func main() {
    c := &serial.Config{
        Name: "/dev/cu.wchusbserial1410",
        Baud: 115200,
    }
    s, err := serial.OpenPort(c)
    if err != nil {
        log.Fatal(err)
    }

    { // flush input buffer (dirty hack)
        buf := make([]byte, 256)
        n, err := s.Read(buf)
        for n == 256 {
            if err != nil {
                log.Fatal(err)
            }
            n, err = s.Read(buf)
        }
    }
    scanner := bufio.NewScanner(s)
    for scanner.Scan() {
        fmt.Printf("%.6f %s\n", float64(time.Now().UnixNano())/1e9, scanner.Text())
    }
    if err := scanner.Err(); err != nil {
        log.Println("Error reading data:", err)
    }
}

