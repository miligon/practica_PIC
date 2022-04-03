#include <main.h>
#INCLUDE <stdlibm.h>

char recieved[64];
char * TxBuffer;
char i = 0;
char c = 0;
int1 motor_status = 0;

volatile int16 pulsos = 0;
volatile int16 indice = 0;
volatile int16 data[278]; // 556 bytes RAM
volatile int8 data_ready = 0;

#INT_RTCC
void timer0(void)
{
   if ( indice < 278 && data_ready == 1)
   {
      data[indice] = pulsos * 185;
      pulsos = 0;
      indice++;
   }
   else
   {
      data_ready = 2;
      
   }
}

#INT_EXT
void  EXT_isr(void) 
{
   if ( data_ready == 1)
   {
      pulsos++;
   }
}

char recibir()
{
   for (i = 0; i < 64; ++i)
   {
      recieved[i] = 0;
   }
   if ( usb_cdc_kbhit() )
   {
      c = usb_cdc_getc();
      if ( c == '#' )
      {
         i = 0;
         recieved[i] = c;
         do
         {
            if (usb_cdc_kbhit())
            {
               ++i;
               recieved[i] = usb_cdc_getc();
            }
         }while(recieved[i] != '\n');
         return 1;
      }
      return 0;
   }
   else
   {
      return 0;
   }   
}

void toogle_motor()
{
   motor_status = !motor_status;
   output_bit(MOTOR, motor_status);
}

void blink_led(int ms)
{
   output_low(LED);
   delay_ms(ms);
   output_high(LED);
   delay_ms(ms);
}

void inicia_medicion()
{
   data_ready = 1;
   pulsos = 0;
   motor_status = 1;
   indice = 0;
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_1);      //5.4 ms overflow

   enable_interrupts(INT_EXT);
   enable_interrupts(INT_RTCC);
   enable_interrupts(GLOBAL);
   output_bit(MOTOR, motor_status);
}

void finaliza_medicion()
{
   disable_interrupts(INT_EXT);
   disable_interrupts(INT_RTCC);
   motor_status = 0;
   output_bit(MOTOR, motor_status);
}

void send_data()
{
   int16 ms = 54;
   usb_cdc_putc(35); //#
   for (int16 i = 0; i < 278; ++i)
   {
      usb_cdc_putc((ms&0xFF00)>>8);
      usb_cdc_putc(ms&0xFF);
      usb_cdc_putc(',');
      usb_cdc_putc((data[i]&0xFF00)>>8);
      usb_cdc_putc(data[i]&0xFF);
      ms = ms + 54;
      if (i != 277)
      {
         usb_cdc_putc(36); //$
      }
   }
   usb_cdc_putc(10); // \n
}

void main()
{
   
   usb_init();
   usb_cdc_init();
   while(!usb_cdc_connected()){blink_led(300);}

   //Example blinking LED program
   while(true)
   {
      if (data_ready == 1)
      {
        //printf(usb_cdc_putc, "%u, %u\n",indice, pulsos );
      }
      if (data_ready == 2)
      {
         finaliza_medicion();
      }
      //blink_led(50);
      if (recibir())
      {
         if (recieved[0] == '#' && recieved[2] == '\n')
         {
            switch(recieved[1])
            {
               case '1':
                  printf(usb_cdc_putc, "#OK\n");
                  inicia_medicion();
                  break;
               case '2':
                  toogle_motor();
                  if (!motor_status)
                  {
                     printf(usb_cdc_putc, "#ON\n");
                  }
                  else
                  {
                     printf(usb_cdc_putc, "#OFF\n");
                  }
                  break;
               case '3':
                  if (!motor_status)
                  {
                     printf(usb_cdc_putc, "#ON\n");
                  }
                  else
                  {
                     printf(usb_cdc_putc, "#OFF\n");
                  }
                  break;
               case '4':
                  switch(data_ready)
                  {
                     case 0:
                        printf(usb_cdc_putc, "#READY\n");
                        break;
                     case 1:
                        printf(usb_cdc_putc, "#BUSY\n");
                        break;
                     case 2:
                        printf(usb_cdc_putc, "#FINISHED\n");
                        break;
                  }
                  break;
               case '5':
                  if ( data_ready == 2 )
                  {
                     send_data();
                  }
                  else
                  {
                     printf(usb_cdc_putc, "#NODATA\n");
                  }
                  break;
               default:
                  break;
            }
         }
      }
   }

}
