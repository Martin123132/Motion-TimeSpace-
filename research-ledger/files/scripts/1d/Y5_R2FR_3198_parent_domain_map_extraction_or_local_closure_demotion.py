from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


RUN_STARTED = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3198-Y5-R2FR-parent-domain-map-extraction-or-local-closure-demotion-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3198_INPUTS.csv"
CANDIDATES = OUT / "P8_Y5_R2FR_3198_PARENT_DOMAIN_CANDIDATE_SWEEP.csv"
REQUIREMENTS = OUT / "P8_Y5_R2FR_3198_DOMAIN_TRIPLE_REQUIREMENT_AUDIT.csv"
DEMOTION = OUT / "P8_Y5_R2FR_3198_LOCAL_BRANCH_DEMOTION_REGISTER.csv"
SEEDS = OUT / "P8_Y5_R2FR_3198_CONSTRUCTIVE_SEED_LEDGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3198_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3198_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "formalization":
        return FW / relative_path
    if location == "post_checkpoint":
        return ROOT / relative_path
    raise ValueError(location)


def rel_to_repo(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def text_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def evidence(path: Path, terms: list[str], limit: int = 5) -> str:
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(text_lines(path), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            clean = " ".join(line.strip().split())
            hits.append(f"L{line_number}:{clean[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


SOURCE_ROWS = [
    {
        "input_id": "SRC3198_00",
        "location": "formalization",
        "relative_path": "33-parent-projection-map.md",
        "role": "parent projection ansatz and known projection gaps",
    },
    {
        "input_id": "SRC3198_01",
        "location": "formalization",
        "relative_path": "48-routing-projector-definitions.md",
        "role": "local/galaxy/cosmology routing projector definitions",
    },
    {
        "input_id": "SRC3198_02",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "conditional projected source law and source-gate status",
    },
    {
        "input_id": "SRC3198_03",
        "location": "formalization",
        "relative_path": "81-local-closure-status-and-parent-roadmap.md",
        "role": "local branch closure status",
    },
    {
        "input_id": "SRC3198_04",
        "location": "formalization",
        "relative_path": "82-parent-dynamics-roadmap.md",
        "role": "parent dynamics roadmap after local closure boxing",
    },
    {
        "input_id": "SRC3198_05",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "current parent equation scaffold and parent-derived gates",
    },
    {
        "input_id": "SRC3198_06",
        "location": "formalization",
        "relative_path": "95-transition-owner-equations-v2.md",
        "role": "transition owner attempts and parent-derived gate",
    },
    {
        "input_id": "SRC3198_07",
        "location": "formalization",
        "relative_path": "96-transition-closure-contract.md",
        "role": "transition closure contract after owner failure",
    },
    {
        "input_id": "SRC3198_08",
        "location": "post_checkpoint",
        "relative_path": "3197-Y5-R2FR-parent-owned-positive-layer-stiffness-or-domain-geometry-constraint-under-AX1090.md",
        "role": "3197 theorem requiring C(Phi), G_N, and rank(J)=4",
    },
    {
        "input_id": "SRC3198_09",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3197_DOMAIN_STIFFNESS_THEOREM.csv",
        "role": "machine-readable 3197 stiffness theorem",
    },
]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for row in SOURCE_ROWS:
        path = resolve(row["location"], row["relative_path"])
        rows.append(
            {
                **row,
                "source_path": rel_to_repo(path),
                "exists": bool_text(path.exists()),
                "generated_utc": now,
            }
        )
    return rows


def candidate_rows() -> list[dict[str, object]]:
    now = stamp()
    specs = [
        {
            "candidate_id": "CAND3198_00",
            "input_id": "SRC3198_00",
            "candidate_object": "parent projection map",
            "terms": ["projection ansatz", "not yet a derivation", "parent action", "projection"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": False,
            "has_observable_transfer": True,
            "status": "projection_ansatz_not_domain_constraint",
            "blocking_reason": "contains projection/routing language but not a parent domain constraint C(Phi)=0 with normal metric and full-rank C1 Jacobian",
        },
        {
            "candidate_id": "CAND3198_01",
            "input_id": "SRC3198_01",
            "candidate_object": "routing projectors P_loc/P_gal/P_cos",
            "terms": ["projector_functions_defined_not_derived", "P_loc", "q_loc", "not derived"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": False,
            "has_observable_transfer": True,
            "status": "routing_projectors_defined_not_parent_derived",
            "blocking_reason": "projectors sort residuals by arena; they do not supply a parent interface distance functional or rank-four mismatch map",
        },
        {
            "candidate_id": "CAND3198_02",
            "input_id": "SRC3198_02",
            "candidate_object": "projected source laws",
            "terms": ["conditional_not_parent_derived", "bounded", "parent functions", "source"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": True,
            "has_width_selection": False,
            "has_observable_transfer": True,
            "status": "conditional_source_law_not_domain_triple",
            "blocking_reason": "useful for residual transfer, but source coupling is conditional and not a positive parent normal metric on C1 mismatch slots",
        },
        {
            "candidate_id": "CAND3198_03",
            "input_id": "SRC3198_03",
            "candidate_object": "local closure status",
            "terms": ["disciplined closure", "not derived", "parent-derived local GR", "local PPN"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": False,
            "has_observable_transfer": True,
            "status": "explicit_closure_not_parent_map",
            "blocking_reason": "source explicitly quarantines the local branch as closure rather than parent-derived GR/Newton limit",
        },
        {
            "candidate_id": "CAND3198_04",
            "input_id": "SRC3198_04",
            "candidate_object": "parent dynamics roadmap",
            "terms": ["disciplined closure", "parent-level route", "local PPN", "roadmap"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": False,
            "has_observable_transfer": False,
            "status": "roadmap_not_extraction",
            "blocking_reason": "roadmap names the parent route but does not instantiate C(Phi), J, or G_N",
        },
        {
            "candidate_id": "CAND3198_05",
            "input_id": "SRC3198_05",
            "candidate_object": "parent equations E0-E8",
            "terms": ["not parent-derived", "conditional closure", "phenomenological", "parent"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": True,
            "has_width_selection": False,
            "has_observable_transfer": True,
            "status": "parent_scaffold_without_interface_domain_metric",
            "blocking_reason": "contains parent-equation language and arena gates, but no rank-four domain constraint map for C1 gluing",
        },
        {
            "candidate_id": "CAND3198_06",
            "input_id": "SRC3198_06",
            "candidate_object": "transition owner equations",
            "terms": ["no transition owner branch is parent-derived", "parent-derived nonlocal kernel", "forbidden", "open targets"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": True,
            "has_width_selection": True,
            "has_observable_transfer": True,
            "status": "nonlocal_kernel_route_open_not_parent_owned",
            "blocking_reason": "closest transition-owner material still records no parent-derived owner; kernel/width clauses remain closure contracts",
        },
        {
            "candidate_id": "CAND3198_07",
            "input_id": "SRC3198_07",
            "candidate_object": "transition closure contract",
            "terms": ["no transition owner branch is parent-derived", "closure", "contract", "survival"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": True,
            "has_observable_transfer": True,
            "status": "closure_contract_not_parent_map",
            "blocking_reason": "documents the honest closure route after owner failure; cannot be promoted to a parent domain map",
        },
        {
            "candidate_id": "CAND3198_08",
            "input_id": "SRC3198_08",
            "candidate_object": "3197 domain stiffness theorem",
            "terms": ["C(Phi)", "G_N", "rank(J)", "K0 = J^T G_N J"],
            "has_C_phi": False,
            "has_J_rank": False,
            "has_G_N_positive": False,
            "has_covariant_measure": False,
            "has_width_selection": True,
            "has_observable_transfer": False,
            "status": "requirement_theorem_not_parent_source",
            "blocking_reason": "derives the required theorem, but explicitly says the parent theory must still supply C(Phi), J, and G_N",
        },
    ]
    input_lookup = {row["input_id"]: row for row in SOURCE_ROWS}
    rows: list[dict[str, object]] = []
    for spec in specs:
        input_spec = input_lookup[spec["input_id"]]
        path = resolve(input_spec["location"], input_spec["relative_path"])
        has_full_triple = spec["has_C_phi"] and spec["has_J_rank"] and spec["has_G_N_positive"]
        rows.append(
            {
                "candidate_id": spec["candidate_id"],
                "source_path": rel_to_repo(path),
                "candidate_object": spec["candidate_object"],
                "evidence": evidence(path, spec["terms"]),
                "has_parent_domain_map_C_phi": bool_text(spec["has_C_phi"]),
                "has_full_rank_J_on_C1_slots": bool_text(spec["has_J_rank"]),
                "has_positive_normal_metric_G_N": bool_text(spec["has_G_N_positive"]),
                "has_covariant_measure_or_descent": bool_text(spec["has_covariant_measure"]),
                "has_width_selection": bool_text(spec["has_width_selection"]),
                "has_observable_transfer_path": bool_text(spec["has_observable_transfer"]),
                "has_complete_domain_triple": bool_text(has_full_triple),
                "extraction_status": spec["status"],
                "blocking_reason": spec["blocking_reason"],
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def requirement_rows(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()

    def any_true(field: str) -> bool:
        return any(row[field] == "true" for row in candidates)

    return [
        {
            "requirement_id": "REQ3198_00",
            "requirement": "parent domain constraint C(Phi)=0 for the local transition/interface",
            "status": "missing",
            "evidence_summary": "no audited source supplies C(Phi) as a parent-owned constraint map; projection and closure maps are not enough",
            "candidate_support_present": bool_text(any_true("has_parent_domain_map_C_phi")),
            "next_action": "construct a flux/domain constraint candidate from parent stress or demote route to closure-only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "requirement_id": "REQ3198_01",
            "requirement": "linearized mismatch Jacobian J on z=(Delta F_L, Delta F'_L, Delta F_R, Delta F'_R)",
            "status": "missing",
            "evidence_summary": "no source proves a four-slot parent Jacobian or rank(J)=4",
            "candidate_support_present": bool_text(any_true("has_full_rank_J_on_C1_slots")),
            "next_action": "derive J after a concrete parent C(Phi) is chosen",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "requirement_id": "REQ3198_02",
            "requirement": "positive normal metric G_N on the constraint codomain",
            "status": "missing",
            "evidence_summary": "no source provides a positive normal metric whose pullback owns the finite-layer stiffness",
            "candidate_support_present": bool_text(any_true("has_positive_normal_metric_G_N")),
            "next_action": "derive G_N from parent kinetic/stress Hessian or keep K0 closure-labeled",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "requirement_id": "REQ3198_03",
            "requirement": "covariant measure/coframe/connection descent compatible with the local layer",
            "status": "partial",
            "evidence_summary": "some parent/source-law files contain covariant or conditional descent language, but not for the full domain triple",
            "candidate_support_present": bool_text(any_true("has_covariant_measure_or_descent")),
            "next_action": "reuse only as a helper once C(Phi), J, and G_N are explicit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "requirement_id": "REQ3198_04",
            "requirement": "transition width/finite-layer selection delta",
            "status": "partial",
            "evidence_summary": "transition closure files discuss width/kernels, but width remains a closure contract rather than parent-owned geometry",
            "candidate_support_present": bool_text(any_true("has_width_selection")),
            "next_action": "connect delta to a parent stiffness/flux scale or leave it as bounded nuisance input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "requirement_id": "REQ3198_05",
            "requirement": "observable transfer path to local tests",
            "status": "partial",
            "evidence_summary": "several files support residual-transfer testing, but not a parent-derived local-GR claim",
            "candidate_support_present": bool_text(any_true("has_observable_transfer_path")),
            "next_action": "turn the closure branch into explicit residual bounds while derivation continues",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def demotion_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "branch_id": "DEM3198_00",
            "branch": "finite-layer/domain-stiffness route to local C1 gluing",
            "prior_status": "conditional route from 3197",
            "new_status": "LOCAL_DOMAIN_ROUTE_DEMOTED_TO_CONDITIONAL_CLOSURE",
            "reason": "corpus sweep did not find parent C(Phi), rank-four J, or positive G_N",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "next_action": "use as a mathematical closure only unless a parent triple is constructed",
            "generated_utc": now,
        },
        {
            "branch_id": "DEM3198_01",
            "branch": "local GR/Newton/PPN safety chain",
            "prior_status": "closure-quarantined",
            "new_status": "REMAINS_CLOSURE_QUARANTINED",
            "reason": "the local branch may be bounded and tested but is not parent-derived by this checkpoint",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "next_action": "carry residual vector into explicit PPN/R10/clock/orbital bounds",
            "generated_utc": now,
        },
        {
            "branch_id": "DEM3198_02",
            "branch": "3194 gluing multiplier reaction force",
            "prior_status": "mathematically coherent finite-layer reaction",
            "new_status": "COHERENT_BUT_NOT_PARENT_OWNED",
            "reason": "multipliers can be recovered from K0, but K0 itself lacks parent source ownership",
            "claim_blocked": "true",
            "valid_for_claim": "false",
            "next_action": "derive K0 from a parent flux/domain map or keep multiplier as closure force",
            "generated_utc": now,
        },
    ]


def seed_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "seed_id": "SEED3198_00",
            "constructive_route": "stress-flux/Poynting-domain constraint",
            "candidate_constraint": "C^nu = n_mu(T_parent^{mu nu} - tau_m T_matter^{mu nu} - tau_em T_EM^{mu nu})|_layer",
            "why_it_matters": "turns source coupling into the domain map itself; the EM Poynting vector is the spatial T_EM^{0i} flux component rather than an afterthought",
            "needed_derivation": "prove parent stress tensor, EM/source descent, signs, units, and rank-four response on the local mismatch slots",
            "risk": "may reduce to an imposed junction condition unless tau_m/tau_em are parent-owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "seed_id": "SEED3198_01",
            "constructive_route": "canonical momentum/domain-wall constraint",
            "candidate_constraint": "C = (Pi_0, Pi_1)_inside - (Pi_0, Pi_1)_outside - source_wall_flux",
            "why_it_matters": "uses the 3193 natural momenta and 3194 multiplier algebra as the boundary reaction language",
            "needed_derivation": "derive the source_wall_flux from parent action variation, not by fitting the missing jump",
            "risk": "without a parent source wall it is just the previous gluing closure in new clothes",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "seed_id": "SEED3198_02",
            "constructive_route": "quotient-geometry invariant mismatch map",
            "candidate_constraint": "C = q(Phi_inside) - q(Phi_outside) projected onto local invariants",
            "why_it_matters": "would make the interface cost a distance between quotient-equivalent parent states",
            "needed_derivation": "define q, prove local vertical directions, supply a positive quotient normal metric, and compute rank(J)",
            "risk": "current quotient/projector files define routing objects but not the metric/rank theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3198_00",
            "result": "NO_PARENT_DOMAIN_TRIPLE_EXTRACTED",
            "claim_status": "NO_LOCAL_GR_OR_PPN_CLAIM",
            "decision": "demote finite-layer local-domain route to explicit conditional closure for now",
            "reason": "all audited parent/projector/transition sources lack at least C(Phi), rank(J)=4, and positive G_N as a parent-owned triple",
            "best_forward_route": "attempt constructive stress-flux/Poynting-domain constraint before pure residual bounding",
            "next_target": "3199-Y5-R2FR-Poynting-source-coupling-domain-map-candidate-or-local-residual-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    candidates: list[dict[str, object]],
    requirements: list[dict[str, object]],
    demotions: list[dict[str, object]],
    seeds: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    full_triples = [row for row in candidates if row["has_complete_domain_triple"] == "true"]
    csv_paths = [INPUTS, CANDIDATES, REQUIREMENTS, DEMOTION, SEEDS, DECISION]
    return [
        {
            "check_id": "VAL3198_00_inputs_exist",
            "check": "all cited source paths exist",
            "pass": bool_text(all(row["exists"] == "true" for row in inputs)),
            "detail": "resolved inputs against post-checkpoint and formalization-workbench",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_01_candidate_coverage",
            "check": "at least eight parent/projection/transition candidates audited",
            "pass": bool_text(len(candidates) >= 8),
            "detail": f"audited={len(candidates)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_02_no_full_triple",
            "check": "no source is promoted to a complete C(Phi), rank-four J, positive G_N triple",
            "pass": bool_text(len(full_triples) == 0),
            "detail": f"complete_triples={len(full_triples)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_03_requirements_block_claim",
            "check": "hard domain requirements remain missing or partial and valid_for_claim=false",
            "pass": bool_text(all(row["valid_for_claim"] == "false" for row in requirements)),
            "detail": ";".join(f"{row['requirement_id']}={row['status']}" for row in requirements),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_04_demotion_recorded",
            "check": "local domain route demotion row exists",
            "pass": bool_text(
                any(row["new_status"] == "LOCAL_DOMAIN_ROUTE_DEMOTED_TO_CONDITIONAL_CLOSURE" for row in demotions)
            ),
            "detail": "closure demotion is explicit and non-claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_05_constructive_next_route",
            "check": "constructive route exists so the next step is not only another missing-input list",
            "pass": bool_text(any("Poynting" in row["constructive_route"] for row in seeds)),
            "detail": "stress-flux/Poynting seed recorded",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_06_decision_nonclaim",
            "check": "decision blocks local-GR/PPN claim and names next target",
            "pass": bool_text(
                decisions[0]["claim_status"] == "NO_LOCAL_GR_OR_PPN_CLAIM"
                and decisions[0]["valid_for_claim"] == "false"
            ),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3198_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": bool_text(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    candidates: list[dict[str, object]],
    requirements: list[dict[str, object]],
    demotions: list[dict[str, object]],
    seeds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    missing = [row for row in requirements if row["status"] == "missing"]
    partial = [row for row in requirements if row["status"] == "partial"]
    strongest = [row for row in candidates if row["extraction_status"] in {
        "conditional_source_law_not_domain_triple",
        "parent_scaffold_without_interface_domain_metric",
        "nonlocal_kernel_route_open_not_parent_owned",
    }]
    lines = [
        "# 3198 - Parent Domain Map Extraction Or Local Closure Demotion Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Maxwell/EM derivation claim, or public-facing result.",
        "",
        "## Result",
        "",
        "The 3197 theorem made the missing object exact:",
        "",
        "```text",
        "K0 = J^T G_N J",
        "```",
        "",
        "with parent domain constraint `C(Phi)=0`, C1 mismatch linearization `C = J z + O(z^2)`, and positive normal metric `G_N`.",
        "",
        "3198 searched the current parent/projection/transition corpus for that complete triple.",
        "",
        "Result:",
        "",
        "```text",
        "NO_PARENT_DOMAIN_TRIPLE_EXTRACTED.",
        "```",
        "",
        "That is not a demolition of the mathematics. It means the finite-layer/domain route is coherent but not parent-owned yet.",
        "",
        "## Requirement Audit",
        "",
        f"Missing hard requirements: {len(missing)}.",
        "",
        *[f"- `{row['requirement_id']}`: {row['requirement']}" for row in missing],
        "",
        f"Partial helper requirements: {len(partial)}.",
        "",
        *[f"- `{row['requirement_id']}`: {row['requirement']}" for row in partial],
        "",
        "The key failed gate is still the full triple:",
        "",
        "```text",
        "C(Phi), rank(J)=4, G_N>0.",
        "```",
        "",
        "## Closest Sources",
        "",
    ]
    for row in strongest:
        lines.extend(
            [
                f"### {row['candidate_id']} - {row['candidate_object']}",
                "",
                f"- Source: `{row['source_path']}`",
                f"- Status: `{row['extraction_status']}`",
                f"- Blocker: {row['blocking_reason']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Closure Demotion",
            "",
            "The local finite-layer/domain route is demoted to an explicit conditional closure until a parent-owned domain map is constructed.",
            "",
        ]
    )
    for row in demotions:
        lines.append(f"- `{row['branch_id']}`: `{row['new_status']}` - {row['reason']}")
    lines.extend(
        [
            "",
            "## Constructive Next Move",
            "",
            "To avoid another loop of simply writing down missing inputs, 3198 records constructive routes to try next.",
            "",
        ]
    )
    for row in seeds:
        lines.extend(
            [
                f"### {row['seed_id']} - {row['constructive_route']}",
                "",
                "```text",
                str(row["candidate_constraint"]),
                "```",
                "",
                f"- Why it matters: {row['why_it_matters']}",
                f"- Needed derivation: {row['needed_derivation']}",
                f"- Risk: {row['risk']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Decision",
            "",
            f"`{decisions[0]['result']}`.",
            "",
            f"Claim status: `{decisions[0]['claim_status']}`.",
            "",
            f"Best forward route: {decisions[0]['best_forward_route']}.",
            "",
            "Next target:",
            "",
            "```text",
            str(decisions[0]["next_target"]),
            "```",
            "",
            "## Generated Evidence",
            "",
            f"- `{rel_to_repo(INPUTS)}`",
            f"- `{rel_to_repo(CANDIDATES)}`",
            f"- `{rel_to_repo(REQUIREMENTS)}`",
            f"- `{rel_to_repo(DEMOTION)}`",
            f"- `{rel_to_repo(SEEDS)}`",
            f"- `{rel_to_repo(DECISION)}`",
            f"- `{rel_to_repo(VALIDATION)}`",
            "",
            "## Validation",
            "",
        ]
    )
    for row in validations:
        lines.append(f"- `{row['check_id']}`: `{row['pass']}` - {row['detail']}")
    lines.extend(["", "All rows remain `valid_for_claim=false`.", ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = input_rows()
    candidates = candidate_rows()
    requirements = requirement_rows(candidates)
    demotions = demotion_rows()
    seeds = seed_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(CANDIDATES, candidates)
    write_csv(REQUIREMENTS, requirements)
    write_csv(DEMOTION, demotions)
    write_csv(SEEDS, seeds)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, candidates, requirements, demotions, seeds, decisions)
    write_csv(VALIDATION, validations)
    write_doc(candidates, requirements, demotions, seeds, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3198 validation failed: {detail}")
    print(f"3198 generated {DOC}")


if __name__ == "__main__":
    main()
