#include <Wire.h>
#include <M5Dial.h>
#include <bme68xLibrary.h>
#include <bsec2.h>

#define SERIAL_SPEED (115200)

#define PORTA_SCL_PIN (15)
#define PORTA_SDA_PIN (13)
#define PORTB_SCL_PIN (1)
#define PORTB_SDA_PIN (2)

#define BME688_ADDR (0x77)

Bsec2 envSensor;

bsecSensor sensorList[] = {
  BSEC_OUTPUT_IAQ,
  BSEC_OUTPUT_CO2_EQUIVALENT,
  BSEC_OUTPUT_BREATH_VOC_EQUIVALENT,
  BSEC_OUTPUT_RAW_TEMPERATURE,
  BSEC_OUTPUT_RAW_PRESSURE,
  BSEC_OUTPUT_RAW_HUMIDITY,
  BSEC_OUTPUT_RAW_GAS,
  BSEC_OUTPUT_STABILIZATION_STATUS,
  BSEC_OUTPUT_RUN_IN_STATUS};

void checkBsecStatus(Bsec2 bsec)
{
  if (bsec.status < BSEC_OK)
  {
    USBSerial.println("BSEC error code:" + String(bsec.status));
  }
  else if (bsec.status > BSEC_OK)
  {
    USBSerial.println("BSEC warning code:" + String(bsec.status));
  }

  if (bsec.sensor.status < BME68X_OK)
  {
    USBSerial.println("BME68X error code:" + String(bsec.sensor.status));
  }
  else if (bsec.sensor.status > BME68X_OK)
  {
    USBSerial.println("BME68X warning code:" + String(bsec.sensor.status));
  }
}

void newDataCallback(const bme68xData data, const bsecOutputs outputs, Bsec2 bsec)
{
  if (!outputs.nOutputs)
  {
    return;
  }

  USBSerial.println("BSEC outputs:\n\ttimestamp = " + String((int)(outputs.output[0].time_stamp / INT64_C(1000000))));
  for (uint8_t i = 0; i < outputs.nOutputs; i++)
  {
    const bsecData output = outputs.output[i];
    switch (output.sensor_id)
    {
    case BSEC_OUTPUT_IAQ:
      USBSerial.println("\tiaq = " + String(output.signal));
      USBSerial.println("\t\tiaq accuracy = " + String((int)output.accuracy));
      break;
    case BSEC_OUTPUT_CO2_EQUIVALENT:
      USBSerial.println("\tco2 = " + String(output.signal) + " ppm");
      USBSerial.println("\t\tco2 accuracy = " + String((int)output.accuracy));
      break;
    case BSEC_OUTPUT_BREATH_VOC_EQUIVALENT:
      USBSerial.println("\tbreath voc = " + String(output.signal) + " ppm");
      USBSerial.println("\t\tbreath voc accuracy = " + String((int)output.accuracy));
      break;
    case BSEC_OUTPUT_RAW_TEMPERATURE:
      USBSerial.println("\ttemperature = " + String(output.signal) + " degC");
      break;
    case BSEC_OUTPUT_RAW_PRESSURE:
      USBSerial.println("\tpressure = " + String(output.signal / 100.0) + " hPa");
      break;
    case BSEC_OUTPUT_RAW_HUMIDITY:
      USBSerial.println("\thumidity = " + String(output.signal) + " %RH");
      break;
    case BSEC_OUTPUT_RAW_GAS:
      USBSerial.println("\tgas resistance = " + String(output.signal));
      break;
    case BSEC_OUTPUT_STABILIZATION_STATUS:
      USBSerial.println("\tstabilization status = " + String(output.signal));
      break;
    case BSEC_OUTPUT_RUN_IN_STATUS:
      USBSerial.println("\trun in status = " + String(output.signal));
      break;
    default:
      break;
    }
  }
}

void setup()
{
  auto cfg = M5.config();
  M5Dial.begin(false, false);
  USBSerial.begin(SERIAL_SPEED);
  Wire.begin(PORTA_SDA_PIN, PORTA_SCL_PIN);

  if (!envSensor.begin(BME688_ADDR, Wire))
  {
    checkBsecStatus(envSensor);
  }
  if (!envSensor.updateSubscription(sensorList, ARRAY_LEN(sensorList), BSEC_SAMPLE_RATE_LP))
  {
    checkBsecStatus(envSensor);
  }

  envSensor.attachCallback(newDataCallback);

  USBSerial.println("BSEC library version " +
            String(envSensor.version.major) + "." + String(envSensor.version.minor) + "." + String(envSensor.version.major_bugfix) + "." + String(envSensor.version.minor_bugfix));
}

void loop()
{
  if (!envSensor.run())
  {
    checkBsecStatus(envSensor);
  }
}
