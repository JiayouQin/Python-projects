#!/usr/bin/env python
# coding: utf-8

# In[11]:


import re 

def str_tobinary(inputstring):
    return ''.join(bin(x)[2:].zfill(8) for x in inputstring.encode('UTF-8'))

def splithalf_l(inputstring):
    try:
        lefthalf = inputstring [:int(len(inputstring)/2)]
        return lefthalf
    except:
        print (f"input length error: length {int(len(inputstring)/2)}")

def splithalf_r(inputstring):
    try:
        righthalf = inputstring [int(len(inputstring)/2):]
        return righthalf
    except:
        print (f"input length error: length {int(len(inputstring)/2)}")

def permutation(inputstring,inputindex):
    tempstring = ""
    for i in inputindex: #55
        tempstring += inputstring[i-1] #permutation
    return tempstring

def permutation_r(inputstring,inputindex):
    templist = []
    x = 0
    for _ in inputstring:
        templist.append(" ")
    for _ in inputindex: #55
        templist[_] = inputstring[x] #permutation
        x += 1    
    return "".join(templist)

def leftshift(inputstring,n):
    return inputstring[n:] + inputstring[0:n]

def key_gen(inputstring):#to do: convert 8 digital
    key_bi = str_tobinary(inputstring)
    tempstring = ""
    key_bi = permutation(key_bi,PC1_index)
    subkey=[]
    stf = 0
    keyleft = splithalf_l(key_bi)
    keyright = splithalf_r(key_bi)
    for i in range(0,16):
        dicttemp = str(i+1)
        keyleft = leftshift(keyleft,rounddict[dicttemp])
        keyright = leftshift(keyright,rounddict[dicttemp])
        key_perm = permutation(keyleft+keyright,PC2_index)
        subkey.append(key_perm)
    return subkey

def bitoascii(inputstring):
    outputstring = ""
    while len(inputstring) > 8 :
        outputstring += chr(int(inputstring[:8],2))
        inputstring = inputstring [8:]
    outputstring += chr(int(inputstring,2))
    return outputstring

def str_tobinary(inputstring):
    return ''.join(bin(x)[2:].zfill(8) for x in inputstring.encode('UTF-8'))

def text_to_64bit(inputstring): #cut messeage block into a lists that contains 64bit units
    outputlist = []
    #some magic that converts inputstring into binary string
    inputstring = ''.join('{:08b}'.format(b) for b in inputstring.encode('utf8'))
    while len (inputstring) != 0:
        if 0 < len(inputstring) < 64:
            for _ in range(0,int(64 - len(inputstring)/8)):
                if len(inputstring) % 8 != 0:
                    print ("Critical error in text to binary algorithm")
                inputstring += "00100000" #add space if input text less than 64 bits
        else:
            tempstring = inputstring[:64]
            inputstring = inputstring[64:]
            outputlist.append(tempstring) 
    return outputlist #returns a list that contains 64bits binary unicode in each index

def xor(mes,subkey):
    newstring = ""
    try:
        for _ in range(len(mes)):
            if mes[_] == subkey[_]:
                newstring += "0"
            else:
                newstring += "1"
        return (newstring)
    except:
        print ("XOR failed, check input string length")

def sbox_logic(inputstring):
    tempstring = ""
    output = ""
    for i in range (0,8): # take 6 bits and cipher 4 bits in the middle
        tempstring = inputstring[:6]
        inputstring = inputstring[6:]
        y = int(tempstring[0] + tempstring[5],2)
        x = int(tempstring[1:5],2)
        output += '{0:04b}'.format(sboxdict[str(i+1)][y][x])  #returns the dicimal value of the table value
    return output

