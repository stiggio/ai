#!/usr/bin/env python3
"""
Stigg API Helper Script

Usage:
    python stigg_api.py <operation> [options]

Operations:
    list-environments     List all environments
    dump-catalog          Dump product catalog for an environment
    preview-merge         Preview merge changes between environments
    merge                 Merge environments or apply template

Environment Variables:
    STIGG_API_KEY        Required. Your Stigg API key

Examples:
    python stigg_api.py list-environments
    python stigg_api.py dump-catalog --env development
    python stigg_api.py dump-catalog --env development --output catalog.json
    python stigg_api.py preview-merge --source development --dest production
    python stigg_api.py merge --source development --dest production
    python stigg_api.py merge --template catalog.json --dest development
    python stigg_api.py merge --template catalog.json --new-env staging --type DEVELOPMENT
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

STIGG_API_URL = "https://api.stigg.io/graphql"


def get_api_key():
    api_key = os.environ.get("STIGG_API_KEY")
    if not api_key:
        print("Error: STIGG_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return api_key


def graphql_request(query: str, variables: dict = None) -> dict:
    api_key = get_api_key()

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        STIGG_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": api_key,
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
            if "errors" in result:
                print(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}", file=sys.stderr)
                sys.exit(1)
            return result["data"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def list_environments():
    query = """
    query {
      environments(paging: { first: 25 }) {
        edges {
          node {
            id
            slug
            displayName
            type
            description
            isSandbox
            provisionStatus
            createdAt
          }
        }
      }
    }
    """
    data = graphql_request(query)
    environments = [edge["node"] for edge in data["environments"]["edges"]]
    return environments


def dump_catalog(environment_slug: str) -> dict:
    query = """
    query DumpCatalog($input: DumpEnvironmentProductCatalogInput!) {
      dumpEnvironmentProductCatalog(input: $input) {
        dump
      }
    }
    """
    variables = {"input": {"environmentSlug": environment_slug}}
    data = graphql_request(query, variables)
    return data["dumpEnvironmentProductCatalog"]["dump"]


def preview_merge(source_slug: str, dest_slug: str, include_coupons: bool = True) -> dict:
    query = """
    query PreviewMerge($input: DumpEnvironmentForForMergeComparisonInput!) {
      dumpEnvironmentForMergeComparison(input: $input) {
        preMergeDump
        postMergeDump
      }
    }
    """
    variables = {
        "input": {
            "sourceEnvironmentSlug": source_slug,
            "destinationEnvironmentSlug": dest_slug,
            "mergeConfiguration": {"includeCoupons": include_coupons}
        }
    }
    data = graphql_request(query, variables)
    return data["dumpEnvironmentForMergeComparison"]


def merge_environments(
    source_slug: str = None,
    dest_slug: str = None,
    source_template: dict = None,
    new_env_name: str = None,
    new_env_type: str = None,
    include_coupons: bool = True,
    migration_type: str = "NONE"
) -> dict:
    query = """
    mutation MergeEnvironment($input: MergeEnvironmentInput!) {
      mergeEnvironment(input: $input) {
        environmentSlug
        taskIds
      }
    }
    """

    input_data = {}

    # Source: either environment slug or template
    if source_slug:
        input_data["sourceEnvironmentSlug"] = source_slug
    elif source_template:
        input_data["sourceTemplate"] = source_template
    else:
        raise ValueError("Either source_slug or source_template must be provided")

    # Destination: either existing environment or new environment
    if dest_slug:
        input_data["destinationEnvironmentSlug"] = dest_slug
    elif new_env_name:
        input_data["destinationEnvironmentName"] = new_env_name
        if new_env_type:
            input_data["destinationEnvironmentType"] = new_env_type
    else:
        raise ValueError("Either dest_slug or new_env_name must be provided")

    input_data["mergeConfiguration"] = {"includeCoupons": include_coupons}
    input_data["migrationType"] = migration_type

    variables = {"input": input_data}
    data = graphql_request(query, variables)
    return data["mergeEnvironment"]


def main():
    parser = argparse.ArgumentParser(description="Stigg API Helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list-environments
    subparsers.add_parser("list-environments", help="List all environments")

    # dump-catalog
    dump_parser = subparsers.add_parser("dump-catalog", help="Dump product catalog")
    dump_parser.add_argument("--env", required=True, help="Environment slug")
    dump_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # preview-merge
    preview_parser = subparsers.add_parser("preview-merge", help="Preview merge changes")
    preview_parser.add_argument("--source", required=True, help="Source environment slug")
    preview_parser.add_argument("--dest", required=True, help="Destination environment slug")
    preview_parser.add_argument("--no-coupons", action="store_true", help="Exclude coupons")
    preview_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # merge
    merge_parser = subparsers.add_parser("merge", help="Merge environments or apply template")
    merge_source = merge_parser.add_mutually_exclusive_group(required=True)
    merge_source.add_argument("--source", help="Source environment slug")
    merge_source.add_argument("--template", help="Template JSON file")
    merge_dest = merge_parser.add_mutually_exclusive_group(required=True)
    merge_dest.add_argument("--dest", help="Destination environment slug")
    merge_dest.add_argument("--new-env", help="New environment name")
    merge_parser.add_argument("--type", choices=["DEVELOPMENT", "PRODUCTION", "SANDBOX"],
                             help="New environment type (required with --new-env)")
    merge_parser.add_argument("--no-coupons", action="store_true", help="Exclude coupons")
    merge_parser.add_argument("--migration", choices=["NONE", "ALL"], default="NONE",
                             help="Customer migration type")

    args = parser.parse_args()

    if args.command == "list-environments":
        environments = list_environments()
        print(json.dumps(environments, indent=2))

    elif args.command == "dump-catalog":
        catalog = dump_catalog(args.env)
        output = json.dumps(catalog, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Catalog saved to {args.output}")
        else:
            print(output)

    elif args.command == "preview-merge":
        result = preview_merge(args.source, args.dest, not args.no_coupons)
        output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Preview saved to {args.output}")
        else:
            print(output)

    elif args.command == "merge":
        template = None
        if args.template:
            with open(args.template) as f:
                template = json.load(f)

        if args.new_env and not args.type:
            parser.error("--type is required when using --new-env")

        result = merge_environments(
            source_slug=args.source,
            dest_slug=args.dest,
            source_template=template,
            new_env_name=args.new_env,
            new_env_type=args.type,
            include_coupons=not args.no_coupons,
            migration_type=args.migration
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
