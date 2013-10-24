/*
    Stepper Implmentation
*/

#include "Stepper.h"
#include <stdlib.h>

Stepper::Stepper( PinName dir, PinName step ) {
    m_dir = new DigitalOut( dir );
    m_step = new DigitalOut( step );
    m_timer = new Timer(); 
    m_control_timer = new Timer();
    m_timer->start();
    m_control_timer->start();
    m_en = 0;
    m_cnt = 0;
    //m_desired_cnt = 0;
    m_speed = 0;
    m_acceleration_limit = 0;
    m_speed_max = 0;
    m_speed_min = 0;
    m_desired_position = 0;
    m_nxt_update = 1;
    m_update_cnt = 0;
    this->setMode( STEP_FULL ); 
}

Stepper::~Stepper( void ) {
    delete m_dir;
    delete m_step;
    delete m_timer;
}

void Stepper::start( void ) {
    m_en = 1;
}

void Stepper::stop( void ) {
    m_en = 0;
}

int Stepper::getCount( void ) {
    return m_cnt;
}

void Stepper::setMode( StepperModes mode ) {
    // Set m_mode to actual divisor 
    m_mode = ( 1 << mode );
}

int Stepper::getModeDivisor( void ) {
    return m_mode;
}

float Stepper::getAccelerationLimit( void ) {
    return m_acceleration_limit;
}

void Stepper::setAccelerationLimit( float acceleration ) {
    m_acceleration_limit = acceleration;
}

float Stepper::getSpeed( void ) {
    return m_speed;
}

void Stepper::setSpeedLimits( float speed_min, float speed_max ) {
    m_speed_min = speed_min;
    m_speed_max = speed_max;
}

int Stepper::getPosition( void ) {
    return m_cnt;
}

void Stepper::setPosition( int desired_position ) {
    m_desired_position = desired_position;
}

void Stepper::update( DigitalOut *dbg_led ) {

    float error;
    float error_dir; 

    float dt = m_control_timer->read_us()/1000000.0f;
    if ( dt >= 0.001 ) {
        m_control_timer->reset();               
        
        error = float(m_desired_position - m_cnt); 
        error_dir = error > 0.0f ? 1.0f : -1.0f;

        // Calculate time to deccelerate from current speed
        float t = abs(m_speed)/m_acceleration_limit;
        // Compute distance required to deccelerate
        float dec_dist = 0.5f*m_acceleration_limit*(t*t);
        
        // If error is <= dec_dist then decellerate, otherwise accelerate
        if ( abs(error) <= dec_dist ) {
            // Handle the case when you are traveling away from your desired position
            if ( m_speed > 0.0f && error_dir == -1.0f || m_speed < 0.0f && error_dir == 1.0f ) {
                m_speed += error_dir*m_acceleration_limit*dt;
            } else {
                m_speed -= error_dir*m_acceleration_limit*dt;
            }
        } else {
            m_speed += error_dir*m_acceleration_limit*dt;
        }
        
        if ( abs(m_speed) > m_speed_max )
            m_speed = error_dir*m_speed_max;
        if ( abs(m_speed) < m_speed_min ) 
            m_speed = error_dir*m_speed_min;
    }   

    // If the motor has reached its goal then don't update
    if ( abs(float(m_desired_position - m_cnt)) <= 1.0f ) {
        m_speed = 0.0f;
        m_timer->reset();
        m_step->write( 0 );
        return;
    }
    if ( abs(m_speed) < 1.0f ) {
        m_timer->reset();
        m_step->write( 0 );
        return;
    }
    if ( m_timer->read_us() >= 500000/abs(int(m_speed)) ) {
        
        // Reset Timer
        m_timer->reset();
        
        // If step is high then set low and return
        if ( m_step->read() ) {
            m_step->write( 0 );
            return;
        }   
        // Debugging!
        dbg_led->write( !dbg_led->read() );
            
        // Set direction based on sign of speed
        if ( m_speed > 0.0f ) {
            m_cnt += 1;
            m_dir->write(1);
        } else {
            m_cnt -= 1;
            m_dir->write(0);
        }
        
        // Step Once
        m_step->write( 1 );
    }
}