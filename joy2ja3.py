import json
import hashlib
import re

def hextodec(hex):
    dec = int(hex, 16)
    return str(dec)

def joy2ja3(joy,raw):
    dumped = json.loads(joy)
    fing=dumped["str_repr"]
    fields=re.findall('\(([^)]+)', fing)
    if len(fields)>2:
        fields[2]=fields[2][1:]
        extensions_list = fields[2:]
    else:
        extensions_list=''
    version=hextodec(fields[0])
    cipher_suite_list=fields[1]
    ciphersuites=''
    for i,cipher in enumerate([cipher_suite_list[i:i+4] for i in range(0, len(cipher_suite_list), 4)]):
        if i==0:
            ciphersuites =hextodec(cipher)
        else:
            ciphersuites =ciphersuites+'-'+hextodec(cipher)

    extensions=''
    elliptic_curve=''
    ec_point_formats=''
    for i,extension in enumerate(extensions_list):
        if i==0:
            extensions=hextodec(extension[0:4])
        else:
            extensions=extensions+'-'+hextodec(extension[0:4])
        if extension[0:4]=='000a':
            tmp=extension[12:]
            supported_groups = [tmp[i:i+4] for i in range(0, len(tmp), 4)]
            for i,group in enumerate(supported_groups):
                if i==0:
                    elliptic_curve =hextodec(group)
                else:
                    elliptic_curve = elliptic_curve+'-'+hextodec(group)
        if extension[0:4]=='000b':
            len_ecpointform = extension[9:10]
            ecpoints=extension[10:]
            ecpoints=[ecpoints[i:i+2] for i in range(0, len(ecpoints), 2)]
            for i,ecpoint in enumerate(ecpoints):
                if i==0:
                    ec_point_formats=hextodec(ecpoint)
                else:
                    ec_point_formats=ec_point_formats+'-'+hextodec(ecpoint)
    out=version+ ','+ciphersuites+','+extensions+','+elliptic_curve+','+ec_point_formats
    ja3 =hashlib.md5(out.encode()).hexdigest()
    if raw==True:
        return out,ja3
    else:
        return ja3

joy=input("Insert the joy line:")
resp =joy2ja3(joy,True)
print(resp[0]+'\n'+resp[1])