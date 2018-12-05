# Discrete Math

These are some helper functions for solving problems in Discrete Math 1.


## Usage
To run the examples:

0. Install Python 3.6+ and Pip, then create a virtualenv and activate it.
	* Usually, `virtualenv venv`, then `. venv/bin/activate` on Linux/Mac will do it,
	`venv\scripts\activate` on Windows. Run `deactivate` to turn it off.
	* If `virtualenv` doesn't exist on Windows, make sure you have pip installed.
	* Make sure you're using the Python 3.6+ version of virtualenv. `python3 -m virtualenv venv` might also do the trick.

1. Install dependencies.
	* With an active virtualenv, `pip install -r requirements.txt`.

2. Enjoy!
	* GCF: Currently, enter `dtudiscrete` and run `./cli.py <a> <b>`, replacing a and b with integers,
	to get the GCF.
    * You may need to run `python` instead of `./`. Make sure your virtualenv is active if you do so.

3. Test!
	* All tests are easily run using `python -m pytest Tests/*`.

## Documentation
To build the documentation (including auto-generated from `__doc__`s), do the following:

0. Enter `doc`. If on Windows, replace following commands `make` with `make.bat`.
1. Run `make html` to build web docs. Run `make latexpdf` to build latex docs.
2. You'll find generated files in `doc/_build` (open `index.html` in a browser to see web docs)

To contribute to the documentation, you can do the following:

1. **Write docstrings** (Triple quotes ''' right under modules, classes, functions) in ReStructuredText (see other source code for how to define parameters, return values, class attributes, LATEX-style math, and more!). It will be **automatically included** in the auto-generated documentation!
2. The documentation is all generated from `doc/source/index.rst`. Sphinx configuration is all in `doc/source/conf.py`.
3. If you write a new module, you need to add it to `index.rst`. See existing modules for how to do this.

## For git noobsies
The Gold Standard of Tutorials: http://rogerdudler.github.io/git-guide/ . Learn it, love it, live it!

First, this is written by an almost-noob, so don't trust too much in what it says. This is also not meant to be an in depth introduction to git. It should, however, be enough to get you working. Also, it assumes you have a working git installation.

To clone(download) this repository:
   1. Move to the desired directory and write `git clone https://github.com/volesen/DiscreteMath.git <name>` where <name> is the name of the directory to place it in. You can also omit `<name>`.

To pull(update your local repository) from origin:
   1. `git pull`.
   2. It may ask to do a "merge commit". If this fails, you'll need to merge/rebase manually.

To push(upload) your changes:
   1. Before anything else, make sure to pull as described above. This helps in dealing with merge conflicts
   2. `git add -A` to add all unignored files (including hidden files) recursively, to the "staging area".
   3. Check `git status` to make sure you're not doing evil things, like adding binary files or deleting something :) .
   4. `git commit -am "<message>"` to create a "commit" with all your changes. This only changes things in your local repository. <message> should be a short description of what your commit changes. [A great guide to writing good messages](https://chris.beams.io/posts/git-commit/).
   5. `git push` to push your newly created commit to the "origin", that is, the server. This is the first time any changes are made outside of your computer. `origin` tells git which source to push to, and `master` tells git to push to the "master" [branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging). (The `origin master` part is unnecessary for me, but that might be something I set up. I'm not sure. As I said, noobie).
   6. Aaand your done.

In general it is better to commit as often as possible. Make sure what you have works and doesn't break anything else, and then commit that shit. Doesn't matter if it's a single line or a corrected punctuation mark in a comment. Commits are not precious. That way you never change too many files at a time or give others the time to do the same, reducing the need to merge files. It also makes it easier to write good commit messages :)
