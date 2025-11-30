#!/bin/bash

# GitHub username
USERNAME="neoastra303"

# Repository name
REPO_NAME="resume-builder"

# Create repository using GitHub API
echo "Creating GitHub repository..."
curl -u $USERNAME https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\",\"private\":false}"

# Add remote and push
echo "Setting up remote and pushing code..."
git remote set-url origin https://github.com/$USERNAME/$REPO_NAME.git
git push -u origin master

echo "Repository setup complete!"