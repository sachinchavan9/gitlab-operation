from userconfig import UserConfig
import gitlab
import os


class Remover(UserConfig):
    def __init__(self):
        UserConfig.__init__(self)
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

    GitLab:{}
    AccessToken:{}
    ############################################
    ############################################
            '''.format(self.url, self.token)
        )
        try:
            project_id = int(input('Project ID:'))
            print('\n[-] remove issues from project id: {}'.format(project_id))
            self._remove_issue(project_id=project_id)
        except ValueError:
            print('\n[x] wrong input!\n')
            exit(0)

    def gitman(self, url, token, ssl_verify=False):
        git = gitlab.Gitlab(url=url, private_token=token,
                            ssl_verify=ssl_verify)
        return git

    def _remove_issue(self, project_id):
        
        git = self.gitman(self.url, self.token, ssl_verify=False)
        print(project_id)


if __name__ == "__main__":
    Remover()
