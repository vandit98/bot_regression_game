# Python Bot (Regression Games)

This template is a starting point for our experimental Python language support in Regression Games. Build Python bots to compete in Minecraft challenges on Regression Games!

* See the [start.py](#start.py) file for starting code
* See the [hunt.py](#hunt.py) file for a more complete bot with real logic

## Requirements

To make a valid bot, you must:

* Have a file called `start.py`
* Have a function with signature `configure_bot(bot)`

## Known Limitations

Python bots on Regression Games work by integrating into our JavaScript bots. This means that the Python calls to the bot are complete via calls to a Node/JavaScript backend. There are some known limitations to the current setup.

* The bot may be slower than JavaScript bots
* There is limited support for code written in separate files

_Please provide us with feedback and suggestions for which limitations are blockers, and any other thoughts you may have!_