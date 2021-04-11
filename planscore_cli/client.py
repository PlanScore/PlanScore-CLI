import time
import argparse
import requests

parser = argparse.ArgumentParser(description="Process some integers.")

parser.add_argument("api_key", help="PlanScore.org API key")
parser.add_argument("input_source", help="Path for input GeoJSON file")
parser.add_argument("output_index", help="Path for output index JSON file")


def main():
    args = parser.parse_args()

    with open(args.input_source, "rb") as file1:
        posted = requests.post(
            "https://api.planscore.org/api-upload",
            data=file1,
            headers={
                "Authorization": f"Bearer {args.api_key}",
            },
        )

        index_url = posted.json()["index_url"]
        plan_url = posted.json()["plan_url"]

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
