import os
import oom_git


def main():
    repo_directory = os.getcwd()
    commment = "commiting after auto generation"
    oom_git.push_to_git(repo_directory=repo_directory, comment=comment)

if __name__ == '__main__':
    main()