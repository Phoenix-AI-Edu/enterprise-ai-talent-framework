"""Minimal dependency-free validation for submitted public tool manifests."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FIELDS = {
    "id", "slug", "title", "status", "positioning", "available_now",
    "demo_url", "primary_cta", "owner", "last_verified",
}
ALLOWED_STATUS = {"公開沙盒示範", "受邀 Demo", "PoC 招募中", "導入評估中"}


def validate(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{path}: invalid JSON: {error}"]

    errors = [f"{path}: missing {field}" for field in REQUIRED_FIELDS - data.keys()]
    if errors:
        return errors
    if not re.fullmatch(r"[a-z0-9_]+", data["id"]):
        errors.append(f"{path}: id must use lowercase letters, digits, or underscores")
    if not re.fullmatch(r"[a-z0-9-]+", data["slug"]):
        errors.append(f"{path}: slug must use lowercase letters, digits, or hyphens")
    if data["status"] not in ALLOWED_STATUS:
        errors.append(f"{path}: status is not an approved public status")
    if not isinstance(data["available_now"], list) or not data["available_now"]:
        errors.append(f"{path}: available_now must contain at least one verified capability")
    if not isinstance(data["primary_cta"], dict) or not data["primary_cta"].get("label") or not data["primary_cta"].get("url"):
        errors.append(f"{path}: primary_cta needs label and url")
    try:
        verified = date.fromisoformat(data["last_verified"])
        if (date.today() - verified).days > 90:
            errors.append(f"{path}: last_verified is over 90 days old")
    except ValueError:
        errors.append(f"{path}: last_verified must use YYYY-MM-DD")
    return errors


def main() -> int:
    paths: list[Path] = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        paths.extend(sorted(path.glob("*.json")) if path.is_dir() else [path])
    if not paths:
        print("Usage: python scripts/validate_tool_manifest.py <manifest.json|directory> [...]")
        return 2
    errors = [error for path in paths for error in validate(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(paths)} tool manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
