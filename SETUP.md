# Nikhil's Advanced GitHub Profile

## Package contents
- `README.md`: terminal-inspired profile with a working typewriter intro, single contribution heatmap, icon badges, stats, and project-focus section. No portrait or duplicate contribution-snake/3D section is displayed.
- `contrib-heatmap.svg` and `stats.svg`: custom SVG cards generated from GitHub's GraphQL API.
- `scripts/generate_profile_art.py`: generates the contribution heatmap and stats card.
- `.github/workflows/profile-art.yml`: daily/manual workflow to refresh the generated SVGs.

## Setup
1. Upload the contents of this ZIP into `NIKHIL2K5/NIKHIL2K5`, preserving `.github/workflows/` and `scripts/`.
2. In **Settings → Actions → General**, enable **Read and write permissions** for workflows.
3. Open **Actions → Update Profile Art → Run workflow**.
4. The workflow refreshes `contrib-heatmap.svg` and `stats.svg` and commits them to `main`.

## Rendering notes
- The header animation is supplied by `readme-typing-svg.demolab.com`.
- Technology badges use Shields.io labels, so each technology name remains visible even if a logo glyph is unavailable.
- The contribution heatmap is the only contribution grid in the README, avoiding duplicate visuals.
- GitHub stats/streak cards rely on their respective public services and may occasionally be rate-limited or temporarily unavailable.
