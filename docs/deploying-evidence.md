# Deploying Evidence Reports to GitHub Pages

The Australian Evidence report site (`reports/au/`) is automatically built and deployed to GitHub Pages on every push to `main`.

**Live site:** https://wisemuffin.github.io/project-zeus/

## How It Works

Evidence queries DuckDB locally and bakes the results into parquet files. These parquets (currently ~520KB) are committed to the repo so the CI build can produce the static site without needing DuckDB.

```
Local: DuckDB → npm run sources → parquet files → git push
CI:    parquet files → npm run build → GitHub Pages
```

The workflow is defined in `.github/workflows/deploy-evidence.yml`.

## One-Time Setup

A repository admin must enable GitHub Pages with the Actions source:

1. Go to **Settings → Pages** in the GitHub repo
2. Under **Source**, select **GitHub Actions**
3. Save

No other configuration is needed. The workflow handles everything else.

## Refreshing Data

After running Dagster and dbt to update the DuckDB warehouse, regenerate the source parquets and push:

```bash
cd reports/au
npm run sources
```

Then commit and push the updated data:

```bash
git add reports/au/.evidence/template/static/data/
git commit -m "Update Evidence source data"
git push
```

The GitHub Actions workflow will automatically rebuild and redeploy the site.

## Adding New Evidence Queries

When you add a new `.md` page with SQL queries in `reports/au/pages/`:

1. Run `npm run sources` locally to generate parquets for the new queries
2. Verify the page renders correctly with `npm run dev`
3. Commit both the new page and the generated parquet files
4. Push — the site redeploys automatically

## Troubleshooting

### Build fails in CI

- Check the [Actions tab](https://github.com/wisemuffin/project-zeus/actions) for logs
- The most common cause is a new query whose parquet wasn't committed. Run `npm run sources` locally and commit the new files under `reports/au/.evidence/template/static/data/`

### Pages shows 404

- Verify GitHub Pages source is set to **GitHub Actions** (not "Deploy from a branch")
- Check that the workflow completed successfully in the Actions tab

### Local dev vs deployed site

The local dev server (`npm run dev`) queries DuckDB directly. The deployed site uses the committed parquets. If you see different data locally vs on the site, run `npm run sources` and commit the updated parquets.
