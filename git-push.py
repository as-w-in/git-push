#!/usr/bin/env python3
import os
import subprocess
import sys
import webbrowser
import time

def run_git_command(command, error_message="Git command failed!"):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ {error_message}\n{e.stderr}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Process interrupted. Exiting...")
        sys.exit(1)

def upload_new_directory():
    try:
        # Handling user input with KeyboardInterrupt protection
        try:
            name = input("📂Project folder name (on Desktop)? ").strip()
            commit_message = input("Commit message? ").strip()
        except KeyboardInterrupt:
            print("\n❌ Process interrupted by user. Exiting...")
            sys.exit(0)  # Exit cleanly

        folder_path = os.path.expanduser(f"~/Desktop/{name}")

        if not os.path.isdir(folder_path):
            print(f"❌ Folder not found: {folder_path}.")
            sys.exit(1)

        os.chdir(folder_path)

        if not os.path.isdir(".git"):
            print("📁 Initializing Git repository...")
            run_git_command(["git", "init"])

        run_git_command(["git", "add", "."])
        run_git_command(["git", "commit", "-m", commit_message])
        run_git_command(["git", "branch", "-M", "main"])

        remote_check = subprocess.run(["git", "remote"], capture_output=True, text=True)
        if "origin" not in remote_check.stdout:
            repo_url = input("Paste the GitHub repo URL: ").strip()
            run_git_command(["git", "remote", "add", "origin", repo_url])

        run_git_command(["git", "pull", "origin", "main", "--rebase"], "Error pulling from remote.")
        run_git_command(["git", "push", "-u", "origin", "main"], "Error pushing to GitHub.")
        print("✅ Successfully pushed to GitHub.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def upload_replace_file():
    try:
        source_file = input("Full path of the file to upload/replace: ").strip()
        repo_path = input("Path to your local Git repo: ").strip()
        target_filename = input("Target file path in the repo (e.g., src/hi.py): ").strip()
        commit_message = input("Commit message? ").strip()

        if not os.path.isfile(source_file):
            print(f"❌ Source file not found: {source_file}")
            sys.exit(1)

        if not os.path.isdir(os.path.join(repo_path, ".git")):
            print(f"❌ Invalid Git repo: {repo_path}")
            sys.exit(1)

        full_target_path = os.path.join(repo_path, target_filename)
        os.makedirs(os.path.dirname(full_target_path), exist_ok=True)
        subprocess.run(["cp", source_file, full_target_path], check=True)

        os.chdir(repo_path)
        run_git_command(["git", "add", target_filename])
        run_git_command(["git", "commit", "-m", commit_message])
        run_git_command(["git", "pull", "origin", "main", "--rebase"])
        run_git_command(["git", "push", "origin", "main"])
        print("✅ File successfully pushed.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nx Process Interrupted.Exiting...")
        sys.exit(1)

def fork_and_pull_request():
    try:
        fork_url = input("Paste the FORKED repo URL (your fork, not the original): ").strip()
        repo_name = fork_url.split("/")[-1].replace(".git", "")
        clone_dir = os.path.expanduser(f"~/Desktop/{repo_name}")

        print("📥 Cloning the forked repo...")
        run_git_command(["git", "clone", fork_url, clone_dir])
        print(f"✅ Repo cloned to: {clone_dir}")

        print("\n🛠️ You can now modify files manually in that folder.")
        input("Press Enter when you're done making changes to continue...")

        os.chdir(clone_dir)
        run_git_command(["git", "add", "."])
        commit_msg = input("Enter commit message for your changes: ").strip()
        run_git_command(["git", "commit", "-m", commit_msg])
        run_git_command(["git", "push", "origin", "main"])

        print("🌐 Opening GitHub to create a pull request...")
        repo_user = fork_url.split("/")[3]
        pr_url = f"https://github.com/{repo_user}/{repo_name}/compare/main...main?expand=1"
        time.sleep(1)
        webbrowser.open(pr_url)
        print("✅ All done! Finish creating the pull request in your browser.")

    except Exception as e:
        print(f"❌ Error during pull request flow: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nx Process Interrupted by the User.Exiting...")
        sys.exit(1)

def main():
    print("What would you like to do?")
    print("1. Upload a NEW DIRECTORY to GitHub")
    print("2. Upload or REPLACE an INDIVIDUAL FILE in an existing repo")
    print("3. Forked REPO: Clone, Modify, and Submit Pull Request")
    
    choice = input("Choose 1, 2, or 3: ").strip()
    if choice == "1":
        upload_new_directory()
    elif choice == "2":
        upload_replace_file()
    elif choice == "3":
        fork_and_pull_request()
    else:
        print("❌ Invalid choice. Please enter 1, 2, or 3.")
        sys.exit(1)

if __name__ == "__main__":
    main()
