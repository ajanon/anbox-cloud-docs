#!/usr/bin/env python3
"""Update URLs in markdown files based on permanent redirects from link checker output."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Update URLs in markdown files based on permanent redirect information."
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to the link checker output JSON file"
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Base directory for resolving relative file paths (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    return parser.parse_args()


def load_link_check_results(file_path: Path) -> list[dict]:
    """Load and parse link checker results from NDJSON file."""
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def is_permanent_redirect(result: dict) -> bool:
    """Check if a result represents a permanent HTTP redirect.

    HTTP 301 (Moved Permanently) and 308 (Permanent Redirect) are considered permanent.
    """
    return result.get("status") == "redirected" and result.get("code") in (301, 308)


def preserve_url_fragment(old_uri: str, new_uri: str) -> str:
    """Preserve URL fragment from old URI if new URI doesn't have one.

    If the old URI has a fragment (#...) and the new URI doesn't,
    append the fragment to the new URI.
    """
    old_parsed = urlparse(old_uri)
    new_parsed = urlparse(new_uri)

    # If old URI has a fragment and new URI doesn't, preserve the fragment
    if old_parsed.fragment and not new_parsed.fragment:
        return urlunparse(
            (
                new_parsed.scheme,
                new_parsed.netloc,
                new_parsed.path,
                new_parsed.params,
                new_parsed.query,
                old_parsed.fragment,
            )
        )

    return new_uri


def update_file_redirects(
    file_path: Path, redirects: list[dict], dry_run: bool = False
) -> tuple[int, set[str]]:
    """Update redirects in a single file.

    Returns the number of lines modified and set of URIs that were found.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified_count = 0
    found_uris = set()

    # Sort redirects by URI length (longest first) to avoid substring issues
    sorted_redirects = sorted(redirects, key=lambda r: len(r["uri"]), reverse=True)

    for redirect in sorted_redirects:
        old_uri = redirect["uri"]
        new_uri = redirect["info"]

        # Preserve URL fragment if present in old URI but not in new URI
        new_uri = preserve_url_fragment(old_uri, new_uri)

        # Track if we found this URI in any line
        uri_found = False

        # Search through all lines for the old URI
        for line_idx, line in enumerate(lines):
            if old_uri not in line:
                continue

            uri_found = True
            found_uris.add(old_uri)
            updated_line = line.replace(old_uri, new_uri)

            if updated_line != line:
                if dry_run:
                    print(f"{file_path}:{line_idx + 1}")
                    print(f"  - {line.rstrip()}")
                    print(f"  + {updated_line.rstrip()}")
                else:
                    lines[line_idx] = updated_line
                modified_count += 1

    if not dry_run and modified_count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return modified_count, found_uris


def group_redirects_by_file(redirects: list[dict]) -> dict[str, list[dict]]:
    """Group redirects by filename for efficient processing."""
    files = {}
    for redirect in redirects:
        filename = redirect["filename"]
        if filename not in files:
            files[filename] = []
        files[filename].append(redirect)
    return files


def main() -> int:
    """Main entry point."""
    args = parse_arguments()

    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        return 1

    # Load and filter results
    print(f"Loading results from {args.input_file}...")
    all_results = load_link_check_results(args.input_file)
    redirects = [r for r in all_results if is_permanent_redirect(r)]

    if not redirects:
        print("No permanent redirects found.")
        return 0

    print(f"Found {len(redirects)} permanent redirect(s)")

    if args.dry_run:
        print("\nDRY RUN - No files will be modified\n")

    # Group redirects by file
    files_to_update = group_redirects_by_file(redirects)

    # Track all URIs we're looking for
    all_uris = {r["uri"] for r in redirects}
    found_uris = set()

    # Process each file
    total_modified = 0
    for filename, file_redirects in files_to_update.items():
        file_path = args.base_dir / filename

        if not file_path.exists():
            print(f"Warning: File '{file_path}' does not exist", file=sys.stderr)
            continue

        modified, uris_in_file = update_file_redirects(
            file_path, file_redirects, args.dry_run
        )
        total_modified += modified
        found_uris.update(uris_in_file)

    # Warn about redirects that weren't found
    missing_uris = all_uris - found_uris
    if missing_uris:
        print(
            f"\nWarning: {len(missing_uris)} redirect(s) not found in any file:",
            file=sys.stderr,
        )
        for uri in sorted(missing_uris):
            print(f"  - {uri}", file=sys.stderr)

    # Summary
    if args.dry_run:
        print(
            f"\nWould modify {total_modified} line(s) in {len(files_to_update)} file(s)"
        )
    else:
        print(f"\nModified {total_modified} line(s) in {len(files_to_update)} file(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
