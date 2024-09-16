The City has been using an antiquated water-meter billing software that requires Water Dep't employees to run daily routes with RFID readers to collect meter data from houses. Water is planning a migration 
from the legacy NSITE system to the Neptune 360 system based on LoRaWaN IoT. Real-time data on meter reads is extremely useful for billing and monitoring leaking pipes, eliminating the need for manually
driving the routes each day. 

Process Description: Each morning, the Water Department queries the AS/400 mainframe and specifies a set # of meter IDs to be loaded into meter readers based on the cycle. This data is uploaded into the
NSITE software that is then used to create empty data fields of the proper format in the readers. The route runners collect the specified data over the course of the day and, at day's end, push the data 
back into the AS/400. 

While the city migrates away from NSITE to Neptune 360, all billing programs are still running through the AS/400 system. As such, up-to-date data from Neptune 360 needs to be fed into the AS/400.
We require a set of scripts that can convert the format of the v4 file format that can be exported out of the Neptune 360 system into an import.txt file that can be imported into the AS/400.

main.py runs a script that transforms the v4.txt file into this import.txt file (found in the output folder). The script utilizes the schema information that is detailed in the Neptune 360 documentation. 


Eventually, billing will be done through the Neptune 360 system itself. Until then, this code will be used. 
