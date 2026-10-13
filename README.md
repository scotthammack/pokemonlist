pokemonlist.py
==============
I wrote this because I was annoyed that I couldn't find a plain-text list of all the Pokemon in the Unova
Pokedex. I was trying to "catch 'em all" and I just wanted a simple list so I could cross off Pokemon as I
catch 'em, but every website I found had them formatted in elaborate HTML tables and crap that I couldn't
easily copy and paste. So I wrote this script to grab a Pokedex from PokeAPI, iterate through it, and print
the results so I could dump it into a text file. While I was at it, I realized it would be convenient to
include the evolution requirements too so I wouldn't have to keep looking them up on Bulbapedia, so I added
that too.

This is a work in progress. It currently does most of what I need it to do for now, but is missing some edge
cases (see "Known issues" below). I may or may not get around to adding that stuff later. Also, it's been
forever since I used Python and I don't really know what I'm doing, so I'm sure there are a million ways I
could have written it better.

I think the pokebase library I'm using is supposed to auto-cache stuff, so hopefully this doesn't hit the
PokeAPI too hard, but if it does, sorry! Please tell me how to fix it!

Oh yeah, also, the pokebase library is currently unmaintained and I did run into one issue where the API
had an endpoint that wasn't accounted for in the library, so I had to go into my local copy of it and add
that endpoint to a list somewhere to get it to work. But I don't remember what it was. Sorry again!

As I write this, I'm seeing that there are other PokeAPI wrapper libraries for Python that are actually
being maintained, so maybe I'll eventually update this to use one of those instead. I just used the first
one they listed in the docs. Oops!

P.S. I have also included in the repo some sample output for some of the more common Pokedexes, so you
don't even need to run this yourself if you just want the data.

Requirements
------------
[PokeBase library](https://github.com/PokeAPI/pokebase)

Usage
-----
`python3 pokemonlist.py original-unova`

Replace original-unova with the Pokedex of your choice, or omit it to default to Kanto. Output goes to stdout.
If you specify a dex that PokeAPI doesn't recognize, it will give you a list of all the available dexes.

There are a couple of options you can define at the top of the script. Maybe I should make these accessible as
command line parameters too. I dunno. For now, they're not, so just edit the script if you want.

* **desired_language** --
	The two-letter code for the language to use for the names of Pokemon, items, and moves.
	(I don't know how to localize the text used within the script. Again, sorry.) Default: 'en'
* **include_number** -- 
	Boolean for whether or not to print the Pokedex number of each Pokemon. Default: True.
* **pad_number** --
	If true, the Pokedex number will be padded with leading zeroes, up to 3 digits (unless the requested
	Pokedex includes 1000 entries or more, in which case it will be 4 digits). If include_number is False,
	this does nothing. Default: True.
* **include_evolution_info** --
	Boolean for whether or not to print the evolution details for each Pokemon. If true, you'll get something
	like "Evolves from Bulbasaur at level 16". If false, you just get the names of the Pokemon (and their
	numbers if include_number is true). Default: True.

Known issues
------------
* Pokemon that evolve into different Pokemon depending on region may not be handled as you'd expect.
* Pokemon that have different evolution triggers in different games (such as the trade evolutions that use items
  instead in Legends: Arceus) may not be handled as you'd expect. I need to decide how to handle this... we
  could guess the game based on the desired Pokedex, but what if it's the national dex? I'm also considering
  letting the user specify a game, but that opens up the possibility of nonsensical combinations of dex and game,
  so I'd have to figure out how to deal with that, too.
* Pokemon that evolve in a specific location may show a location from a different game than expected.
* The evolution data for Alcremie does not go into detail on the different types of Sweets that may be held, or
  the different directions or time you can spin. I don't plan on adding this; knowing that you get an Alcremie is
  enough as far as I'm concerned. Also, the name of "Sweets" is not localized into the desired language, due to
  there not being a category in PokeAPI specifically for Sweets as far as I can tell.
* Pokemon that have multiple forms were showing up as requiring a specific form to evolve, when in fact that form
  is only required for one particular form of the evolution (example: either form of Shellos will evolve into
  a Gastrodon of some sort, so I don't care about the forms of either). To fix this, I just made a list of
  Pokemon whose forms I don't care about, and don't show the forms if they're in that list. This is a crappy
  solution and I'm sure there's a better way of handling it, but I haven't thought of it yet. 
* The script runs slower than it seems like it should.
