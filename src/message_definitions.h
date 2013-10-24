#ifndef MESSAGE_DEFINITIONS_H
#define MESSAGE_DEFINITIONS_H

// An example of a message definition, this one only has a parameter to set the value of an led
const uint8_t MsgTypeDebug = 1;
typedef struct __attribute__ ((__packed__)) {
    uint8_t led_on;
} MsgDebug;  

// Setter Messages
const uint8_t MsgTypeStepperPosition = 2;
typedef struct __attribute__ ((__packed__)) {
    int32_t desired_position;
} MsgStepperPosition;  

const uint8_t MsgTypeStepperLimits = 3;
typedef struct __attribute__ ((__packed__)) {
    float acceleration_limit;
    float speed_min;
    float speed_max;
} MsgStepperLimits;

const uint8_t MsgTypeStepperPubFrequency = 4;
typedef struct __attribute__ ((__packed__)) {
    int16_t frequency; // Cannot be greater than 1000
} MsgStepperPubFrequency;

const uint8_t MsgTypeStepperFeedback = 5;
typedef struct __attribute__ ((__packed__)) {
    float position;
    float speed;
    uint32_t timestamp;
} MsgStepperFeedback;

const uint8_t MsgTypeServoPosition = 6;
typedef struct __attribute__ ((__packed__)) {
    float cmd;
} MsgServoPosition;

const uint8_t MsgTypeServoCalibration = 7;
typedef struct __attribute__ ((__packed__)) {
    float range;
    int degrees;
} MsgServoCalibration;

#endif