# Abdelhalim Azzouz — Academic Website

Personal academic website built with Quarto and deployed with GitHub Pages.

## Local preview

Install Quarto, then run:

```bash
quarto preview
```

## Deployment

Every push to `main` triggers the workflow `.github/workflows/publish.yml`, which renders the site with Quarto and deploys it directly to GitHub Pages.

In GitHub: **Settings → Pages → Build and deployment → Source → GitHub Actions**.
