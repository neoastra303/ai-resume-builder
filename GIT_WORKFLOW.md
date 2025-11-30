# Git Workflow and Branching Strategy

## Branching Model

We follow a simplified GitFlow workflow:

### Main Branches
- `master` - Production-ready code
- `develop` - Integration branch for features

### Supporting Branches
- Feature branches - For developing new features
- Hotfix branches - For紧急 fixes to production
- Release branches - For preparing new releases

## Branch Naming Conventions

- Feature branches: `feature/description-in-kebab-case`
- Bug fix branches: `fix/description-in-kebab-case`
- Hotfix branches: `hotfix/description-in-kebab-case`
- Release branches: `release/version-number`

## Commit Message Guidelines

Follow conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `test:` Adding or modifying tests
- `chore:` Maintenance tasks

Example:
```
feat: add AI-powered resume suggestions

Implement OpenAI integration for generating resume content suggestions
based on user input and industry best practices.

Closes #123
```

## Pull Request Process

1. Create feature branch from `develop`
2. Make changes and commit with clear messages
3. Push branch to remote repository
4. Create pull request to `develop` branch
5. Request code review from team members
6. Address feedback and make changes if needed
7. Merge after approval

## Release Process

1. Create release branch from `develop`
2. Update version numbers and changelog
3. Merge release branch to `master` and `develop`
4. Tag the release on `master`
5. Deploy to production