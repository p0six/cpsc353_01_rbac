#!/usr/bin/env python
import sys

'''
Course: CPSC-353, Summer 2017, Professor Kenytt Avery
Programming Assignment 01: Role-Based Access Control (RBAC) System
Author: Michael Romero, Josh Eden, Diego Franchi
Date: 6/2/17
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
        with open(group_file, "r") as groups_from_file:  # users: alice, bob, charlie
            for line in groups_from_file:
                line = line.strip().replace(' ', '')
                groups_users = line.split(":")
                groups.append([groups_users[0], groups_users[1].strip().split(",")])
    except IOError as e:
        fail_gracefully(e, group_file)
    return groups


def populate_resources(resource_file):
    resources = []  # Parse the resourceFile and create a data structure to represent it
    try:
        with open(resource_file, "r") as resources_from_file:
            resource_entries = resources_from_file.read().split("\n\n")
            for resource in resource_entries:
                resource_lines = resource.split("\n")
                resource_name = resource_lines[0].split(":")[0]  # /shared/project1/
                groups_permissions_packed = [x.replace(' ', '') for x in resource_lines[1:]]  # [[users:read,execute],]
                group_privileges = []
                for group_permissions_packed in groups_permissions_packed:  # users:read,execute
                    group_permissions = group_permissions_packed.split(":")
                    group_name = group_permissions[0]
                    permissions_list = group_permissions[1].split(",")  # read,write,execute
                    group_privileges.append([group_name, permissions_list])
                resources.append([resource_name, group_privileges])
    except IOError as e:
        fail_gracefully(e, resource_file)
    return resources


def populate_membership(groups, subject):
    membership = []  # Populate "membership" array with groups the subject belongs to
    for groupIndex, user_list in enumerate(groups):
        if subject in user_list[1]:
            membership.append(user_list[0])
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
        with open(action_file, "r") as actions_from_file:  # Test permission data against attempted actions
            action_entries = actions_from_file.read().split("\n")
            for action_entry in action_entries:
                subject_action_resource = action_entry.split()  # alice, read, /home/alice/
                subject = subject_action_resource[0]
                action = subject_action_resource[1]
                resource = subject_action_resource[2]
                subject_is_member_of = populate_membership(group_data, subject)
                action_allowed_by = populate_required_membership(action, resource, resource_data)

                # If subject is member of a group with permissions to perform action on resource...
                authorization = "ALLOW" if [i for i in subject_is_member_of if i in action_allowed_by] else "DENY"
                print "{0} {1} {2} {3}".format(authorization, subject, action, resource)
    except IOError as e:
        fail_gracefully(e, action_file)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage(sys.argv[0])
    main(sys.argv[1], sys.argv[2], sys.argv[3])
