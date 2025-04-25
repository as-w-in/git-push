# Git-Push
# Git Push Automation Script

![Python](https://img.shields.io/badge/Python-3.12.6-blue.svg)
![GPL](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-green.svg)


# git-push: Automation Script

This script automates common Git operations like uploading a new directory to GitHub, uploading/replacing an individual file in an existing Git repository, and working with forked repositories to create pull requests.

## Features:
- Upload a new directory to GitHub.
- Upload or replace an individual file in an existing repository.
- Fork a GitHub repo, clone it, modify it, and submit a pull request.

## Requirements:
- Git must be installed on your system.
- A GitHub account and repository for pushing files.
- Basic knowledge of how Git works.
- Python 3.x or Bash (for the shell version)

## Usage:

### 1. Upload a New Directory to GitHub
- The script will ask you for the folder name on your Desktop and the commit message.
- It will initialize a Git repository if not already initialized, stage and commit all files, and push to the remote GitHub repository.

### 2. Upload or Replace an Individual File in an Existing Repo
- This allows you to replace or upload a specific file in an existing GitHub repo.
- Provide the path to the file you want to upload/replace, the local Git repository path, and the target file path inside the repo.

### 3. Forked Repo: Clone, Modify, and Submit a Pull Request
- This option clones a forked repo from GitHub to your Desktop, lets you modify it, and then pushes the changes to your forked repository.
- Afterward, it opens GitHub in your browser to submit a pull request.

## How to Use the Script

1. **Download the Script:**
   - Download the script by cloning or downloading the repository.

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
