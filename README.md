# junkware-bot
Generate and tweet fictional patent


Using Twitter command-line util [t](https://github.com/sferik/t#features)

ex. 

  mongoexport --db junks --collection junks --csv --query "{},{"molecule":1}" --fields title --quiet | head -2 | tail -1 | xargs t update
