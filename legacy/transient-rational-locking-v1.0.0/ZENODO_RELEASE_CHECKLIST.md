# Zenodo Release Checklist

1. Push repository to GitHub.
2. Connect the repository to Zenodo and enable releases.
3. Create a GitHub release tag `v1.0.0`.
4. Confirm `.zenodo.json` is present at repository root.
5. After Zenodo ingests the release, verify:
   - title
   - author/ORCID
   - license
   - version DOI
   - concept DOI
6. Update `CITATION.cff` DOI field in the next commit/release if you want the minted DOI embedded.

Zenodo registers a specific-version DOI and a concept DOI for all versions. GitHub releases can be archived through Zenodo's integration. Official docs:
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://support.zenodo.org/help/en-gb/1-upload-deposit/97-what-is-doi-versioning
- https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
