# GitHub Actions Workflows

## Available Workflows

### 1. `build-and-release.yml`
**Automatic Build and Release Publishing**

- **Trigger**: Create tag `v*.*.*` (e.g. `v1.0.0`)
- **What it does**:
  - Builds application for Linux, Windows, and macOS
  - Creates installers (.deb, .dmg, .exe/zip)
  - Publishes GitHub release with artifacts

**Usage**:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 2. `build-test.yml`
**Test Build on Code Changes**

- **Trigger**: Push to `main`/`develop` or Pull Request
- **What it does**:
  - Tests build on all platforms
  - Checks for artifacts
  - Saves artifacts for inspection (1 day)

## Configuration

### Requirements

- Python 3.12
- All dependencies in `requirements.txt`
- Working `build.py`

### Permissions

For automatic releases, `GITHUB_TOKEN` is provided automatically.

To enable releases, allow GitHub Actions to create releases:
1. Settings → Actions → General
2. Workflow permissions → Read and write permissions

## Creating Releases

1. Prepare code for release
2. Create tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
3. GitHub Actions automatically:
   - Builds application on all platforms
   - Creates release
   - Uploads all files

4. Verify result:
   - Go to **Releases** section on GitHub
   - All files should be uploaded

See [RELEASE.md](RELEASE.md) for details

