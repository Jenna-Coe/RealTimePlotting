import time
import os
from collections import deque
import matplotlib.pyplot as plt
data_file_env = "ENVDataAPR10.txt"
data_file_prs = "PRSDataAPR10.txt"
poll_interval_s = 0.5   #seconds between check
max_points = 400     #points shown


current_reading_env = ""
current_reading_prs = ""
timestamp_env = ""
timestamp_prs = ""
last_timestamp_env = None
last_timestamp_prs = None

first_timestamp_env = None
first_timestamp_prs = None


def read_n_to_last_line(filename, n=1):
    """Returns the nth before last line of a file (n=1 gives last line)"""
    num_newlines = 0
    with open(filename, 'rb') as f:
        #for line in f:
            #if line.strip():
                #o.write(line)
        try:
            f.seek(-2, os.SEEK_END)    
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line

def give_me_value(last_line, key):
    parts = [p.strip() for p in last_line.strip().split("|")]

    for part in parts:
        if ":" not in part:
            continue
            
        key_from_line,val = part.split(":",1)
        key_from_line = key_from_line.strip().upper()
        val = val.strip()
    
        if key_from_line == key.upper():
            try:
                return float(val)
            except ValueError:
                return None
    return None     
    

humidity = []
temperature = []
dewpoint = []
pressure = []
time_env = []
time_prs = []

plt.ion()

fig, axs = plt.subplots(4, 1, figsize=(8, 10))

line_hum, = axs[0].plot([], [])
line_temp, = axs[1].plot([], [])
line_dew, = axs[2].plot([], [])
line_prs, = axs[3].plot([], [])

axs[0].set_title("Relative Humidity")
axs[1].set_title("Temperature")
axs[2].set_title("Dew Point")
axs[3].set_title("Pressure")

axs[0].set_ylabel("Humidity (%)")
axs[1].set_ylabel("Temperature (°C)")
axs[2].set_ylabel("Dew Point (°C)")
axs[3].set_ylabel("Pressure (psi)")

axs[3].set_xlabel("Time (milliseconds)")

plt.tight_layout()

while True:
    current_reading_env = read_n_to_last_line(data_file_env)
    current_reading_prs = read_n_to_last_line(data_file_prs)

    timestamp_env_str = current_reading_env.split("|")[0].strip()
    #timestamp_env = float(timestamp_env_str.split(":")[1])

    print(f"timestamp_env_str = {timestamp_env_str} (line 96)")
    #h, m, s = timestamp_env_str.split(":")
    #timestamp_env = int(h)*3600 + int(m)*60 + int(s)

    # environment
    if timestamp_env_str == last_timestamp_env:
        print("the line is the same")
    else:
        # print("env raw:",current_reading_env)
        hum = give_me_value(current_reading_env, "HUM")
        temp = give_me_value(current_reading_env, "Air TMP")
        dew = give_me_value(current_reading_env, "DEW")

        print(f'HUM: {hum}')
        print(f'TEMP: {temp}')
        print(f'DEW: {dew}')

        if hum is not None and temp is not None and dew is not None:
            print(f'HUM: {hum}')
            print(f'TEMP: {temp}')
            print(f'DEW: {dew}')

            humidity.append(float(hum))
            temperature.append(float(temp))
            dewpoint.append(float(dew))

            last_timestamp_env = timestamp_env_str

            #if first_timestamp_env is None:
            #    first_timestamp_env = timestamp_env

            #time_env.append((timestamp_env - first_timestamp_env)/60)
            time_env.append(float(timestamp_env_str))

        #last_timestamp_env = timestamp_env


    timestamp_prs_str = current_reading_prs.split("|")[0].strip()
    
    print(f"timestamp_prs_str = {timestamp_prs_str}")
    #h, m, s = timestamp_prs_str.split(":")
    #timestamp_prs = int(h)*3600 + int(m)*60 + int(s)


    # pressure
    if timestamp_prs_str == last_timestamp_prs:
        print("the line is the same")
    else:
        prs_value = give_me_value(current_reading_prs, "PRS")
        print(f'PRS: {prs_value}')
        

        if prs_value is not None:
            pressure.append(float(prs_value))
            
            #if first_timestamp_prs is None:
                #first_timestamp_prs = timestamp_prs
            
            #time_prs.append((timestamp_prs - first_timestamp_prs)/60)
            time_prs.append(float(timestamp_prs_str))

            last_timestamp_prs = timestamp_prs_str


        #last_timestamp_prs = timestamp_prs

    x_env = time_env
    x_prs = time_prs
    #x_env = range(len(humidity))
    #x_prs = range(len(pressure))

    print(f"(x_env, humidity): ({x_env}, {humidity})")
    print(f"(x_prs, pressure): ({x_prs}, {pressure})")
    print(f"(x_env, dew): ({x_env}, {dewpoint})")
    print(f"(x_env, temperature): ({x_env}, {temperature})")

    line_hum.set_data(x_env, humidity)
    line_temp.set_data(x_env, temperature)
    line_dew.set_data(x_env, dewpoint)
    line_prs.set_data(x_prs, pressure)

    print('here')

    for ax in axs:
        ax.relim()
        ax.autoscale_view()

    print('here2')

    plt.pause(0.5)

    time.sleep(1)

    
