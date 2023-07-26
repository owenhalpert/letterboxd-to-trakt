# letterboxd-to-trakt
A simple Python script to add all the movies on your Letterboxd watchlist to your Trakt watchlist.

# Usage
1. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository to your local computer
2. Export your data from https://letterboxd.com/settings/data/
3. Unzip the data download and move or copy your watchlist.csv file into the letterboxd-to-trakt folder
4. Create a new Trakt API app: https://trakt.tv/oauth/applications/new
5. Use `urn:ietf:wg:oauth:2.0:oob` as your Redirect uri
6. Open main.py in letterboxd-to-trakt and fill in your `CLIENT_ID` and `CLIENT_SECRET` on lines 86 and 87
7. Open a Terminal window and run `python main.py`

Enjoy!
