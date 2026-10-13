import pokebase as pb
import sys

desired_dex = 'original-unova'

if len(sys.argv) > 1:
	desired_dex = sys.argv[1]
dex = pb.APIResource('pokedex', desired_dex)

def clean_up_name(name):
	return name.replace('-', ' ').title()

def find_species(chain, pokemon_name):
	for link in chain.evolves_to:
		if link.species.name == pokemon_name:
			return chain
		if len(link.evolves_to) > 0:
			return find_species(link, pokemon_name)
	return

for entry in dex.pokemon_entries:
	species = entry.pokemon_species
	txt = "{}: {}".format(str(entry.entry_number).zfill(3), clean_up_name(species.name))
	chain = pb.APIResource('pokemon-species', species.name).evolution_chain.chain
	if chain:
		while chain.species.name != species.name:
			index = 0
			for x in range(0, len(chain.evolves_to)):
				if (chain.evolves_to[x].species.name == species.name):
					index = x
			chain = chain.evolves_to[index]
		#if chain.species.name != species.name:
		#	chain = find_species(chain, species.name)
		#if chain:
		#	details = chain.evolution_details
		details = chain.evolution_details
		if details:
			txt = txt + ": Evolves from " + clean_up_name(species.evolves_from_species.name)
			if details[0].trigger.name == 'level-up':
				if details[0].min_level:
					txt = txt + " at level " + str(details[0].min_level)
				else:
					txt = txt + " when leveled up"
			elif details[0].trigger.name == 'use-item':
				txt = txt + " when exposed to " + clean_up_name(details[0].item.name)
			elif details[0].trigger.name == 'trade':
				txt = txt + " when traded"
			else:
				txt = txt + " by doing something weird"
			if details[0].location:
				txt = txt + " at " + clean_up_name(details[0].location)
			if details[0].held_item:
				txt = txt + " while holding " + clean_up_name(details[0].held_item.name)
			if details[0].relative_physical_stats == 1:
				txt = txt + " with Attack greater than Defense"
			elif details[0].relative_physical_stats == 0:
				txt = txt + " with Attack equal to Defense"
			elif details[0].relative_physical_stats == -1:
				txt = txt + " with Defense greater than Attack"
			if details[0].known_move:
				txt = txt + " while knowing " + clean_up_name(details[0].known_move.name)
			if details[0].known_move_type:
				txt = txt + " while knowing a " + clean_up_name(details[0].known_move_type.name) + "-type move"
			if details[0].party_type:
				txt = txt + " with a " + clean_up_name(details[0].party_type.name) + "-type Pokemon in the party"
			if details[0].min_happiness:
				txt = txt + " with friendship " + str(details[0].min_happiness)
			if details[0].min_beauty:
				txt = txt + " with beauty " + str(details[0].min_beauty)
			if details[0].min_affection:
				txt = txt + " with affection " + str(details[0].min_affection)
			if details[0].near_special_rock:
				txt = txt + " near a special rock"
			if details[0].needs_overworld_rain:
				txt = txt + " in rain"
			if details[0].gender == 1:
				txt = txt + " (female only)"
			elif details[0].gender == 2:
				txt = txt + " (male only)"
			elif details[0].gender == 3:
				txt = txt + " (genderless only)"
	print(txt)
