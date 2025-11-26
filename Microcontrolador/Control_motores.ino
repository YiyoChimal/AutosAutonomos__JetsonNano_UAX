#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Dirección detectada del PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Pulso mínimo y máximo para servos comunes (ajústalo según tu modelo)
#define SERVO_MIN  110  // ~0 grados
#define SERVO_MAX  490  // ~180 grados

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("Iniciando PCA9685 con I2C en GPIO 0 y 1...");

  // ⚠️ Forzar el bus I2C en los pines 0 (SDA) y 1 (SCL)
  Wire.begin(0, 1);
  pwm.begin();
  pwm.setPWMFreq(50);  // Frecuencia típica de servos: 50 Hz

  delay(500);
}

void loop() {
  Serial.println("Moviendo servos canal 0 y 1...");

  // Recorre de 0° a 180°
  for (int pulso = SERVO_MIN; pulso <= SERVO_MAX; pulso++) {
    pwm.setPWM(0, 0, pulso);  // Servo en canal 0
    pwm.setPWM(1, 0, pulso);  // Servo en canal 1
    delay(5);
  }

  delay(500);

  // Regresa de 180° a 0°
  for (int pulso = SERVO_MAX; pulso >= SERVO_MIN; pulso--) {
    pwm.setPWM(0, 0, pulso);
    pwm.setPWM(1, 0, pulso);
    delay(5);
  }

  delay(1000);
}
