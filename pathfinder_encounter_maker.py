# -*- coding: utf-8 -*-
"""
@author: Rob Welch (http://robwel.ch)
License: The GNU General Public License v3.0 (except where noted)
"""

import argparse
import sys

parser = argparse.ArgumentParser(description="Pathfinder encounter maker")
parser.add_argument("--players", action="store", dest='players', type=int, default=4, help="Number of player characters in the game (4 recommended).")
parser.add_argument("--apl", action="store", dest='apl', type=int, default=-1, help="Average level of the party.")
parser.add_argument("--enemies", action="store", dest='enemies', type=int, default="1", help="How many enemies are in the encounter.")
parser.add_argument("--difficulty", action="store", type=int, default=0, help="Difficulty modifier. Set it to 1 for slightly hard, 2 for hard, 3 for very hard (etc). It can also go negative.")

def lookup_stat(stat_name, CR):
    """
    Table source: http://paizo.com/pathfinderRPG/prd/bestiary/monsterCreation.html
    The table itself is released under the Open Game License.
    """
    monster_stat_lookup_table = """CR,Hit Points,Armor Class,Attack (High),Attack (Low),Average Damage High,Average Damage Low,Ability DC (Primary),Ability DC (Secondary),Save (Good),Save (Poor)
0,10,11,1,0,4,3,11,8,3,0
1,15,12,2,1,7,5,12,9,4,1
2,20,14,4,3,10,7,13,9,5,1
3,30,15,6,4,13,9,14,10,6,2
4,40,17,8,6,16,12,15,10,7,3
5,55,18,10,7,20,15,15,11,8,4
6,70,19,12,8,25,18,16,11,9,5
7,85,20,13,10,30,22,17,12,10,6
8,100,21,15,11,35,26,18,12,11,7
9,115,23,17,12,40,30,18,13,12,8
10,130,24,18,13,45,33,19,13,13,9
11,145,25,19,14,50,37,20,14,14,10
12,160,27,21,15,55,41,21,15,15,11
13,180,28,22,16,60,45,21,15,16,12
14,200,29,23,17,65,48,22,16,17,12
15,220,30,24,18,70,52,23,16,18,13
16,240,31,26,19,80,60,24,17,19,14
17,270,32,27,20,90,67,24,18,20,15
18,300,33,28,21,100,75,25,18,20,16
19,330,34,29,22,110,82,26,19,21,16
20,370,36,30,23,120,90,27,20,22,17
21,400,37,31,24,130,98,27,20,23,18
22,440,39,32,25,140,105,28,21,23,18
23,480,40,33,26,150,113,29,22,24,19
24,520,42,35,27,165,124,30,23,25,20
25,560,43,36,28,180,135,30,24,26,21
26,600,44,37,29,195,145,31,25,27,22
27,640,45,38,30,210,155,32,26,28,23
28,680,46,39,31,225,165,33,27,29,24
29,720,47,40,32,240,175,34,28,30,25
30,760,48,41,33,255,185,35,29,31,26
"""
    
    try:    
        i=0
        while True:
            if monster_stat_lookup_table.split("\n")[i].split(",")[0] == str(CR):
                cr_line = i
                break
            else:
                i+=1
    except IndexError:
        raise IndexError("Desired CR ("+str(CR)+") not found")
    
    try:
        i = 0
        while True:
            if monster_stat_lookup_table.split("\n")[0].split(",")[i] == stat_name:
                stat_index = i
                break
            else:
                i+=1
    except IndexError:
        raise IndexError("Desired stat not found")
        
    return int( monster_stat_lookup_table.split("\n")[cr_line].split(",")[stat_index] )
        
def set_cr(input_dict):
    """
    This is the main function that will build the stat block, based on a
    dictionary containing the difficulty mod, apl, number of characters
    and number of enemies. It returns another dictionary containing a
    stat block for the enemies.
    """
    output = {}
    output["CR"] = input_dict["difficulty_mod"] + input_dict["average_party_level"] + adjust_average_party_level(input_dict["average_party_level"], input_dict["no_of_chars"]) - get_cr_mod_for_creatures(input_dict["no_of_enemies"])
    
    for stat in ["CR","Hit Points","Armor Class","Attack (High)","Attack (Low)","Average Damage High","Average Damage Low","Ability DC (Primary)","Ability DC (Secondary)","Save (Good)","Save (Poor)"]:
       output[stat] = lookup_stat(stat, output["CR"])
       
    output["BAB"] = get_bab(output["Hit Points"], output["Attack (High)"], output["Attack (Low)"])
        
    output["CR"] += get_cr_mod_for_creatures(input_dict["no_of_enemies"])
    return output
    
def get_cr_mod_for_creatures(no_of_creatures):
    """
    Table source: http://www.d20pfsrd.com/gamemastering/
    The table itself is released under the Open Game License.
    """
    if no_of_creatures == 1:
        return 0
    if no_of_creatures == 2:
        return 2
    if no_of_creatures == 3:
        return 3
    if no_of_creatures in range(4,6):
        return 4
    if no_of_creatures in range(6,8):
        return 5
    if no_of_creatures in range(8,12):
        return 6
    if no_of_creatures in range(12,16):
        return 7
    if no_of_creatures in range(16,20):
        return 8
    raise IndexError("Too many creatures, maybe try mass combat?")
    
def adjust_average_party_level(apl, no_of_players):
    """
    No source for this one, it's arbitrary. Most folks recommend APL-1 for 3 players and +1 for 5 players,
    but not much else. Beyond that, it now scales as x*2 (e.g. apl is -4 for 2 players, -8 for 1)
    Todo: make this work a wee bit better close to apl=0
    """
    if no_of_players <= 2 or no_of_players >=6:
        print("Warning: values for strange party sizes are strictly approximate.")
    diff = no_of_players - 4
    if diff+apl>0:
        return int((diff * abs(diff)*0.5)) # we'll try this and see how it goes
    else:
        return apl-2
        
def get_bab(hp, attack_max, attack_min):
    """
    Again, this is a rule of thumb. For a faster creature, the BAB will be higher, for a slower one it
    will be lower. Additionally, if the creature type has lower hit die, the BAB will be higher,
    and vice-versa. But please accept this as a rule of thumb :)
    I have not given the CMB and CMD - those are entirely up to you - it depends if your enemy has a lot
    of STR or DEX.
    """
    bab_from_attack = int( (attack_max+attack_min)/2 - 20)
    bab_from_hp = int( hp*0.1*0.75 )
    return max(bab_from_attack, bab_from_hp)

if __name__ == "__main__" and sys.stdout.isatty():
    args = parser.parse_args()
    if args.apl == -1:
        raise IOError("Please supply an average party level (run this script with the -h flag for instructions)")
    input_dict = {}
    input_dict["no_of_chars"] = args.players
    input_dict["average_party_level"] = args.apl
    input_dict["no_of_enemies"] = args.enemies
    input_dict["difficulty_mod"] = args.difficulty # 0=normal, 3=epic, -1 = easy
    output = set_cr(input_dict)
    print("\nEncounter with "+str(args.players)+" players at average level "+str(args.apl)+" with "+str(args.enemies)+" enemies at difficulty mod "+str(args.difficulty)+":")

    longest_string_length = len("Ability DC (Secondary)")
        
    for key, value in sorted(output.items()):
        len_diff = longest_string_length - len(key)
        spaces = " "*len_diff
        print(str(key)+spaces+" : "+str(value))
