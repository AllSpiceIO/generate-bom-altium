#! /usr/bin/env python3

# Generate a BOM from a PrjPcb file.
# For more information, read the README file in this directory.

import argparse
import csv
import json
import os
import sys
from contextlib import ExitStack

from allspice import AllSpice
from allspice.utils.bom_generation import generate_bom


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="generate_bom", description="Generate a BOM from a project repository."
    )
    parser.add_argument(
        "repository", help="The repo containing the project in the form 'owner/repo'"
    )
    parser.add_argument(
        "source_file",
        help=(
            "The path to the source file used to generate the BOM. If this is an Altium project, "
            "this should be the .PrjPcb file. For an OrCAD project, this should be the .dsn file. "
            "Example: 'Archimajor.PrjPcb', 'Schematics/Beagleplay.dsn'."
        ),
    )
    parser.add_argument(
        "--columns",
        help=(
            "A path to a JSON file mapping columns to the attributes they are from. See the README "
            "for more details. Defaults to 'columns.json'."
        ),
        default="columns.json",
    )
    parser.add_argument(
        "--source_ref",
        help=(
            "The git reference the BOM should be generated for (eg. branch name, tag name, commit "
            "SHA). Defaults to the main branch."
        ),
        default="main",
    )
    parser.add_argument(
        "--allspice_hub_url",
        help="The URL of your AllSpice Hub instance. Defaults to https://hub.allspice.io.",
    )
    parser.add_argument(
        "--output_file",
        help="The path to the output file. If absent, the CSV will be output to the command line.",
    )
    parser.add_argument(
        "--group_by",
        help=(
            "A comma-separated list of columns to group the BOM by. If not present, the BOM will "
            "be flat."
        ),
    )
    parser.add_argument(
        "--variant",
        help=(
            "The variant of the project to generate the BOM for. If not present, the BOM will be "
            "generated for the default variant. This is not used for OrCAD projects."
        ),
    )

    args = parser.parse_args()

    columns_file = args.columns
    with open(columns_file, "r") as f:
        columns = json.loads(f.read())

    auth_token = os.environ.get("ALLSPICE_AUTH_TOKEN")
    if auth_token is None:
        print("Please set the environment variable ALLSPICE_AUTH_TOKEN")
        exit(1)

    if args.allspice_hub_url is None:
        allspice = AllSpice(token_text=auth_token)
    else:
        allspice = AllSpice(
            token_text=auth_token, allspice_hub_url=args.allspice_hub_url
        )

    repo_owner, repo_name = args.repository.split("/")
    repository = allspice.get_repository(repo_owner, repo_name)
    group_by = args.group_by.split(",") if args.group_by else None

    print("Generating BOM...", file=sys.stderr)

    bom_rows = generate_bom(
        allspice,
        repository,
        args.source_file,
        columns,
        group_by=group_by,
        ref=args.source_ref,
        variant=args.variant,
    )

    with ExitStack() as stack:
        keys = bom_rows[0].keys()
        if args.output_file is not None:
            f = stack.enter_context(open(args.output_file, "w"))
            writer = csv.DictWriter(f, fieldnames=keys)
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=keys)

        writer.writeheader()
        writer.writerows(bom_rows)

    print("Generated bom.", file=sys.stderr)
