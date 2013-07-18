pocketlib.py
=========

Python class for adding items to Pocket.

[http://getpocket.com](http://getpocket.com)

# Usage
Use the library directly:

`
import pocketlib
pocketlib.auth()
pocketlib.add_item("url", "title", "tags")
`

Create an instance:

`
from pocketlib import Pocket

p = Pocket()
p.auth()
`

Catch return codes (from Pocket API) to work with:

`
from pocketlib import Pocket

p = Pocket()
(statuscode, statusmessage) = p.add_item(...)
`

# Notes
Totally copied large portions of [InstapaperLib](https://github.com/mrtazz/InstapaperLibrary) for this. Before tonight, I had never written Python before. So I owe a huge debt of gratitude to that project. 

The Pocket API consumer key is stored in the config.ini file; feel free to change this up. Once authenticated once, this script shouldn't need to authorize again. It stores the username and access token in the config.ini file.