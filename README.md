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
	* All tests are easily run using `python -m pytest tests`.

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

To **configure** git:
   1. `git config --global user.name <name>` where `<name>` is your git (or GitHub) username.
   2. `git config --global user.email <email>` where `<name>` is your git (or GitHub) email.
   3. Confirm that the information is correct with `git config --global --list`.

To **clone** (download) this repository:
   1. Move to the desired directory and write `git clone https://github.com/volesen/DiscreteMath.git <dir>` where `<dir>` is the name of the directory to place it in.

To **pull** (update your local repository) from origin:
   1. `git pull`.
   2. Done. If this fails, it's probably because you've changed or removed some files others have also changed or removed.

To create a **branch**:
   1. Create an issue using the web GUI. From here on `<id>` will refer to the id of the issue. For example 14.
   1. Create a new branch `git checkout -b <name>` where `<name>` is `<id>-issue`. This also moves your HEAD to the new branch.

To **push** (upload) your changes to the current branch:
   1. Before anything else, make sure to pull the current branch with `git pull`. This helps in dealing with merge conflicts
   2. `git add .` to add all your changed, deleted and added files to the "staging area".
   3. `git commit -m "<message>"` to create a "commit" with all your changes. This only changes things in your local repository. <message> should be a short description of what your commit changes. [A great guide to writing good messages](https://chris.beams.io/posts/git-commit/).
   4. `git push` to push your newly created commit to the branch. This is the first time any changes are made outside of your computer. [branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging). If it is a new branch write `git push --set-upstream origin <name>` where `<name>` is the name of the branch.
   5. Aaand your done.

To **swap** branch (if you want to work at multiple branches simultaneously):
   1. `git checkout <name>` where `<name>` is the name of the branch.

To **delete** a branch:
   1. To delete a local branch write `git branch -d <name>` where `<name>` is the name of the branch.
   1. To delete a remote branch (be careful!) write `git push origin --delete <name>` where <name> is the name of the branch.
   
To **move** or delete files without breaking git:
   1. To move a file that's tracked by git without breaking things, use `git mv <source> <dest>`.
   2. To delete a file that's tracked by git, use `git rm <to_delete>`.

In general it is better to commit as often as possible. Make sure what you have works and doesn't break anything else, and then commit that shit. Doesn't matter if it's a single line or a corrected punctuation mark in a comment. Commits are not precious. That way you never change too many files at a time or give others the time to do the same, reducing the need to merge files. It also makes it easier to write good commit messages :)

### Rebasing and Why You Need It
Imagine the following situation:
   - You start a branch `feature` from some commit on `master`; let's call this commit 0a.
   - You make 3 commits to feature: 1b, 2b, and 3b.
   - Meanwhile, 5 new commits are made on master: 1a, 2a, 3a, 4a, 5a.
   - It comes time to merge feature with master. But there's a problem:
       You worked from 0a, thus you can't `git merge` with master, which is at 5a.
   - What to do?

Right now your feature branch looks like this: 0a -> 1b -> 2b -> 3b.

You need it to look like this: 0a -> **1a -> 2a -> 3a -> 4a -> 5a** -> 1b -> 2b -> 3b.

To make this reality, you can use the *magic of rebasing*!
   1. Checkout your branch: `git checkout feature`.
   2. Hit git log. It looks like 0a -> 1b -> 2b -> 3b.
   2. *Rebase* from master: `git rebase master`.
   4. Hit git log. It now looks like 0a -> **1a -> 2a -> 3a -> 4a -> 5a** -> 1b -> 2b -> 3b.
   5. You've *changed history*. Now, if you were to go `git checkout master` and `git merge feature`, everything will work!

You'll notice a **problem**: Because of the changed history, you can no longer push to the remote branch. This can be fixed in two ways:
   * If you're an asshole: `git push --force`. You'll overwrite the entire remote branch with your local one. **CAREFUL!**
   * If you can live with a merge commit: `git pull feature`. You'll create a merge commit, combining the rebased and unrebased versions, after which `git push` will work flawlessly.

Also, a PSA: Delete your branches when they're merged!
