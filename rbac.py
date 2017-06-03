#!/usr/bin/env python
import sys

'''
Author: Michael Romero
Date: 6/2/17
Course: CPSC 353, Summer 2017, Professor Kenytt Avery
Programming Assignment 01
'''

def usage(scriptname):
    msg = 'Usage: %s GROUPS RESOURCE ATTEMPTS' % scriptname
    sys.exit(msg)

if len(sys.argv) != 4:
    usage(sys.argv[0])


def populate_resources(resource_file):
    # Parse the resourceFile and create a data structure to represent it
    resources = []
    with open(resource_file, "r") as resourcesFromFile:
        resource_entries = resourcesFromFile.read().split("\n\n")
        for resourceEntry in resource_entries:
            resource_object_and_subject_and_perms = resourceEntry.split("\n")
            resource_object = resource_object_and_subject_and_perms[0].split(":")[0]
            resource_subjects_and_perms = [x.strip(' ').replace(' ', '') for x in resource_object_and_subject_and_perms[1:]]
            subject_and_perms = []
            for resourceSubjectAndPerms in resource_subjects_and_perms:
                group_perms = resourceSubjectAndPerms.split(":")
                perms = group_perms[1].split(",")
                subject_and_perms.append([group_perms[0], perms])
            resources.append([resource_object, subject_and_perms])
    return resources


def populate_groups(group_file):
    # Parse the groupFile and create a data structure to represent it
    groups = []
    with open(group_file, "r") as groupsFromFile:
        for line in groupsFromFile:
            line = line.strip().replace(' ', '')
            groups_users = line.split(":")
            groups.append([groups_users[0], groups_users[1].strip().split(",")])
    return groups


def main(group_file, resource_file, action_file):
    groups = populate_groups(group_file)
    resources = populate_resources(resource_file)

    # Now that we've populated our groups and resources permission data, test them against attempted actions
    with open(action_file, "r") as actionsFromFile:
        action_entries = actionsFromFile.read().split("\n")
        for actionEntry in action_entries:
            subject_action_resource = actionEntry.split() # alice, read, /home/alice/
            subject = subject_action_resource[0]
            action = subject_action_resource[1]
            resource = subject_action_resource[2]
            subject_is_member_of = []
            action_to_resource_allowed_by_members_of = []

            # We populate "subject_is_member_of" array with groups the subject belongs to
            for groupIndex, userList in enumerate(groups):
                if subject in userList[1]:
                    subject_is_member_of.append(userList[0])

            # We populate "action_to_resource_allowed_by_members_of" array with groups authorized to perform action on resource
            for resourceIndex, groupsPrivsOfResource in enumerate(resources):
                if groupsPrivsOfResource[0] == resource:
                    for group, privileges in groupsPrivsOfResource[1]:
                        if action in privileges:
                            action_to_resource_allowed_by_members_of.append(group)

            # Compare the groups our subject is a member of to the list of groups allowed to perform the action on resource
            if [i for i in subject_is_member_of if i in action_to_resource_allowed_by_members_of]:
                print "ALLOW " + subject + " " + action + " " + resource
            else:
                print "DENY " + subject + " " + action + " " + resource

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])