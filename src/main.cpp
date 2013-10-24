#include "mbed.h"
#include "msg_interface.h"
#include "message_definitions.h"
#include "Stepper.h"
#include "Servo.h"

// serial communications and message passing interface
Serial pc(USBTX, USBRX); // tx, rx
MessageIface msgIface( &pc );

// Stepper 
Stepper stepper( p23, p24 ); // dir, step

// Servo
Servo plucker(p25);

// display LEDs
DigitalOut stepper_led(LED4);
DigitalOut debug_led(LED3);
DigitalOut pkt_rx_led(LED2);
DigitalOut init_led(LED1);

Timer timer; 
Timer feedback_timer;

int main() {

    // Start timers
    timer.start();
    feedback_timer.start();

    // Set baudrate
    pc.baud( 115200 );

    // Initial values for stepper motor
    stepper.start();

    // Set up initial values for plucker
    // DONT TRUST THIS
    //plucker.calibrate( 0.00085, 180 );
    // Starting position
    //plucker.write( 0.2 ); 

    uint16_t feedback_frequency = 0;
    
    debug_led = 0;  // set by value in recieves messages
    pkt_rx_led = 0; // toggle every time any packet is recieved
    init_led = 1;   // on when program starts
    
    while(1) {
    
        // Update Stepper Control
        stepper.update( &stepper_led );
        
        // Check if we should send stepper feedback
        if ( feedback_frequency > 0 ) {
            if ( float(feedback_timer.read_us()) > 1000000.0f/float(feedback_frequency) ) {
                feedback_timer.reset();
                pkt_rx_led = !pkt_rx_led;      // toggle LED every time we get any packet
                MsgStepperFeedback msg_fdbk;
                msg_fdbk.position = stepper.getPosition();
                msg_fdbk.speed = stepper.getSpeed();
                msg_fdbk.timestamp = timer.read_us();
                msgIface.sendPacket( MsgTypeStepperFeedback, (uint8_t*)&msg_fdbk, sizeof(MsgStepperFeedback) ); 
                
            }
        }   
        
        // Update input queue
        msgIface.getBytes();
        
        // Check if there is a valid packet to use
        uint8_t *rx_data;
        uint8_t rx_len;
        if ( msgIface.peekPacket( &rx_data, &rx_len ) ) {
            uint8_t msg_type = rx_data[0]; // first byte is type
            uint8_t* msg_data = rx_data+1; // rest of the bytes are data
            
            pkt_rx_led = !pkt_rx_led;      // toggle LED every time we get any packet
               
            // Handle Various Message Types     
            switch ( msg_type ) {
            case MsgTypeDebug: {                
                // copy out the data you need
                MsgDebug* msg_debug = (MsgDebug*)msg_data;
                debug_led = msg_debug->led_on;      // use '->' because msg_debug is a pointer to a struct
                // here I make a new message that is a copy of the one I got, and send it back
                MsgDebug return_msg_debug;
                return_msg_debug.led_on = debug_led;  // use '.' because msg_debug_copy is a struct
                msgIface.sendPacket( MsgTypeDebug, (uint8_t*)&return_msg_debug, sizeof(MsgDebug) );                
                break;              
                }  
            case MsgTypeStepperPosition: {
                MsgStepperPosition* msg_position = (MsgStepperPosition*)msg_data;               
                stepper.setPosition( msg_position->desired_position );
                break;
                }
            case MsgTypeStepperLimits: { 
                MsgStepperLimits* msg_limits = (MsgStepperLimits*)msg_data;
                stepper.setAccelerationLimit( msg_limits->acceleration_limit );
                stepper.setSpeedLimits( msg_limits->speed_min, msg_limits->speed_max );
                break;
                }
            case MsgTypeStepperPubFrequency: {
                MsgStepperPubFrequency* msg_freq = (MsgStepperPubFrequency*)msg_data;
                feedback_frequency = msg_freq->frequency;
                timer.reset();
                feedback_timer.reset();
                break;
                }
            case MsgTypeServoPosition: {
                MsgServoPosition* msg_servo = (MsgServoPosition*)msg_data;
                plucker.write( msg_servo->cmd );
                break;
                }
            case MsgTypeServoCalibration: {
                MsgServoCalibration* msg_calib = (MsgServoCalibration*)msg_data;
                plucker.calibrate( msg_calib->range, msg_calib->degrees );
                break;
                }                             
            }
            // done with this message, remove from the queue
            msgIface.dropPacket();
        }
        
        // Push bytes out of output queue
        msgIface.sendNow();
    }
}



    
