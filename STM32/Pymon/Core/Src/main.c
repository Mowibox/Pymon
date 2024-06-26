/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "buzzer.h"
#include "buzzer_tones.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
Buzzer_HandleTypeDef hbuzzer;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim3;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_TIM1_Init(void);
static void MX_TIM3_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_TIM1_Init();
  MX_TIM3_Init();
  /* USER CODE BEGIN 2 */

  //Buzzer configuration
  uint8_t buf;
  Buzzer_InitTypeDef buzzerConfig;
  buzzerConfig.channel = TIM_CHANNEL_1;
  buzzerConfig.timer = &htim3;
  buzzerConfig.timerClockFreqHz = HAL_RCC_GetPCLK2Freq(); // NOTE: this should be freq of timer, not frequency of peripheral clock
  Buzzer_Init(&hbuzzer, &buzzerConfig);
  Buzzer_Start(&hbuzzer);

  GPIO_TypeDef * Red_GPIO = GPIOF;
  uint16_t Red_PIN = GPIO_PIN_1;

  GPIO_TypeDef * Yellow_GPIO = GPIOA;
  uint16_t Yellow_PIN = GPIO_PIN_1;

  GPIO_TypeDef * Green_GPIO = GPIOB;
  uint16_t Green_PIN = GPIO_PIN_0;

  GPIO_TypeDef * Blue_GPIO = GPIOA;
  uint16_t Blue_PIN = GPIO_PIN_7;


  //Boot sequence
  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_C4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, GPIO_PIN_7, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_D4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_E4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_SET);
  Buzzer_Note(&hbuzzer, NOTE_F4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_G4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_A4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, NOTE_B4);
  HAL_Delay(200);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_SET);
  Buzzer_Note(&hbuzzer, NOTE_C5);
  HAL_Delay(500);

  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
  Buzzer_Note(&hbuzzer, 0);


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {


	  //Data reception
	  HAL_UART_Receive(&huart2, &buf, 1, 1000);

	  //Red color
	  if (buf == 'r'){
		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
		  Buzzer_Note(&hbuzzer, NOTE_C4);
	  }
	  //Yellow color
	  else if (buf == 'y'){
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
		  Buzzer_Note(&hbuzzer, NOTE_D4);
	  }
	  //Green color
	  else if (buf == 'g'){
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
		  Buzzer_Note(&hbuzzer, NOTE_E4);
	  }
	  //Blue color
	  else if (buf == 'b'){
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_SET);
		  Buzzer_Note(&hbuzzer, NOTE_F4);
	  }
	  //None
	  else if (buf == 'n'){
		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  Buzzer_Note(&hbuzzer, 0);
	  }

	  //Main menu sequence
	  else if (buf == 'm'){
		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_SET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(250);

		  HAL_GPIO_WritePin(Red_GPIO, Red_PIN, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(Yellow_GPIO, Yellow_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Green_GPIO, Green_PIN, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(Blue_GPIO, Blue_PIN, GPIO_PIN_RESET);
		  HAL_Delay(50);

	  }


    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_TIM1;
  PeriphClkInit.Tim1ClockSelection = RCC_TIM1CLK_HCLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 7;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 65535;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterOutputTrigger2 = TIM_TRGO2_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.BreakFilter = 0;
  sBreakDeadTimeConfig.Break2State = TIM_BREAK2_DISABLE;
  sBreakDeadTimeConfig.Break2Polarity = TIM_BREAK2POLARITY_HIGH;
  sBreakDeadTimeConfig.Break2Filter = 0;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 7;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 65535;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 49;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 38400;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  huart2.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(Blue_LED_GPIO_Port, Blue_LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, Green_LED_Pin|Red_LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(Yellow_LED_GPIO_Port, Yellow_LED_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : Blue_LED_Pin */
  GPIO_InitStruct.Pin = Blue_LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(Blue_LED_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : Green_LED_Pin Red_LED_Pin */
  GPIO_InitStruct.Pin = Green_LED_Pin|Red_LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : Yellow_LED_Pin */
  GPIO_InitStruct.Pin = Yellow_LED_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(Yellow_LED_GPIO_Port, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
