#
# Finds the values for the "magic number" table used in the calculation
# of the CRC byte of VAG MQB canbus messages.
#
# by Ronaldo Cordeiro - https://github.com/ronaldocordeiro/
#
# usage: python find_CRC_mask.py [input file]
#
import sys

#
# Returns the "magic number" supposed to be applied in the middle of CRC calculation process by performing the initial part,
# reversing the final part of the process from the calculated CRC, then applying XOR to the two resulting bytes
#
def findKey(msgBody):
    crcLookupTable = [ 0, 47, 94, 113, 188, 147, 226, 205, 87, 120, 9, 38, 235, 196, 181, 154, 174, 129, 240, 223, 18, 61, 76, 99, 249, 214, 167, 136, 69, 106,
     27, 52, 115, 92, 45, 2, 207, 224, 145, 190,  36, 11, 122, 85, 152, 183, 198, 233, 221, 242, 131, 172, 97, 78, 63, 16, 138, 165, 212, 251, 54, 25, 104, 71, 230, 201, 184, 151, 90, 117,
     4, 43, 177, 158, 239, 192, 13, 34, 83, 124, 72, 103, 22, 57, 244, 219, 170, 133, 31, 48, 65, 110, 163, 140, 253, 210, 149, 186, 203, 228, 41, 6, 119, 88, 194, 237, 156, 179, 126, 81,
     32, 15, 59, 20, 101, 74, 135, 168, 217, 246, 108, 67, 50, 29, 208, 255, 142, 161, 227, 204, 189, 146, 95, 112, 1, 46, 180, 155, 234, 197, 8, 39, 86, 121, 77, 98, 19, 60, 241, 222,
     175, 128, 26, 53, 68, 107, 166, 137, 248, 215, 144, 191, 206, 225, 44, 3, 114, 93, 199, 232, 153, 182, 123, 84, 37, 10, 62, 17, 96, 79, 130, 173, 220, 243, 105, 70, 55, 24, 213, 250,
     139, 164, 5, 42, 91, 116, 185, 150, 231, 200, 82, 125, 12, 35, 238, 193, 176, 159, 171, 132, 245, 218, 23, 56, 73, 102, 252, 211, 162, 141, 64, 111, 30, 49, 118, 89, 40, 7, 202, 229,
     148, 187, 33, 14, 127, 80, 157, 178, 195, 236, 216, 247, 134, 169, 100, 75, 58, 21, 143, 160, 209, 254, 51, 28, 109, 66]

    msgLen=len(msgBody)
    crc = 0xFF
    for i in range(1,msgLen):
        crc^=msgBody[i]
        crc=crcLookupTable[crc]
 
    key=crcLookupTable.index(msgBody[0]^0xFF) ^ crc
    return key

if len(sys.argv) > 2:
    sys.exit("usage: python "+argv[0]+" [input file]")
elif len(sys.argv) == 2:
    prompt=False
    try:
        sys.stdin=open(sys.argv[1],"r")
    except:
        sys.exit("Couldn't open file "+sys.argv[1])
else:
    prompt=True

P_L_CC_KENNUNG_APV = [None]*16

while True:
    if prompt:
        print("Input message bytes in hex format. Empty line or ctrl-Z plus Return to finish\n")

    try:
        msg=input()
    except:
        break

    msgLen=len(msg.split())
    if msgLen==0:
        break
    elif msgLen<4 or msgLen>8:
        sys.exit("Message length out of range (expected 4 to 8 hex values)")

    try:
        msgSet=[int(byte,16) for byte in msg.split()]
    except:
        sys.exit("Invalid hex values found")

    counter=msgSet[1] & 0x0F
    P_L_CC_KENNUNG_APV[counter]=findKey(msgSet)


print("[", end='')
for i in range(16):
    print(None if P_L_CC_KENNUNG_APV[i] is None else hex(P_L_CC_KENNUNG_APV[i]),end='')
    print(',' if i<15 else ']\n',end='')

