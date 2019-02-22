import sys
import math
from random import randint

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]

z_list, l_list = [], []

for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]
    z_list += [[zone_id, platinum_source]]

for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    l_list += [[zone_1, zone_2]]

# game loop
while True:
    my_platinum = int(input())  # your available Platinum

    z_vis = []          # list zona visible
    z_pod = []          # list zona dengan pod (indeks 0 sd i)
    pos_move = []       # list possible move untuk tiap pod ke-i
    count = 0           # indeks pada pos_move, variabel dummy
    move = []           # list print

    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]

        if visible == 1:
            z_vis += [[z_id, owner_id, pods_p0, pods_p1, visible, platinum]]

        if owner_id == 0:
            z_pod += [[z_id, owner_id, pods_p0, pods_p1, visible, platinum]]
            #print(len(l_list))

            pos_move.append([])

            for i in range(len(l_list)):
                if l_list[i][0] == z_pod[count][0]:
                    pos_move[count].append(l_list[i][1])
                elif l_list[i][1] == z_pod[count][0]:
                    pos_move[count].append(l_list[i][0])

            count += 1

        #pos_move = [i for i in z_vis if i not in z_pod]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    #print(len(pos_move), len(z_pod))

    # first line for movement commands, second line no longer used (see the protocol in the statement for details)
    for i in range(len(z_pod)):
        pod_val = z_pod[i][2] // 2 if z_pod[i][2] // 2 > 0 else 1
        move += [pod_val, z_pod[i][0], pos_move[i][randint(0, len(pos_move[i]) - 1)]]

    for i in move:
        print(i, end = " ")
    print()
    print("WAIT")
