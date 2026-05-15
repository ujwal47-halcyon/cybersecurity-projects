#include "RF24.h"
#include "esp_bt.h"
#include "esp_wifi.h"
#include "esp_task_wdt.h"

#define WDT_TIMEOUT     10        // Watchdog timeout in seconds
#define REINIT_INTERVAL 30000     // Re-initialize radio every 30 seconds
#define MIN_CHANNEL     2
#define MAX_CHANNEL     79
#define HOP_STEP        2

RF24 radio(5, 13, 4000000);

byte channel = 45;
unsigned int flag = 0;
unsigned long lastReinitTime = 0;
unsigned long hopCount = 0;

bool initRadio() {
  radio.stopConstCarrier();
  delay(20);

  if (!radio.begin()) {
    Serial.println("[ERROR] radio.begin() failed");
    return false;
  }

  radio.setAutoAck(false);
  radio.stopListening();
  radio.setRetries(0, 0);
  radio.setPayloadSize(5);
  radio.setAddressWidth(3);
  radio.setPALevel(RF24_PA_MAX, true);
  radio.setDataRate(RF24_2MBPS);
  radio.setCRCLength(RF24_CRC_DISABLED);
  radio.startConstCarrier(RF24_PA_MAX, channel);

  Serial.println("[OK] Radio initialized");
  return true;
}

void hopChannel() {
  if (flag == 0) {
    channel += HOP_STEP;
  } else {
    channel -= HOP_STEP;
  }

  // Boundary clamp — prevents byte overflow/underflow
  if (channel >= MAX_CHANNEL) {
    channel = MAX_CHANNEL;
    flag = 1;
  } else if (channel <= MIN_CHANNEL) {
    channel = MIN_CHANNEL;
    flag = 0;
  }

  radio.setChannel(channel);
  hopCount++;
}

void periodicReinit() {
  unsigned long now = millis();
  if (now - lastReinitTime >= REINIT_INTERVAL) {
    Serial.printf("[INFO] Periodic reinit — uptime: %lus, hops: %lu\n",
                  now / 1000, hopCount);

    if (!initRadio()) {
      Serial.println("[WARN] Reinit failed, retrying in 5s...");
      delay(5000);
      initRadio();  // One retry
    }

    lastReinitTime = now;
  }
}

void setup() {
  // Kill BT and WiFi stacks completely
  esp_bt_controller_deinit();
  esp_wifi_stop();
  esp_wifi_deinit();
  esp_wifi_disconnect();

  Serial.begin(115200);
  delay(1000);
  Serial.println("[BOOT] Starting jammer...");

  // Watchdog — resets ESP32 if loop() hangs for WDT_TIMEOUT seconds
  esp_task_wdt_init(WDT_TIMEOUT, true);
  esp_task_wdt_add(NULL);

  // Retry radio init up to 5 times on boot
  int attempts = 0;
  while (!initRadio()) {
    attempts++;
    Serial.printf("[RETRY] Attempt %d failed, retrying...\n", attempts);
    delay(1000);
    if (attempts >= 5) {
      Serial.println("[FATAL] Radio not responding after 5 attempts. Check wiring.");
      // Don't halt — watchdog will reset the board after WDT_TIMEOUT seconds
      while (1) { delay(100); }
    }
  }

  lastReinitTime = millis();
  Serial.println("[BOOT] Jammer running.");
}

void loop() {
  esp_task_wdt_reset();  // Pet the watchdog — proves loop() is alive

  hopChannel();
  periodicReinit();
}
