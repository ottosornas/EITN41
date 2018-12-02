from pcapfile import savefile
from ipaddress import IPv4Address

testcap = open('cia.log.4.pcap', 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

abuIP = "61.78.13.37"
mixIP = "102.123.40.24"
nrOfPartners = 8
allSets = []

def learningPhase():     
    info = []

    for pkt in capfile.packets:
        ipSource = pkt.packet.payload.src.decode('UTF8')
        ipDestination = pkt.packet.payload.dst.decode('UTF8')

        info.append({
            "ipSource": ipSource,
            "ipDestination": ipDestination
        })
    return info

def find_receivers(abu_ip, mix_ip, m):

    rows = learningPhase()

    currentSet = set()
    nazirFound = False
    for i in range(len(rows)):
        ipSource = rows[i]["ipSource"]
        ipDestination = rows[i]["ipDestination"]
        if nazirFound and ipSource == mix_ip:
            currentSet.add(ipDestination)        
            try:
                if rows[i+1]["ipSource"] != mix_ip:
                    allSets.append(currentSet)                    
                    currentSet = set()
                    nazirFound = False
            except IndexError:
                continue

        if ipSource == abu_ip and ipDestination == mix_ip:
            nazirFound = True
    findDisjoint()

def findDisjoint():
    disjointSets = []

    for currentSet in allSets:
        isDisjoint = True
        for disjoint_set in disjointSets:
            if currentSet.isdisjoint(disjoint_set) != True:
                isDisjoint = False

        if isDisjoint:
            disjointSets.append(currentSet)
            allSets.remove(currentSet)

        if len(disjointSets) >= nrOfPartners:
            disjointSets = disjointSets[:nrOfPartners]
            break
    exclusionPhase(disjointSets)

def exclusionPhase(disjointSets):
   
    for currentSet in allSets:
        noneDisjoinSets = []
        for disjointSet in disjointSets:
            if currentSet.isdisjoint(disjointSet) != True:
                noneDisjoinSets.append(disjointSet)
        
        #R ∩ Ri =/= ∅ and R ∩ Rj = ∅, ∀j =/= i 
        if len(noneDisjoinSets) == 1:
            noneDisjointSet = noneDisjoinSets[0]
            disjointSets.remove(noneDisjointSet)
            intersec = noneDisjointSet.intersection(currentSet)
            disjointSets.append(intersec)
    print(getIPSum(disjointSets))

def getIPSum(disjointSets):
    IPsum = 0
    for itemSet in disjointSets:
        for item in itemSet:
            print(str(item))
            IPsum += int(IPv4Address(item))
    return str(IPsum)

find_receivers(abuIP, mixIP, nrOfPartners)