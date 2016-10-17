#undef HID_ENABLED

// Arduino Due ADC->DMA->USB 1MSPS
// by stimmer
// from http://forum.arduino.cc/index.php?topic=137635.msg1136315#msg1136315
// Input: Analog in A0
// Output: Raw stream of uint16_t in range 0-4095 on Native USB Serial/ACM

// on linux, to stop the OS cooking your data: 
// stty -F /dev/ttyACM0 raw -iexten -echo -echoe -echok -echoctl -echoke -onlcr

const uint16_t bufsize = 256;

volatile int bufn,obufn;
uint16_t buf[4][bufsize];   // 4 buffers of 256 readings

void ADC_Handler(){     // move DMA pointers to next buffer
  static uint32_t prev_mcs = 0;
  static uint32_t c = 0;
  int f=ADC->ADC_ISR;
  if (f&(1<<27)){
   bufn=(bufn+1)&3;
   ADC->ADC_RNPR=(uint32_t)buf[bufn];
   ADC->ADC_RNCR=bufsize;
  }
//  uint32_t mcs = micros();
//
//  if ((++c % (256 * 256)) == 0) {
//    Serial.println(mcs - prev_mcs);
//  }
//  prev_mcs = mcs;
}

void setup(){
//  Serial.begin(115200);
//  Serial.println("Hello");
  SerialUSB.begin(0);
  while(!SerialUSB);
  pmc_enable_periph_clk(ID_ADC);
  adc_init(ADC, SystemCoreClock, 21UL * 1000000UL, ADC_STARTUP_FAST);
  adc_set_resolution(ADC, ADC_12_BITS);
  ADC->ADC_MR |=0x80; // free running

  ADC->ADC_CHER=0x80; 

  NVIC_EnableIRQ(ADC_IRQn);
  ADC->ADC_IDR=~(1<<27);
  ADC->ADC_IER=1<<27;
  ADC->ADC_RPR=(uint32_t)buf[0];   // DMA buffer
  ADC->ADC_RCR=bufsize;
  ADC->ADC_RNPR=(uint32_t)buf[1]; // next DMA buffer
  ADC->ADC_RNCR=bufsize;
  bufn=obufn=1;
  ADC->ADC_PTCR=1;
  ADC->ADC_CR=2;
}

void loop(){
  while(obufn==bufn); // wait for buffer to be full
  SerialUSB.write((uint8_t *)buf[obufn],512); // send it - 512 bytes = 256 uint16_t
  obufn=(obufn+1)&3;    
}
