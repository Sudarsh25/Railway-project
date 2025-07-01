import mraa                                                                     
import time                                                                     
                                                                                
# Initialize GPIO pins                                                          
IN1 = mraa.Gpio(23)  # PA1                                                      
IN2 = mraa.Gpio(24)  # PA2                                                      
IN3 = mraa.Gpio(25)  # PA5                                                      
IN4 = mraa.Gpio(26) # PC21                                                      
                                                                                
# Set GPIO directions to OUT                                                    
IN1.dir(mraa.DIR_OUT)                                                           
IN2.dir(mraa.DIR_OUT)                                                           
IN3.dir(mraa.DIR_OUT)                                                           
IN4.dir(mraa.DIR_OUT)                                                           
                                                                                
# Step sequence for 28BYJ-48 stepper motor (Half-step mode)                     
STEP_SEQUENCE = [                                                               
    [1, 0, 0, 0],                                                               
    [1, 1, 0, 0],                                                               
    [0, 1, 0, 0],                                                               
    [0, 1, 1, 0],                                                               
    [0, 0, 1, 0],                                                               
    [0, 0, 1, 1],                                                               
    [0, 0, 0, 1],                                                               
    [1, 0, 0, 1]                                                                
]                                                                               
                                                                                
# Function to set GPIO outputs                                                  
def set_step(w1, w2, w3, w4):                                                   
    IN1.write(w1)                                                               
    IN2.write(w2)                                                               
    IN3.write(w3)                                                               
    IN4.write(w4)                                                               
                                                                                
# Rotate stepper motor                                                          
def rotate_motor(steps, delay=0.002):                                           
    for _ in range(steps):                                                      
        for step in STEP_SEQUENCE:                                              
            set_step(*step)                                                     
            time.sleep(delay)                                                   
                                                                                
# Rotate motor 512 steps (One full rotation)                                    
rotate_motor(1024)                                                              
                                                                                
# Cleanup GPIO (set all pins to LOW)                                            
set_step(0, 0, 0, 0)                                                            
                                                                                
print("Motor rotation completed.")  
