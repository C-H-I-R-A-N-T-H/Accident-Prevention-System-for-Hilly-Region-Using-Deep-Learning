#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <LiquidCrystal_I2C.h>

// ---------------- OLED ----------------
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ---------------- Ultrasonic ----------------
#define TRIG_PIN 9
#define ECHO_PIN 10

// ---------------- LCD ----------------
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ---------------- LEDs ----------------
const int RED_LED = 3;
const int GREEN_LED = 4;
const int ANIMAL_LED = 5;

void setup() {
  Serial.begin(9600);

  // LCD Init
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("STAY ALERT &");
  lcd.setCursor(0, 1);
  lcd.print("STAY SAFE");

  // OLED Init
  Wire.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED not found!");
    while (1);
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(10, 20);
  display.println("Starting...");
  display.display();
  delay(1000);

  // Ultrasonic pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // LEDs
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(ANIMAL_LED, OUTPUT);

  digitalWrite(GREEN_LED, HIGH);
}

void loop() {

  // ---- Ultrasonic to OLED ----
  long duration;
  float distance;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(10, 10);
  display.print("DISTANCE:");

  display.setTextSize(3);
  display.setCursor(20, 35);
  display.print(distance);
  display.print("cm");
  display.display();

  // ---- LCD Alerts ----
  if (Serial.available() > 0) {
    char command = Serial.read();

    digitalWrite(RED_LED, LOW);
    digitalWrite(ANIMAL_LED, LOW);
    digitalWrite(GREEN_LED, LOW);

    lcd.clear();

    if (command == '1') {
      digitalWrite(RED_LED, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("BIKE AHEAD");
    }
    else if (command == '2') {
      digitalWrite(RED_LED, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("CAR AHEAD");
    }
    else if (command == '3') {
      digitalWrite(RED_LED, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("TRUCK AHEAD");
    }
    else if (command == '4') {
      digitalWrite(ANIMAL_LED, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("ANIMAL AHEAD");
    }
    else {
      digitalWrite(GREEN_LED, HIGH);
      lcd.setCursor(0, 0);
      lcd.print("STAY ALERT &");
      lcd.setCursor(0, 1);
      lcd.print("STAY SAFE");
      return;
    }

    delay(2000);

    digitalWrite(RED_LED, LOW);
    digitalWrite(ANIMAL_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("STAY ALERT &");
    lcd.setCursor(0, 1);
    lcd.print("STAY SAFE");
  }

  delay(100);
}
