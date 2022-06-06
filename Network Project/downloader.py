import socket
import json
import os
from datetime import datetime
import time

format = "utf-8"
port = 8000

while True:
    # Asks for the content name downloading.
    # It creates a chunknames list with that content_name.
    # Opens the "contents.txt" file in read mode to get the which peer has the file.
    # "chunkExist" flag is initially set to True.
    content_name = input("Please enter the file name you want to download: ")
    chunknames = [content_name + '_1', content_name + '_2', content_name + '_3', content_name + '_4', content_name + '_5']
    file = open("contents.txt", "r")
    chunkExist = True
    contentDictionary = json.loads(file.read())
    file.close()

    # Checks is there any chunk name in contentDicctionary as key.
    # If there is not, it clears the flag "chunkExist".
    # And asks for valid input until it finds existing file and sets
    # flag "chunkExist".
    # if there is file it continues to while loop.
    for chunk in chunknames:
        if chunk not in contentDictionary.keys():
            print(f"There is no hosted chunk named {file}")
            chunkExist = False
    while not chunkExist:
        content_name = input('Please enter valid file name: ')
        chunknames = [content_name + '_1', content_name + '_2', content_name + '_3', content_name + '_4', content_name + '_5']
        for chunk in chunknames:
            if chunk in contentDictionary.keys():
                chunkExist = True
            
    while True:
        # Takes the ip values corresponding to chunks from chunknames list
        # and puts the ip into ips
        for chunk in chunknames:
            ips = contentDictionary[chunk]
            tries = 0

            # For each ip in ips checks is it the owned computer's ip.
            # If it is not equal to computer's ip it continues download process.
            # This is need for not blocking the software due to it will try to download
            # file from its own computer.
            for ip in ips:
                if ip != socket.gethostbyname(socket.gethostname()):
                    try:
                        # Creates a TCP socket for ip which is in ips through port 8000
                        # and connects to socket that ip.
                        address = (ip, port)
                        downloader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        downloader.settimeout(5)
                        downloader.connect(address)

                        # Creating a message dict with key "chunks".
                        # With json it converts the dict to string and sends it to the 
                        # address which connected.
                        message = {"chunks": chunk}
                        message = json.dumps(message).encode(format)
                        downloader.send(message)

                        # Opens a file as binary write as chunks
                        with open(chunk, 'wb') as f:

                            # infinitly tries to receive file through socket
                            # and writes it as file named chunk name.
                            # If there is no data breaks the infinite loop.
                            while True:
                                print('receiving data...')
                                data = downloader.recv(2048)
                                if not data:
                                    break
                                f.write(data)
                        f.close()

                        # Holds the time of download.
                        # Prints the information of time, chunk and ip
                        # also hold the info in download_log.txt file.
                        logTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                        logmessage = f"Time: {logTime}\nChunk: {chunk}\nFrom: {ip}\n"
                        print(logmessage)
                        log = open("download_log.txt", "a")
                        log.write(logmessage + "\n")
                        log.close()

                        # Send back to the uploader message that download finished
                        downloader.send("Download finished".encode(format))
                        break

                    # If encountered error print the information
                    # and increase the number of tries.
                    except socket.error:
                        print(f"Connection could not established with {ip}")
                        tries += 1

                    # Finally it is closes the socket even it is succeeded or not.
                    finally:
                        downloader.close()
            # After trying for each ip if it cannot download.
            # It prints the information that chunk cannot be downloaded.
            # Waits 2 seconds and lears the console for readability
            if tries == len(ips):
                print("CHUNK " + chunk + " CANNOT BE DOWNLOADED FROM ONLINE PEERS")
        break
    
    # If successfully recieved every chunks it asks for the extension to pack the file.
    extension = input("Please enter the extension of original file for packing: ")
    filename = content_name + "." + extension
    with open(filename,"wb") as outfile:
        for chunk in chunknames:
            with open(chunk, "rb") as infile:
                outfile.write(infile.read() )
            infile.close()

    # Ask to client for s/he wants to download another file.
    # Either way it clears the console eventually.
    resume = input("Do you want to download another file ? Y/N: ")
    if resume.lower() != 'y':
        os.system("cls")
        break
    else:
        time.sleep(1)
        os.system("cls")