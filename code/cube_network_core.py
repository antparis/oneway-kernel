#!/usr/bin/env python3
"""Core objects for the quarantined cube-internal-axis research harness.

This module models an N x N x N directed nearest-neighbour network. It does
not assign physical meaning to the couplings and it does not evaluate eml★.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple
import cmath

Site = Tuple[int, int, int]
Edge = Tuple[Site, Site]


@dataclass(frozen=True)
class CycleData:
    vertices: Tuple[Site, ...]
    forward_product: complex
    reverse_product: complex
    phase_forward: float
    phase_reverse: float
    log_mod_forward: float
    log_mod_reverse: float
    asymmetry_ratio: complex | None
    min_reverse_modulus: float


class CubeNetwork:
    def __init__(self, n: int, couplings: Mapping[Edge, complex]):
        if n < 2:
            raise ValueError("n must be >= 2")
        self.n = int(n)
        self.sites: Tuple[Site, ...] = tuple(product(range(n), repeat=3))
        self.couplings: Dict[Edge, complex] = dict(couplings)
        self._validate_edges()

    def _validate_edges(self) -> None:
        valid = set(self.sites)
        for (u, v), value in self.couplings.items():
            if u not in valid or v not in valid:
                raise ValueError(f"edge outside cube: {(u, v)}")
            if manhattan(u, v) != 1:
                raise ValueError(f"non-nearest-neighbour edge: {(u, v)}")
            if value == 0:
                raise ValueError("zero couplings are excluded; use an explicit cut mask")

    @classmethod
    def reciprocal(cls, n: int, value: complex = 1.0 + 0.0j) -> "CubeNetwork":
        c: Dict[Edge, complex] = {}
        for u, v in undirected_neighbour_edges(n):
            c[(u, v)] = value
            c[(v, u)] = value
        return cls(n, c)

    def directed_matrix(self) -> List[List[complex]]:
        idx = {s: i for i, s in enumerate(self.sites)}
        m = [[0j for _ in self.sites] for _ in self.sites]
        for (u, v), val in self.couplings.items():
            m[idx[v]][idx[u]] = val
        return m

    def gauge_transform(self, site_factors: Mapping[Site, complex]) -> "CubeNetwork":
        """Apply the gradient GL(1,C) site law J_uv -> (g_u/g_v) J_uv."""
        c: Dict[Edge, complex] = {}
        for (u, v), val in self.couplings.items():
            gu = complex(site_factors[u])
            gv = complex(site_factors[v])
            if gu == 0 or gv == 0:
                raise ValueError("site gauge factors must be nonzero")
            c[(u, v)] = (gu / gv) * val
        return CubeNetwork(self.n, c)

    def active_adjacency(self, removed: Iterable[Site] = ()) -> Dict[Site, List[Site]]:
        blocked = set(removed)
        adj = {s: [] for s in self.sites if s not in blocked}
        for (u, v), val in self.couplings.items():
            if u in blocked or v in blocked or val == 0:
                continue
            adj[u].append(v)
        return adj

    def reachable(self, sources: Iterable[Site], removed: Iterable[Site] = ()) -> set[Site]:
        adj = self.active_adjacency(removed)
        seen = {s for s in sources if s in adj}
        stack = list(seen)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    def cycle_data(self, vertices: Sequence[Site]) -> CycleData:
        if len(vertices) < 2:
            raise ValueError("cycle requires at least two vertices")
        cyc = tuple(vertices)
        fwd = 1 + 0j
        rev = 1 + 0j
        min_rev = float("inf")
        for i, u in enumerate(cyc):
            v = cyc[(i + 1) % len(cyc)]
            jf = self.couplings[(u, v)]
            jr = self.couplings[(v, u)]
            fwd *= jf
            rev *= jr
            min_rev = min(min_rev, abs(jr))
        ratio = None if rev == 0 else fwd / rev
        return CycleData(
            vertices=cyc,
            forward_product=fwd,
            reverse_product=rev,
            phase_forward=cmath.phase(fwd),
            phase_reverse=cmath.phase(rev),
            log_mod_forward=log(abs(fwd)),
            log_mod_reverse=log(abs(rev)),
            asymmetry_ratio=ratio,
            min_reverse_modulus=min_rev,
        )


def manhattan(a: Site, b: Site) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


def undirected_neighbour_edges(n: int) -> Iterator[Tuple[Site, Site]]:
    for x, y, z in product(range(n), repeat=3):
        u = (x, y, z)
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            v = (x + dx, y + dy, z + dz)
            if max(v) < n:
                yield u, v


def plaquettes(n: int) -> Iterator[Tuple[Site, Site, Site, Site]]:
    """Yield oriented elementary square plaquettes in xy, xz and yz planes."""
    for x in range(n - 1):
        for y in range(n - 1):
            for z in range(n):
                yield ((x, y, z), (x + 1, y, z), (x + 1, y + 1, z), (x, y + 1, z))
    for x in range(n - 1):
        for y in range(n):
            for z in range(n - 1):
                yield ((x, y, z), (x + 1, y, z), (x + 1, y, z + 1), (x, y, z + 1))
    for x in range(n):
        for y in range(n - 1):
            for z in range(n - 1):
                yield ((x, y, z), (x, y + 1, z), (x, y + 1, z + 1), (x, y, z + 1))


def shell_depth(site: Site, n: int) -> int:
    return min(site[0], site[1], site[2], n - 1 - site[0], n - 1 - site[1], n - 1 - site[2])


def shell_counts(n: int) -> List[int]:
    out: List[int] = []
    d = 0
    while n - 2 * d > 0:
        length = n - 2 * d
        inner = max(length - 2, 0)
        out.append(length**3 - inner**3)
        d += 1
    return out


def combinatorial_summary(n: int) -> dict[str, int | List[int]]:
    total = n**3
    interior = max(n - 2, 0) ** 3
    shell = total - interior
    contacts = 3 * n * n * (n - 1)
    return {
        "n": n,
        "total_sites": total,
        "outer_shell_sites": shell,
        "strict_interior_sites": interior,
        "visible_faces": 6 * n * n,
        "internal_faces": 6 * n * n * (n - 1),
        "undirected_contacts": contacts,
        "shell_counts": shell_counts(n),
    }
