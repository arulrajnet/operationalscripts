# -*- coding: utf-8 -*-

__author__ = 'arul'

import sys
import json
import time
from fabric.api import *
from fabric.contrib import files
import re
from fabric.tasks import Task

"""
Basically its doing mongo operations of Backup and Restore
"""

env.use_ssh_config = True

class MongoTask(Task):

    DB_NAME = MONGO_HOST = MONGO_USER = MONGO_PASSWORD = None

    def __init__(self, func, *args, **kwargs):
        super(MongoTask, self).__init__(*args, **kwargs)
        self.func = func

    def run(self, *args, **kwargs):
        global DB_NAME, MONGO_HOST, MONGO_USER, MONGO_PASSWORD

        if "dbname" in kwargs:
            self.dbname = kwargs["dbname"]
            DB_NAME = kwargs["dbname"]

        if "mongo_host" in kwargs:
            self.mongo_host = kwargs["mongo_host"]
            MONGO_HOST = kwargs["mongo_host"]

        if "mongo_user" in kwargs:
            self.mongo_user = kwargs["mongo_user"]
            MONGO_USER = kwargs["mongo_user"]

        if "mongo_password" in kwargs:
            self.mongo_password = kwargs["mongo_password"]
            MONGO_PASSWORD = kwargs["mongo_password"]

        return self.func(*args, **kwargs)


def __list_collection__(dbname):
    """
    List all the mongo collections from the given database.
    :param dbname:
    :return:
    """
    coll_str = run("""mongo %s --eval "printjson(db.getCollectionNames())" --quiet""" % dbname)
    if coll_str:
        collections = json.loads(coll_str)
        # remove system.* collections
        for name in collections:
            match = re.search("system.*", name)
            if match:
                collections.remove(name)
        return collections
    return None


def __choose_collections__(dbname):
    collections = __list_collection__(dbname)

    if len(collections) == 0:
        print "No collections with in DB : %s" % dbname
        return None

    collections_dict = dict()

    i = 1
    for collection in collections:
        collections_dict[i] = collection
        i += 1

    print "Collections : "

    for key in sorted(collections_dict.keys()):
        print "\t %s. %s" % (key, collections_dict[key])

    collection_nos = prompt("Which collections you want to select. For ex: 1-3,6-8,10?", validate=r'^[0-9,-]+$')

    rangewithend = lambda start, end: range(start, end+1)

    # 1-3,6-8,10
    if collection_nos:
        collection_ranges = collection_nos.split(',')
        extracted_range = list()
        for r in collection_ranges:
            rl = [int(i) for i in r.split('-')]
            rl.sort()
            if len(rl) > 1:
                extracted_range = extracted_range + rangewithend(rl[0], rl[1])
            else:
                extracted_range = extracted_range + rl
        extracted_range = list(set(extracted_range))

    selected_collections = list()
    for no in extracted_range:
        selected_collections.append(collections_dict[no])

    print "Selected Collections : "
    print "\t %s" % selected_collections
    yesorno = prompt("Do you want to continue. y|n?", validate=r'y|n')
    if yesorno == "n":
        return None

    return selected_collections


@task(alias="list", task_class=MongoTask)
@with_settings(hide('stdout'), warn_only=True)
def _list(dbname=None, mongo_host=None, mongo_user=None, mongo_password=None):
    collections = __list_collection__(dbname)

    if len(collections) == 0:
        print "No collections with in DB : %s" % DB_NAME
        return None

    print "--"*20
    print "%-20s" % "Collection Name"
    print "--"*20
    for name in collections:
        print "%-20s" % name
    print "--"*20


@task(alias="count", task_class=MongoTask)
@with_settings(hide('stdout'), warn_only=True)
def _count(dbname=None, mongo_host=None, mongo_user=None, mongo_password=None):
    pass
    collections = __list_collection__(dbname)
    if len(collections) == 0:
        print "No collections with in DB : %s" % DB_NAME
        return None

    collections_count = list()

    for name in collections:
        no_of_docs = run("""mongo %s --eval "db.%s.count()" --quiet""" % (dbname, name))
        collections_count.append((name, no_of_docs))

    print "--"*40
    print "%-40s %10s" % ("Collection Name", "Count")
    print "--"*40
    for count_tuble in collections_count:
        print "%-40s %10d" % (count_tuble[0], int(count_tuble[1]))
    print "--"*40


@task(default=True, task_class=MongoTask)
@with_settings(hide('stdout'), warn_only=True)
def backup(dbname=None, mongo_host=None, mongo_user=None, mongo_password=None):
    _backup(dbname)


def _backup(dbname):
    collection_names = __choose_collections__(dbname)
    if collection_names is None:
        return

    timestamp = time.time()
    backup_dir = "/opt/%s" % timestamp

    backup_dir = prompt("Change backup directory?", default=backup_dir)
    run("mkdir -p %s" % backup_dir)

    for name in collection_names:
        print "Backup %s" % name
        run("mongodump --collection %s --db %s --out %s" % (name, dbname, backup_dir))
    return backup_dir, collection_names


@task(task_class=MongoTask)
@with_settings(hide('stdout'), warn_only=True)
def backuprestore(dbname=None, mongo_host=None, mongo_user=None, mongo_password=None, target_collection=None):
    if target_collection is None:
        print "Please give `target_collection` argument."
        return

    backup_dir, collection_names = _backup(dbname)

    for name in collection_names:
        pass
        dump_file_path = "%s/%s/%s.bson" % (backup_dir, dbname, name)
        run("mongorestore -d %s -c %s %s" % (dbname, target_collection, dump_file_path))


@task(task_class=MongoTask)
@with_settings(hide('stdout'), warn_only=True)
def drop(dbname=None, mongo_host=None, mongo_user=None, mongo_password=None):
    collection_names = __choose_collections__(dbname)
    if collection_names is None:
        return

    yesorno = prompt("Are you sure want to drop above collections. y|n?", validate=r'y|n')
    if yesorno == "n":
        return None

    for name in collection_names:
        run("""mongo %s --eval "printjson(db.%s.drop())" --quiet""" % (dbname, name))

if __name__ == '__main__':
    print "Usage: fab -H hostname -f %s backup:dbname=database-name" % sys.argv[0]
    print "Usage: fab -H hostname -f %s backuprestore:dbname=database-name,target_collection=collection-name" % sys.argv[0]
    print "Usage: fab -H hostname -f %s drop:dbname=database-name" % sys.argv[0]