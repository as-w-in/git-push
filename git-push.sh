#!/bin/bash

# Function to run git commands and handle errors
run_git_command() {
    local command="$1"
    local error_message="${2:-Git command failed!}"

    $command
    if [ $? -ne 0 ]; then
        echo "❌ $error_message"
        exit 1
    fi
}

# Upload a new directory to GitHub
upload_new_directory() {
    # Handling user input with KeyboardInterrupt protection
    read -p "📂Project folder name (on Desktop)? " name
    read -p "Commit message? " commit_message

    folder_path="$HOME/Desktop/$name"

    if [ ! -d "$folder_path" ]; then
        echo "❌ Folder not found: $folder_path."
        exit 1
    fi

    cd "$folder_path" || exit

    if [ ! -d ".git" ]; then
        echo "📁 Initializing Git repository..."
        run_git_command "git init"
    fi

    run_git_command "git add ."
    run_git_command "git commit -m '$commit_message'"
    run_git_command "git branch -M main"

    if ! git remote | grep -q "origin"; then
        read -p "Paste the GitHub repo URL: " repo_url
        run_git_command "git remote add origin $repo_url"
    fi

    run_git_command "git pull origin main --rebase"
    run_git_command "git push -u origin main"
    echo "✅ Successfully pushed to GitHub."
}

# Upload or replace an individual file in an existing repo
upload_replace_file() {
    read -p "Full path of the file to upload/replace: " source_file
    read -p "Path to your local Git repo: " repo_path
    read -p "Target file path in the repo (e.g., src/hi.py): " target_filename
    read -p "Commit message? " commit_message

    if [ ! -f "$source_file" ]; then
        echo "❌ Source file not found: $source_file"
        exit 1
    fi

    if [ ! -d "$repo_path/.git" ]; then
        echo "❌ Invalid Git repo: $repo_path"
        exit 1
    fi

    full_target_path="$repo_path/$target_filename"
    mkdir -p "$(dirname "$full_target_path")"
    cp "$source_file" "$full_target_path"

    cd "$repo_path" || exit
    run_git_command "git add $target_filename"
    run_git_command "git commit -m '$commit_message'"
    run_git_command "git pull origin main --rebase"
    run_git_command "git push origin main"
    echo "✅ File successfully pushed."
}

# Forked repo: Clone, Modify, and Submit Pull Request
fork_and_pull_request() {
    read -p "Paste the FORKED repo URL (your fork, not the original): " fork_url
    repo_name=$(basename "$fork_url" .git)
    clone_dir="$HOME/Desktop/$repo_name"

    echo "📥 Cloning the forked repo..."
    run_git_command "git clone $fork_url $clone_dir"
    echo "✅ Repo cloned to: $clone_dir"

    echo -e "\n🛠️ You can now modify files manually in that folder."
    read -p "Press Enter when you're done making changes to continue..."

    cd "$clone_dir" || exit
    run_git_command "git add ."
    read -p "Enter commit message for your changes: " commit_msg
    run_git_command "git commit -m '$commit_msg'"
    run_git_command "git push origin main"

    echo "🌐 Opening GitHub to create a pull request..."
    repo_user=$(echo "$fork_url" | cut -d "/" -f 4)
    pr_url="https://github.com/$repo_user/$repo_name/compare/main...main?expand=1"
    sleep 1
    xdg-open "$pr_url" &> /dev/null
    echo "✅ All done! Finish creating the pull request in your browser."
}

# Main function to choose action
main() {
    echo "What would you like to do?"
    echo "1. Upload a NEW DIRECTORY to GitHub"
    echo "2. Upload or REPLACE an INDIVIDUAL FILE in an existing repo"
    echo "3. Forked REPO: Clone, Modify, and Submit Pull Request"

    read -p "Choose 1, 2, or 3: " choice

    case "$choice" in
        1)
            upload_new_directory
            ;;
        2)
            upload_replace_file
            ;;
        3)
            fork_and_pull_request
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1, 2, or 3."
            exit 1
            ;;
    esac
}

# Run the script
main
