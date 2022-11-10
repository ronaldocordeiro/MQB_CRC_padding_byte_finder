# MQB CRC padding byte finder

Some of the CANbus messages used in VAG (Volkswagen, Audi, Seat, Skoda) cars in MQB platform contain a CRC byte. The CRC is transmitted as the first byte (byte 0) in the message payload, calculated on the remaining bytes. The CRC8H2f AUTOSAR algorithm used to calculate the CRC is detailed in the document below:

https://www.autosar.org/fileadmin/user_upload/standards/classic/4-3/AUTOSAR_SWS_CRCLibrary.pdf

VAG MQB platform adds a padding byte to the message in the CRC calculating process. If the message is 4 byte long, CRC is calculated on bytes 1 to 3 (since byte 0 is reserved for the CRC itself), with a "4th" padding byte added. If the message is 8 byte long, CRC is calculated on bytes 1 to 7, with an "8th" padding byte added.
The padding byte varies depending on the CANbus message ID and, in some cases, depending also on the "counter" field, contained in the lower 4 bits of byte 1, which cycles from the values 0 to 15 in sequence of messages of the same ID. Implementations of the CRC calculation including the padding byte can be found on:

https://github.com/commaai/opendbc/blob/master/can/common.cc

The code contained here allows the user to find the padding bytes used to calculate the CRC for a message ID. Since it uses a reverse calculation of CRC, up to 16 samples (with different counter numbers) of the message must be collected from CANbus traffic and used as the input for the program.

# Usage

Collect samples of real messages from the CANbus traffic. In order to obtain all of the 16 values for the padding bytes, 16 messages with different values from 0 to 15 for the "counter" field should be collected. In the example below, the messages collected have the ID 0x31E (tsk_07), 8 byte long, with the counter field (lower 4 bits in the second byte) varying from 0 to F:

0x31E    8   5E E0 3F 00 00 00 00 C0  
0x31E    8   94 E1 3F 00 00 00 00 C0  
0x31E    8   2E E2 3F 00 00 00 00 C0  
0x31E    8   6C E3 3F 00 00 00 00 C0  
0x31E    8   C1 E4 3F 00 00 00 00 C0  
0x31E    8   BE E5 3F 00 00 00 00 C0  
0x31E    8   39 E6 3F 00 00 00 00 C0  
0x31E    8   3F E7 3F 00 00 00 00 C0  
0x31E    8   76 E8 3F 00 00 00 00 C0  
0x31E    8   49 E9 3F 00 00 00 00 C0  
0x31E    8   7D EA 3F 00 00 00 00 C0  
0x31E    8   5B EB 3F 00 00 00 00 C0  
0x31E    8   F8 EC 3F 00 00 00 00 C0  
0x31E    8   51 ED 3F 00 00 00 00 C0  
0x31E    8   24 EE 3F 00 00 00 00 C0  
0x31E    8   CD EF 3F 00 00 00 00 C0  

## Manual entry:

py find_CRC_padding_byte.py    
Input message bytes in hex format. Empty line or ctrl-Z plus Return to finish

6C E3 3F 00 00 00 00 C0  
Input message bytes in hex format. Empty line or ctrl-Z plus Return to finish

24 EE 3F 00 00 00 00 C0  
Input message bytes in hex format. Empty line or ctrl-Z plus Return to finish  

^Z  
[None,None,None,0x31,None,None,None,None,None,None,None,None,None,None,0x59,None]

Since only 2 lines with "counter" values 3 and F were entered, the resulting list contains values only for the items 3 and 14, all others remain with the value "None".

## Reading from file

py find_CRC_padding_byte.py samples\tsk_07.txt  
[0x78,0x68,0x3a,0x31,0x16,0x8,0x4f,0xde,0xf7,0x35,0x19,0xe6,0x28,0x2f,0x59,0x82]  

Sample data files supplied in the "samples" folder contain messages with all 16 values for the field "counter", so all items in the resulting list are filled with the padding byte corresponding to the value of "counter".