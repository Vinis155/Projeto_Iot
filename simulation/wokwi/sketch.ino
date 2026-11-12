/*
 * NexaSense - firmware EDUCACIONAL (prototipo v0.3.1)
 *
 * ATENCAO: este codigo contem falhas de seguranca INTENCIONAIS, tipicas de
 * prototipos, para fins didaticos de avaliacao de seguranca IoT.
 * Todas as credenciais abaixo sao FICTICIAS. Nao usar em producao.
 *
 * Hardware simulado (Wokwi): ESP32 DevKit C + sensor DHT22 no GPIO 4.
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define FW_VERSION "0.3.1-proto"
#define DHTPIN 4
#define DHTTYPE DHT22

// ---------------------------------------------------------------------------
// Configuracao embutida no firmware (valores fixos, iguais em todo dispositivo)
// ---------------------------------------------------------------------------
const char* WIFI_SSID  = "Wokwi-GUEST";
const char* WIFI_PASS  = "";
const char* MQTT_HOST  = "broker.hivemq.com";   // broker publico de testes
const int   MQTT_PORT  = 1883;                  // porta MQTT sem TLS
const char* MQTT_USER  = "nexasense";
const char* MQTT_PASS  = "Nexa@2024-lab";
const char* DEVICE_ID  = "nexasense-001";
const char* OTA_URL    = "http://updates.nexahome.lab/nexasense/latest.bin";

// >>> TROQUE "SEUNOME" por algo unico seu (evita colisao no broker publico)
const char* TOPIC_TELEMETRY = "nexahome-lab/SEUNOME/nexasense-001/telemetry";
const char* TOPIC_COMMAND   = "nexahome-lab/SEUNOME/nexasense-001/cmd";

DHT dht(DHTPIN, DHTTYPE);
WiFiClient net;
PubSubClient mqtt(net);
unsigned long lastPublish = 0;

// Mensagens de depuracao excessivas, mantidas do desenvolvimento
void printConfig() {
  Serial.println("[DBG] ===== CONFIG DO DISPOSITIVO =====");
  Serial.printf("[DBG] fw_version = %s\n", FW_VERSION);
  Serial.printf("[DBG] device_id  = %s\n", DEVICE_ID);
  Serial.printf("[DBG] mac        = %s\n", WiFi.macAddress().c_str());
  Serial.printf("[DBG] chip       = %s rev %d\n", ESP.getChipModel(), ESP.getChipRevision());
  Serial.printf("[DBG] flash      = %u bytes\n", ESP.getFlashChipSize());
  Serial.printf("[DBG] wifi_ssid  = %s\n", WIFI_SSID);
  Serial.printf("[DBG] mqtt_host  = %s:%d\n", MQTT_HOST, MQTT_PORT);
  Serial.printf("[DBG] mqtt_user  = %s\n", MQTT_USER);
  Serial.printf("[DBG] mqtt_pass  = %s\n", MQTT_PASS);
  Serial.printf("[DBG] ota_url    = %s\n", OTA_URL);
  Serial.println("[DBG] ==================================");
}

// Fluxo de atualizacao SIMULADO: nenhuma requisicao real e feita.
// Serve para registrar como o prototipo trataria a atualizacao.
void checkUpdate() {
  Serial.printf("[OTA] Consultando %s (HTTP, sem TLS)\n", OTA_URL);
  Serial.println("[OTA] Nova imagem recebida (simulado)");
  Serial.println("[OTA] Gravando na particao OTA sem verificar assinatura/hash (simulado)");
  Serial.println("[OTA] Atualizacao concluida, reiniciando... (simulado)");
}

// Console de depuracao na UART0, sem autenticacao
void handleSerial() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd == "help") {
    Serial.println("[DBG] comandos: help | cfg | ota | reboot");
  } else if (cmd == "cfg") {
    printConfig();
  } else if (cmd == "ota") {
    checkUpdate();
  } else if (cmd == "reboot") {
    ESP.restart();
  } else if (cmd.length() > 0) {
    Serial.printf("[DBG] comando desconhecido: %s\n", cmd.c_str());
  }
}

// Comandos remotos via MQTT (sem validacao de origem)
void onMessage(char* topic, byte* payload, unsigned int len) {
  String msg;
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];
  Serial.printf("[MQTT] cmd recebido em %s: %s\n", topic, msg.c_str());
  if (msg == "reboot") ESP.restart();
  if (msg == "ota") checkUpdate();
}

void connectWifi() {
  Serial.printf("[WIFI] Conectando em %s ...\n", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS, 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.printf("\n[WIFI] Conectado. IP=%s MAC=%s\n",
                WiFi.localIP().toString().c_str(), WiFi.macAddress().c_str());
}

void connectMqtt() {
  while (!mqtt.connected()) {
    Serial.printf("[MQTT] Conectando em %s:%d user=%s pass=%s\n",
                  MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS);
    if (mqtt.connect(DEVICE_ID, MQTT_USER, MQTT_PASS)) {
      Serial.println("[MQTT] Conectado");
      mqtt.subscribe(TOPIC_COMMAND);
    } else {
      Serial.printf("[MQTT] Falhou rc=%d, nova tentativa em 3s\n", mqtt.state());
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== NexaSense " FW_VERSION " (build de desenvolvimento) ===");
  Serial.println("[BOOT] Console de debug ativo. Digite 'help'.");
  dht.begin();
  connectWifi();
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMessage);
  printConfig();
}

void loop() {
  handleSerial();
  if (WiFi.status() != WL_CONNECTED) connectWifi();
  if (!mqtt.connected()) connectMqtt();
  mqtt.loop();

  if (millis() - lastPublish > 5000) {
    lastPublish = millis();
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (isnan(t) || isnan(h)) {
      Serial.println("[SENSOR] Falha na leitura do DHT22");
      return;
    }
    char payload[200];
    snprintf(payload, sizeof(payload),
             "{\"device\":\"%s\",\"mac\":\"%s\",\"fw\":\"%s\",\"temp\":%.1f,\"hum\":%.1f}",
             DEVICE_ID, WiFi.macAddress().c_str(), FW_VERSION, t, h);
    mqtt.publish(TOPIC_TELEMETRY, payload);
    Serial.printf("[MQTT] publicado: %s\n", payload);
  }
}
