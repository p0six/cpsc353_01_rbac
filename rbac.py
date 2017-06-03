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

def populateResources(resourceFile):
    # Parse the resourceFile and create a data structure to represent it
    resources = []
    with open(resourceFile, "r") as resourcesFromFile:
        resourceEntries = resourcesFromFile.read().split("\n\n")
        for resourceEntry in resourceEntries:
            resourceObjectAndSubjectAndPerms = resourceEntry.split("\n")
            resourceObject = resourceObjectAndSubjectAndPerms[0].split(":")[0]
            resourceSubjectsAndPerms = [x.strip(' ').replace(' ', '') for x in resourceObjectAndSubjectAndPerms[1:]]
            subjectAndPerms = []
            for resourceSubjectAndPerms in resourceSubjectsAndPerms:
                groupPerms = resourceSubjectAndPerms.split(":")
                perms = groupPerms[1].split(",")
                subjectAndPerms.append([groupPerms[0], perms])
            resources.append([resourceObject, subjectAndPerms])
    return resources

def populateGroups(groupFile):
    # Parse the groupFile and create a data structure to represent it
    groups = []
    with open(groupFile, "r") as groupsFromFile:
        for line in groupsFromFile:
            line = line.strip().replace(' ', '')
            groupsUsers = line.split(":")
            groups.append([groupsUsers[0], groupsUsers[1].strip().split(",")])
    return groups

def main(groupFile, resourceFile, actionFile):
    groups = populateGroups(groupFile)
    resources = populateResources(resourceFile)
    # Now that we've populated our groups and resources permission data, test them against attempted actions
    with open(actionFile, "r") as actionsFromFile:
        actionEntries = actionsFromFile.read().split("\n")
        for actionEntry in actionEntries:
            subjectActionResource = actionEntry.split() # alice, read, /home/alice/
            subject = subjectActionResource[0]
            action = subjectActionResource[1]
            resource = subjectActionResource[2]
            subjectIsMemberOf = []
            actionToResourceAllowedByMembersOf = []

            # We populate "subjectIsMemberOf" array with groups the subject belongs to
            for groupIndex, userList in enumerate(groups):
                if subject in userList[1]:
                    subjectIsMemberOf.append(userList[0])

            # We populate "actionToResourceAllowedByMembersOf" array with groups authorized to perform action on resource
            for resourceIndex, groupsPrivsOfResource in enumerate(resources):
                if groupsPrivsOfResource[0] == resource:
                    for group, privileges in groupsPrivsOfResource[1]:
                        if action in privileges:
                            actionToResourceAllowedByMembersOf.append(group)

            # Compare the groups our subject is a member of to the list of groups allowed to perform the action on resource
            if [i for i in subjectIsMemberOf if i in actionToResourceAllowedByMembersOf]:
                print "ALLOW " + subject + " " + action + " " + resource
            else:
                print "DENY " + subject + " " + action + " " + resource

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])