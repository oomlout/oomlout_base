import git

def push_to_git(**kwargs):
    repo_directory = kwargs.get('repo_directory', os.getcwd())
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
    #subprocess.run(["git", "add", "*"])
    #subprocess.run(["git", "commit", "-m", f"comitting after {count} generations"])
    #subprocess.run(["git", "push"])