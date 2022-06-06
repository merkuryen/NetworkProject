import socket
import time
import os
import json
from datetime import datetime
import math

# Formating the string as utf-8
format = "utf-8"

# Broadcast Address for hamachi
port = 5001
broadcast_ip = "25.255.255.255"
address = (broadcast_ip, port)

# Get the computer's ip
# gethostname() is taking the getting the hostname of device
# gethostbyname() is convereting the hostname to ipv4 format.
ip = socket.gethostbyname(socket.gethostname())

# UDP service socket for announcer
                            #Ipv4       ,     UDP
announcer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

###########################
# Testing in LAN
IP = ip.split(".")
IP[3] = "255"
ip = ".".join(IP)
testAddress = (ip, port)
###########################

# For each file in current directory add the file to files list
# if file name is a sub directory check the directory and add files to 
# files list if there is file.
def getFiles(chunks):
    for chunk in os.listdir(os.curdir):
        '''if os.path.isdir(os.path.join(os.curdir, chunk)):
            for subChunk in os.listdir(os.path.join(os.curdir, chunk)):            
                if '.' not in subChunk and subChunk not in chunks:
                    chunks.append(subChunk)         '''    
        if '.' not in chunk and chunk not in chunks:
            chunks.append(chunk)

# Divides the files into chunks
def ChunkDivider(Filename):
    x = Filename.split(".")
    content_name = x[0]
    filename = content_name + "." + x[1]
    c = os.path.getsize(filename)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = content_name + '_' + str(index)
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
    chunk_file.close()

# Take the file name from user to host
# Divide the file to 5 chunks
# Inform the user about file is ready to host
# Wait 4 seconds and clear the terminal and start to announcment
filename = input("Enter file name with its extension you want to host: ")
ChunkDivider(filename)
print(f"{filename} ready to host.")
time.sleep(1)
os.system("cls")

counter = 0
while True:
    # Create list for holdin the files' name 
    chunks = []

    # Fill the files list with file names in directory
    getFiles(chunks)
    #print(chunks)

    # Create a dict named "t" and convert it to string with JSON
    t = {"chunks": chunks} 
    message = json.dumps(t)

    # Send the information with the username and files in username's computer to broadcast
    # Wait for 1 min
    announcer.sendto(message.encode(format), address)
    announcmentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    # Hold the log which file announced when
    log = f"---Announcement Info---\nTime: {announcmentTime}\nFile name: {filename}\nIP: {address[0]}\n"
    print(log)
    counter += 1
    file = open("announcer_log.txt", "a")
    file.write(log + "\n")
    file.close()

    # Wait for 1 minute
    time.sleep(60)

    # Counting the number of announcements.
    # When counter is equal to 5 clear the terminal for readability.
    if counter == 5:
        os.system("cls")
        counter = 0
