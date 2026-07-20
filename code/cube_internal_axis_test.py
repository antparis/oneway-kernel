#!/usr/bin/env python3
"""Raw-data runner for the quarantined cube internal-axis programme."""
from __future__ import annotations
import argparse
import cmath
import json
import random
from pathlib import Path
from cube_network_core import (
    CubeNetwork,
    combinatorial_summary,
    plaquettes,
    shell_depth,
    undirected_neighbour_edges,
)


def build_random_network(n: int, seed: int) -> CubeNetwork:
    rng = random.Random(seed)
    couplings = {}
    for u, v in undirected_neighbour_edges(n):
        for a, b in ((u, v), (v, u)):
            rho = 10 ** rng.uniform(-0.4, 0.4)
            phi = rng.uniform(-3.141592653589793, 3.141592653589793)
            couplings[(a, b)] = rho * cmath.exp(1j * phi)
    return CubeNetwork(n, couplings)


def random_gauge(net: CubeNetwork, seed: int) -> dict:
    rng = random.Random(seed)
    return {
        site: 10 ** rng.uniform(-0.5, 0.5) * cmath.exp(1j * rng.uniform(-3.14, 3.14))
        for site in net.sites
    }


def cycle_record(net: CubeNetwork, cycle, index: int, quasi_pole_scale: float) -> dict:
    data = net.cycle_data(cycle)
    moduli = sorted(abs(value) for value in net.couplings.values())
    median_scale = moduli[len(moduli) // 2]
    return {
        "cycle_index": index,
        "vertices": cycle,
        "forward_product": [data.forward_product.real, data.forward_product.imag],
        "reverse_product": [data.reverse_product.real, data.reverse_product.imag],
        "phase_forward": data.phase_forward,
        "phase_reverse": data.phase_reverse,
        "log_mod_forward": data.log_mod_forward,
        "log_mod_reverse": data.log_mod_reverse,
        "asymmetry_ratio": None
        if data.asymmetry_ratio is None
        else [data.asymmetry_ratio.real, data.asymmetry_ratio.imag],
        "min_reverse_modulus": data.min_reverse_modulus,
        "quasi_pole_threshold": quasi_pole_scale * median_scale,
        "quasi_pole_flag": data.min_reverse_modulus < quasi_pole_scale * median_scale,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20240517)
    parser.add_argument("--max-plaquettes", type=int, default=12)
    parser.add_argument("--output", type=Path, default=Path("cube_internal_axis_raw.json"))
    parser.add_argument("--quasi-pole-scale", type=float, default=1e-3)
    args = parser.parse_args()

    net = build_random_network(args.n, args.seed)
    gauged = net.gauge_transform(random_gauge(net, args.seed + 1))
    records = []
    for index, cycle in enumerate(plaquettes(args.n)):
        if index >= args.max_plaquettes:
            break
        before = cycle_record(net, cycle, index, args.quasi_pole_scale)
        after = cycle_record(gauged, cycle, index, args.quasi_pole_scale)
        records.append(
            {
                "before": before,
                "after_gradient_GL1C": after,
                "delta_forward_product_abs": abs(
                    complex(*before["forward_product"]) - complex(*after["forward_product"])
                ),
                "delta_reverse_product_abs": abs(
                    complex(*before["reverse_product"]) - complex(*after["reverse_product"])
                ),
            }
        )

    boundary = [site for site in net.sites if shell_depth(site, args.n) == 0]
    center_depth = max(shell_depth(site, args.n) for site in net.sites)
    center = [site for site in net.sites if shell_depth(site, args.n) == center_depth]
    payload = {
        "status": "LOCAL RAW OUTPUT; NOT PROJECT CERTIFICATE",
        "configuration": {
            "n": args.n,
            "seed": args.seed,
            "max_plaquettes": args.max_plaquettes,
            "quasi_pole_scale": args.quasi_pole_scale,
        },
        "combinatorics": combinatorial_summary(args.n),
        "boundary_site_count": len(boundary),
        "central_site_count": len(center),
        "reachable_from_boundary_count": len(net.reachable(boundary)),
        "cycle_records": records,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
