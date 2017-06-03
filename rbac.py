#!/usr/bin/env python
import sys

'''
Author: Michael Romero
Date: 6/2/17
Course: CPSC-353, Summer 2017, Professor Kenytt Avery
Programming Assignment 01
'''


def usage(script_name):
    msg = 'Usage: %s GROUPS RESOURCES ATTEMPTS' % script_name
    sys.exit(msg)


def fail_gracefully(e, failed_file):
    print "I/O error({0}): {1}, {2}".format(e.errno, e.strerror, failed_file)
    sys.exit(1)


def populate_groups(group_file):
    groups = []  # Parse the groupFile and create a data structure to represent it
    try:
        with open(group_file, "r") as groupsFromFile:
            for line in groupsFromFile:
                line = line.strip().replace(' ', '')
                groups_users = line.split(":")
                groups.append([groups_users[0], groups_users[1].strip().split(",")])
    except IOError as e:
        fail_gracefully(e, group_file)
    return groups


def populate_resources(resource_file):
    resources = []  # Parse the resourceFile and create a data structure to represent it
    try:
        with open(resource_file, "r") as resourcesFromFile:
            resource_entries = resourcesFromFile.read().split("\n\n")
            for resourceEntry in resource_entries:
                resource_object_subject_perms = resourceEntry.split("\n")
                resource_object = resource_object_subject_perms[0].split(":")[0]
                resource_subjects_and_perms = [x.strip(' ').replace(' ', '') for x in resource_object_subject_perms[1:]]
                subject_and_perms = []
                for resourceSubjectAndPerms in resource_subjects_and_perms:
                    group_perms = resourceSubjectAndPerms.split(":")
                    perms = group_perms[1].split(",")
                    subject_and_perms.append([group_perms[0], perms])
                resources.append([resource_object, subject_and_perms])
    except IOError as e:
        fail_gracefully(e, resource_file)
    return resources


def populate_membership(groups, subject):
    membership = []  # Populate "membership" array with groups the subject belongs to
    for groupIndex, userList in enumerate(groups):
        if subject in userList[1]:
            membership.append(userList[0])
    return membership


def populate_required_membership(action, resource, resources):
    action_allowed_by = [] # We populate "action_allowed_by" array with groups authorized to perform action on
    for resourceIndex, resource_groups_privileges in enumerate(resources):
        if resource_groups_privileges[0] == resource:
            for group, privileges in resource_groups_privileges[1]:
                if action in privileges:
                    action_allowed_by.append(group)
    return action_allowed_by


def main(group_file, resource_file, action_file):
    group_data = populate_groups(group_file)
    resource_data = populate_resources(resource_file)
    try:
        with open(action_file, "r") as actionsFromFile:  # Test permission data against attempted actions
            action_entries = actionsFromFile.read().split("\n")
            for actionEntry in action_entries:
                subject_action_resource = actionEntry.split()  # alice, read, /home/alice/
                subject = subject_action_resource[0]
                action = subject_action_resource[1]
                resource = subject_action_resource[2]
                subject_is_member_of = populate_membership(group_data, subject)
                action_allowed_by = populate_required_membership(action, resource, resource_data)

                # If subject is member of a group with permissions to perform action on resource...
                authorization = "ALLOW" if [i for i in subject_is_member_of if i in action_allowed_by] else "DENY"
                print authorization + " " + subject + " " + action + " " + resource
    except IOError as e:
        fail_gracefully(e, action_file)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage(sys.argv[0])
    main(sys.argv[1], sys.argv[2], sys.argv[3])