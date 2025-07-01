import mraa
import time
import serial

# �✅ Define GPIO Pin for IR Sensor Output (UPDATE this based on available GPIOs
IR_SENSOR_PIN = 14  # Change this based on `ls /sys/class/gpio`
UART_PORT = "/dev/ttyS3"  # Serial Port for UART communication
UART_BAUD_RATE = 115200

# �✅ Initialize IR Sensor GPIO
try:
    ir_sensor = mraa.Gpio(IR_SENSOR_PIN)
    ir_sensor.dir(mraa.DIR_IN)  # Set as input
    print("�✅ IR Sensor Initialized on GPIO", IR_SENSOR_PIN)
except ValueError as e:
    print("�❌ GPIO Initialization Error:", e)
    exit(1)

# �✅ Initialize UART Communication
try:
    ser = serial.Serial(UART_PORT, UART_BAUD_RATE, timeout=1)
    print("�✅ UART Communication Established")
except serial.SerialException as e:
root@rugged-board-a5d2x-sd1:~/gps# cay Ir_sensor.py                             
-sh: cay: command not found                                                     
root@rugged-board-a5d2x-sd1:~/gps# cat Ir_sensor.py                             
import mraa                                                                     
import time                                                                     
import serial                                                                   
                                                                                
# �✅ Define GPIO Pin for IR Sensor Output (UPDATE this based on available GPIO)
IR_SENSOR_PIN = 14  # Change this based on `ls /sys/class/gpio`                 
UART_PORT = "/dev/ttyS3"  # Serial Port for UART communication                  
UART_BAUD_RATE = 115200                                                         
                                                                                
# �✅ Initialize IR Sensor GPIO                                                 
try:                                                                            
    ir_sensor = mraa.Gpio(IR_SENSOR_PIN)                                        
    ir_sensor.dir(mraa.DIR_IN)  # Set as input                                  
    print("�✅ IR Sensor Initialized on GPIO", IR_SENSOR_PIN)                   
except ValueError as e:                                                         
    print("�❌ GPIO Initialization Error:", e)                                  
    exit(1)                                                                     
                                                                                
# �✅ Initialize UART Communication                                             
try:                                                                            
    ser = serial.Serial(UART_PORT, UART_BAUD_RATE, timeout=1)                   
    print("�✅ UART Communication Established")                                 
except serial.SerialException as e:                                             
    print("�❌ UART Error:", e)                                                 
    exit(1)                                                                     
                                                                                
def uart_transmit(message):                                                     
    """Send data over UART."""                                                  
    ser.write(message.encode())                                                 
                                                                                
# �✅ Send System Start Message                                                 
uart_transmit("�🚆 Railway Crack Detection System Initialized\r\n")             
print("�🚆 Railway Crack Detection System Initialized")                         
                                                                                
try:                                                                            
    while True:                                                                 
        sensor_state = ir_sensor.read()  # Read IR sensor value                 
                                                                                
        if sensor_state == 1:                                                   
            # �✅ No crack detected: Send message over UART                     
            uart_transmit("�✅ Track is Clear\r\n")                             
            print("�✅ Track is Clear")                                         
        else:                                                                   
            # �⚠�️ Crack detected: Send alert over UART                          
            uart_transmit("�⚠�️ Crack Detected on Track! �⚠�️\r\n")               
            print("�⚠�️ Crack Detected on Track! �⚠�️")                           
                                                                                
        time.sleep(0.5)  # Delay to avoid spamming UART                         
except KeyboardInterrupt:                                                       
    print("�🚆 Stopping Crack Detection System...")                             
    uart_transmit("�🚆 Crack Detection System Stopped\r\n")                     
    ser.close()                                                                 
                
