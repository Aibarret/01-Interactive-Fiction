#!/usr/bin/env python3
import sys,os,json,re
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

# Removes Harlowe formatting from Twison description
def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*?)\|([^\]]*?\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->\])]*?)->[^\]]*?\]\]',r'[ \1 ]',description)
    description = re.sub(r'\[\[(.+?)\]\]',r'[ \1 ]',description)
    return description

def update_damage(current,damage):
    if "damage" in current:
        damage += int(current["damage"])
    return damage

def update(current,choice,game_desc):
    if choice == "":
        return current
    for l in current["links"]:
        if l["name"].lower() == choice:
            current = find_passage(game_desc, l["pid"])
            return current
    print("No")
    return current
    

def render(current,damage):
    print("\n\n")
    print("Damage: {damage}".format(damage=damage))
    print("\n\n")
    if damage < 4:
        print(current["name"])
        print(format_passage(current["text"]))
    if damage > 3:
        print("GAME OVER")
    print("\n\n")

def get_input():
    choice = input("What would you like to do? quit to exit ")
    choice = choice.lower().strip()
    return choice



def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    damage = 0


    while choice != "quit" and current != {} or damage > 3:
        current = update(current,choice,game_desc)
        damage = update_damage(current,damage)
        render(current,damage)
        choice = get_input()
    print("GAME OVER")


if __name__ == "__main__":
    main()