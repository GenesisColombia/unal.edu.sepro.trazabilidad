/* gpio.c  D.J.Whale  8/07/2014
 *
 * A very simple interface to the GPIO port on the Raspberry Pi.
 */

/***** INCLUDES *****/
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <wiringPi.h>
//#include <pigpio.h>
#include "gpio.h"

void gpio_init()
{
#ifndef GPIO_SIMULATED
   if (wiringPiSetup () == -1)
   //  if (gpioInitialise() < 0)
   {
      fprintf(stderr, "pigpio initialisation failed\n");
      return 1;
   }else{
	printf("OK!!");
	}
#endif
}
void gpio_relase()
{
  system("gpio mode 8 alt0");
  system("gpio mode 9 alt0");
}

void gpio_terminate()
{
//gpioTerminate();
}

void gpio_setin(int g)
{
#ifndef GPIO_SIMULATED
  //bcm2835_gpio_fsel(g, BCM2835_GPIO_FSEL_OUTP);
  pinMode(g, INPUT);
  // gpioSetMode(g, PI_INPUT);
#else
  printf("gpio:in:%d\n", g);
#endif
}


void gpio_setout(int g)
{
#ifndef GPIO_SIMULATED
  /* always INP_GPIO before OUT_GPIO */
  //INP_GPIO(g); #### this causes glitching
  //bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);
  pinMode(g,OUTPUT);
  // gpioSetMode(g, PI_OUTPUT);
#else
  printf("gpio:out:%d\n", g);
#endif
}


void gpio_high(int g)
{
#ifndef GPIO_SIMULATED
  digitalWrite(g, 1);
  //  gpioWrite(g, 1);
#else
  printf("gpio:high:%d\n", g);
#endif
}


void gpio_low(int g)
{
#ifndef GPIO_SIMULATED
  digitalWrite(g, 0);
  //gpioWrite(g, 0);
#else
  printf("gpio:low:%d\n", g);
#endif
}


void gpio_write(int g, int v)
{
#ifndef GPIO_SIMULATED
  digitalWrite(g, v);
  // gpioWrite(g, v);
#else
  printf("gpio:write:%d=%d\n", g, v);
#endif
}


int  gpio_read(int g)
{
#ifndef GPIO_SIMULATED
  return digitalRead(g);
  //  return gpioRead(g);
#else
  return 0; /* always low in simulation */
#endif
}


/***** END OF FILE *****/
