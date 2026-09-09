from client import ZabCluster

def main():
    print("=== Zab Fast Leader Election ===")
    # Cluster with 3 servers: Server 1, 2, 3
    # Server 3 has newest ZXID 108
    cluster = ZabCluster({
        1: (1, 100),
        2: (1, 105),
        3: (1, 108)
    })

    res = cluster.run_election()
    print("Zab Election Result:", res)
    assert res["elected_leader"] == 3
    assert res["winning_zxid"] == 108

    print("Zab Fast Leader Election verified successfully!")

if __name__ == "__main__":
    main()
