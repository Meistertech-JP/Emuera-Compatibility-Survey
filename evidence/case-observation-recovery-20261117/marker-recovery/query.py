import argparse
import json
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("--case", required=True)
args = parser.parse_args()
path = pathlib.Path(__file__).with_name("risk-observations.jsonl")
for line in path.read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row["case_id"] == args.case:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        raise SystemExit(0)
raise SystemExit(1)
