import pokebase as pb
import sys

desired_dex = 'kanto'
desired_language = 'en'
include_number = True
pad_number = True
include_evolution_info = True

if len(sys.argv) > 1:
	desired_dex = sys.argv[1]
dex = pb.APIResource('pokedex', desired_dex)

try:
	dex.id
except:
	print("Dex not found. Available dexes:")
	dex_list = pb.APIResourceList('pokedex')
	for result in dex_list:
		print("\t" + result["name"])
	quit()

padding_digits = 1
if pad_number:
	padding_digits = 3
	if len(dex.pokemon_entries) > 999:
		padding_digits = 4

def get_name_in_language(thing, language):
	for localized_name in thing.names:
		if localized_name.language.name == desired_language:
			return localized_name.name
	return thing.name

def find_species(chain, pokemon_name):
	for link in chain.evolves_to:
		if link.species.name == pokemon_name:
			return link 
		if len(link.evolves_to) > 0:
			return find_species(link, pokemon_name)
	return

def get_evolution_info(species_name):
	chain = pb.APIResource('pokemon-species', species_name).evolution_chain.chain
	details = None
	txt = ""
	if chain:
		if chain.species.name != species.name:
			chain = find_species(chain, species.name)
		if chain:
			details = chain.evolution_details
		if details:
			txt = txt + ": Evolves from " + get_name_in_language(species.evolves_from_species, desired_language)
			if details[0].trigger.name == 'level-up':
				if details[0].min_level:
					txt = txt + " at level " + str(details[0].min_level)
				else:
					txt = txt + " when leveled up"
			elif details[0].trigger.name == 'in-battle-level-up':
				txt = txt + " when leveled up in battle starting at level " + str(details[0].min_level)
			elif details[0].trigger.name == 'use-item':
				txt = txt + " when exposed to " + get_name_in_language(details[0].item, desired_language)
			elif details[0].trigger.name == 'trade':
				txt = txt + " when traded"
			elif details[0].trigger.name == 'use-move':
				txt = txt + " after using " + get_name_in_language(details[0].used_move, desired_language)
				if details[0].min_move_count:
					txt = txt + " " + str(details[0].min_move_count) + " times"
			elif details[0].trigger.name == 'three-defeated-bisharp':
				txt = txt + " after defeating 3 " + get_name_in_language(pb.APIResource('pokemon-species', 'bisharp'), desired_language) + " that hold a " + get_name_in_language(pb.APIResource('item', 'leaders-crest'), desired_language)
			elif details[0].trigger.name == 'gimmighoul-coins':
				txt = txt + "when leveled up while having at least 999 " + get_name_in_language(pb.APIResource('pokemon-species', 'gimmighoul'), desired_language) + " Coins"
			else:
				txt = txt + " by doing something weird"
			if details[0].location:
				txt = txt + " at " + get_name_in_language(details[0].location, desired_language)
			if details[0].held_item:
				txt = txt + " while holding " + get_name_in_language(details[0].held_item, desired_language)
			if details[0].relative_physical_stats == 1:
				txt = txt + " with Attack greater than Defense"
			elif details[0].relative_physical_stats == 0:
				txt = txt + " with Attack equal to Defense"
			elif details[0].relative_physical_stats == -1:
				txt = txt + " with Defense greater than Attack"
			if details[0].known_move:
				txt = txt + " while knowing " + get_name_in_language(details[0].known_move, desired_language)
			if details[0].known_move_type:
				txt = txt + " while knowing a " + get_name_in_language(details[0].known_move_type, desired_language) + "-type move"
			if details[0].party_type:
				txt = txt + " with a " + get_name_in_language(details[0].party_type, desired_language) + "-type Pokemon in the party"
			if details[0].min_happiness:
				txt = txt + " with friendship " + str(details[0].min_happiness)
			if details[0].min_beauty:
				txt = txt + " with beauty " + str(details[0].min_beauty)
			if details[0].min_affection:
				txt = txt + " with affection " + str(details[0].min_affection)
			if details[0].min_steps:
				txt = txt + " after " + str(details[0].min_steps) + " steps"
			if details[0].min_damage_taken:
				txt = txt + " after taking " + str(details[0].min_damage_taken) + " damage"
			if details[0].turn_upside_down:
				txt = txt + " while holding the device upside down"
			if details[0].near_special_rock:
				txt = txt + " near a special rock"
			if details[0].needs_overworld_rain:
				txt = txt + " in rain"
			if details[0].time_of_day and details[0].time_of_day != "":
				txt = txt + " during " + details[0].time_of_day
			if details[0].gender == 1:
				txt = txt + " (female only)"
			elif details[0].gender == 2:
				txt = txt + " (male only)"
			elif details[0].gender == 3:
				txt = txt + " (genderless only)"
	return txt

for entry in dex.pokemon_entries:
	species = entry.pokemon_species
	txt = get_name_in_language(species, desired_language)
	if include_number:
		txt = "{}: {}".format(str(entry.entry_number).zfill(padding_digits), txt)
	if include_evolution_info:
		txt = txt + get_evolution_info(species.name)
	print(txt)
