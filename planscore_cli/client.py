import sys
import re
import time
import json
import argparse
import requests
import subprocess

parser = argparse.ArgumentParser(description="Process some integers.")

parser.add_argument("api_key", help="PlanScore.org API key")
parser.add_argument("input_source", help="Path for input GeoJSON file")
parser.add_argument("output_index", help="Path for output index JSON file")
parser.add_argument("-d", "--description", help="Plan description text")
parser.add_argument("--endpoint-url", help="Endpoint URL", default="api.planscore.org")
parser.add_argument("--library-metadata", help="Library metadata JSON", type=json.loads)


def upload_geojson(endpoint_url, api_key, input_source):
    """Submit GeoJSON content in the named file to PlanScore API"""
    with open(input_source, "rb") as file1:
        posted = requests.post(
            f"https://{endpoint_url}/api-upload",
            data=file1,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )

        if posted.status_code != 200:
            print(posted.json(), file=sys.stderr)
            raise RuntimeError(
                f"Bad status response from {endpoint_url}: {posted.status_code}"
            )
            exit(1)

        index_url = posted.json()["index_url"]
        plan_url = posted.json()["plan_url"]

    return index_url, plan_url


def upload_datasource(
    endpoint_url, api_key, input_source, description, library_metadata
):
    """Submit any datasource content in the named file to PlanScore API"""
    got = requests.get(
        f"https://{endpoint_url}/upload",
        headers={"Authorization": f"Bearer {api_key}"},
    )

    s3_url, form = got.json()
    result = subprocess.check_output(
        [
            "curl",
            s3_url,
            "--include",  # <--- output headers
            "--form",
            f"key={form['key']}",
            "--form",
            f"AWSAccessKeyId={form['AWSAccessKeyId']}",
            "--form",
            f"x-amz-security-token={form['x-amz-security-token']}",
            "--form",
            f"policy={form['policy']}",
            "--form",
            f"signature={form['signature']}",
            "--form",
            f"acl={form['acl']}",
            "--form",
            f"success_action_redirect={form['success_action_redirect']}",
            "--form",
            f"file=@{input_source}",
        ]
    )
    api_url = re.search(r"^Location: (.+)$", result.decode("utf8"), re.M).group(1)

    posted = requests.post(
        api_url,
        data=json.dumps(
            {
                "description": description,
                "library_metadata": library_metadata,
            }
        ),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    return posted.json().get("index_url"), posted.json().get("plan_url")


def main():
    args = parser.parse_args()

    if (
        args.input_source.endswith(".geojson")
        and args.description is None
        and args.library_metadata is None
    ):
        index_url, plan_url = upload_geojson(
            args.endpoint_url,
            args.api_key,
            args.input_source,
        )
    else:
        index_url, plan_url = upload_datasource(
            args.endpoint_url,
            args.api_key,
            args.input_source,
            args.description,
            args.library_metadata,
        )

    start_time = time.time()

    while True:
        time.sleep(1)
        got = requests.get(index_url)

        if got.json()["status"] is not None:
            break

    elapsed = time.time() - start_time

    with open(args.output_index, "w") as file2:
        file2.write(got.text)

    print(f"Wrote {plan_url} to {args.output_index} after {elapsed:.3f}sec")
