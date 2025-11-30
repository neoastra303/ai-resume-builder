# GitHub Repository Setup Guide

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Sign in to your GitHub account if prompted
3. Fill in the repository details:
   - Repository name: `resume-builder`
   - Description: "AI Resume Builder - Professional Resume Creation Platform"
   - Public (recommended for portfolio projects)
   - UNCHECK "Initialize this repository with a README"
4. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

Run these commands in your terminal:

```bash
# Navigate to your project directory
cd C:\Users\DisCode\Desktop\resume_builder

# Add the remote origin (replace with your actual username if different)
git remote set-url origin https://github.com/neoastra303/resume-builder.git

# Push your code to GitHub
git push -u origin master
```

## Step 3: Verify the Push

After the push completes, visit https://github.com/neoastra303/resume-builder to see your repository.

## Troubleshooting

If you get authentication errors:
1. Use GitHub personal access token instead of password
2. Or configure SSH keys for GitHub

If you get "repository not found" errors:
1. Double-check the repository name spelling
2. Ensure the repository was created on GitHub
3. Verify you're using the correct username