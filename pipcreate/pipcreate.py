# -*- coding: utf-8 -*-

import os
import sys
import random
import getpass
import difflib
import time
import subprocess
import webbrowser

import travispy
import pkgtools
import pkgtools.pypi as pp
import github
from travispy import TravisPy

from time import sleep
from cookiecutter.main import get_user_config, generate_context, generate_files

import keyring

import re
ascii_re = re.compile('^[a-zA-Z]+$')

import logging

log = logging.getLogger(__name__)
log.setLevel(20)

def main(proposal=None,target_dir=None):
    """
        

    """
    if not target_dir:
        target_dir = os.getcwd()
        log.info('will use target dir', target_dir)
    token = keyring.get_password('session','github_token')
    if token is None:
        turl = 'https://github.com/settings/tokens/new'
        log.info('I will need a new token to access yoru github account, please give me a token that have `write:repo_hook` enable.')
        log.info("I'll try to open github for you at the right page, otherwise please visit", turl)
        sleep(5)
        webbrowser.open_new_tab(turl)
        token = getpass.getpass('github token:')
        keyring.set_password('session','github_token', token)
        log.info('token stored in your keyring as session:github_token')


    # generate a python package name

    adjectives = ['red','green','blue','purple','fluffy','soft','hard','golden','silver']
    nouns = ['moon', 'frog', 'lake','orchid','lilly','saphire','gem','sun','lilly','ocean','lampshade','fish']
    if not proposal.isidentifier() and len(proposal)>3:
        log.info('package name are recommend to be valid python identifiers, and at least 3 letters long', proposal)
        sys.exit(-1)


    if not proposal:
        proposal = random.choice(adjectives).capitalize()+random.choice(nouns).capitalize()
    plist = None

    #  compare name with existing package name, warn if too close

    log.info('Comparing "%s" to other existing package name...' % proposal)
    pypi = pp.PyPIXmlRpc()
    if plist is None:
        plist = pypi.list_packages()
    closest = difflib.get_close_matches(proposal.lower(), map(str.lower, plist), cutoff=0.8)
    if closest:
        if proposal in closest:
            log.info(proposal, 'already exists, maybe you woudl prefer to contribute to this package ?')
        else:
            log.info(proposal, 'name is close to the following packae name :', closest)
    else:

        log.info(proposal, 'seem to have a sufficiently specific name')


    #  Actually authenticate with github 
    #  Create (if do not exist) the named repo, and et clone URL.

    gh = github.Github(token)
    u = gh.get_user()
    log.info('Logged in on GitHub as ', u.name)
    from github import UnknownObjectException 
    try:
        repo = u.get_repo(proposal)
        log.info('It appears like %s repository already exists, using it as remote' %proposal)
        existing = True
    except UnknownObjectException:
        repo = u.create_repo(proposal)
        existing = False

    ssh_url = repo.ssh_url
    slug = repo.full_name
    log.info('Workin with repository',slug)


    # Clone github repo locally, over SSH an chdir into it

    log.info("Clonning github repository locally")
    subprocess.call(['git', 'clone' , ssh_url])
    os.chdir(proposal)
    log.info('I am now in ',os.getcwd())


    # Done with github directly. Login to travis

    t = TravisPy.github_auth(token, uri='https://api.travis-ci.org')
    user = t.user()
    log.info('Travis user:',user.name)

    # Ask travis to sync with github, try to fetch created repo with exponentially decaying time.

    last_sync = user.synced_at
    log.info('syncing Travis with Github, this can take a while...')
    r = t._session.post(t._session.uri+'/users/sync')
    import time
    for i in range(10):
        try:
            time.sleep((1.5)**i)
            r= t.repo(slug)
            if t.user().synced_at == last_sync:
                raise ValueError('synced not really done, t.repo() can be duplicate')
            log.info('\nsyncing done')
            break
        except:
            log.info('.')
    ## todo , warn if not found


    #  Enable travis hook for this repository

    log.info('Enabling travis hooks for this repository')
    resp = t._session.put(t._session.uri+"/hooks/",
                        json={
                            "hook": {
                                "id": r.id ,
                                "active": True
                            }
                        },
                      )
    if resp.json()['result'] is True:
        log.info('Travis hook for this repository are now enabled.')
        log.info('Continuous interation test shoudl be triggerd everytime you push code to github')
    else:
        log.info("I was not able to set up Travis hooks... somethin went wrong.")


    # ##  Do the same for read the doc.

    # ## Shoudl we do https://coveralls.io/?

    # ## Todo
    #     - initiate template with something like cookie cutter
    #     - handle case where use is not registered with one of the above services.
    #     - easier way to et github token

    context_file = os.path.expanduser('~/.cookiecutters/cookiecutter-pypackage/cookiecutter.json')
    context = generate_context(context_file)

    os.chdir('..')
    context['cookiecutter']['full_name'] = user.name
    context['cookiecutter']['email'] = user.email
    context['cookiecutter']['github_username'] = user.login
    context['cookiecutter']['project_name'] = proposal
    context['cookiecutter']['repo_name'] = proposal.lower()


    generate_files(
            repo_dir=os.path.expanduser('~/.cookiecutters/cookiecutter-pypackage/'),
            context=context
        )
    os.chdir(proposal)

    log.info(os.getcwd())
    os.listdir('.')

    subprocess.call(['git','add','.'])

    subprocess.call(['git','commit',"-am'initial commit of %s'" % proposal])

    subprocess.call(['git', "push", "origin", "master:master"])

    webbrowser.open('https://travis-ci.org/{slug}'.format(slug=r.slug))
