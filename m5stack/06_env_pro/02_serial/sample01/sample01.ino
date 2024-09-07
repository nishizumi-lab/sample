#include <bsec2.h>

void checkBsecStatus(Bsec2 bsec);
void newDataCallback(const bme68xData data, const bsecOutputs outputs,  Bsec2 bsec);

/* Create an object of the class Bsec2 */
Bsec2 envSensor;

/* Entry point for the example */
void setup(void) {
    /* Desired subscription list of BSEC2 outputs */
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

    /* Initialize the communication interfaces */
    Serial.begin(115200);
    Wire.begin(21, 22);

    /* Valid for boards with USB-COM. Wait until the port is open */
    while (!Serial) delay(10);

    /* Initialize the library and interfaces */
    if (!envSensor.begin(BME68X_I2C_ADDR_HIGH, Wire)) {
        checkBsecStatus(envSensor);
    }

    /* Subsribe to the desired BSEC2 outputs */
    if (!envSensor.updateSubscription(sensorList, ARRAY_LEN(sensorList),
                                      BSEC_SAMPLE_RATE_LP)) {
        checkBsecStatus(envSensor);
    }

    /* Whenever new data is available call the newDataCallback function */
    envSensor.attachCallback(newDataCallback);

    Serial.println("BSEC library version " + String(envSensor.version.major) +
                   "." + String(envSensor.version.minor) + "." +
                   String(envSensor.version.major_bugfix) + "." +
                   String(envSensor.version.minor_bugfix));
}

/* Function that is looped forever */
void loop(void) {
    if (!envSensor.run()) {
        checkBsecStatus(envSensor);
    }
}

void newDataCallback(const bme68xData data, const bsecOutputs outputs,  Bsec2 bsec) {
    if (!outputs.nOutputs) {
        return;
    }

    for (uint8_t i = 0; i < outputs.nOutputs; i++) {
        const bsecData output = outputs.output[i];
        switch (output.sensor_id) {
            case BSEC_OUTPUT_IAQ:
                Serial.print("{\"iaq\":" + String(output.signal) + ",");
                Serial.print("\"iaq accuracy\":" + String((int)output.accuracy) + ",");
                break;
            case BSEC_OUTPUT_CO2_EQUIVALENT:
              // ppm
                Serial.print("\"co2\":" + String(output.signal) + ",");
                Serial.print("\"co2 accuracy\":" + String((int)output.accuracy) + ",");
                break;
            case BSEC_OUTPUT_BREATH_VOC_EQUIVALENT:
                // ppm
                Serial.print("\"breath voc\":" + String(output.signal) + ",");
                Serial.print("\"breath voc accuracy\":" + String((int)output.accuracy) + ",");
                break;
            case BSEC_OUTPUT_RAW_TEMPERATURE:
                // degC
                Serial.print("\"temperature\":" + String(output.signal) + ",");
                break;
            case BSEC_OUTPUT_RAW_PRESSURE:
                // hPa
                Serial.print("\"pressure\":" + String(output.signal) + ",");
                break;
            case BSEC_OUTPUT_RAW_HUMIDITY:
                // %RH
                Serial.print("\"humidity\":" + String(output.signal) + ",");
                break;
            case BSEC_OUTPUT_RAW_GAS:
                Serial.print("\"gas resistance\":" + String(output.signal) + ",");
                break;
            case BSEC_OUTPUT_STABILIZATION_STATUS:
                Serial.print("\"stabilization status\":" + String(output.signal) + ",");
                break;
            case BSEC_OUTPUT_RUN_IN_STATUS:
                Serial.print("\"run in status\":" + String(output.signal));
                break;
            default:
                break;
        }

    }
    Serial.println("}");
}

void checkBsecStatus(Bsec2 bsec) {
    if (bsec.status < BSEC_OK) {
        Serial.println("BSEC error code : " + String(bsec.status));

    } else if (bsec.status > BSEC_OK) {
        Serial.println("BSEC warning code : " + String(bsec.status));
    }

    if (bsec.sensor.status < BME68X_OK) {
        Serial.println("BME68X error code : " + String(bsec.sensor.status));
    } else if (bsec.sensor.status > BME68X_OK) {
        Serial.println("BME68X warning code : " + String(bsec.sensor.status));
    }
}



