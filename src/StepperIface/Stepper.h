/*
    Stepper Interfacing Code using DRV8824/DRV8825
    Provides a speed setter/getter interface, keeps track of the current stepper counts. 
*/
#include "mbed.h"

// Modes
enum StepperModes { STEP_FULL, STEP_HALF, STEP_4TH, STEP_8TH, STEP_16TH, STEP_32ND };

class Stepper { 
public:
    Stepper( PinName dir, PinName step );
    ~Stepper();
    
    void start( void );
    void stop( void );
    
    int getCount( void );
    
    int getModeDivisor( void );
    void setMode( StepperModes mode );
    
    float getAccelerationLimit( void );
    void setAccelerationLimit( float acceleration );
    
    float getSpeed( void );
    void setSpeedLimits( float speed_min, float speed_max );
    
    int getPosition( void );
    void setPosition( int desired_position );
    
    void update( DigitalOut *dbg_led );
    
private:
    // Enable/Disable
    bool m_en; 

    // State variables
    float m_speed; 
    int m_cnt;
    // Step Mode 
    uint8_t m_mode;
    // Speed and acceleration limits
    float m_acceleration_limit;
    float m_speed_min;
    float m_speed_max;
    
    // Desired Position
    int m_desired_position;
    
    int m_nxt_update;
    int m_update_cnt;
    
    // Timer and pins 
    Timer* m_timer;
    Timer* m_control_timer;
    DigitalOut* m_dir;
    DigitalOut* m_step;
};