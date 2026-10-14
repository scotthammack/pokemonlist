import pokebase as pb
import sys

### Options
desired_dex = 'kanto'
desired_language = 'en'
include_number = True
pad_number = True
include_evolution_info = True
print_debug_messages = False


### Defaults
padding_digits = 1	# will be set to either 3 or 4 later depending on dex if pad_number is true
gen = None

# There's gotta be a better way of doing this but I can't think of it right now.
ignore_forms_list = ['burmy', 'shellos', 'deerling', 'flabebe', 'floette', 'pumpkaboo']

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

if pad_number:
	padding_digits = 3
	if len(dex.pokemon_entries) > 999:
		padding_digits = 4

def debug_print(txt):
	if print_debug_messages:
		print(txt)

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
	return None

def pokemon_exists_in_dex(species_name):
	for entry in dex.pokemon_entries:
		if entry.pokemon_species.name == species_name:
			return True
	return False

def dex_get_gen_name(dex):
	gen_list = pb.APIResourceList('generation')
	for group in dex.version_groups:
		for gen in gen_list:
			gen_groups = pb.APIResource('generation', gen['name']).version_groups
			for gen_group in gen_groups:
				if gen_group.name == group.name:
					return gen['name']

def find_best_details_index(details):
	for x in range(0, len(details)):
		for vg in dex.version_groups:
			debug_print("Checking " + details[x].version_group.name + " against " + vg.name)
			if details[x].version_group.name == vg.name:
				return x
	debug_print("No matching details found. Using default")
	return 0

