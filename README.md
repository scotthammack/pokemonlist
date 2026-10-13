I wrote this because I was annoyed that I couldn't find a plain-text list of all the Pokemon in the Unova
Pokedex. I was trying to "catch 'em all" and I just wanted a simple list so I could cross off Pokemon as I
catch 'em, but every website I found had them formatted in elaborate HTML tables and crap that I couldn't
easily copy and paste. So I wrote this script to grab a Pokedex from PokeAPI, iterate through it, and print
the results so I could dump it into a text file. While I was at it, I realized it would be convenient to
include the evolution requirements too so I wouldn't have to keep looking them up on Bulbapedia, so I added
that too.

This is a work in progress. It currently does most of what I need it to do for now, but is missing some edge
cases like regional forms and Pokemon that have different evolution requirements in different games. I may
or may not get around to adding that stuff later. Also, it's been forever since I used Python and I don't
really know what I'm doing, so I'm sure there are a million ways I could have written it better. It runs
unexpectedly slowly.

I think the pokebase library I'm using is supposed to auto-cache stuff, so hopefully this doesn't hit the
PokeAPI too hard, but if it does, sorry! Please tell me how to fix it!

Oh yeah, also, the pokebase library is currently unmaintained and I did run into one issue where the API
had an endpoint that wasn't accounted for in the library, so I had to go into my local copy of it and add
that endpoint to a list somewhere. But I don't remember what it was. Sorry again!

As I write this, I'm seeing that there are other PokeAPI wrapper libraries for Python that are actually
being maintained, so maybe I'll eventually update this to use one of those instead. I just used the first
one they listed in the docs. Oops!

Requirements
------------
[PokeBase library](https://github.com/PokeAPI/pokebase)

Usage
-----
`python3 pokemonlist.py original-unova`

Replace original-unova with the Pokedex of your choice, or omit it to default to Kanto. Output goes to stdout.

There are a couple of options you can define at the top of the script, such as desired_language, include_number,
and include_evolution_info. Maybe I should make these accessible as command line parameters too. I dunno. For
now, they're not, so just edit the script if you want.

* desired_language
	The two-letter code for the language to use for the names of Pokemon, items, and moves.
	(I don't know how to localize the text used within the script. Again, sorry.)
* include_number
	Boolean for whether or not to print the Pokedex number of each Pokemon. If true, the number will be
	padded with leading zeroes (3 digits if the requested dex has less than 1000 entries, 4 digits
	otherwise).
* include_evolution_info
	Boolean for whether or not to print the evolution details for each Pokemon. If true, you'll get something
	like "Evolves from Bulbasaur at level 16". If false, you just get the names of the Pokemon (and their
	numbers if include_number is true).
