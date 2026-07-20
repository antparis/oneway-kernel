#!/usr/bin/env python3
import cmath
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from cube_network_core import (  # noqa: E402
    CubeNetwork,
    combinatorial_summary,
    plaquettes,
    shell_counts,
    undirected_neighbour_edges,
)


def random_net(n=3, seed=20240517):
    rng = random.Random(seed)
    couplings = {}
    for u, v in undirected_neighbour_edges(n):
        for a, b in ((u, v), (v, u)):
            couplings[(a, b)] = (0.3 + rng.random()) * cmath.exp(1j * rng.uniform(-3, 3))
    return CubeNetwork(n, couplings)


class CubeTests(unittest.TestCase):
    def test_combinatorics(self):
        summary = combinatorial_summary(3)
        self.assertEqual(
            (summary["total_sites"], summary["outer_shell_sites"], summary["strict_interior_sites"]),
            (27, 26, 1),
        )
        self.assertEqual(
            (summary["visible_faces"], summary["internal_faces"], summary["undirected_contacts"]),
            (54, 108, 54),
        )
        self.assertEqual(shell_counts(7), [218, 98, 26, 1])

    def test_gradient_gauge_preserves_directed_cycle_products(self):
        net = random_net()
        cycle = next(plaquettes(3))
        before = net.cycle_data(cycle)
        rng = random.Random(9)
        gauge = {
            site: (0.2 + rng.random()) * cmath.exp(1j * rng.random())
            for site in net.sites
        }
        after = net.gauge_transform(gauge).cycle_data(cycle)
        self.assertAlmostEqual(abs(before.forward_product - after.forward_product), 0.0, places=12)
        self.assertAlmostEqual(abs(before.reverse_product - after.reverse_product), 0.0, places=12)

    def test_two_cycle_survives_on_open_chain(self):
        couplings = {
            ((0, 0, 0), (1, 0, 0)): 2 + 3j,
            ((1, 0, 0), (0, 0, 0)): -1 + 0.5j,
        }
        for u, v in undirected_neighbour_edges(2):
            couplings.setdefault((u, v), 1 + 0j)
            couplings.setdefault((v, u), 1 + 0j)
        net = CubeNetwork(2, couplings)
        cycle = ((0, 0, 0), (1, 0, 0))
        before = net.cycle_data(cycle).forward_product
        gauge = {site: 1 + 0j for site in net.sites}
        gauge[(0, 0, 0)] = 3 + 2j
        gauge[(1, 0, 0)] = 0.4 - 1j
        after = net.gauge_transform(gauge).cycle_data(cycle).forward_product
        self.assertAlmostEqual(abs(before - after), 0.0, places=12)

    def test_negative_mutant_omitted_edge_changes_product(self):
        net = random_net()
        cycle = next(plaquettes(3))
        reference = net.cycle_data(cycle).forward_product
        mutant = dict(net.couplings)
        u, v = cycle[0], cycle[1]
        mutant[(u, v)] *= 1.7
        changed = CubeNetwork(3, mutant).cycle_data(cycle).forward_product
        self.assertGreater(abs(reference - changed), 1e-8)

    def test_equal_count_does_not_fix_connectivity(self):
        net = CubeNetwork.reciprocal(3)
        removed_a = {(1, 1, 1)}
        removed_b = {(1, 1, 0)}
        source = {(0, 1, 1)}
        center = {(1, 1, 1)}
        self.assertEqual(len(removed_a), len(removed_b))
        self.assertNotEqual(
            bool(net.reachable(source, removed_a) & center),
            bool(net.reachable(source, removed_b) & center),
        )


if __name__ == "__main__":
    unittest.main()
