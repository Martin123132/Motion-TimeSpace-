from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import time
import traceback
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from local_dispersive_preparation_20260906 import POST, MAIN_STATE, active_main_workers, limit_resources

OUTPUT = POST / "source-intake/functional_rg/5514"
TARGET = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
PINS = {
    "source-intake/functional_rg/5451/P8_Y5_BRR5396_5451_VALIDATION.csv": "044970454133debdebc767be3821991916943c0725b11b3d96408a921102614d",
    "source-intake/functional_rg/5513/source_register.csv": "d1ebcff25a564c86cf89afcee1e4910b0acbfd5e5361b45901ddbcec58361729",
    "source-intake/functional_rg/5451/D4_event_endpoint_xt_overlap_cover.csv": "6a82bd1570e6ae40c29f57dc42ec8a47c1d2de6bc240d22f1b82eec55827aa0b",
    "source-intake/functional_rg/5468/D4_exact_outer_cuboid_manifest.csv": "7c528bd3481884f36536b39dc5c7e13629efbf3aad5f1b525bf72ff1677bfb29",
    "source-intake/functional_rg/5513/D4_parent_v59_resumable_final_branch_active_cuboid_closure_result.json": "fc13d197f267b3c379ce825cd89e61eda7018f49a80e4afc5722bb4be72bd232",
    "source-intake/functional_rg/5468/D4_exact_outer_cuboid_membership.csv": "501c9d685ad235752ac9a9e985f1e166ee9c28734da1a9ae6bce87a2945fc345",
    "source-intake/functional_rg/5468/source_register.csv": "b6f6554ac6afddd28aed4d3a414217753da102d46bca7eff2865e34d9a6059e4",
    "scripts/Y5_R2FR_5513_D4_parent_v59_resumable_final_branch_active_cuboid_closure.py": "7349a0db3653c8038f2b14018b996ff94181800093bb8818d78c170f5c2ec6ff",
    "source-intake/functional_rg/5469/D4_resumable_three_axis_cuboid_result.json": "30c6173a16f5738966e6f7093272bbce5b1a9dac00f6989bf77dcab16d414202",
    "source-intake/functional_rg/5513/P8_Y5_BRR5512_5513_VALIDATION.csv": "e35cf6fdb93830039a9304d9d0d08dc901d1843f4044dab10969d5420b0314ba",
    "source-intake/functional_rg/5468/P8_Y5_BRR5467_5468_VALIDATION.csv": "3e55f22a0a73f811de99c54514f4d1449e79e2ed81069115b2b38aae78c6f5f1",
    "source-intake/functional_rg/5513/D4_parent_v59_active_cuboid_union_audit.csv": "6fd7f902a8c3d6e73fa78ec4da21b2dad3383fa3992aa5bd4b6b3719a6512bd9",
    "source-intake/functional_rg/5469/source_register.csv": "0e5a06f3a19cd0302f159b2ba0baac4e6c18d6412a8b5a72425397b812ae50e3",
    "source-intake/functional_rg/5469/P8_Y5_BRR5468_5469_VALIDATION.csv": "502b4472c915da92952f5cca22f16e41e1e4613a936d9bf2bf2a37f4a6bb8b20",
    "source-intake/functional_rg/5513/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json": "7ab2c0b74444f4bfd3d828c0dcf36409fd771d4963ef55012fdbe734e7c2c6e6",
    "source-intake/functional_rg/5469/D4_resumable_three_axis_cuboid_certificates.csv": "0f52e5afb7b0058a5e89d939d02923ae8ee1edd37228f24d959d70250c5d4946",
    "scripts/Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py": "0c0f75c1a4d642c97a559b6938b80e141f220a5b5b8e5e7733b3d48ab779749f",
    "scripts/local_dispersive_preparation_20260906.py": "74090c8c0ea2b65e57132cb2e16621d51f8d80d5b18c52bf552b4198d6a7f148",
    "source-intake/functional_rg/5467/D4_outer_leaf_epsilon_fiber_manifest.csv": "7d8b94b1bd9ec3cabe329e0f7d91b8bc3cac873a812223c79bd5e26e5542e162",
    "scripts/Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py": "ad932efe91d0f90c94549677a7b8bc897df3ed8819a55d0a07db182773a0c8a3",
    "source-intake/functional_rg/5467/source_register.csv": "38333621f273d0b8cde6149e9c0db734ebc3238eea2bc1200d89b422d5739d4c"
}
REGISTERS = [f"source-intake/functional_rg/{checkpoint}/source_register.csv" for checkpoint in (5513, 5468, 5469, 5467)]
MANIFEST = "source-intake/functional_rg/5468/D4_exact_outer_cuboid_manifest.csv"
MEMBERSHIP = "source-intake/functional_rg/5468/D4_exact_outer_cuboid_membership.csv"
FIBERS = "source-intake/functional_rg/5467/D4_outer_leaf_epsilon_fiber_manifest.csv"
LEAVES = "source-intake/functional_rg/5451/D4_event_endpoint_xt_overlap_cover.csv"
OLD_CERTIFICATES = "source-intake/functional_rg/5469/D4_resumable_three_axis_cuboid_certificates.csv"
MAIN_RESULT = "source-intake/functional_rg/5513/D4_parent_v59_resumable_final_branch_active_cuboid_closure_result.json"
AXES = ("epsilon_real", "x", "t")
SEMANTIC_FIELDS = ("event_id", "event_type", "branch_owner_id", "mapped_cell_id", "term_id", "primary_surface_id", "path_segment", "gap_enclosure_method")
FIBER_KEY_FIELDS = (
    "event_id", "event_type", "branch_owner_id", "mapped_cell_id", "term_id", "primary_surface_id",
    "epsilon_bin_index", "epsilon_subdivision_count", "path_segment", "x_lower", "x_upper", "x_width",
    "t_lower", "t_upper", "t_width", "parameter_area", "physical_path_area_abs_upper", "refinement_depth",
    "refinement_path", "path_speed_abs_upper", "gap_enclosure_method",
)
LOWER_FIELDS = ("minimum_amplitude_denominator_abs_lower", "relative_root_abs_lower",
                "selected_global_root_abs_lower", "collision_jacobian_abs_lower")
