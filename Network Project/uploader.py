import socket
import json
from datetime import datetime

# Set the parameters for TCP connection
port = 8000
ip = socket.gethostbyname(socket.gethostname())
addr = (ip,port)

# Create a TCP socket for uploader
uploader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the computer's address to the socket and start to listen
# for upto 6 peer. After 6 peer it will start to refuse connections.
uploader.bind(addr)
uploader.listen(6)

# Inform the file provider about started to listen for 
# incoming connections through socket.
print("Started to listen for download requests.")

while True:

    # Open a connections_log.txt file to log the connections recieved.
    connections = open("connections_log.txt", "a")

    # Accept a connection and create a connection socket
    # and take the address of connected peer.
    connection, address = uploader.accept()

    #  Hold the ip address and create a log variable.
    ip = address[0]
    log = f"---Uploader Info---\nConnection: {ip}"

    # Write the log into the file and close the file.
    # Lastly print the log to the screen so that peer can see who
    # connected.
    connections.write(log + "\n")
    connection.close
    print(log)
    
    while True:
        
        # Recieve message through connection socket.
        message = connection.recv(2048)
        
        # Message will be json format. So that we need to parse it to dictionary.
        data = json.loads(message)

        # chunk_name will be equal to the value of "chunks" key.
        chunk_name = data["chunks"]

        # Print the information who requested which chunk_name.
        print(f"Requested: {chunk_name}")

        # Hold the log of who requested from which ip.
        request = open("requests_log.txt", "a")
        log = f"Requested: {chunk_name}\nFrom: {ip}\n"
        request.write(log + "\n")
        request.close
        
        # Open the chunk in read mode as binary.
        chunkFile = open(chunk_name, "rb")

        # Read the file and store it in temp.
        # If temp is empty break the while loop.
        # If temp is not empty send it through connection socket.
        while True:
            temp = chunkFile.read(2048)
            if not temp:
                break
            connection.send(temp)

        # Close the file when upload finished.
        chunkFile.close()

        # Take the upload time and format it to mm-dd-yy h-m-s
        uploadTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        # Change the log variable which defined before to 
        # Time: uploadTime
        # Sent to: ip
        # Chunk name: chunk_name
        log = f"Time: {uploadTime}\nSent to: {ip}\nChunk name: {chunk_name}\n"

        # Inform the peer as what file sent.
        print(log)

        # Hold the log of uploads
        uploads = open("uploads_log.txt", "a")
        uploads.write(log + "\n")
        uploads.close()

        # As everything finished close the connection socket.
        connection.close()
        break
