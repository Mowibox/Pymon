# STM32 Pymon

This directory houses the microcontroller part of Pymon.

## Configuration

For this project, we are using a NUCLEO F303K8 development board.

Serial communication takes place through the VCP port, on USART2 with a baud rate of 38400.

The pin configuration is as follows:

| Description | Morpho Pin | Arduino Pin | Configuration |
|-------------|------------|-------------|---------------|
|   Red LED   |    PA7     |     A6      |  GPIO_Output  |
|  Yellow LED |    PB0     |     D3      |  GPIO_Output  |
|  Green LED  |    PA1     |     D8      |  GPIO_Output  |
|   Blue LED  |    PF1     |     A1      |  GPIO_Output  |
|   Buzzer    |    PA6     |     A5      |   TIM3_CH1    |

Channel 1 of Timer 3 is activated to generate a PWM signal, allowing the buzzer to be used.

The buzzer library and how to integrate it into a project are specified the following [repository](https://github.com/brapacz/stm32-buzzer)
