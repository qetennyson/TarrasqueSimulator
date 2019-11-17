import random
from weapons import TwoHandedSword, CompositeLongbow
from spells import Spell
from collections import namedtuple

#TODO: Add Armor!

class Creature:

    def __init__(self, name, lvl):
        self.name = name
        self.lvl = lvl
        self.stats = {
            'int': self.gen_scores(4),
            'str': self.gen_scores(4),
            'dex': self.gen_scores(4),
            'cha': self.gen_scores(4),
            'wis': self.gen_scores(4),
            'con': self.gen_scores(4),
        }
        self.hp = sum([random.randint(1, 8) for _ in range(self.lvl)])
        self.ac = 10 + self.stats.get('dex') + 1
        self.initiative = 0

    def gen_scores(self, rolls):
        scores = [random.randint(1, 6) for i in range(rolls)]
        if len(scores) > 1:
            scores.remove(min(scores))

        return sum(scores)

    def get_initiative(self):
        self.initiative = self.stats.get('dex') + random.randint(1, 20)

    def get_attack_roll(self):
        BAB = 5
        modifier = ((self.stats.get('str') - 10 // 2))
        return random.randint(1, 20) + BAB + modifier

    def __repr__(self):
        output = f'\n{self.name}\n HP: {self.hp} Init: {self.initiative} \n\n'
        for k, v in self.stats.items():
            output += f'{k.title()}: {v}\n'
        return output

class Fighter(Creature):
    def __init__(self, name, lvl):
        super().__init__(name, lvl)
        self.cr_class = 'Fighter'
        self.stats = {
            'int': self.gen_scores(4),
            'str': self.gen_scores(4) + 5,
            'dex': self.gen_scores(4),
            'cha': self.gen_scores(4),
            'wis': self.gen_scores(4),
            'con': self.gen_scores(4),
        }
        self.hp = sum([random.randint(1, 10) for _ in range(self.lvl)])
        self.ac = self.stats.get('dex') + 8
        self.weapon = TwoHandedSword(True)

    def get_attack_roll(self):
        BAB = 15
        modifier = ((self.stats.get('str') - 10 // 2))
        return random.randint(1, 20) + BAB + modifier if not self.weapon.masterwork \
            else random.randint(1, 20) + BAB + modifier + 1

    def attack(self, a_roll, target):

        if a_roll > target.ac:
            damage = self.weapon.damage * self.weapon.crit if a_roll < 18 \
                else self.weapon.damage * self.weapon.crit + 1

            target.hp -= int(damage)

            print(f'{self.name} attacks {target.name} for {int(damage)}!')
        else:
            print(f'{self.name} misses {target.name}.')

class Ranger(Creature):
    def __init__(self, name, lvl):
        super().__init__(name, lvl)
        self.cr_class = 'Ranger'
        self.stats = {
            'int': self.gen_scores(4),
            'str': self.gen_scores(4),
            'dex': self.gen_scores(4) + 5,
            'cha': self.gen_scores(4),
            'wis': self.gen_scores(4),
            'con': self.gen_scores(4),
        }
        self.hp = sum([random.randint(1, 10) for _ in range(self.lvl)])
        self.ac = 10 + self.stats.get('dex') + 3
        self.weapon = CompositeLongbow(True)

    def get_attack_roll(self):
        BAB = 15
        modifier = ((self.stats.get('str') - 10 // 2))
        return random.randint(1, 20) + BAB + modifier if not self.weapon.masterwork \
            else random.randint(1, 20) + BAB + modifier + 1

    def attack(self, a_roll, target):
        damage = self.weapon.damage if a_roll < 18 \
            else self.weapon.damage * self.weapon.crit
        if a_roll > target.ac:
            target.hp -= int(damage)

            print(f'{self.name} shoots {target.name} for {int(damage)}!')
        else:
            print(f'{self.name} misses {target.name}.')

class Wizard(Creature):
    def __init__(self, name, lvl):
        super().__init__(name, lvl)
        self.cr_class = 'Wizard'
        self.stats = {
            'int': self.gen_scores(4) + 5,
            'str': self.gen_scores(4),
            'dex': self.gen_scores(4),
            'cha': self.gen_scores(4),
            'wis': self.gen_scores(4),
            'con': self.gen_scores(4),
        }
        self.hp = sum([random.randint(1, 6) for _ in range(self.lvl)])
        self.ac = 10 + self.stats.get('dex') + 3

        self.spellbook = {
            '1': Spell('Clashing Rocks', 9, 'smash', sum([random.randint(1,6) for _ in range(1,20)]), 4),
            '2': Spell('Stormbolts', 8, 'shock', sum([random.randint(1,8) for _ in range(1,20)]), 4),
            '3': Spell('Greater Shout', 8, 'yell', sum([random.randint(1,6) for _ in range(1,10)]), 4),
            '4': Spell('Finger of Death', 7, 'ray', 10*self.lvl, 4),
            '5': Spell('Caustic Eruption', 7, 'acid', sum([random.randint(1,6) for _ in range(1,self.lvl)]), 4),
        }

    def cast_spell(self, target):
        try:
            spell_num = random.choice(list(self.spellbook.keys()))
        except:
            return None

        spell = self.spellbook.get(spell_num)
        damage = spell.damage
        spell_power = spell.lvl + 10 + 4

        if target.saving_throw(spell, self) < spell_power:
            target.hp -= damage
            print(f'{self.name} the Wizard, hits the Tarrasque with {spell.name} for {damage} damage!')
        elif spell.name == 'Stormbolts':
            target.hp -= damage // 2
            print(f'{self.name} the Wizard, casts {spell.name}.  It grazes the Tarrasque dealing {damage // 2}!')
        else:
            print(f'The {target.name} dodged the spell effects!')

        if spell.max_casts == 0:
            self.spellbook.pop(spell_num)



class Tarrasque(Creature):

    def __init__(self, name='the Tarrasque', lvl=30):
        super().__init__(name, lvl)
        self.name = name
        self.cr_class = 'Monster'
        self.stats = {
            'int': self.gen_scores(2),
            'str': self.gen_scores(10),
            'dex': self.gen_scores(4),
            'cha': self.gen_scores(3),
            'wis': self.gen_scores(3),
            'con': self.gen_scores(10),
        }
        self.hp = sum([random.randint(1, 10) for _ in range(self.lvl)]) + 360
        self.ac = 40

        self.attack_dict = {
            '1': self.bite,
            '2': self.claws,
            '3': self.tail_slap,
            '4': self.spines,
        }

    def saving_throw(self, spell, caster):
        if spell.type not in ['ray', 'cone', 'line', 'magicmissle']:
            return random.randint(1,20) + 2 + 3
        else:
            if random.randint(1,3) == 1:
                caster.hp -= spell.damage
            return 99


    def regeneration(self):
        self.hp += 40

    def spines(self, targets):
        for target in targets:
            if self.get_attack_roll() > target.ac:
                damage = (sum([random.randint(1,10) for _ in range(2)]) + 15) * 3
                target.hp -= damage

                print(f'{self.name} launches a spine at {target.name}, it hits for {damage}')
            else:
                print(f'{self.name} launches a spine, but it misses!')

    def bite(self, a_roll, target):
        if a_roll > target.ac:
            damage = (sum([random.randint(1, 8) for _ in range(4)]) + 15 + random.randint(15, 20)) * 3

            print(f'{self.name} bites {target.name} for {damage} damage')

            target.hp -= damage

        else:
            print(f'{self.name} misses {target.name}.')

    def claws(self, a_roll, target):
        if a_roll > target.ac:
            damage = random.randint(1, 12) + 15 + 37

            print(f'{self.name} claws {target.name} for {damage} damage')

            target.hp -= damage

        else:
            print(f'{self.name} misses {target.name}.')

    def tail_slap(self, a_roll, target):
        if a_roll > target.ac:
            damage = sum([random.randint(1, 8) for _ in range(3)]) + 7 + 32

            print(f'{self.name} tail slaps {target.name} for {damage} damage')

            target.hp -= damage

        else:
            print(f'{self.name} misses {target.name}.')

    def __repr__(self):
        output = f'\n{self.name}\nHP: \
        {self.hp} Init: {self.initiative} \n\n'
        for k, v in self.stats.items():
            output += f'{k.title()}: {v}\n'
        return output

