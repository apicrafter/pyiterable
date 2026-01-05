# GitHub Pages Deployment Setup

This document describes how to deploy the Iterable Data documentation to GitHub Pages at `iterabledata.github.io`.

## Prerequisites

1. A GitHub repository named `iterabledata.github.io` under the `iterabledata` organization
   - **Note**: If your repository has a different name or organization, you'll need to adjust the `organizationName` and `projectName` in `docusaurus.config.js`

2. GitHub Pages enabled in repository settings with "GitHub Actions" as the source

## Configuration

The documentation is configured for deployment to `iterabledata.github.io`:

- **URL**: `https://iterabledata.github.io`
- **Base URL**: `/` (root path)
- **Organization**: `iterabledata`
- **Project**: `iterabledata.github.io`

## Setup Steps

1. **Enable GitHub Pages**:
   - Go to your repository settings on GitHub
   - Navigate to **Pages** in the left sidebar
   - Under **Source**, select **GitHub Actions** as the source
   - This will automatically create the `github-pages` environment

2. **Push to main branch**:
   - The GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) will automatically:
     - Build the Docusaurus site when changes are pushed to `main`
     - Deploy to GitHub Pages
   - The workflow triggers on:
     - Pushes to `main` branch that affect files in `docs/` directory
     - Manual workflow dispatch

3. **Verify deployment**:
   - After the workflow completes, your site will be available at `https://iterabledata.github.io`
   - The deployment typically takes 1-2 minutes

## Repository Structure Considerations

If your repository is **not** named `iterabledata.github.io` under the `iterabledata` organization, you have two options:

### Option 1: Deploy from current repository
If deploying from `datenoio/iterabledata`:
- Update `docusaurus.config.js`:
  ```javascript
  organizationName: 'datenoio',
  projectName: 'iterabledata',
  baseUrl: '/iterabledata/',  // Note the trailing slash
  ```
- Your site will be available at `https://datenoio.github.io/iterabledata/`

### Option 2: Deploy to separate repository
1. Create a new repository `iterabledata/iterabledata.github.io`
2. Set up a workflow to copy built files from this repository to that repository
3. Or use the current configuration if you plan to move/rename the repository

## Manual Deployment

You can also deploy manually using the Docusaurus CLI:

```bash
cd docs
npm install
npm run build
npm run deploy
```

This requires the `GITHUB_TOKEN` environment variable to be set with appropriate permissions.

## Troubleshooting

- **Environment error**: If you see an error about the `github-pages` environment, make sure GitHub Pages is enabled in your repository settings with "GitHub Actions" as the source
- **Build failures**: Check the GitHub Actions logs for specific error messages
- **404 errors**: Verify the `baseUrl` in `docusaurus.config.js` matches your repository structure

