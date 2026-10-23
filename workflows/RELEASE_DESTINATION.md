# Approved future release destination — NOT IMPLEMENTED

This document preserves the destination from the [Owner Goal Authority](https://docs.google.com/document/d/1_tY5lHTuDW4Kt8ujrU--vAcNXYj4T1rKRMLvEhKQLIw/edit); it is **not** a release mechanism or an authorization to publish.

A later batch must implement and verify an owner-controlled, per-theme release flow with:

- independently scoped theme versions/tags/history and no changes to unrelated theme versions;
- a dry-run that produces the **exact install layout** (root-level CSS and licensed resources) and tests that same final artifact;
- source/asset permission checks, archive contents and resource paths, reproducible checksum/hash and binding to exact commit/tag;
- safe per-theme version selection/increment, explicit Owner authorization for publication *separate* from PR merge, and collision/immutable-tag protections;
- GitHub Release publication plus verification of the downloaded public asset when executable;
- diagnosable partial failures, recovery/rollback guidance and no silent replacement of published tags/releases.

Use [GPP's release system](https://github.com/rezahh107/Gravity-Presentation-Profiles/blob/main/docs/release/OWNER_RELEASE_GUIDE.md) for proven principles when that work begins; do not copy its WordPress/Gravity-specific machinery.

**This batch:** no packaging, version calculation, tagging, release workflow, publishing credentials or public release. A green structural CI does not satisfy any of the release requirements above.
