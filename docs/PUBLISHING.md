# Publishing status and operation

The user authorized a public repository and a here.now viewer for link-based use. The package has an agent entry point, verified installer, CLI and searchable static viewer. The public GitHub repository is https://github.com/wescalemarketing/jeremy-haynes-knowledge-base. Read AGENT_START.md for installation. Remote status is recorded in reports/PUBLICATION.json.

No credentials or claim tokens belong in the repository. here.now anonymous sites expire after 24 hours unless claimed; permanent hosting requires an authenticated account or claiming the generated site. The viewer package is the verified v0.4.0 snapshot; GitHub includes subsequent publication documentation updates.

Build the viewer with `python3 tools/build_web.py --out /tmp/jeremy-viewer`. Run tests and skill validation, regenerate the package manifest and ZIP, test a fresh installation, then publish the folder including the ZIP and release metadata. Verify the hosted package hash and live page before reporting success.
