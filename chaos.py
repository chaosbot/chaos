#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join, exists
import os
import time
import sys
import logging
import subprocess
import settings
import schedule
import cron
import shutil
import github_api as gh
import github_api.prs
import github_api.voting
import github_api.repos
import github_api.comments

# Has a sideeffect of creating private key if one doesn't exist already
# Currently imported just for the sideeffect (not currently being used)
import encryption  # noqa: F401


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.getLogger("requests").propagate = False
    logging.getLogger("sh").propagate = False

    log = logging.getLogger("chaosbot")

    if exists("voters.json"):
        log.info("Moving voters,json to server directory!")
        shutil.move("./voters.json", "./server/voters.json")

    api = gh.API(settings.GITHUB_USER, settings.GITHUB_SECRET)

    log.info("starting up and entering event loop")

    os.system("pkill chaos_server")

    server_dir = join(dirname(abspath(__file__)), "server")
    subprocess.Popen([sys.executable, "server.py"], cwd=server_dir)

    # Schedule all cron jobs to be run
    cron.schedule_jobs()

    log.info("Setting description to {desc}".format(desc=settings.REPO_DESCRIPTION))
    github_api.repos.set_desc(api, settings.URN, settings.REPO_DESCRIPTION)

    log.info("Blocking users specified in blocklist")
    with open(join(dirname(__file__), "blocklist"), "r") as blocklist:
        try:
            github_api.users.set_blocklist(api, blocklist.readlines())
        except:
            log.exception("Failed to update blocklist")

    while True:
        # Run any scheduled jobs on the next second.
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