def logic_64_encrypt(inputstring,keys_input):
    inputstring = permutation(inputstring,Perm_init)
    mes_left = splithalf_l(inputstring) #split
    mes_right = splithalf_r(inputstring) #split
    for i in range (0,16): #cipher loop
        mes_right_temp = permutation(mes_right,expandindex) #expand to 48 bits
        mes_right_temp = xor(mes_right_temp,keys_input[i])
        mes_right_temp = sbox_logic(mes_right_temp) #cipher and shrink to 32 bits again
        mes_right_temp = permutation(mes_right_temp,Perm_ciph)
        mes_right_temp = xor(mes_right_temp,mes_left)
        mes_left = mes_right
        mes_right = mes_right_temp
    #end of the loop  
    mes_left,mes_right = mes_right,mes_left
    return permutation(mes_left + mes_right,Perm_r)#reverse initial permutation
    
def decrypt_64(inputstring): #cut messeage block into a lists that contains 64bit units
    outputlist = []
    #convert inputstring into 8 digital string
    while len (inputstring) != 0:
            tempstring = inputstring[:64]
            inputstring = inputstring[64:]
            outputlist.append(tempstring)
    return outputlist
    
def decryption(cipher,subkeys):
    inputlist =  decrypt_64(cipher)
    subkeys = subkeys[::-1]
    outputstring = ""
    for i in range(len(inputlist)):
        outputstring += logic_64_encrypt(inputlist[i],subkeys)
    return outputstring

def checkfile():
    try :
        file = open("DES_text.txt", "r")
        file.close() 
        file = open("DES_encrypted.txt", "r")
        file.close() 
    except:
        print ("file has not been found, a new file will be created")
        f= open("DES_text.txt","w+")
        f.close()
        f= open("DES_encrypted.txt","w+")
        file.close()
        
def keyinput_to8():
    key_input = ""
    while len(key_input) > 8 or key_input == "":
        key_input = input ("Please give the key value here (maximal 8 digits)")
    while 0 < len(key_input) < 8:
        key_input += " "
    return key_input

rounddict = {"1":1,"2":1,"3":2,"4":2,"5":2,"6":2,"7":2,"8":2,"9":1,"10":2,"11":2,"12":2,"13":2,"14":2,"15":2,"16":2}

Perm_init = [58,50,42,34,26,18,10,2,
            60,52,44,36,28,20,12,4,
            62,54,46,38,30,22,14,6,
            64,56,48,40,32,24,16,8,
            57,49,41,33,25,17,9,1,
            59,51,43,35,27,19,11,3,
            61,53,45,37,29,21,13,5,
            63,55,47,39,31,23,15,7]
Perm_r = [40,8,48,16,56,24,64,32,
            39,7,47,15,55,23,63,31,
            38,6,46,14,54,22,62,30,
            37,5,45,13,53,21,61,29,
            36,4,44,12,52,20,60,28,
            35,3,43,11,51,19,59,27,
            34,2,42,10,50,18,58,26,
            33,1,41,9,49,17,57,25]
expandindex = [32,1,2,3,4,5,
                4,5,6,7,8,9,
                8,9,10,11,12,13,
                12,13,14,15,16,17,
                16,17,18,19,20,21,
                20,21,22,23,24,25,
                24,25,26,27,28,29,
                28,29,30,31,32,1]
Perm_ciph = [16,7,20,21,29,12,28,17,
                1,15,23,26,5,18,31,10,
                2,8,24,14,32,27,3,9,
                19,13,30,6,22,11,4,25]
PC1_index = [57,49,41,33,25,17,9,
            1,58,50,42,34,26,18,
            10,2,59,51,43,35,27,
            19,11,3,60,52,44,36,
            63,55,47,39,31,23,15,
            7,62,54,46,38,30,22,
            14,6,61,53,45,37,29,
            21,13,5,28,20,12,4]
PC2_index = [14,17,11,24,1,5,
                3,28,15,6,21,10,
                23,19,12,4,26,8,
                16,7,27,20,13,2,
                41,52,31,37,47,55,
                30,40,51,45,33,48,
                44,49,39,56,34,53,
                46,42,50,36,29,32]
