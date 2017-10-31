# Pathfinder Encounter Maker

Making your own monsters and encounters in Pathfinder? This tool will generate approximate stats for those monsters, using only basic information about your party (average party level, party size, number of monsters, and desired difficulty).

It's not intended to be an all-inclusive monster generator - rather it represents an attempt to help DMs balance the difficulty of their encounters, using Paizo's lookup tables (and a few cludges).

This is a CLI program written in Python 2.7.x. After downloading it, open up a terminal (or cmd, I won't judge) and run it like this:

```sh
python pathfinder_encounter_maker.py --apl 12 --enemies 2 --players 3 --difficulty 0

Encounter with 3 players at average level 12 with 2 enemies at difficulty mod 0:
Ability DC (Primary)   : 19
Ability DC (Secondary) : 13
Armor Class            : 24
Attack (High)          : 18
Attack (Low)           : 13
Average Damage High    : 45
Average Damage Low     : 33
BAB                    : 9
CR                     : 12
Hit Points             : 130
Save (Good)            : 13
Save (Poor)            : 9
```

## Sources

* Most stats: http://paizo.com/pathfinderRPG/prd/bestiary/monsterCreation.html
* Setting CR mod: http://www.d20pfsrd.com/gamemastering/

## License

This program has the GPLv3 license. The pathfinder lookup tables are licensed under the Open Game License.

## Contributions

Are welcome!
