with open("result.bmp", "r") as file:
    bmp = file.read()

with open("pi.txt", "r") as file:
    pi = file.read()

def getPi():
    global cpi
    cpi += 1
    return int(pi[cpi-1])

cpi = 0

num = ord(bmp[14]) + 14

flagLst = ("a "*64).split(" ")

charNum = 0

for i in range(0, 64): # Going to 64 characters cause I don't know the length of the flag
    for i2 in range(0, 8):
        pin = getPi()
        num2 = num + pin
        charNum |= (0x01 & ord(bmp[num2])) << i2
        # print("num : %d / pi : %d / num2 : %d / charNum : %s" % (num, pin, num2, bin(charNum))) # debugging
        num += 10
    # print(chr(charNum)) # debugging
    flagLst[i] = chr(charNum)
    charNum = 0

flag = "".join(flagLst)
print(flag)
