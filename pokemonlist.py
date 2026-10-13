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

def get_name(thing, language):
	for localized_name in thing.names:
		if localized_name.language.name == desired_language:
			return localized_name.name
	return thing.name

def get_form_name(form, language):
	for localized_name in form.form_names:
		if localized_name.language.name == desired_language:
			return localized_name.name
	return ""

def find_species(chain, pokemon_name):
	for link in chain.evolves_to:
		if link.species.name == pokemon_name:
			return link 
		if len(link.evolves_to) > 0:
			return find_species(link, pokemon_name)
	return

def pokemon_exists_in_dex(species_name):
	for entry in dex.pokemon_entries:
		if entry.pokemon_species.name == species_name:
			return True
	return False

def get_evolution_info(species_name):
	chain = pb.APIResource('pokemon-species', species_name).evolution_chain.chain
	details = None
	txt = ""
	if chain:
		if chain.species.name != species.name:
			chain = find_species(chain, species.name)
		if chain:
			details = chain.evolution_details
		if details and pokemon_exists_in_dex(species.evolves_from_species.name):
			txt = txt + ": Evolves from " + get_name(species.evolves_from_species, desired_language)
			if details[0].required_pokemon_form:
				form_name = get_form_name(details[0].required_pokemon_form, desired_language)
				if form_name != "":
					txt = txt + " (" + form_name + ")"
			if details[0].trigger.name == 'level-up':
				if details[0].min_level:
					txt = txt + " starting at level " + str(details[0].min_level)
				else:
					txt = txt + " when leveled up"
			elif details[0].trigger.name == 'in-battle-level-up':
				txt = txt + " when leveled up in battle starting at level " + str(details[0].min_level)
			elif details[0].trigger.name == 'use-item':
				txt = txt + " when exposed to " + get_name(details[0].item, desired_language)
			elif details[0].trigger.name == 'trade':
				txt = txt + " when traded"
			elif details[0].trigger.name == 'use-move':
				txt = txt + " after using " + get_name(details[0].used_move, desired_language)
				if details[0].min_move_count:
					txt = txt + " " + str(details[0].min_move_count) + " times"
			elif details[0].trigger.name == 'three-defeated-bisharp':
				txt = txt + " after defeating 3 " + get_name(pb.APIResource('pokemon-species', 'bisharp'), desired_language) + " that hold a " + get_name(pb.APIResource('item', 'leaders-crest'), desired_language)
			elif details[0].trigger.name == 'gimmighoul-coins':
				txt = txt + "when leveled up while having at least 999 " + get_name(pb.APIResource('pokemon-species', 'gimmighoul'), desired_language) + " Coins"
			elif details[0].trigger.name == 'shed':
				txt = txt + " starting at level 20 with an empty slot in the party"
				txt = txt + " and at least 1 " + get_name(pb.APIResource('item', 'poke-ball'), desired_language) + " in the bag"
			elif details[0].trigger.name == 'spin':
				txt = txt + " by spinning around while holding a Sweet"
			elif details[0].trigger.name == 'three-critical-hits':
				txt = txt + " after landing 3 critical hits in a single battle"
			elif details[0].trigger.name == 'take-damage':
				if species.name == 'runerigus':
					txt = txt + " while standing under an arch"
				txt = txt + " after taking " + str(details[0].min_damage_taken) + " points of damage without fainting"
			elif details[0].trigger.name == 'recoil-damage':
				txt = txt + " after taking " + str(details[0].min_damage_taken) + " points of recoil damage without fainting"
			elif details[0].trigger.name == 'agile-style-move':
				txt = txt + " after using " + get_name(details[0].used_move, desired_language) + " in the agile style"
				if details[0].min_move_count:
					txt = txt + " " + str(details[0].min_move_count) + " times"
			elif details[0].trigger.name == 'strong-style-move':
				txt = txt + " after using " + get_name(details[0].used_move, desired_language) + " in the strong style"
				if details[0].min_move_count:
					txt = txt + " " + str(details[0].min_move_count) + " times"
			elif details[0].trigger.name == 'meltan-candies':
				txt = txt + " after using 400 " + get_name(pb.APIResource('item', 'meltan-candy'), desired_language) + " (only in Pokemon Go)"
			elif details[0].trigger.name == 'tower-of-darkness' or details[0].trigger.name == 'tower-of-waters':
				txt = txt + " when evolved at " + get_name(pb.APIResource('location', 'tower-of-darkness'), desired_language) + " or " + get_name(pb.APIResource('location', 'tower-of-waters'), desired_language)
			else:
				txt = txt + " by doing something weird"
			if details[0].location:
				txt = txt + " at " + get_name(details[0].location, desired_language)
			if details[0].held_item and details[0].trigger.name != 'spin':
				txt = txt + " while holding " + get_name(details[0].held_item, desired_language)
			if details[0].relative_physical_stats == 1:
				txt = txt + " with Attack greater than Defense"
			elif details[0].relative_physical_stats == 0:
				txt = txt + " with Attack equal to Defense"
			elif details[0].relative_physical_stats == -1:
				txt = txt + " with Defense greater than Attack"
			if details[0].known_move:
				txt = txt + " while knowing " + get_name(details[0].known_move, desired_language)
			if details[0].known_move_type:
				txt = txt + " while knowing a " + get_name(details[0].known_move_type, desired_language) + "-type move"
			if details[0].party_type:
				txt = txt + " with a " + get_name(details[0].party_type, desired_language) + "-type Pokemon in the party"
			if details[0].min_happiness:
				txt = txt + " with friendship " + str(details[0].min_happiness)
			if details[0].min_beauty:
				txt = txt + " with beauty " + str(details[0].min_beauty)
			if details[0].min_affection:
				txt = txt + " with affection " + str(details[0].min_affection)
			if details[0].min_steps:
				txt = txt + " when leveled up outside of a ball after walking " + str(details[0].min_steps) + " steps"
			if details[0].turn_upside_down:
				txt = txt + " while holding the device upside down"
			if details[0].near_special_rock:
				txt = txt + " near a special rock"
			if details[0].needs_overworld_rain:
				txt = txt + " in rain"
			if details[0].time_of_day and details[0].time_of_day != "" and details[0].trigger.name != 'spin':
				txt = txt + " during " + details[0].time_of_day
			if details[0].gender == 1:
				# Basculegion and Meowstic have different forms depending on gender, but we
				# don't care about that. Should probably come up with a better check for this
				# instead of just special-casing these, but this will do for now.
				if species.name != 'basculegion' and species.name != 'meowstic':
					txt = txt + " (female only)"
			elif details[0].gender == 2:
				if species.name != 'basculegion' and species.name != 'meowstic':
					txt = txt + " (male only)"
			elif details[0].gender == 3:
				txt = txt + " (genderless only)"
	return txt

for entry in dex.pokemon_entries:
	species = entry.pokemon_species
	txt = get_name(species, desired_language)
	if include_number:
		txt = "{}: {}".format(str(entry.entry_number).zfill(padding_digits), txt)
	if include_evolution_info:
		txt = txt + get_evolution_info(species.name)
	print(txt)
