----------- How program works -----------

Firstly, announcer should be started to ask the peer what file will be hosted.
File name should be entered as "filename.extension". After filename entered and it is exist
announcer firstly divide it to 5 chunks. Later it start to read files from directory and hold itin dictionary.
Converts the dictionary to JSON and send the message to all peers through 5001 port.
After file ready to be hosted, uploader should be started it will start to listen for download requests from other peers through port 5001.
If peer want to downlaod file from other peers. Firstly, discovery should be started. 
Thus, discover start to listen other hoster's announcer and hold the info of which chunk is hosted by who in a text file. 
After that downloader should be started. Downloader will be ask for the peer which file peer want to download.
After it will check file is exist or not by reading the text file which created by discovery. If file exists it will take the
ips and hold in list. After that it is going to start to request the file from peers. When download is finished it will ask for 
file extension. File extension should be entered without ".". After file packed it will ask the peer will it be download 
a new file or not.

For readability purpose during the discovery and announcement console will be cleaned after several times of discovery and announcement.

----------- Program limitations -----------

Not tested for Mac or linux. No know issues for those operating systems.
If download is cut off and cannot be downloaded from other peers it will still ask for the extension.