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
#remake_map = {
#	'firered-leafgreen': 'red-blue',
#	'heartgold-soulsilver': 'gold-silver',
#	'omega-ruby-alpha-sapphire': 'ruby-sapphire',
#	'brilliant-diamond-shining-pearl': 'diamond-pearl'
#}

if len(sys.argv) > 1:
	desired_dex = sys.argv[1]
dex = pb.APIResource('pokedex', desired_dex)
version_group_list = pb.APIResourceList('version-group')

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

def dex_get_gen(dex):
	gen_list = pb.APIResourceList('generation')
	for group in dex.version_groups:
		for item in gen_list:
			gen = pb.APIResource('generation', item['name'])
			for gen_group in gen.version_groups:
				if gen_group.name == group.name:
					return gen

# This is not used... yet
#def find_closest_version_group(requested_group):
#	closest_order = 0
#	closest_group = None
#	for item in version_group_list:
#		group = pb.APIResource('version-group', item['name'])
#		if group.order > closest_order and group.order <= requested_group.order:
#			closest_order = group.order
#			closest_group = group
#	return closest_group

def find_best_details_index(details):
	for index, evolution in enumerate(details):
		for vg in dex.version_groups:
			debug_print("Checking " + evolution.version_group.name + " against " + vg.name)
			if evolution.version_group.name == vg.name:
				return index
	debug_print("No matching details found. Using default evolution")
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
				# In Legends Arceus, evolutions that are normally trade evolutions are done using
				# either the item the Pokemon would normally need to hold during the trade, or if
				# none, a Linking Cord. PokeAPI does not treat these as a separate evolution
				# trigger, so we have to do it ourselves.
				if dex.name == 'hisui':
					if not details[index].held_item:
						txt = txt + " when exposed to " + get_name(pb.APIResource('item', 'linking-cord'), desired_language)
					else:
						txt = txt + " when exposed to " + get_name(pb.APIResource('item', details[index].held_item.name), desired_language)
				else:
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
					if details[index].location:
						txt = txt + " at " + get_name(details[index].location, desired_language)
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
				# in the case of Runerigus, we already printed the name of the location (to make
				# the sentence less awkward), so don't print it again
				if species.name != 'runerigus':
					txt = txt + " at " + get_name(details[index].location, desired_language)
			if details[index].held_item and details[index].trigger.name != 'spin':
				# If it's Hisui and it's a trade evolution, we already printed the name of the
				# required item earlier, so don't do it here
				if not (dex.name == 'hisui' and details[index].trigger.name == 'trade'):
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
				# PokeAPI's data does not seem to account for the minimum friendship value
				# changing globally in gen 8, so some Pokemon have a value of 160 and others
				# have 220 depending on when the evolution was introduced. Because of this,
				# we are just ignoring the value from the API and setting it based on the gen
				# instead. I don't like this, but it seems necessary.
				if (not gen) or (gen.id >= 8):
					min_happiness = 160
				else:
					min_happiness = 220
				txt = txt + " with friendship " + str(min_happiness)
			if details[index].min_beauty:
				txt = txt + " with beauty " + str(details[index].min_beauty)
			if details[index].min_affection:
				if gen and (gen.id == 6 or gen.id == 7):
					txt = txt + " with affection " + str(details[index].min_affection)
			if details[index].min_steps:
				txt = txt + " when leveled up outside of a ball after walking " + str(details[index].min_steps) + " steps"
			if details[index].turn_upside_down:
				txt = txt + " while holding the device upside down"
			if details[index].near_special_rock:
				txt = txt + " near "
				if species.name == 'leafeon':
					txt = txt + "a Moss Rock"
				elif species.name == 'glaceon':
					txt = txt + "an Ice Rock"
				else:	# should never happen but just in case
					txt = txt + "a special rock"
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
			elif details[index].gender == 3:	# not currently used afaik
				txt = txt + " (genderless only)"
	return txt

gen = dex_get_gen(dex)

for entry in dex.pokemon_entries:
	species = entry.pokemon_species
	txt = get_name(species, desired_language)
	if include_number:
		txt = "{}: {}".format(str(entry.entry_number).zfill(padding_digits), txt)
	if include_evolution_info:
		txt = txt + get_evolution_info(species.name)
	print(txt)
