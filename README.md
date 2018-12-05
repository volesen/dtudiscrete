# Discrete Math

These are some helper functions for solving problems in Discrete Math 1.


## Usage
To run the examples:

0. Create a virtualenv and activate it.
	* Usually, `virtualenv venv`, then `. bin/activate` on Linux/Mac will do it,
	`venv\scripts\activate` on Windows.
	* If `virtualenv` doesn't exist on Windows, make sure you have pip installed.

1. Install dependencies.
	* `pip install -r requirements.txt` will do it.

2. Enjoy!
	* GCF: Currently, run `./cli.py <a> <b>`, replacing a and b with integers,
	to get the GCF.

3. Test!
	* All tests are easily run using `python -m pytest Tests/*`.

## For git noobsies
First, this is written by an almost-noob, so don't trust too much in what it says. This is also not meant to be an in depth introduction to git. It should, however, be enough to get you working. Also, it assumes you have a working git installation.

To clone(download) this repository:
	* Move to the desired directory and write `git clone https://github.com/volesen/DiscreteMath.git <name>` where <name> is the name of the directory to place it in.

To pull(update your local repository) from origin:
	* `git pull origin master`.
	* Done. If this fails, it's probably because you've changed or removed some files others have also changed or removed.

To push(upload) your changes:
	* Before anything else, make sure to pull as described above. This helps in dealing with merge conflicts
	* `git add .` to add all your changed, deleted and added files to the "staging area".
	* `git commit -m "<message>"` to create a "commit" with all your changes. This only changes things in your local repository. <message> should be a short description of what your commit changes. [A great guide to writing good messages](https://chris.beams.io/posts/git-commit/).
	* `git push origin master` to push your newly created commit to the "origin", that is, the server. This is the first time any changes are made outside of your computer. `origin` tells git which source to push to, and `master` tells git to push to [branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) "master". (The `origin master` part is unnecessary for me, but that might be something I set up. I'm not sure. As I said, noobie).
	* Aaand your done.

In general it is better to commet as often as possible. Make sure what you have works and doesn't break anything else, and then commit that shit. Doesn't matter if it's a single line or a corrected punctuation mark in a comment. Commits are not precious. That way you never change too many files at a time or give others the time to do the same, reducing the need to merge files. It also makes it easier to write good commit messages :)
