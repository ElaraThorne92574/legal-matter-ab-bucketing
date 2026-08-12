import json
import sys

from legal_split import assign_matter


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 run_matter.py MATTER_ID")
    matter = {"matter_id": sys.argv[1], "document": "engagement-letter"}
    print(json.dumps(assign_matter(matter), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

