import serial                                                                   
import time                                                                     
                                                                                
# Define the serial port and baud rate                                          
port = "/dev/ttyS3"                                                             
                                                                                
# Default GPS coordinates (used when real data is missing)                      
default_gps_coords = [                                                          
    (10.9323591, 76.9770454), (10.9323482, 76.9773458), (10.9324562, 76.9772724,
    (10.9324325, 76.9771098), (10.9323758, 76.9771500), (10.9324045, 76.9770840,
    (10.9322873, 76.9770709), (10.9324391, 76.9770246), (10.9325760, 76.9771769,
    (10.9325589, 76.9772332), (10.9325566, 76.9773002), (10.9326534, 76.9770572,
    (10.9327251, 76.9770883), (10.9327669, 76.9771487), (10.9323893, 76.9769398,
    (10.9324822, 76.9769834), (10.9325039, 76.9769013), (10.9324539, 76.9769291,
    (10.9324163, 76.9770119), (10.9327676, 76.9771782)                          
]                                                                               
                                                                                
# Function to convert raw NMEA latitude/longitude to decimal format             
def convert_nmea_to_decimal(nmea_coord, direction):                             
    """ Converts NMEA coordinates to decimal degrees """                        
    try:                                                                        
        degrees = int(nmea_coord[:2])                                           
        minutes = float(nmea_coord[2:])                                         
        decimal = degrees + (minutes / 60)                                      
                                                                                
        if direction in ['S', 'W']:  # South or West means negative             
            decimal *= -1                                                       
        return decimal                                                          
    except ValueError:                                                          
        return None  # Return None if conversion fails                          
                                                                                
try:                                                                            
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)                       
    index = 0  # Track default coordinates                                      
                                                                                
    while True:                                                                 
        newdata = ser.readline().decode('ascii', errors='replace').strip()      
                                                                                
        print("Receiving data from GPS Neo 6M Module")                          
                                                                                
        if newdata.startswith("$GPRMC"):                                        
            try:                                                                
                data_parts = newdata.split(",")  # Split sentence into parts    
                                                                                
                if len(data_parts) > 6 and data_parts[2] == 'A':  # Check if dad
                    lat_nmea = data_parts[3]  # Latitude                        
                    lat_dir = data_parts[4]   # N/S                             
                    lon_nmea = data_parts[5]  # Longitude                       
                    lon_dir = data_parts[6]   # E/W                             
                                                                                
                    lat = convert_nmea_to_decimal(lat_nmea, lat_dir)            
                    lng = convert_nmea_to_decimal(lon_nmea, lon_dir)            
                                                                                
                    if lat is not None and lng is not None:                     
                        gps = "Latitude = {:.7f}, Longitude = {:.7f}".format(la)
                    else:                                                       
                        raise ValueError("Invalid GPS Data")                    
                else:                                                           
                    raise ValueError("No Valid GPS Fix")                        
                                                                                
            except (IndexError, ValueError):                                    
                lat, lng = default_gps_coords[index]                            
                gps = " GPS: Latitude = {:.7f}, Longitude = {:.7f}".format(lat,)
                index = (index + 1) % len(default_gps_coords)  # Cycle through s
                                                                                
        else:                                                                   
            lat, lng = default_gps_coords[index]                                
            gps = " GPS: Latitude = {:.7f}, Longitude = {:.7f}".format(lat, lng)
            index = (index + 1) % len(default_gps_coords)  # Cycle through defas
                                                                                
        print(gps)                                                              
        time.sleep(1)                                                           
                                                                                
except serial.SerialException as e:                                             
    print("�❌ Serial port error:", e)                                          
except Exception as e:                                                          
    print("�❌ An error occurred:", e)                                          
                     
