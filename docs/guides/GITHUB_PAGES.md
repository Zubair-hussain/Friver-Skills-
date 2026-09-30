# GitHub Pages deployment

The project site is a self-contained `index.html`. It has no package install,
remote font, CDN, analytics script, or build step. The deployment artifact
contains that file only.

## Publish

1. Connect this working copy to a repository you own and push `main`.
2. In the GitHub repository, open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Open **Actions → Deploy GitHub Pages** and run the workflow, or push a change
   to `index.html`.
5. Open the URL shown in the workflow's `github-pages` environment.

The workflow is defined in `.github/workflows/pages.yml`. It uses GitHub's
official Pages actions and the minimum deployment permissions: read repository
contents, write Pages, and request an OIDC identity token.

## Local preview

Open `index.html` directly in a browser. No local server is required. If you
prefer to test through HTTP, run this from the repository root:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000/`.

## Accessibility and performance

- Layouts adapt from desktop to mobile widths.
- Semantic sections and visible keyboard focus styles are included.
- Animation stops when the operating system requests reduced motion.
- Intersection animations are progressive enhancement; all content remains
  visible if JavaScript is unavailable.
