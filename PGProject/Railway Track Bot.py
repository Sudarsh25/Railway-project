import mraa                                                                     
import serial                                                                   
import time                                                                     
                                                                                
# �✅ GPIO Pins                                                                 
TRIG_PIN = 12                                                                   
ECHO_PIN = 13                                                                   
IR_SENSOR_PIN = 14                                                              
STEP_PINS = [23, 24, 25, 26]  # PA1, PA2, PA5, PC21                             
UART_PORT = "/dev/ttyS3"                                                        
UART_BAUD_RATE = 115200                                                         
                                                                                
# �✅ Stepper Motor Sequence (Half-step mode)                                   
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
                                                                                
# �✅ Default GPS coordinates (for fallback)                                    
DEFAULT_GPS_COORDS = [                                                          
    (10.9323591, 76.9770454), (10.9323482, 76.9773458),                         
    (10.9324562, 76.9772724), (10.9324325, 76.9771098)                          
]                                                                               
                                                                                
# �✅ Initialize GPIO and UART                                                  
def initialize():                                                               
    """Initialize all GPIO pins and UART"""                                     
    global trigPin, echoPin, ir_sensor, motor_pins, ser                         
                                                                                
    # �✅ Ultrasonic Sensor                                                     
    trigPin = mraa.Gpio(TRIG_PIN)                                               
    echoPin = mraa.Gpio(ECHO_PIN)                                               
    trigPin.dir(mraa.DIR_OUT)                                                   
    echoPin.dir(mraa.DIR_IN)                                                    
                                                                                
    # �✅ IR Sensor                                                             
    ir_sensor = mraa.Gpio(IR_SENSOR_PIN)                                        
    ir_sensor.dir(mraa.DIR_IN)                                                  
                                                                                
    # �✅ Stepper Motor                                                         
    motor_pins = [mraa.Gpio(pin) for pin in STEP_PINS]                          
    for pin in motor_pins:                                                      
        pin.dir(mraa.DIR_OUT)                                                   
                                                                                
    # �✅ UART for GPS                                                          
    try:                                                                        
        ser = serial.Serial(UART_PORT, UART_BAUD_RATE, timeout=1)               
        print("�✅ UART Communication Established")                             
    except serial.SerialException as e:                                         
        print("�❌ UART Error:", e)                                             
        exit(1)                                                                 
                                                                                
# �✅ Measure Distance with Ultrasonic Sensor                                   
def measure_distance():                                                         
    trigPin.write(0)                                                            
    time.sleep(0.00001)                                                         
    trigPin.write(1)                                                            
    time.sleep(0.00001)                                                         
    trigPin.write(0)                                                            
                                                                                
    start_time = time.time()                                                    
    timeout = start_time + 0.02  # 20ms timeout                                 
                                                                                
    while echoPin.read() == 0 and time.time() < timeout:                        
        start_time = time.time()                                                
                                                                                
    stop_time = time.time()                                                     
    timeout = stop_time + 0.02                                                  
                                                                                
    while echoPin.read() == 1 and time.time() < timeout:                        
        stop_time = time.time()                                                 
                                                                                
    elapsed_time = stop_time - start_time                                       
    distance = (elapsed_time * 34300) / 2  # in cm                              
    return round(distance, 2)                                                   
                                                                                
# �✅ Read IR Sensor                                                            
def read_ir_sensor():                                                           
    return ir_sensor.read()                                                     
                                                                                
# �✅ Rotate Stepper Motor                                                      
def rotate_motor(steps=512, delay=0.002):                                       
    for _ in range(steps):                                                      
        for step in STEP_SEQUENCE:                                              
            for i in range(4):                                                  
                motor_pins[i].write(step[i])                                    
            time.sleep(delay)                                                   
                                                                                
# �✅ GPS Data                                                                  
def convert_nmea_to_decimal(nmea_coord, direction):                             
    """Converts NMEA coordinates to decimal degrees"""                          
    try:                                                                        
        degrees = int(nmea_coord[:2])                                           
        minutes = float(nmea_coord[2:])                                         
        decimal = degrees + (minutes / 60)                                      
                                                                                
        if direction in ['S', 'W']:                                             
            decimal *= -1                                                       
        return decimal                                                          
    except ValueError:                                                          
        return None                                                             
                                                                                
def get_gps_location(index):                                                    
    """Read GPS data or use fallback coordinates"""                             
    try:                                                                        
        data = ser.readline().decode('ascii', errors='replace').strip()         
                                                                                
        if data.startswith("$GPRMC"):                                           
            parts = data.split(",")                                             
            if len(parts) > 6 and parts[2] == 'A':                              
                lat = convert_nmea_to_decimal(parts[3], parts[4])               
                lon = convert_nmea_to_decimal(parts[5], parts[6])               
                                                                                
                if lat is not None and lon is not None:                         
                    return (lat, lon)                                           
                                                                                
        # Use default GPS coordinates in case of invalid data                   
        return DEFAULT_GPS_COORDS[index % len(DEFAULT_GPS_COORDS)]              
                                                                                
    except Exception as e:                                                      
        print("�❌ GPS Error:", e)                                              
        return DEFAULT_GPS_COORDS[index % len(DEFAULT_GPS_COORDS)]              
                                                                                
# �✅ Main Loop                                                                 
def main():                                                                     
    initialize()                                                                
    gps_index = 0                                                               
                                                                                
    print("�🚆 Starting IoT Railway Track Crack Detection Robot...")            
                                                                                
    try:                                                                        
        while True:                                                             
            # �✅ Measure distance with ultrasonic sensor                       
            distance = measure_distance()                                       
            print("�📏 Distance:", distance, "cm")                              
            time.sleep(0.5)                                                     
                                                                                
            # �✅ Read IR sensor                                                
            ir_state = read_ir_sensor()                                         
            if ir_state == 1:                                                   
                print("�✅ Track is Clear")                                     
            else:                                                               
                print("�⚠�️ Crack Detected on Track! �⚠�️")                       
                                                                                
            time.sleep(0.5)                                                     
                                                                                
            # �✅ Rotate stepper motor (one full rotation)                      
            print("�🔧 Rotating Stepper Motor...")                              
            rotate_motor(512)                                                   
                                                                                
            # �✅ GPS Location                                                  
            gps_location = get_gps_location(gps_index)                          
            print("�📍 GPS: Latitude =", gps_location[0], "Longitude =", gps_l )
            gps_index += 1                                                      
                                                                                
            # �✅ Delay before next iteration                                   
            time.sleep(1)                                                       
                                                                                
    except KeyboardInterrupt:                                                   
        print("\n�🚦 Stopping System...")                                       
        # Clean up motor pins                                                   
        for pin in motor_pins:                                                  
            pin.write(0)                                                        
        ser.close()                                                             
                                                                                
# �✅ Run the Program                                                           
if __name__ == "__main__":                                                      
    main()                                                                      
                                 
