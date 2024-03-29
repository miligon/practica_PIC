#include <main.h>

char recieved[64]; // Buffer de recepcion para datos USB Serial
char i = 0;
char c = 0; 
int1 motor_status = 0; // Guarda el estado del motor

volatile int16 pulsos = 0; // contador de pulsos interrupcionj
volatile int16 rev = 0;
volatile int16 indice = 0; // indice datos medicion
volatile int16 data[250];
volatile int8 data_ready = 0; // bandera para saber el estado de la medicion
                              // 0 -> No se ha realizado medicion
                              // 1 -> Medicion en proceso
                              // 2 -> Medicion finalizada
#INT_RTCC
void timer0(void)
{
   if ( indice < 250 && data_ready == 1)
   {
      data[indice] = pulsos;
      pulsos = 0;
      indice++; 
      //output_toggle(LED2);
   }
   else
   {
      data_ready = 2;

   }
   set_timer0(64597);
   output_toggle(LED2);
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
   // Recibe una trama a traves del USB Serial
   
   // Limpia el buffer de recepción
   for (i = 0; i < 64; ++i)
   {
      recieved[i] = 0;
   }
   // Detecta si hay datos para recibir
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
         }while(recieved[i] != '\n'); // Sale del Loop cuando le llega un fin de linea 0x10
         return 1;
      }
      return 0;
   }
   else
   {
      return 0;
   }   
}

void toggle_motor()
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
   // Inicializa las variables para la medicion
   data_ready = 1;
   pulsos = 0;
   indice = 0;
   
   //Configura el Timer0
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_256);      //5.4 ms overflow
   set_timer0(64597);

   enable_interrupts(INT_EXT);
   enable_interrupts(INT_RTCC);
   enable_interrupts(GLOBAL);
   
   // Activa el motor
   motor_status = 1;
   output_high(MOTOR);
}

void finaliza_medicion()
{
   disable_interrupts(INT_EXT);
   disable_interrupts(INT_RTCC);
   disable_interrupts(GLOBAL);
   // Desactiva el motor
   output_low(MOTOR);
   motor_status = 0;
   data_ready = 3;
}

void send_data()
{
   //Envia la informacion
   int16 ms = 0;
   usb_cdc_putc(35); //#
   int16 rps = 0;
   for (int16 i = 0; i < 250; i++)
   {
      usb_cdc_putc((ms&0xFF00)>>8); //1 byte MSB  tiempo
      usb_cdc_putc(ms&0xFF);        //1 byte LSB  tiempo
      usb_cdc_putc(',');            // separador ,  
      usb_cdc_putc((data[i]&0xFF00)>>8); //1 byte MSB  rpms
      usb_cdc_putc(data[i]&0xFF);        //1 byte LSB  rpms
      ms = ms + 20;
      if (i != 250)
      {
         usb_cdc_putc(36); //$
      }
   }
   usb_cdc_putc(13); // \r
   usb_cdc_putc(10); // \n
}

void main()
{
   input_state(pin_B0);
   delay_ms(500);
   blink_led(1000);
   inicia_medicion();
   while(data_ready==1){blink_led(10);}
   finaliza_medicion();
   output_low(LED2);
   
   //Inicializa CDC
   usb_init();
   usb_cdc_init();
   while(!usb_cdc_connected()){blink_led(300);}

   //Example blinking LED program
   while(true)
   {     
      // Recibe datos del USB serial
      if (recibir())
      {
         // Verifica la estructura de la trama
         if (recieved[0] == '#' && recieved[2] == '\n')
         {
            // Selecciona el caso dependiendo del comando recibido
            switch(recieved[1])
            {
               case '1':
                  printf(usb_cdc_putc, "#OK\n");
                  inicia_medicion();
                  break;
               case '2':
                  toggle_motor();
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
                 send_data();
                 break;
               default:
                  break;
            }
         }
      }
   }

}