def get_evolution_info(species_name):
	chain = pb.APIResource('pokemon-species', species_name).evolution_chain.chain
	details = None
	txt = ""
	if chain:
		if chain.species.name != species.name:
			chain = find_species(chain, species.name)
		if chain:
			details = chain.evolution_details
			index = find_best_details_index(details)
		if details and pokemon_exists_in_dex(species.evolves_from_species.name):
			txt = txt + ": Evolves from " + get_name(species.evolves_from_species, desired_language)
			if details[index].required_pokemon_form and not species.evolves_from_species.name in ignore_forms_list:
				form_name = get_form_name(details[index].required_pokemon_form, desired_language)
				if form_name != "":
					txt = txt + " (" + form_name + ")"
			if details[index].trigger.name == 'level-up':
				if details[index].min_level:
					txt = txt + " starting at level " + str(details[index].min_level)
				else:
					txt = txt + " when leveled up"
			elif details[index].trigger.name == 'in-battle-level-up':
				txt = txt + " when leveled up in battle starting at level " + str(details[index].min_level)
			elif details[index].trigger.name == 'use-item':
				txt = txt + " when exposed to " + get_name(details[index].item, desired_language)
			elif details[index].trigger.name == 'trade':
				txt = txt + " when traded"
			elif details[index].trigger.name == 'use-move':
				txt = txt + " after using " + get_name(details[index].used_move, desired_language)
				if details[index].min_move_count:
					txt = txt + " " + str(details[index].min_move_count) + " times"
			elif details[index].trigger.name == 'three-defeated-bisharp':
				txt = txt + " after defeating 3 " + get_name(pb.APIResource('pokemon-species', 'bisharp'), desired_language) + " that hold a " + get_name(pb.APIResource('item', 'leaders-crest'), desired_language)
			elif details[index].trigger.name == 'gimmighoul-coins':
				txt = txt + "when leveled up while having at least 999 " + get_name(pb.APIResource('item', 'gimmighoul-coin'), desired_language) + "s"
			elif details[index].trigger.name == 'shed':
				txt = txt + " starting at level 20 with an empty slot in the party"
				if dex.name != 'hoenn':
					txt = txt + " and at least 1 " + get_name(pb.APIResource('item', 'poke-ball'), desired_language) + " in the bag"
			elif details[index].trigger.name == 'spin':
				txt = txt + " by spinning around while holding a Sweet"
			elif details[index].trigger.name == 'three-critical-hits':
				txt = txt + " after landing 3 critical hits in a single battle"
			elif details[index].trigger.name == 'take-damage':
				if species.name == 'runerigus':
					txt = txt + " while standing under an arch"
				txt = txt + " after taking " + str(details[index].min_damage_taken) + " points of damage without fainting"
			elif details[index].trigger.name == 'recoil-damage':
				txt = txt + " after taking " + str(details[index].min_damage_taken) + " points of recoil damage without fainting"
			elif details[index].trigger.name == 'agile-style-move':
				txt = txt + " after using " + get_name(details[index].used_move, desired_language) + " in the agile style"
				if details[index].min_move_count:
					txt = txt + " " + str(details[index].min_move_count) + " times"
			elif details[index].trigger.name == 'strong-style-move':
				txt = txt + " after using " + get_name(details[index].used_move, desired_language) + " in the strong style"
				if details[index].min_move_count:
					txt = txt + " " + str(details[index].min_move_count) + " times"
			elif details[index].trigger.name == 'meltan-candies':
				txt = txt + " after using 400 " + get_name(pb.APIResource('item', 'meltan-candy'), desired_language) + " (only in Pokemon Go)"
			elif details[index].trigger.name == 'tower-of-darkness' or details[index].trigger.name == 'tower-of-waters':
				txt = txt + " when evolved at " + get_name(pb.APIResource('location', 'tower-of-darkness'), desired_language) + " or " + get_name(pb.APIResource('location', 'tower-of-waters'), desired_language)
			else:
				txt = txt + " by doing something weird"
			if details[index].location:
				txt = txt + " at " + get_name(details[index].location, desired_language)
			if details[index].held_item and details[index].trigger.name != 'spin':
				txt = txt + " while holding " + get_name(details[index].held_item, desired_language)
			if details[index].relative_physical_stats == 1:
				txt = txt + " with Attack greater than Defense"
			elif details[index].relative_physical_stats == 0:
				txt = txt + " with Attack equal to Defense"
			elif details[index].relative_physical_stats == -1:
				txt = txt + " with Defense greater than Attack"
			if details[index].known_move:
				txt = txt + " while knowing " + get_name(details[index].known_move, desired_language)
			if details[index].known_move_type:
				txt = txt + " while knowing a " + get_name(details[index].known_move_type, desired_language) + "-type move"
			if details[index].party_type:
				txt = txt + " with a " + get_name(details[index].party_type, desired_language) + "-type Pokemon in the party"
			if details[index].min_happiness:
				txt = txt + " with friendship " + str(details[index].min_happiness)
			if details[index].min_beauty:
				txt = txt + " with beauty " + str(details[index].min_beauty)
			if details[index].min_affection:
				if gen_name == 'generation-vi' or gen_name == 'generation-vii':
					txt = txt + " with affection " + str(details[index].min_affection)
			if details[index].min_steps:
				txt = txt + " when leveled up outside of a ball after walking " + str(details[index].min_steps) + " steps"
			if details[index].turn_upside_down:
				txt = txt + " while holding the device upside down"
			if details[index].near_special_rock:
				txt = txt + " near a special rock"
			if details[index].needs_overworld_rain:
				txt = txt + " in rain"
			if details[index].time_of_day and details[index].time_of_day != "" and details[index].trigger.name != 'spin':
				txt = txt + " during " + details[index].time_of_day.replace('-', ' ')
			if details[index].gender == 1:
				# Basculegion and Meowstic have different forms depending on gender, but we
				# don't care about that. Should probably come up with a better check for this
				# instead of just special-casing these, but this will do for now.
				if species.name != 'basculegion' and species.name != 'meowstic':
					txt = txt + " (female only)"
			elif details[index].gender == 2:
				if species.name != 'basculegion' and species.name != 'meowstic':
					txt = txt + " (male only)"
			elif details[index].gender == 3:
				txt = txt + " (genderless only)"
	return txt

gen_name = dex_get_gen_name(dex)

debug_print("Generation: " + str(gen_name))
for entry in dex.pokemon_entries:
	species = entry.pokemon_species
	txt = get_name(species, desired_language)
	if include_number:
		txt = "{}: {}".format(str(entry.entry_number).zfill(padding_digits), txt)
	if include_evolution_info:
		txt = txt + get_evolution_info(species.name)
	print(txt)
