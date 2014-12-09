# PipCreate

[![img](https://badge.fury.io/py/pipcreate.png)](http://badge.fury.io/py/pipcreate)

[![img](https://api.travis-ci.org/Carreau/PipCreate.png?branch=master)](https://travis-ci.org/Carreau/pipcreate)

[![img](https://pypip.in/d/pipcreate/badge.png)](https://pypi.python.org/pypi/pipcreate)


Creating Python package make simple. 

Because you should be focused on the feature of your packages, not on the hosting
testing building infrastructure.

 - [x] Choose package name if you have no idea.
 - [x] check that the name is not taken
 - [x] set up github remote
 - [x] hook up travis-ci with Github
 - [ ] hook Read the doc with Github
 - [ ] hook covertall with Github
 - [ ] help build and release
   - [ ] refuse to put on PyPi if travis failing

But as example are better:

```bash
$ python3 -m pipcreate frobulator
will use target dir /Users/bussonniermatthias/eraseme
    # Will open github at the right page and ask you for a private token at first launch.
Comparing "frobulator" to other existing package name...
    # Genrate Package name if you have no idea
frobulator seem to have a sufficiently specific name
Logged in on GitHub as  Matthias Bussonnier
Workin with repository Carreau/frobulator
Clonning github repository locally
Cloning into 'frobulator'...
warning: You appear to have cloned an empty repository.
Checking connectivity... done.
I am now in  /Users/bussonniermatthias/eraseme/frobulator
Travis user: Matthias Bussonnier
syncing Travis with Github, this can take a while...
......
syncing done
Enabling travis hooks for this repository
Travis hook for this repository are now enabled.
Continuous interation test shoudl be triggerd everytime you push code to github
/Users/bussonniermatthias/eraseme/frobulator
    # clone, do the first commit
    # re-push and open travis on build page to be sure all is right.
```

Rely heavily on other packages, TraviPy, pygithub and cookiecutter.

While cookiecutter is nice and allow a lot of flexibility, I think it require too much thinking
or is too frightening when you don't have time to loose or is a beginnier.

Pipcreate will make most decision for you allowing you to focus on what you like to. 
