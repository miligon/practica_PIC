#include <18F4550.h>
#device ADC=16


#fuses HSPLL,NOWDT,NOBROWNOUT,NOPROTECT,NOLVP,NODEBUG,USBDIV,PLL3,CPUDIV1,VREGEN,MCLR,NOPBADEN

#use delay(clock=48MHz,crystal=12MHz,USB_FULL)
#define LED   PIN_B2
#define MOTOR PIN_B3
#define SENSOR PIN_B0
#define DELAY 500

#define  USB_CONFIG_PID       0x000A
#define  USB_CONFIG_VID       0x04d8
#define USB_CONFIG_BUS_POWER 100
#define USB_STRINGS_OVERWRITTEN

char USB_STRING_DESC_OFFSET[]={0,4,14};

char const USB_STRING_DESC[]={
   //string 0 - language
      4,  //length of string index
      0x03,  //descriptor type (STRING)
      0x09,0x04,  //Microsoft Defined for US-English
   //string 1 - manufacturer
      10,  //length of string index
      0x03,  //descriptor type (STRING)
      'h',0,
      'o',0,
      'l',0,
      'a',0,
   //string 2 - product
      10,  //length of string index
      0x03,  //descriptor type (STRING)
      'u',0,
      'a',0,
      'r',0,
      't',0
};
#include <usb_cdc.h>

