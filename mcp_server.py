import sys
import json
from client import ZabCluster

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "elect":
        cluster = ZabCluster({int(k): tuple(v) for k, v in params.get("nodes", {}).items()})
        return cluster.run_election()
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
