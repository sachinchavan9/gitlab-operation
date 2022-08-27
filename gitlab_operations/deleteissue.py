#!/usr/bin python
from gitlab_operations.userconfig import UserConfig
import gitlab
import os
from prettytable import PrettyTable
import json
import sys
import re

import warnings
warnings.filterwarnings("ignore")


class Remover(UserConfig):
    def __init__(self):
        UserConfig.__init__(self)
        self._project_id = None
        try:
            self._get_project_id()
        except KeyboardInterrupt:
            print('\n\nGood bye!\n')

    def _get_project_id(self):
        os.system('clear')
        print('\n[==================|GitLab Project|==================]\n')
        print(
            '''
    ############################################
    ############################################
    BE CAREFULL WHILE ADDING PROJECT ID
    IT WILL WIPE ALL YOUR PROJECT ISSUES

    GitLab: {}
    AccessToken: {}
    Config File Path: {}
    ############################################
    ############################################
            '''.format(self.url, self.token, self._config_file_path)
        )
        try:
            gitman = self.gitman(
                url=self.url, token=self.token, ssl_verify=False)
            confirm_printprojects = input(
                '\nDo you want to list all available projects? (y/N): ')
            if confirm_printprojects.lower() == "y":
                self._get_projects(gitman)
            self._project_id = int(input('\nProject ID: '))
            print(
                '\n[-] counting issues from project id: {}'.format(self._project_id))
            self._remove_issue(project_id=self._project_id, gitlab=gitman)
        except ValueError:
            print('\n[x] wrong input!\n')
            exit(0)
        except Exception as ex:
            print('\n[x] {}\n'.format(ex))

    def _get_projects(self, gl):
        projects = gl.projects.list(all=True)
        x = PrettyTable()
        x.field_names = ['ID', 'Project']
        x.align["ID"] = "r"
        x.align["Project"] = "l"
        rows = [[project.id, project.name_with_namespace]
                for project in projects]
        x.add_rows(rows)
        print(x)

    def gitman(self, url, token, ssl_verify=False):
        git = gitlab.Gitlab(url=url, private_token=token,
                            ssl_verify=ssl_verify)
        return git

    def _remove_issue(self, project_id, gitlab):
        project = gitlab.projects.get(project_id)
        issues = project.issues.list(all=True)

        open_issue = [i for i in issues if i.state == 'opened']
        oi = len(open_issue)
        print('\n[+] Open: {}'.format(oi))

        closed_issue = [i for i in issues if i.state == 'closed']
        ci = len(closed_issue)

        ai = oi+ci
        print('[x] Closed: {}'.format(ci))
        print('[-] All: {}'.format(ai))

        if not ai:
            print('\n[x] no issues for erase\n')
            exit(0)

        # optional issue title filtering
        search_pattern_regex = input(
            '\nIf you want to only delete certain issues, enter a regex pattern to filter the issue title for, leave blank to apply no filtering: '
        )
        if search_pattern_regex == "":
            search_pattern_regex = ".*"
        r = re.compile(search_pattern_regex)
        filtered_issues = [x for x in issues if r.match(x.title)]
        #filtered_issues = list(filter(r.match, issues))
        print(f"\nThe following issues are gonna be deleted from the repository:")
        for printissue in filtered_issues:
            print(f"{printissue.iid}: {printissue.title}")
        
        confirm = input(
            '\nAre you sure to erase the above listed {} issues from GitLab project ID#{} (y/N): '.format(len(filtered_issues), project_id))
        if not confirm:
            print('\n[x] good bye!\n')
            exit(0)
        elif confirm.lower() == 'y':
            print('\n[-] erasing the project issues, plese wait...\n')
            # -------------------------------------------------------------------------
            # progress bar
            current_counter = 0
            COUNTER = 1

            total_iteration = len(filtered_issues)

            sys.stdout.write("|{}|".format("-" * 100))
            sys.stdout.flush()
            sys.stdout.write("\b" * 101)
            # -------------------------------------------------------------------------

            for i in filtered_issues:
                status_bar_string = "{} of {} ".format(
                    COUNTER, total_iteration)
                sys.stdout.write(status_bar_string)
                sys.stdout.flush()

                sys.stdout.write("\b" * len(status_bar_string))
                # progress bar code above
                # main code
                project.issues.delete(i.iid)

                # progress bar
                percent = (COUNTER / total_iteration) * 100
                if current_counter < int(percent):
                    current_counter = int(percent)
                    sys.stdout.write('█' * int(percent))
                    sys.stdout.write("\b" * int(percent))
                COUNTER += 1
                sys.stdout.flush()
            sys.stdout.write("\n")
            print('\n[+] {} issues are successfully erased...!\n'.format(ai))
        else:
            print('\n[x] wrong input!\n')
            exit(0)


def main():
    Remover()
