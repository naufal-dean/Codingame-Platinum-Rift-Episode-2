#!/usr/bin/env python3
import sys
import math
import random

# Deklarasi struktur data peta
# Link list peta menggunakan struktur graph (Daftar zona lain yang terhubung secara langsung)
class Map:
    def __init__(self, _nZone, _nLink, _pAmt):
        self.nZone = _nZone
        self.nLink = _nLink
        self.pAmt = _pAmt

        self.baseList = [0 for _ in range(self.pAmt)]
        self.platList = [0 for _ in range(self.nZone)]
        self.visiList = [0 for _ in range(self.nZone)]
        self.ownrList = [-1 for _ in range(self.nZone)]
        self.distList = [-1 for _ in range(self.nZone)]
        self.linkList = [[] for _ in range(self.nZone)]
        self.podsList = [[0 for _ in range(self.pAmt)] for _ in range(self.nZone)]

    def initDistList(self, _zone, _dstList, _distance):
        _dstList[_zone] = _distance
        print(_zone, _distance, file=sys.stderr)

        counted = []
        for i in range(len(self.linkList[_zone])):
            targetValue = _dstList[self.linkList[_zone][i]]
            if ((targetValue > _dstList[_zone] or targetValue == -1) and _distance < 25):
                counted.append(i)
                _dstList[self.linkList[_zone][i]] = _distance + 1
                
        print(counted, file=sys.stderr)

        for i in range(len(counted)):
            print("Counting", i, len(counted) // 2,file=sys.stderr)
            if (i == len(counted) // 2):
                self.initDistList(self.linkList[_zone][counted[i]], _dstList, _distance + 1)
            

    def assignBase(self):
        for i in range(len(self.visiList)):
            if (self.visiList[i] == 1 and self.ownrList[i] != -1):
                self.baseList[self.ownrList[i]] = i

    def isDeadEnd(self, zone):
        for i in range(len(self.linkList[zone])):
            if self.distList[self.linkList[zone][i]] == -1:
                return False
            elif self.distList[zone] < self.distList[self.linkList[zone][i]]:
                return False
        return True

    def printLink(self):
        print(self.linkList, file=sys.stderr)

    def addLink(self, _zone1, _zone2):
        self.linkList[_zone1].append(_zone2)
        self.linkList[_zone2].append(_zone1)

    def updatePlat(self, _zone, _plat):
        self.platList[_zone] = _plat

    def updateOwnr(self, _zone, _ownr):
        self.ownrList[_zone] = _ownr

    def updatePods(self, _zone, _ownr ,_pods):
        self.podsList[_zone][_ownr] = _pods

    def updateVisi(self, _zone, _visi):
        self.visiList[_zone] = _visi

    def visible(self, _zone):
        return self.visiList[_zone]

    def owner(self, _zone):
        return self.ownrList[_zone]

    def plat(self, _zone):
        return self.platList[_zone]

    def getPods(self, _zone, _ownr):
        return self.podsList[_zone][_ownr]

    def getEnemyPodCount(self, _zone, _id):
        count = 0

        for i in range(len(self.podsList[_zone])):
            if (i != _id):
                count += self.podsList[_zone][i]
        
        return count

    def isEnemyBase(self, zone, myId):
        for i in range(len(self.baseList)):
            if (zone == self.baseList[i] and i != myId):
                return True
        return False


#Fungsi penentu arah gerak pod
def decideMove(zone, map, moveList, myId, turn):
    '''
    limit = random.randint(0,len(map.linkList[zone])-1)
    podAmt = map.getPods(zone, myId)
    print(moveList, file=sys.stderr)
    '''
    podAmt = map.getPods(zone, myId)
    decVal = []
    moveAmt = 0

    # Jangan berpindah bila sedang baku hantam
    if (map.getEnemyPodCount(zone, myId) >0):
        return None;

    # Bila petak aman, timbang posisi sekitar
    for i in range(len(map.linkList[zone])):
        # Prioritas kejar musuh
        if (map.getEnemyPodCount(map.linkList[zone][i], myId) > 0 or map.isEnemyBase(map.linkList[zone][i], myId)):
            decVal.append(30)
        # Hindari melewati lagi petak yang sudah dikuasai
        elif (map.owner(map.linkList[zone][i]) == myId):
            decVal.append(-6)
        # Prioritaskan mengambil alih petak musuh
        else:
            decVal.append(map.plat(map.linkList[zone][i]))
            if (map.owner(map.linkList[zone][i]) != myId and map.owner(map.linkList[zone][i]) != -1):
                decVal[i] += 4

    if (turn < 10):
        moveAmt = (podAmt // 2) + 1
    else:
        moveAmt = ((podAmt * 3) // 4) + 1

    moveList.append([moveAmt, zone, getMax(decVal, map, zone)])
    if map.distList[getMax(decVal, map, zone)] == -1 or map.distList[getMax(decVal, map, zone)] > map.distList[zone]:
        map.distList[getMax(decVal, map, zone)] = map.distList[zone] + 1
        if map.isDeadEnd(getMax(decVal, map, zone)):
            map.distList[getMax(decVal, map, zone)] -= 1

#Fungsi penentu petak dengan prioritas tertinggi
def getMax(decVal, map, zone):
    maxVal = max(decVal)
    maxDex = decVal.index(maxVal)

    '''
    sameWeightList = []
    for i in range(len(decVal)):
        if (decVal[i] == maxVal)
            sameWeightList.append(map.)

    if (sameCounter > 1):
        pass
    '''

    if (maxVal == -6):
        #return map.linkList[zone][random.randint(0,len(decVal)-1)]
        distance = []
        for i in range(len(map.linkList[zone])):
            distance.append(map.distList[map.linkList[zone][i]])

        maxVal = max(distance)

        #Pengecekan keberadaan 2 poin dengan tingkat prioritas sama
        dupl = []
        for i in range(len(distance)):
            if maxVal == distance[i]:
                dupl.append(i)

        if (len(dupl) > 1):
            maxDex = dupl[random.randint(0, len(dupl) -1 )]
        else:
            maxDex = distance.index(maxVal)


    return map.linkList[zone][maxDex]

#Fungsi utama----------------------------------------------------
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]

map = Map(zone_count, link_count, player_count)

# map value initialization
for i in range(zone_count):
    zone_id, platinum_source = [int(j) for j in input().split()]
    map.updatePlat(zone_id, platinum_source)

for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    map.addLink(zone_1, zone_2)

#map.printLink()

# game loop
turn = 0

while True:
    my_platinum = int(input())  # your available Platinum

    # Update informasi peta
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
        map.updateOwnr(z_id, owner_id)
        map.updatePods(z_id, 0, pods_p0)
        map.updatePods(z_id, 1, pods_p1)
        map.updateVisi(z_id, visible)
        map.updatePlat(z_id, platinum)

    if (turn == 0):
        print(map.visiList, file=sys.stderr)
        map.assignBase()
        print(map.baseList, file=sys.stderr)
        map.distList[map.baseList[my_id]] = 0

    # Move algorithm = Decision weight
    # Iterasi melalui semua zona yang ada di peta untuk mencari pod teman lalu gerakkan berdasarkan algoritma
    # Move list = [n, origin, target]
    move = []
    for zone in range(zone_count):
        myPod = map.getPods(zone, my_id)
        if (myPod > 0):
            decideMove(zone, map, move, my_id, turn)

    #Eksekusi gerakan
    for i in range(len(move)):
        print(move[i][0], move[i][1], move[i][2], end=" ")
  
    print("")    
    print("WAIT")
    turn += 1