sboxdict = {"1":[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
            [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
            [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
            [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
            "2":[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
            [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
            [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
            [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],],
            "3":[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
            [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
            [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
            [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
            "4":[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
            [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
            [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
            [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
            "5":[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
            [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
            [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
            [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
            "6":[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
            [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
            [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
            [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
            "7":[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
            [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
            "8":[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
            [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
            [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
            [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]}


# In[22]:


"""
This program uses DES encryption method, 
it has basically 3 functions: read file and encrypt, encrypt input or read file and decrypt

encrypt file: importing text from "DES_text.txt", encrypt text and output to DES_encrypted.txt
encrypt input: input a string and encrypt, then output to DES_encrypted.txt
decrypt file: read DES_encrypted.txt, decrypt and output to DES_decrypted.txt

"""
print("""
This program uses DES encryption method, 
it has basically 3 functions: read file and encrypt, encrypt input or read file and decrypt

encrypt file: importing text from "DES_text.txt", encrypt text and output to DES_encrypted.txt
encrypt input: input a string and encrypt, then output to DES_encrypted.txt
decrypt file: read DES_encrypted.txt, decrypt and output to DES_decrypted.txt
-----------------------------------------------------------------------
This program will automatically generate txt file in file path of this program and close itself the first time it runs
""")

askimport = input ("Do you want to import a file or write text?\nType i to import encrypted data, w to write text, d to decrypt data:")
askimport.lower()
checkfile()
while askimport != "i" and askimport != "w" and askimport != "d": # a simple input check
    askimport = input ("Type i to import encrypted data, w to write text, d to decrypt data:")
if askimport == "i":
    file = open("DES_text.txt", "r")
    textinput = file.read()
    file.close() 
    print ("--------------------This is the contents of the File---------------------")
    print (textinput)
    print ("-------------------------------------------------------------------------")
    
elif askimport == "w":
    textinput = input ("Type any text in here")
    print ("-----------------------------Plain Text----------------------------------")
    print (textinput)
    print ("-------------------------------------------------------------------------")
    
elif askimport == "d":
        file = open("DES_encrypted.txt", "r")
        textinput = file.read()
        file.close()
        print ("--------------------This is the contents of the File---------------------")
        print (textinput)
        print ("-------------------------------------------------------------------------")
if textinput == "":
    run = False
else:
    run = True
if run:
    key_input = "" #input the key
    while len(key_input) != 8:
        key_input = keyinput_to8()
    subkeys = key_gen(key_input)
    if askimport != "d":
        inputlist = text_to_64bit(textinput) #cut text to 64-bits blocks
        outputstring = ""
        plaintext = ""
        for i in range(len(inputlist)):
            plaintext += inputlist[i]
            outputstring += logic_64_encrypt(inputlist[i],subkeys)
            #again, some magic that converts binary unicode into strings
        print ("-----------------Plain Text------------")
        print (bitoascii(plaintext))
        print ("-----------------Encrypted data--------")
        print (outputstring)
        file = open("DES_encrypted.txt","w+")  
        file.write(outputstring) 
        file.close() 

    elif run and askimport == "d":
        try:
            outputstring = decryption(textinput,subkeys)
            outputstring = bytes(int(b, 2) for b in re.split('(........)', outputstring) if b).decode('utf8')
            #again, some magic that converts binary unicode into strings
            print (outputstring)
            file = open("DES_decrypted.txt", "w+")
            file.write(outputstring)
            file.close()
        except:
            print ("Invalid value, check key")
    else:
        pass
input("Press Enter to continue...")


# In[6]:


inputstring = "12345678"
outputlist = []
#some magic that converts inputstring into binary string
inputstring = ''.join('{:08b}'.format(b) for b in inputstring.encode('utf8'))
print (inputstring)
while len (inputstring) != 0:
    if 0 < len(inputstring) < 64:
        for _ in range(0,64 - len(inputstring)/8):
            inputstring += "00100000" #add space if input text less than 64 bits
            print ("+1")
    else:
        tempstring = inputstring[:64]
        inputstring = inputstring[64:]
        outputlist.append(tempstring) 
print(outputlist)  #returns a list that contains 64bits binary unicode in each index


# In[5]:


len("0011000100110010001100110011010000110101001101100011011100111000")


# In[ ]:




