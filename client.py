class ZabNodeVote:
    """Zab Fast Leader Election vote state."""
    def __init__(self, node_id: int, epoch: int, zxid: int):
        self.node_id = node_id
        self.epoch = epoch
        self.zxid = zxid
        # Proposed vote (epoch, zxid, server_id)
        self.vote = (epoch, zxid, node_id)

    def compare_and_update(self, other_epoch: int, other_zxid: int, other_server_id: int) -> bool:
        other_vote = (other_epoch, other_zxid, other_server_id)
        if other_vote > self.vote:
            self.vote = other_vote
            return True # Adopted superior vote
        return False

class ZabCluster:
    def __init__(self, nodes: dict[int, tuple[int, int]]):
        """nodes: {node_id: (epoch, zxid)}"""
        self.nodes = {nid: ZabNodeVote(nid, ep, zx) for nid, (ep, zx) in nodes.items()}

    def run_election(self) -> dict:
        # All nodes broadcast their initial vote
        # Iterate until convergence
        changed = True
        while changed:
            changed = False
            for nid, node in self.nodes.items():
                for other_nid, other_node in self.nodes.items():
                    if nid != other_nid:
                        if node.compare_and_update(*other_node.vote):
                            changed = True

        # Count votes
        winner = next(iter(self.nodes.values())).vote[2]
        return {
            "cluster_size": len(self.nodes),
            "elected_leader": winner,
            "winning_epoch": next(iter(self.nodes.values())).vote[0],
            "winning_zxid": next(iter(self.nodes.values())).vote[1]
        }
