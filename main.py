import random

from creatures import Fighter, Ranger, Tarrasque, Wizard
from initiative_queue import Queue
from faker import Faker


def gen_fighter(name):
    return Fighter(name, 20)

def gen_ranger(name):
    return Ranger(name, 20)

def gen_wizard(name):
    return Wizard(name, 20)

FAKE = Faker()

NAMES = [FAKE.name() for _ in range(100)]

winning_parties = []
class_gen_functions = [gen_fighter, gen_ranger, gen_wizard]


def build_battle(party, boss):
    combat = [char for char in party]
    combat.append(boss)

    for creature in combat:
        creature.get_initiative()

    combat.sort(key=lambda x: x.initiative, reverse=True)

    combat_queue = Queue()
    for creature in combat:
        combat_queue.enqueue(creature)

    return combat_queue


def simulation():
    # Generate a random party and build Tarrasque
    party = [random.choice(class_gen_functions)(random.choice(NAMES)) for _ in range(6)]
    tarrasque = Tarrasque()


    # Place party members and Tarrasque in circular queue after initiative rolls.
    combat_queue = build_battle(party, tarrasque)

    # Party 'fights' Tarrasque until they're dead or the Tarrasque dies.
    while len(party) > 0 and tarrasque.hp > 0:
        print(f'\n{len(party)} party members remain!')
        print(f'TARRASQUE HP: {tarrasque.hp}\n')
        combatant = combat_queue.dequeue()
        if combatant.name != 'the Tarrasque' and combatant.cr_class != 'Wizard':
            att_roll = combatant.get_attack_roll()
            combatant.attack(att_roll, tarrasque)
        elif combatant.cr_class == 'Wizard':
            combatant.cast_spell(tarrasque)
        else:
            att_roll = tarrasque.get_attack_roll()

            """Selects a random attack method from the Tarrasque's dictionary of possible attack methods and performs 
            the attack. """
            t_move_value = str(random.randint(1, len(tarrasque.attack_dict)))
            att_method = tarrasque.attack_dict.get(t_move_value)

            if att_method.__name__ == 'spines':
                att_method([random.choice(party) for _ in range(random.randint(1,6))])
            else:
                att_method(att_roll, random.choice(party))

            #TODO: Regeneration makes it impossible for the party to win.
            # tarrasque.regeneration()

        party = [member for member in party if member.hp > 0]
        print()
        for member in party:
            print(f'{member.name}, has {member.hp} HP')

        if combatant.hp > 0:
            combat_queue.enqueue(combatant)

    # If the party was victorious, store the victors from the party and return them.
    if len(party) > 0:
        victors = [(member.name, member.cr_class, member.hp) for member in party]
        return victors
    else:
        return tarrasque


battle_tracker = {}
wins = 0
simulations = 1000
for round in range(simulations):
    results = simulation()

    if type(results) == list:
        battle_tracker[f'simulation {round+1}'] = results
        wins += 1
    else:
        battle_tracker[f'simulation {round+1}'] = results

for k, v in battle_tracker.items():
    if isinstance(v, list):
        print(f'{k.title()}: \n')
        print(f' *** VICTORY! ***\n')
        for character in v:
            print(f'Name: {character[0]}')
            print(f'Class: {character[1]}')
            print(f'HP Remaining: {character[2]}')
            print()
    else:
        print(f'{k.title()}: {v.name.title()} with {v.hp} HP remaining')

print(f'The party was victorious {wins/simulations*100:.5f}% of the time.')


