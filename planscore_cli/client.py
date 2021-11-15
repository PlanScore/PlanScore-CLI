import sys
import time
import json
import argparse
import requests

parser = argparse.ArgumentParser(description="Process some integers.")

parser.add_argument("api_key", help="PlanScore.org API key")
parser.add_argument("input_source", help="Path for input GeoJSON file")
parser.add_argument("output_index", help="Path for output index JSON file")
parser.add_argument("--endpoint-url", help="Endpoint URL", default="api.planscore.org")


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


def main():
    args = parser.parse_args()

    index_url, plan_url = upload_geojson(
        args.endpoint_url, args.api_key, args.input_source
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