CLAIM_FIELDS = ("valid_for_full_outer_parent_leaf_enclosure", "valid_for_full_event_cell_finite_cover",
                "valid_for_D4_event_local_W3_bound", "valid_for_all_operator_local_GR_claim", "valid_for_full_MTS_claim")


def digest(path):
    checksum = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def read_csv(relative):
    with (POST / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def read_json(relative):
    return json.loads((POST / relative).read_text(encoding="utf-8-sig"))


def truth(value):
    return value is True or value == "True"


def number(value):
    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError("Nonfinite certificate/domain value")
    return converted


def exact(value):
    return Fraction.from_float(number(value))


def box(row):
    result = tuple((exact(row[axis + "_lower"]), exact(row[axis + "_upper"])) for axis in AXES)
    if any(lower >= upper for lower, upper in result):
        raise ValueError("Empty or reversed box")
    return result


def volume(bounds):
    return math.prod(upper - lower for lower, upper in bounds)


def contained(inner, outer):
    return all(outer_lower <= lower < upper <= outer_upper for (lower, upper), (outer_lower, outer_upper) in zip(inner, outer))


def exact_cover(root, children):
    if not children or any(not contained(child, root) for child in children):
        return {"exact_closed_cover": False, "contained": False, "interior_disjoint": False, "volume_error": "unavailable"}
    ordered = sorted(children, key=lambda child: child[0])
    overlap = False
    for index, left in enumerate(ordered):
        for right in ordered[index + 1:]:
            if right[0][0] >= left[0][1]:
                break
            if all(max(left_axis[0], right_axis[0]) < min(left_axis[1], right_axis[1]) for left_axis, right_axis in zip(left, right)):
                overlap = True
                break
        if overlap:
            break
    error = volume(root) - sum((volume(child) for child in children), Fraction(0))
    return {"exact_closed_cover": error == 0 and not overlap, "contained": True,
            "interior_disjoint": not overlap, "volume_error": str(error),
            "root_exact_volume": str(volume(root)), "child_count": len(children)}


def semantic_key(row):
    return tuple(row[field] for field in SEMANTIC_FIELDS) + tuple(
        number(row[field]).hex() for field in ("epsilon_imaginary_lower", "epsilon_imaginary_upper"))


def interval_union_length(intervals):
    if not intervals:
        return Fraction(0)
    ordered = sorted(intervals)
    total = Fraction(0)
    lower, upper = ordered[0]
    for next_lower, next_upper in ordered[1:]:
        if next_lower > upper:
            total += upper - lower
            lower, upper = next_lower, next_upper
        else:
            upper = max(upper, next_upper)
    return total + upper - lower


def union_cover(root, children):
    if not children or any(not contained(child, root) for child in children):
        return {"exact_closed_cover": False, "contained": False}
    epsilon_boundaries = sorted({endpoint for child in children for endpoint in child[0]})
    union_volume = Fraction(0)
    for epsilon_lower, epsilon_upper in zip(epsilon_boundaries, epsilon_boundaries[1:]):
        active = [child for child in children if child[0][0] <= epsilon_lower and epsilon_upper <= child[0][1]]
        x_boundaries = sorted({endpoint for child in active for endpoint in child[1]})
        area = Fraction(0)
        for x_lower, x_upper in zip(x_boundaries, x_boundaries[1:]):
            intervals = [child[2] for child in active if child[1][0] <= x_lower and x_upper <= child[1][1]]
            area += (x_upper - x_lower) * interval_union_length(intervals)
        union_volume += (epsilon_upper - epsilon_lower) * area
    summed_volume = sum((volume(child) for child in children), Fraction(0))
    error = volume(root) - union_volume
    return {"exact_closed_cover": error == 0, "contained": True, "root_exact_volume": str(volume(root)),
            "union_exact_volume": str(union_volume), "volume_error": str(error),
            "overlap_volume_excess": str(summed_volume - union_volume), "overlap_present": summed_volume > union_volume,
            "epsilon_slabs": len(epsilon_boundaries) - 1, "child_count": len(children)}


def identifier(row, members):
    member_hash = hashlib.sha256("\n".join(sorted(members)).encode()).hexdigest()
    payload = [*semantic_key(row), *(number(row[axis + suffix]).hex() for axis in AXES for suffix in ("_lower", "_upper")), member_hash]
    suffix = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()[:16]
    return f"{row['event_id']}__{row['mapped_cell_id']}__{row['path_segment']}__CUBOID__{suffix}", member_hash


def lower_bounds(rows):
    if not rows or not all(truth(row["probe_passed"]) for row in rows):
        raise ValueError("Nonaccepted row cannot supply a bound")
    result = {}
    for field in LOWER_FIELDS:
        value = min(number(row[field]) for row in rows)
        if value <= 0:
            raise ValueError(f"Nonpositive lower certificate bound: {field}")
        result[field] = math.nextafter(value, -math.inf)
    upper_inputs = [number(row["integrated_regular_path_abs_upper"]) for row in rows]
    if any(value < 0 for value in upper_inputs):
        raise ValueError("Negative upper bound")
    upward_inputs = [Fraction.from_float(math.nextafter(value, math.inf)) for value in upper_inputs]
    result["integrated_regular_path_abs_upper"] = math.nextafter(float(sum(upward_inputs, Fraction(0))), math.inf)
    return result


def workbench_snapshot():
    root = POST.parent / "formalization-workbench"
    if not root.is_dir():
        raise FileNotFoundError(root)
    records = []
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories.sort()
        for filename in sorted(filenames):
            path = Path(directory) / filename
            stat = path.stat()
            records.append((str(path.relative_to(root)), stat.st_size, stat.st_mtime_ns))
    return {"files": len(records), "metadata_sha256": hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()}


def provenance():
    for relative, expected in PINS.items():
        if digest(POST / relative) != expected:
            raise ValueError(f"Pinned input changed: {relative}")
    sources = dict(PINS)
    register_counts = {}
    for register in REGISTERS:
        entries = read_csv(register)
        register_counts[register] = len(entries)
        for entry in entries:
            path = Path(entry.get("source_path") or entry.get("path"))
            relative = str(path.resolve().relative_to(POST.resolve())).replace("\\", "/")
            expected = entry["sha256"]
            if relative in sources and sources[relative] != expected:
                raise ValueError(f"Conflicting source hashes: {relative}")
            if relative not in sources and digest(path) != expected:
                raise ValueError(f"Historical source register changed: {relative}")
            sources[relative] = expected
    return sources, register_counts


def require(checks, name, condition, evidence):
    checks[name] = {"passed": bool(condition), "evidence": evidence}
    if not condition:
        raise ValueError(f"{name}: {evidence}")


def controls():
    root = ((Fraction(0), Fraction(1)),) * 3
    halves = [((Fraction(0), Fraction(1, 2)), *root[1:]), ((Fraction(1, 2), Fraction(1)), *root[1:])]
    escaped = [((Fraction(0), Fraction.from_float(math.nextafter(1.0, math.inf))), *root[1:])]
    overlapping = [((Fraction(0), Fraction(3, 4)), *root[1:]), ((Fraction(1, 4), Fraction(1)), *root[1:])]
    return {
        "exact_two_piece_union_accepted": exact_cover(root, halves)["exact_closed_cover"],
        "duplicate_box_rejected": not exact_cover(root, [root, root])["exact_closed_cover"],
        "gap_rejected": not exact_cover(root, halves[:1])["exact_closed_cover"],
        "one_ulp_escape_rejected": not exact_cover(root, escaped)["exact_closed_cover"],
        "overlapping_closed_cover_verified_as_union": union_cover(root, overlapping)["exact_closed_cover"],
        "overlap_is_explicit_not_erased": union_cover(root, overlapping)["overlap_volume_excess"] == "1/2",
        "union_method_rejects_gap": not union_cover(root, halves[:1])["exact_closed_cover"],
    }


def write_json(path, payload):
    serialized = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8") as stream:
        stream.write(serialized)


def write_csv(path, rows):
    if not rows:
        raise ValueError("Refusing an empty certificate table")
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def calculate(checks):
    manifest_rows = read_csv(MANIFEST)
    manifest = {row["cuboid_job_id"]: row for row in manifest_rows}
    fiber_rows = read_csv(FIBERS)
    fibers = {row["fiber_job_id"]: row for row in fiber_rows}
    memberships = read_csv(MEMBERSHIP)
    members = defaultdict(list)
    used_fibers = set()
    for row in memberships:
        cuboid, fiber = row["cuboid_job_id"], row["source_fiber_job_id"]
        if cuboid not in manifest or fiber not in fibers or fiber in used_fibers:
            raise ValueError("Missing or duplicate global fiber membership")
        used_fibers.add(fiber)
        members[cuboid].append(fiber)
    require(checks, "global_manifest_dimensions_and_partition", len(manifest_rows) == len(manifest) == len(members) == 21065
            and len(fiber_rows) == len(fibers) == len(used_fibers) == 99522
            and sum(int(row["source_leaf_count"]) for row in manifest_rows) == 606990
            and sum(int(row["source_leaf_count"]) for row in fiber_rows) == 606990,
            {"cuboids": len(manifest), "fibers": len(fibers), "membership_rows": len(memberships)})
    for checkpoint, relative in (
        (5513, "source-intake/functional_rg/5513/P8_Y5_BRR5512_5513_VALIDATION.csv"),
        (5468, "source-intake/functional_rg/5468/P8_Y5_BRR5467_5468_VALIDATION.csv"),
        (5469, "source-intake/functional_rg/5469/P8_Y5_BRR5468_5469_VALIDATION.csv"),
        (5451, "source-intake/functional_rg/5451/P8_Y5_BRR5396_5451_VALIDATION.csv"),
    ):
        validation = read_csv(relative)
        require(checks, f"prior_{checkpoint}_validation_passes", bool(validation) and all(truth(row["passed"]) for row in validation), len(validation))

    state, result = read_json(str(MAIN_STATE.relative_to(POST))), read_json(MAIN_RESULT)
    target = manifest[TARGET]
    require(checks, "main_complete_state_is_bound_to_target", state["cuboid_job_id"] == TARGET
            and state["source_fiber_membership_sha256"] == target["source_fiber_membership_sha256"]
            and box(state["root"]) == box(target) and len(state["accepted"]) == 218
            and not state["stack"] and not state["unresolved"]
            and result["exact_active_cuboid_closure"] is True and result["failed_validation_count"] == 0,
            {"accepted": len(state["accepted"]), "pending": len(state["stack"]), "unresolved": len(state["unresolved"])})
    accepted_cover = exact_cover(box(state["root"]), [box(row) for row in state["accepted"]])
    require(checks, "accepted_subcuboids_independently_cover_root_exactly", accepted_cover["exact_closed_cover"], accepted_cover)
    new_bounds = lower_bounds(state["accepted"])
    require(checks, "regional_bounds_positive_and_outward_carried", all(new_bounds[field] > 0 for field in LOWER_FIELDS), new_bounds)
    old_certificates = read_csv(OLD_CERTIFICATES)
    old_by_id = {row["cuboid_job_id"]: row for row in old_certificates}
    require(checks, "old_certificate_is_not_replaced_or_duplicated", len(old_by_id) == len(old_certificates) == 1 and TARGET not in old_by_id
            and sum(int(row["source_leaf_count"]) for row in old_certificates) == 810, list(old_by_id))
    certified_ids = set(old_by_id) | {TARGET}
    certificates, fiber_audit, cover_audit = [], [], {}
    leaf_lookup = defaultdict(dict)
    selected_fibers = {}
    for cuboid_id in sorted(certified_ids):
        root = manifest[cuboid_id]
        root_members = members[cuboid_id]
        reproduced_id, member_hash = identifier(root, root_members)
        require(checks, cuboid_id + "_semantic_and_member_signature", reproduced_id == cuboid_id
                and member_hash == root["source_fiber_membership_sha256"] and len(root_members) == int(root["source_fiber_count"]),
                {"fiber_count": len(root_members), "signature": member_hash})
        fiber_boxes = []
        count = 0
        for fiber_id in root_members:
            fiber = fibers[fiber_id]
            if semantic_key(fiber) != semantic_key(root) or not contained(box(fiber), box(root)):
                raise ValueError(f"Fiber owner or domain does not match parent: {fiber_id}")
            fiber_boxes.append(box(fiber))
            first, last = int(fiber["source_subdivision_index_lower"]), int(fiber["source_subdivision_index_upper"])
            if last - first + 1 != int(fiber["source_leaf_count"]):
                raise ValueError("Fiber source-index interval is not a bijection")
            key = tuple(fiber[field] for field in FIBER_KEY_FIELDS)
            for source_index in range(first, last + 1):
                if source_index in leaf_lookup[key]:
                    raise ValueError("Duplicate expected source leaf")
                leaf_lookup[key][source_index] = fiber_id
            selected_fibers[fiber_id] = (cuboid_id, fiber)
            count += int(fiber["source_leaf_count"])
        cover = union_cover(box(root), fiber_boxes)
        cover_audit[cuboid_id] = cover
        require(checks, cuboid_id + "_fiber_union_exact_with_overlap_recorded", cover["exact_closed_cover"] and count == int(root["source_leaf_count"]), cover)
        if cuboid_id == TARGET:
            bounds = new_bounds
            certificate_source = MAIN_RESULT
            parent_revision = result["parent_revision"]
        else:
            old = old_by_id[cuboid_id]
            require(checks, "old_certificate_scope_and_binding", truth(old["valid_for_exact_outer_cuboid_transplant"])
                    and old["source_fiber_membership_sha256"] == member_hash
                    and all(old[field] == root[field] for field in ("event_id", "mapped_cell_id", "term_id", "branch_owner_id", "path_segment"))
                    and all(exact(old[field]) == exact(root[field]) for field in ("x_lower", "x_upper", "t_lower", "t_upper"))
                    and exact(old["epsilon_cuboid_real_lower"]) == exact(root["epsilon_real_lower"])
                    and exact(old["epsilon_cuboid_real_upper"]) == exact(root["epsilon_real_upper"]),
                    old["cuboid_job_id"])
            bounds, certificate_source, parent_revision = lower_bounds([old]), OLD_CERTIFICATES, old["parent_revision"]
        certificates.append({**root, **bounds, "certificate_source": certificate_source, "parent_revision": parent_revision,
                             "certificate_source_sha256": PINS[certificate_source], "probe_passed": True,
                             "valid_for_exact_outer_cuboid_transplant": True, "bound_transfer": "SAME_OWNER_EXACT_SUBDOMAIN_RESTRICTION",
                             **{field: False for field in CLAIM_FIELDS}})

    selected_leaf_rows, seen, observed = [], set(), defaultdict(list)
    outer_count = 0
    with (POST / LEAVES).open(encoding="utf-8-sig", newline="") as stream:
        for ordinal, row in enumerate(csv.DictReader(stream), start=1):
            if row["cover_owner"] != "OUTER_PARENT_TRIANGLE":
                continue
            outer_count += 1
            key = tuple(row[field] for field in FIBER_KEY_FIELDS)
            if key not in leaf_lookup:
                continue
            source_index = int(row["epsilon_subdivision_index"])
            fiber_id = leaf_lookup[key].get(source_index)
            if fiber_id is None:
                continue
            identity = (fiber_id, source_index)
            if identity in seen:
                raise ValueError("Repeated source identity in original cover")
            seen.add(identity)
            cuboid_id, fiber = selected_fibers[fiber_id]
            root = manifest[cuboid_id]
            if (not truth(row["geometry_cover_leaf_passes"]) or not truth(row["requires_parent_outer_amplitude_enclosure"])
                    or exact(row["gap_abs_lower"]) < exact(5e-6)
                    or not contained(box(row), box(fiber)) or not contained(box(row), box(root))
                    or semantic_key(row) != semantic_key(root)):
                raise ValueError(f"Original source leaf does not lie in its certified outer domain: {ordinal}")
            for field in ("material_root_denominator_abs_lower", "implicit_material_derivative_abs_lower"):
                if number(row[field]) <= 0:
                    raise ValueError("Source geometry denominator is nonpositive")
            observed[fiber_id].append((source_index, box(row)[0]))
            selected_leaf_rows.append({
                "source_data_row_ordinal": ordinal, "cuboid_job_id": cuboid_id, "source_fiber_job_id": fiber_id,
                "epsilon_subdivision_index": source_index, "epsilon_bin_index": row["epsilon_bin_index"],
                **{field: row[field] for field in SEMANTIC_FIELDS},
                **{axis + suffix: row[axis + suffix] for axis in AXES for suffix in ("_lower", "_upper")},
                "epsilon_imaginary_lower": row["epsilon_imaginary_lower"], "epsilon_imaginary_upper": row["epsilon_imaginary_upper"],
                "source_gap_abs_lower": row["gap_abs_lower"], "source_cover_sha256": PINS[LEAVES],
                "valid_for_this_source_leaf_parent_enclosure": True,
                "valid_for_full_outer_parent_leaf_enclosure": False, "valid_for_all_operator_local_GR_claim": False,
            })
    require(checks, "original_outer_source_count_reproduced", outer_count == 606990, outer_count)
    for fiber_id, (cuboid_id, fiber) in selected_fibers.items():
        entries = sorted(observed[fiber_id])
        expected_count = int(fiber["source_leaf_count"])
        if len(entries) != expected_count:
            raise ValueError(f"Source leaves missing from fiber: {fiber_id}")
        epsilon_union = (entries[0][1][0] == exact(fiber["epsilon_real_lower"])
                         and entries[-1][1][1] == exact(fiber["epsilon_real_upper"])
                         and all(left[0] + 1 == right[0] and left[1][1] == right[1][0] for left, right in zip(entries, entries[1:])))
        if not epsilon_union:
            raise ValueError(f"Source epsilon union is not binary-exact: {fiber_id}")
        fiber_audit.append({"cuboid_job_id": cuboid_id, "source_fiber_job_id": fiber_id,
                            "expected_source_leaves": expected_count, "verified_source_leaves": len(entries),
                            "source_index_bijection": True, "exact_epsilon_union": True, "same_owner_containment": True})
    newly_certified = sum(row["cuboid_job_id"] == TARGET for row in selected_leaf_rows)
    require(checks, "new_and_carried_source_counts_are_exact", newly_certified == 39732 and len(selected_leaf_rows) == 40542
            and len(seen) == len(selected_leaf_rows) and len(selected_fibers) == 1559,
            {"new": newly_certified, "total": len(selected_leaf_rows), "verified_fibers": len(selected_fibers)})
    frontier = [{"cuboid_job_id": row["cuboid_job_id"], "evaluation_priority": int(row["evaluation_priority"]),
                 "source_leaf_count": int(row["source_leaf_count"]), "source_fiber_count": int(row["source_fiber_count"]),
                 "certified": row["cuboid_job_id"] in certified_ids,
                 "action": "ALREADY_CERTIFIED_DO_NOT_RECOMPUTE" if row["cuboid_job_id"] in certified_ids else "NEEDS_BOUND_CERTIFICATE"}
                for row in manifest_rows]
    remaining = [row for row in frontier if not row["certified"]]
    remaining.sort(key=lambda row: row["evaluation_priority"])
    require(checks, "source_membership_is_unique_and_counts_conserved", len(remaining) == 21063
            and sum(row["source_leaf_count"] for row in remaining) + len(selected_leaf_rows) == 606990,
            {"certified_cuboids": len(certified_ids), "remaining": len(remaining)})
    payload = {
        "checkpoint": 5514, "revision": "D4-parent-v59-exact-source-leaf-transplant-v1",
        "decision": "CERTIFIED_ACTIVE_CUBOID_TRANSPLANTED__CONTINUE_OUTER_COVER",
        "newly_certified_cuboid_id": TARGET, "newly_certified_source_leaf_count": newly_certified,
        "certified_cuboid_count": len(certified_ids), "certified_source_leaf_count": len(selected_leaf_rows),
        "source_leaf_count": outer_count, "cuboid_count": len(manifest), "certified_fiber_count": len(selected_fibers),
        "remaining_cuboid_count": len(remaining), "remaining_source_leaf_count": outer_count - len(selected_leaf_rows),
        "next_target": remaining[0], "valid_for_exact_source_leaf_transplant": True,
        **{field: False for field in CLAIM_FIELDS},
        "parent_numeric_reevaluations": 0,
        "no_representative_margin_transferred": True, "no_epsilon_average_used": True,
        "physical_coupled_O4_reference_is_separate": True,
    }
    return payload, certificates, selected_leaf_rows, fiber_audit, frontier, {"accepted_root_cover": accepted_cover, "source_fiber_covers": cover_audit}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="initial")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if not arguments.tag.replace("-", "").isalnum():
        raise ValueError("Use a nonempty alphanumeric tag")
    limit_resources()
    sources, register_counts = provenance()
    workers = active_main_workers()
    directory = OUTPUT / arguments.tag
    if arguments.dry_run:
        print(json.dumps({"sources_checked": len(sources), "historical_register_counts": register_counts,
                          "active_main_workers": workers, "destination_exists": directory.exists(),
                          "writes": False, "parent_numeric_reevaluations": 0}, indent=2))
        return
    if workers or (POST / "runs/O4-coupled-companion.lock").exists():
        raise RuntimeError("Another MTS numerical owner is active")
    if directory.exists():
        raise FileExistsError("Use a new tag; prior evidence is immutable")
    lock_path = POST / "runs/5514-transplant.lock"
    with lock_path.open("x", encoding="utf-8") as stream:
        json.dump({"pid": os.getpid(), "tag": arguments.tag}, stream)
    checks, started = {}, time.perf_counter()
    workbench = workbench_snapshot()
    directory.mkdir(parents=True)
    write_json(directory / "manifest.json", {"source_hashes": sources, "script_sha256": digest(Path(__file__)),
                                            "historical_register_counts": register_counts})
    with (directory / "executed-script.py").open("xb") as stream:
        stream.write(Path(__file__).read_bytes())
    try:
        for name, passed in controls().items():
            require(checks, name, passed, "exact binary-rational cover control")
        payload, certificates, leaf_map, fiber_audit, frontier, cover_audit = calculate(checks)
        require(checks, "source_hashes_preserved", all(digest(POST / relative) == expected for relative, expected in sources.items()), len(sources))
        require(checks, "workbench_metadata_preserved", workbench_snapshot() == workbench, workbench)
        require(checks, "broad_claims_remain_false", all(payload[field] is False for field in CLAIM_FIELDS), list(CLAIM_FIELDS))
        payload.update({"created_utc": datetime.now(timezone.utc).isoformat(), "runtime_seconds": time.perf_counter() - started,
                        "validation_row_count": len(checks), "failed_validation_count": 0, "source_hashes": sources,
                        "script_sha256": digest(Path(__file__)), "workbench_metadata_fingerprint": workbench})
        write_csv(directory / "D4_combined_outer_cuboid_certificates.csv", certificates)
        write_csv(directory / "D4_certified_outer_source_leaf_map.csv", leaf_map)
        write_csv(directory / "D4_certified_outer_fiber_audit.csv", fiber_audit)
        write_csv(directory / "D4_outer_coverage_frontier.csv", frontier)
        write_json(directory / "exact_coverage_audit.json", cover_audit)
        write_csv(directory / "source_register.csv", [{"source_path": str(POST / relative), "sha256": expected, "exists": True} for relative, expected in sources.items()])
        write_csv(directory / "P8_Y5_BRR5513_5514_VALIDATION.csv", [{"checkpoint": 5514, "validation_gate": name, "passed": value["passed"],
                  "evidence": json.dumps(value["evidence"], sort_keys=True)} for name, value in checks.items()])
        payload["output_hashes"] = {path.name: digest(path) for path in directory.iterdir() if path.is_file()}
        write_json(directory / "D4_exact_source_leaf_transplant_result.json", payload)
        write_json(directory / "completion.marker", {"state": "COMPLETE", "result_sha256": digest(directory / "D4_exact_source_leaf_transplant_result.json"),
                                                   "failed_validation_count": 0})
        print(json.dumps({key: value for key, value in payload.items() if key not in ("source_hashes", "output_hashes")}, indent=2))
    except Exception as error:
        write_json(directory / "failure.json", {"error": str(error), "traceback": traceback.format_exc(), "checks": checks,
                                               "valid_for_exact_source_leaf_transplant": False})
        raise
    finally:
        lock_path.unlink()


if __name__ == "__main__":
    main()
