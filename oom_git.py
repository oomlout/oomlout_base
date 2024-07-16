#print env path variable
#import git
import os


def clone(**kwargs):
    repo = kwargs['repo']
    #remove.git from repo name
    repo = repo.replace(".git", "")
    directory = kwargs.get('directory', os.getcwd())
    #add repo name to directory
    directory = os.path.join(directory, repo.split("/")[-1])
    #if directory doesn't exist make it
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        #if it does exist pull instead of clone
        print(f"directory {directory} already exists")
        pull(directory=directory)
        return

    #make absolute
    directory = os.path.abspath(directory)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%%%%%  cloning from github")
    print(f"cloning {repo} to {directory}")
    #do in one os.system call
    os.system(f"git clone {repo} {directory}")
    # git pull origin master
    os.system(f"cd {directory} && git pull origin main")


def pull(**kwargs):
    directory = kwargs.get('directory', os.getcwd())
    #make absolute
    directory = os.path.abspath(directory)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%%%%%  pulling from github")
    print(f"pulling from {directory}")
    #do in one os.system call
    os.system(f"cd {directory} && git pull")
    
    
def push(**kwargs):
    push_to_git(**kwargs)


def push_to_git(**kwargs):    
    directory = kwargs.get('directory', "")
    cwd = os.getcwd()
    repo_directory = kwargs.get('repo_directory', "")
    if repo_directory == "":
        repo_directory = directory
        if repo_directory == "":
            repo_directory = os.getcwd()
    
    count = kwargs.get('count', 1)
    comment = kwargs.get('comment', f"comitting after {count} generations")
    #push to github
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%%%%%  pushing to github")
    #remove the lock file on thsi repo if it exists
    try:
        os.remove(".git/index.lock")
    except:
        pass
    use_command_line = True

    if not use_command_line:
        print(f"pushing to {repo_directory}")
        import git 
        result = repo = git.Repo(repo_directory)
        print(result)
        result =  repo.git.add("*")
        print(result)
        result = repo.index.commit(comment)
        print(result)

        result = origin = repo.remote(name='origin')
        result = origin.push()
        print(result)
    else:
        print(f"pushing to {repo_directory}")
        #use os.system to do it all in one command
        os.system(f"cd {repo_directory} && git add *")
        os.system(f"cd {repo_directory} && git commit -m \"{comment}\"")
        os.system(f"cd {repo_directory} && git push")
        
    