# Nikhil's Advanced GitHub Profile

## Package contents
- `README.md`: terminal-style design inspired by the reference, with your existing animated typewriter header, tech stack, statistics, and contribution sections. The large portrait image has been removed so it cannot leave a huge blank panel.
- `nikhil-cyber-portrait-blue.png`: source image for the ASCII portrait generator.
- `scripts/generate_profile_art.py`: generates a custom contribution heatmap, stats card, and ASCII portrait.
- `.github/workflows/profile-art.yml`: daily/manual workflow to update the generated SVGs.
- The 3D contribution and snake workflows are included if available from the earlier starter bundle.

## Setup
1. Upload the contents of this ZIP into `NIKHIL2K5/NIKHIL2K5`, preserving `.github/workflows/` and `scripts/`.
2. Keep `README.md` and `nikhil-cyber-portrait-blue.png` in the repository root. The portrait GIF is no longer displayed by the README.
3. In Settings → Actions → General, enable **Read and write permissions** for workflows.
4. Open Actions → **Update Profile Art** → Run workflow.
5. The workflow will generate `contrib-heatmap.svg`, `stats.svg`, and `nikhil-ascii.svg` and commit them to `main`.
6. The 3D and snake graphics depend on their own workflows and published branches. If one is blank immediately after setup, run its matching workflow once and allow the generated branch to publish. The contribution heatmap has been given extra vertical space so the last row is not clipped.

The workflow uses GitHub's automatically provided `GITHUB_TOKEN`. Do not add a personal access token to the repository.
