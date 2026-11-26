# gjed.github.io

The homepage at [gjed.github.io](https://gjed.github.io/). It lists every public gjed repository that publishes GitHub Pages.

## How it works

`build.py` reads the repositories from the GitHub API, keeps the public, non-fork, non-archived ones with Pages enabled, and renders them into `index.html`. Each card links to the repository's homepage URL, or to `https://gjed.github.io/<repo>/` when none is set.

`projects.txt` sets the order: listed repositories come first, in that order, and Pages projects not listed follow alphabetically.

Build locally:

```sh
python3 build.py --out _site
python3 -m http.server -d _site
```

## Release and deploy

- Merging to `main` runs semantic-release, which tags `vX.Y.Z` and creates the GitHub release from Conventional Commits.
- The tag triggers the Pages workflow, which builds and deploys the site.
- The Pages workflow also runs weekly and on demand, rebuilding the latest release so new Pages projects appear without a release.

Renovate keeps the workflow actions and the semantic-release dependencies up to date.

## License

The code is licensed under [Apache 2.0](LICENSE). The gjed brand assets in `assets/brand/` (logos, favicons and design tokens) are not covered by that license: all rights reserved.
