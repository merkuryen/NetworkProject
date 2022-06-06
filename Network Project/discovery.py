import os
import socket
import json
from datetime import datetime

port = 5001

# Create a socket for listener
#                         IPv4          , UDP
listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get the computer's ip
# gethostname() is taking the getting the hostname of device
# gethostbyname() is convereting the hostname to ipv4 format.
ip = socket.gethostbyname(socket.gethostname())

addr = ('', port)
listener.bind(addr)

# Create a dict for content info of which user has the what file.
# It is dict because it will listen for long time so that
# it won't add the same names multiple times.
contentDictionary = {}

# Get the parameters of files, user_ip and
# puts it contentDictionary.
def contentManager(chunks, user_ip):
    for c in chunks:
        if c in contentDictionary.keys():
            if user_ip not in contentDictionary[c]:
                contentDictionary[c].append(user_ip)
        else:
            ips = [user_ip] 
            contentDictionary.update({c: ips})


counter = 0
while True:
    # Listen incoming 2048 bytes through socket
    message, address = listener.recvfrom(2048)
    counter += 1
    
    # Incoming message will be in JSON format so it should be parsed
    data = json.loads(message)

    # Get the "chunks" value and hold it in files variable
    chunks = data["chunks"]

    # Seperate the ip and port from address tuple
    user_ip = address[0]
    user_port = address[1]
    discoveryTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    # Print the information of which user has the what files
    print(f"Time: {discoveryTime}\nPeer: {user_ip}:{user_port}\nChunks: {chunks}\n")

    # Give the parameters chunks and ip address into contentManager function.
    # It will fill the ContnntDictionary.
    contentManager(chunks, user_ip)

    # Open a "contents.txt" file in write mode.
    # Convert the contentDictionary to string with json
    # and write the information into file.
    # This will be used with downloader service.
    # Because it will check the which peer has the which file.
    file = open("contents.txt", "w")
    file.write(json.dumps(contentDictionary)+"\n")
    file.close()

    # Everytime message recieved counter is increased.
    # Here it will check if number of recieves 10 or not.
    # If it is 10 console will be cleared for readability.
    # Counter will be set to 0 again.
    if counter == 10:
        os.system("cls")
        counter = 0

