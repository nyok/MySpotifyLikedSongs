import os
import json
import base64
import hashlib
import requests
from dotenv import load_dotenv

def getEnv():
    try:
        load_dotenv()
        username = str(os.environ['GITHUB_USERNAME'])
        repo = str(os.environ['GITHUB_REPO'])
        token = str(os.environ['GITHUB_TOKEN'])
        return (username, repo, token)
    except:
        print("Environment variables not set")
        exit()

# Checking if a branch exists
# Request to get all branches of the repository,
# and return False if the branch does not exist
def existBranch(branch_name):
    branches = requests.get(
        f'https://api.github.com/repos/{username}/{repo}/git/refs',
        headers=headers
    ).json()
    try:
        for branch in branches:
            if branch['ref'] == 'refs/heads/' + branch_name:
                return True
        return False
    except Exception:
        return False

# Each file, branch and repo on GitHub has a unique ID (hash sum).
# It is needed to modify files or change branches
def getSha(path):
    r = requests.get(
        f'https://api.github.com/repos/{username}/{repo}/contents/{path}',
        auth=(username, token),
        data=json.dumps({'branch': new_branch_name})
    )
    sha = r.json()['sha']
    return sha

def getBranchSha(branch_name):
    try:
        branches = requests.get(
            f'https://api.github.com/repos/{username}/{repo}/git/refs',
            headers=headers
        ).json()
        for branch in branches:
            sha = None
            if branch['ref'] == 'refs/heads/' + branch_name:
                sha = branch['object']['sha']
            return sha
    except Exception:
        return None

# Get unique ID (hash sum) of local file
def getLocalSha(path):
    filesize_bytes = os.path.getsize(path)
    s = hashlib.sha1()
    s.update(b"blob %u\0" % filesize_bytes)
    with open(path, 'rb') as f:
        s.update(f.read())
    return s.hexdigest()

# Find out if the file exists.
# If we don't get the hash sum for the file
def existFile(path):
    r = requests.get(
        f'https://api.github.com/repos/{username}/{repo}/contents/{path}',
        auth=(username, token)
    )
    return r.ok

# Read the contents of the file into a string
def ReadFile(path):
    lines = ""
    with open(path, 'r') as f:
        for line in f:
            lines += line
    return lines

# Takes the contents of a file and commits to a branch
def makeFileAndCommit(content, sha=None):
    b_content = content.encode('utf-8')
    base64_content = base64.b64encode(b_content)
    base64_content_str = base64_content.decode('utf-8')
    f = {'path':'',
     'message': commit_message,
     'content': base64_content_str,
     'sha':sha,
     'branch': new_branch_name}
    return f

# Pushes the commit to a separate branch
def sendFile(path, data):
    f_resp = requests.put(
        f'https://api.github.com/repos/{username}/{repo}/contents/{path}',
        auth=(username, token),
        headers={ "Content-Type": "application/json" },
        data=json.dumps(data)
    )
    return f_resp

# Creates a branch
def createBranch():
    main_branch_sha = getBranchSha('main')
    requests.post(
        f'https://api.github.com/repos/{username}/{repo}/git/refs',
        auth=(username, token),
        data=json.dumps({
            'ref':f'refs/heads/{new_branch_name}',
            'sha':main_branch_sha})
        ).json()

def main():
    if not existBranch(new_branch_name):
        createBranch()
    # Do not include these files
    exclude = ['.env', '.git', '.cache']
    # Added the "updated_folder" folder to the "project_path" so that only this folder is tracked
    for (dirname, dirs, files) in os.walk(project_path+updated_folder):
        dirs[:] = [d for d in dirs if d not in exclude]
        files = [f for f in files if not f in exclude]
        files = [os.path.join(dirname, file) for file in files]
        for path in files:
            git_path = path.removeprefix(project_path)
            sha = None
            changed = True
            if existFile(git_path):
                sha = getSha(git_path)
                local_sha = getLocalSha(path)
            if not (sha is None):
                if local_sha == sha:
                    changed = False
                else:
                    changed = True
            if changed:
                lines = ReadFile(path)
                f = makeFileAndCommit(lines, sha)
                r = sendFile(git_path, f)

if __name__ == '__main__':
    username, repo, token = getEnv()
    new_branch_name = 'main'
    headers = {'Authorization': 'token ' + token}
    project_path = os.path.dirname(os.path.realpath(__file__))+'/'
    updated_folder = 'LikedSongs'
    commit_message = 'New songs (Automatic update)'
    main()
