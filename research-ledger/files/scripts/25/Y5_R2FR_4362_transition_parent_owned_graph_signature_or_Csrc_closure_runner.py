from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4362"
CLAIM_ID = "L-203"
BRANCH = "MTS_R2FR_Y5_TRANSITION_PARENT_OWNED_GRAPH_SIGNATURE_OR_CSRC_CLOSURE_RUNNER_4362"
MARKER = "PPC4161_TRANSITION_PARENT_OWNED_GRAPH_SIGNATURE_OR_CSRC_CLOSURE_RUNNER_4362"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_OWNED_GRAPH_SIGNATURE_OR_CSRC_CLOSURE_RUNNER_4362"
DECISION = "GRAPH_SIGNATURE_REJECTED_CURRENT_CORPUS_CSRC_RUNNER_INSTANTIATED_NONCLAIM"
NEXT_TARGET = "4363-Y5-R2FR-transition-first-Csrc-projection-input-or-parent-graph-edge-proof.md"

FORMAL_PATH = FORMAL / "378-PPC4161-transition-parent-owned-graph-signature-or-Csrc-closure-runner.md"
DOC_PATH = POST / "4362-Y5-R2FR-transition-parent-owned-graph-signature-or-Csrc-closure-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4362_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4362_00_4361_formal": (
        FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md",
        "C_src_open :=",
        "4361 names the explicit source-coupling closure vector when owner/no-wA is unsigned.",
    ),
    "SRC4362_01_4361_csrc_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_CSRC_CLOSURE_ROWS.csv",
        "CSRC4361_4_decision",
        "4361 closure schema and fallback decision rows.",
    ),
    "SRC4362_02_4361_premises": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_PREMISE_AUDIT.csv",
        "P4361_1_parent_owned_connected_graph",
        "Parent-owned connected graph remains an unsigned theorem premise.",
    ),
    "SRC4362_03_1606_edge_audit": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv",
        "EDGE1606_7_verdict",
        "Concrete source-relevant graph edge audit used to test the graph-signature route.",
    ),
    "SRC4362_04_4334_tail_basis": (
        SOURCE_DIR / "P8_Y5_R2FR_4334_OPEN_TAIL_VECTOR_BASIS.csv",
        "T4334_0_Xi",
        "Open-tail vector basis that local arenas already project from.",
    ),
    "SRC4362_05_4334_projection_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_SOURCE_CONTRACT.csv",
        "PI4334_5_WEP",
        "Projection-matrix source contract for WEP/PPN/R10/clock/orbital/EM arenas.",
    ),
    "SRC4362_06_350_projection_formal": (
        FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md",
        "R_arena = Pi_arena T_open.",
        "Formal open-tail projection contract: residuals must be produced by fixed sourced matrices.",
    ),
    "SRC4362_07_4361_packet": (
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        "C_src_open",
        "Private packet already requires explicit C_src_open if the owner graph is unsigned.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    rendered = csv_line(row)
    path.write_text(text + rendered, encoding="utf-8")


def csv_line(row: Iterable[str]) -> str:
    from io import StringIO

    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def graph_signature_rows() -> List[Dict[str, str]]:
    input_path = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv"
    imported = read_csv(input_path)
    rows: List[Dict[str, str]] = []
    for row in imported:
        parent_owned = row.get("parent_owned", "")
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "input_edge_id": row.get("edge_id", ""),
                "edge": row.get("edge", ""),
                "template_role": row.get("template_role", ""),
                "input_evidence_status": row.get("evidence_status", ""),
                "input_parent_owned": parent_owned,
                "4362_zero_route_status": "SIGNED" if parent_owned == "True" else "UNSIGNED_BLOCKER",
                "current_blocker": row.get("current_blocker", ""),
                "effect_on_graph_zero": "supports_Z_graph" if parent_owned == "True" else "blocks_Z_graph",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "input_edge_id": "GRAPH4362_verdict",
            "edge": "parent-owned ordinary-matter action graph",
            "template_role": "all source-relevant edges plus measure/readout owner",
            "input_evidence_status": "NOT_PARENT_CERTIFIED",
            "input_parent_owned": "False",
            "4362_zero_route_status": "GRAPH_SIGNATURE_REJECTED_CURRENT_CORPUS",
            "current_blocker": "at least one required parent-owned edge is unsigned; current audit has no parent-owned certified edge set",
            "effect_on_graph_zero": "no theorem-zero for Delta_w_component_vector or Xi_src_hidden",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    )
    return rows


def csrc_vector_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "CSRC4362_0_delta_w_component_vector",
            "symbol": "Delta_w_component_vector",
            "definition": "source/species/material relative action-weight vector retained when the parent graph is not signed",
            "formula_or_import": "import CSRC4361_0_delta_w_vector: Delta_w_AB = sum_i DeltaQ_i^AB * delta_w_i + R_material_basis + R_parent_edge",
            "feeds": "WEP, Newton/source-normalization, local_GR, PPN through source-to-metric response",
            "required_inputs": "material tensor; source/readout basis; signed parent edge coefficients; no-cancellation convention",
            "current_status": "OPEN_SYMBOLIC_COMPONENT",
            "numeric_value_present": "False",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CSRC4362_1_Xi_open",
            "symbol": "Xi_open",
            "definition": "open hidden source-label/source-prefactor tail outside the signed owner/no-wA branch",
            "formula_or_import": "import CSRC4361_1_Xi_open and T4334_0_Xi",
            "feeds": "all local arenas through Pi_arena^C and Pi_arena^T",
            "required_inputs": "D_Hperp ln w_A; marker/source derivatives; operator norms; material/source bounds",
            "current_status": "OPEN_SYMBOLIC_ENVELOPE",
            "numeric_value_present": "False",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CSRC4362_2_tau_WEP_product",
            "symbol": "tau_WEP product",
            "definition": "MICROSCOPE-style product branch abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 before tau inversion",
            "formula_or_import": "import CSRC4361_2_WEP_product and 4358/4359 tau-min fork",
            "feeds": "WEP and source-normalization amplitude bounds",
            "required_inputs": "tau_min>0 or parent-owned action-measure zero theorem; official source/material/readout contraction",
            "current_status": "PRODUCT_BOUND_ONLY_NOT_AMPLITUDE",
            "numeric_value_present": "False",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CSRC4362_3_epsilon_Gsrc_open",
            "symbol": "epsilon_Gsrc_open",
            "definition": "finite source/coupling drift envelope entering Newton/local-GR source normalization",
            "formula_or_import": "import CSRC4361_3_local_source_budget",
            "feeds": "Newton, local_GR, PPN, orbital and clock through calibrated source normalization",
            "required_inputs": "P_WEP, P_Xi, P_coeff, P_proj, P_tail; source-worldtube and metric transfer constants",
            "current_status": "OPEN_SYMBOLIC_BUDGET",
            "numeric_value_present": "False",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CSRC4362_4_T_open_projection_basis",
            "symbol": "T_open",
            "definition": "existing 4334 open-tail vector projected into local arenas",
            "formula_or_import": "T_open=(Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tail_guard_sum, epsilon_tau_open, epsilon_boundary_projector_open, ordinary_matter_shadow_open)",
            "feeds": "R10, PPN, clock, orbital, EM, WEP projection matrices",
            "required_inputs": "source-backed numeric Pi_arena rows fixed before scoring",
            "current_status": "DEFINED_BASIS_NO_NUMERIC_MATRIX",
            "numeric_value_present": "False",
            "source_backed_numeric": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_projection_rows() -> List[Dict[str, str]]:
    return [
        {
            "arena_id": "ARENA4362_0_WEP",
            "arena": "WEP/source-composition",
            "residual_symbol": "R_WEP",
            "projection_law": "R_WEP = Pi_WEP^C C_src_open + Pi_WEP^T T_open",
            "observable_or_bound": "eta_TiPt, eta_AB, source-composition acceleration contrast",
            "required_projection_inputs": "source-charge basis; material sensitivity matrix; tau_WEP; official readout/source contraction",
            "imported_marker": "PI4334_5_WEP; CSRC4361_2_WEP_product",
            "missing_marker": "MISSING_SOURCE_CHARGE_PROJECTION; MISSING_TAU_WEP_LOWER_BOUND; MISSING_MATERIAL_TENSOR",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_1_PPN",
            "arena": "PPN/Cassini/local solar tests",
            "residual_symbol": "R_PPN",
            "projection_law": "R_PPN = Pi_PPN^C C_src_open + Pi_PPN^T T_open",
            "observable_or_bound": "gamma-1, beta-1, alpha_i, xi, zeta_i, Gdot/G",
            "required_projection_inputs": "metric Green operator; source-to-metric transfer; preferred-frame map; GM/time convention",
            "imported_marker": "PI4334_1_PPN",
            "missing_marker": "MISSING_LOCAL_METRIC_TRANSFER_MATRIX; MISSING_SOURCE_TO_METRIC_GREEN_OPERATOR",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_2_R10",
            "arena": "R10 short-range fifth-force",
            "residual_symbol": "R_R10(lambda)",
            "projection_law": "R_R10(lambda) = Pi_R10^C(lambda) C_src_open + Pi_R10^T(lambda) T_open",
            "observable_or_bound": "alpha(lambda) bound curve",
            "required_projection_inputs": "K_X; Qbar_XH(lambda); qbar_XT vector; lambda profile; full source-backed bound curve",
            "imported_marker": "PI4334_0_R10",
            "missing_marker": "MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE; MISSING_LAMBDA_PROFILE",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_3_clock",
            "arena": "clock/redshift/atomic standards",
            "residual_symbol": "R_clock",
            "projection_law": "R_clock = Pi_clock^C C_src_open + Pi_clock^T T_open",
            "observable_or_bound": "clock ratios, redshift residuals, alpha/mass-ratio drifts",
            "required_projection_inputs": "clock sensitivity coefficients; tau reference convention; alpha/mass response; source normalization",
            "imported_marker": "PI4334_2_clock",
            "missing_marker": "MISSING_CLOCK_SPECIES_TRANSFER_MATRIX; MISSING_ALPHA_MASS_SENSITIVITIES",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_4_orbital",
            "arena": "orbital/ephemeris/binary dynamics",
            "residual_symbol": "R_orbital",
            "projection_law": "R_orbital = Pi_orbital^C C_src_open + Pi_orbital^T T_open",
            "observable_or_bound": "GM convention residuals, ephemeris drift, binary/orbital frame tests",
            "required_projection_inputs": "GM convention; orbital frame; range/time transfer; source support and worldtube map",
            "imported_marker": "PI4334_3_orbital",
            "missing_marker": "MISSING_ORBITAL_FRAME_AND_GM_TRANSFER_MATRIX; MISSING_SOURCE_WORLDTUBE_MAP",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_5_EM",
            "arena": "EM/stress/Poynting/radiation",
            "residual_symbol": "R_EM",
            "projection_law": "R_EM = Pi_EM^C C_src_open + Pi_EM^T T_open",
            "observable_or_bound": "Poynting flux, constitutive tails, radiation/source-current deformation",
            "required_projection_inputs": "Hilbert EM flux map; constitutive deformation matrix; current normalization; Hodge ownership",
            "imported_marker": "PI4334_4_EM",
            "missing_marker": "MISSING_EM_FLUX_CONSTITUTIVE_TRANSFER_MATRIX; MISSING_CURRENT_NORMALIZATION",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_6_Newton_source",
            "arena": "Newton/source normalization",
            "residual_symbol": "epsilon_Gsrc_open",
            "projection_law": "epsilon_Gsrc_open = Pi_Gsrc^C C_src_open + Pi_Gsrc^T T_open",
            "observable_or_bound": "universality of calibrated G_N/GM and weak-field source mass",
            "required_projection_inputs": "source-worldtube map; M_Hdress owner; calibration branch; no non-Hilbert source hair",
            "imported_marker": "CSRC4361_3_local_source_budget",
            "missing_marker": "MISSING_PARENT_OWNED_G_CAL_SOURCE_NORMALIZATION; MISSING_SOURCE_MASS_OWNER",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "arena_id": "ARENA4362_7_local_GR",
            "arena": "local GR/Newton limit",
            "residual_symbol": "R_local_GR",
            "projection_law": "R_local_GR = Pi_GR^C C_src_open + Pi_GR^T T_open",
            "observable_or_bound": "metric residual vector, conservation/Bianchi closure, Newtonian weak-field reduction",
            "required_projection_inputs": "parent graph signature; source normalization; metric transfer; conservation and boundary silence",
            "imported_marker": "TH4361_3_full_owner_no_wA; GRAPH4362_verdict",
            "missing_marker": "MISSING_PARENT_GRAPH_SIGNATURE; MISSING_ALL_ARENA_PROJECTIONS; MISSING_BIANCHI_CONSERVATION_CLOSURE",
            "runner_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def runner_rows(arena_rows_in: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena in arena_rows_in:
        blockers = [
            item.strip()
            for item in arena["missing_marker"].split(";")
            if item.strip()
        ]
        rows.append(
            {
                "run_id": f"RUN4362_{arena['arena_id'].split('_')[-1]}",
                "arena_id": arena["arena_id"],
                "arena": arena["arena"],
                "input_vector": "C_src_open plus T_open",
                "projection_fixed_before_scoring": "False",
                "required_blockers": " | ".join(blockers),
                "computed_residual": "NOT_COMPUTED_PLACEHOLDER_INPUTS",
                "comparison_status": "NOT_SCORED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "run_id": "RUN4362_all",
            "arena_id": "ALL",
            "arena": "combined local-test package",
            "input_vector": "C_src_open plus T_open",
            "projection_fixed_before_scoring": "False",
            "required_blockers": "at least one graph/source/projection blocker remains in every local arena",
            "computed_residual": "NO_LOCAL_CLAIM",
            "comparison_status": "GRAPH_ZERO_REJECTED_AND_CLOSURE_RUNNER_BLOCKS_AS_DESIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4362_0_graph_zero",
            "gate": "parent-owned graph gives Delta_w_component_vector=0",
            "requirement": "all source-relevant ordinary-matter edges parent-owned plus measure/readout/no-reentry signed",
            "current_result": "FAIL_CURRENT_CORPUS",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4362_1_Csrc_runner",
            "gate": "explicit C_src_open closure runner exists",
            "requirement": "C_src components and arena projections registered with blocker-preserving nonclaim status",
            "current_result": "PASS_NONCLAIM_INFRASTRUCTURE",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4362_2_arena_scoring",
            "gate": "score local arenas",
            "requirement": "numeric source-backed Pi_arena^C/Pi_arena^T matrices and numeric C_src/T_open components fixed before residuals",
            "current_result": "BLOCKED_PLACEHOLDER_INPUTS",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4362_3_public_local_GR",
            "gate": "claim local GR/Newton/R10/WEP/PPN/clock/orbital pass",
            "requirement": "graph zero or finite residual vector beats sourced bounds with conservation/Bianchi closure",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4362_0",
            "decision": DECISION,
            "rationale": "The parent-owned graph route was actually tested against the 1606 edge audit, and every required source-relevant edge remains unsigned/not parent-certified. Therefore the zero theorem cannot be promoted. Instead, the failure branch is now runnable as a concrete nonclaim closure: C_src_open is carried with T_open into WEP, PPN, R10, clock, orbital, EM, Newton/source and local-GR projection rows. Every arena blocks claims until source-backed numeric projection inputs are supplied.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4362_0",
            "item": "graph zero route",
            "status": "REJECTED_CURRENT_CORPUS_NOT_REJECTED_FOREVER",
            "detail": "The theorem remains a possible route only if future parent action files sign the ordinary-matter graph/measure/readout owner clauses.",
        },
        {
            "status_id": "STAT4362_1",
            "item": "C_src_open runner",
            "status": "INSTANTIATED_NONCLAIM",
            "detail": "Local-test arenas now have explicit C_src/T_open projection contracts rather than a shapeless missing coupling.",
        },
        {
            "status_id": "STAT4362_2",
            "item": "local claims",
            "status": "ALL_BLOCKED",
            "detail": "No WEP, PPN, R10, clock, orbital, EM, Newton or local-GR pass is claimed.",
        },
        {
            "status_id": "STAT4362_3",
            "item": "next useful move",
            "status": "FILL_FIRST_SOURCE_BACKED_PROJECTION_INPUT",
            "detail": "The practical leap forward is one real Pi_arena row or one real parent-owned graph edge, not another broad missing-input ledger.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4362_0",
            "next_target": NEXT_TARGET,
            "question": "Can one C_src projection input be source-backed, or can one parent-owned graph edge be proven in the parent action grammar?",
            "preferred_route": "Fill the first real projection row, preferably Pi_WEP or Pi_PPN, because it turns the coupling problem into an actual finite residual calculation.",
            "derive_route": "Prove one parent-owned edge as a typed action-density morphism with measure/no-reentry ownership.",
            "fallback_route": "Keep C_src_open explicit and build bounded nonclaim smoke rows until enough source-backed projection inputs exist.",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    graph: List[Dict[str, str]],
    vector: List[Dict[str, str]],
    arenas: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "check": check,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add(
        "VAL4362_00_sources_exist",
        "all cited local source paths exist",
        all(row["path_exists"] == "True" for row in sources),
        "source register path_exists flags",
    )
    add(
        "VAL4362_01_needles_found",
        "all cited local source needles found",
        all(row["needle_found"] == "True" for row in sources),
        "source register needle_found flags",
    )
    imported_edge_rows = [row for row in graph if row["input_edge_id"].startswith("EDGE1606_")]
    add(
        "VAL4362_02_edge_rows_imported",
        "1606 edge audit imported",
        len(imported_edge_rows) >= 8,
        f"imported_edge_rows={len(imported_edge_rows)}",
    )
    add(
        "VAL4362_03_graph_zero_blocked",
        "graph zero blocked if any parent-owned edge is unsigned",
        any(row["4362_zero_route_status"] == "UNSIGNED_BLOCKER" for row in imported_edge_rows)
        and any(row["input_edge_id"] == "GRAPH4362_verdict" for row in graph),
        "current audit contains unsigned blockers and explicit verdict row",
    )
    add(
        "VAL4362_04_csrc_components_present",
        "C_src_open components present",
        {row["symbol"] for row in vector} >= {"Delta_w_component_vector", "Xi_open", "tau_WEP product", "epsilon_Gsrc_open", "T_open"},
        "C_src plus T_open basis",
    )
    add(
        "VAL4362_05_major_arenas_present",
        "major local arenas present",
        {row["arena"] for row in arenas}
        >= {
            "WEP/source-composition",
            "PPN/Cassini/local solar tests",
            "R10 short-range fifth-force",
            "clock/redshift/atomic standards",
            "orbital/ephemeris/binary dynamics",
            "EM/stress/Poynting/radiation",
            "Newton/source normalization",
            "local GR/Newton limit",
        },
        "WEP/PPN/R10/clock/orbital/EM/Newton/local_GR rows",
    )
    add(
        "VAL4362_06_all_arena_claims_blocked",
        "all arena claims blocked",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in arenas),
        "claim_allowed and valid_for_claim flags",
    )
    add(
        "VAL4362_07_runner_claims_blocked",
        "runner blocks all claims",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner),
        "runner flags",
    )
    add(
        "VAL4362_08_claim_gate_forbidden",
        "public local claim gate forbidden",
        any(row["gate_id"] == "GATE4362_3_public_local_GR" and row["current_result"] == "FORBIDDEN" for row in gates),
        "claim gate row",
    )
    add(
        "VAL4362_09_decision_nonclaim",
        "decision is nonclaim",
        decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False",
        DECISION,
    )
    add(
        "VAL4362_10_status_next_target",
        "next target selected",
        next_targets[0]["next_target"] == NEXT_TARGET,
        NEXT_TARGET,
    )
    add(
        "VAL4362_11_formal_marker",
        "formal marker written",
        MARKER in read_text(FORMAL_PATH),
        str(FORMAL_PATH),
    )
    add(
        "VAL4362_12_post_doc_marker",
        "post checkpoint marker written",
        MARKER in read_text(DOC_PATH),
        str(DOC_PATH),
    )
    add(
        "VAL4362_13_spine_marker",
        "spine marker appended",
        MARKER in read_text(FORMAL / "07-unification-spine.md"),
        str(FORMAL / "07-unification-spine.md"),
    )
    add(
        "VAL4362_14_packet_marker",
        "packet marker appended",
        PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
        str(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
    )
    add(
        "VAL4362_15_claim_register",
        "claim register updated",
        f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"),
        str(FORMAL / "02-claims-register.csv"),
    )
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    graph: List[Dict[str, str]],
    vector: List[Dict[str, str]],
    arenas: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    graph_preview = [
        row
        for row in graph
        if row["input_edge_id"].startswith("EDGE1606_") or row["input_edge_id"] == "GRAPH4362_verdict"
    ]
    formal = f"""# PPC4161 transition: parent-owned graph signature or C_src closure runner

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4361 proved the owner/no-wA theorem only as a conditional theorem. This checkpoint does the next honest thing: it tests whether the current corpus already signs the parent-owned ordinary-matter graph. It does not. Therefore the branch is not allowed to say that the source coupling vanishes. The failure branch is promoted into a concrete nonclaim runner.

## Exact objects

`C_src_open := (Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open)`.

`T_open := (Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tail_guard_sum, epsilon_tau_open, epsilon_boundary_projector_open, ordinary_matter_shadow_open)`.

For every local arena, the checkpoint requires a fixed-before-scoring projection contract:

`R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open`.

No residual may be scored until the used projection matrices and vector components are numeric, source-backed, and fixed before seeing the desired local-test result.

## Parent-owned graph test

The graph-zero route would need every source-relevant ordinary-matter edge, measure/coframe owner clause, and readout/no-reentry clause to be parent-signed. The current 1606 edge audit does not supply that signature.

{md_table(graph_preview, ["input_edge_id", "edge", "input_evidence_status", "input_parent_owned", "4362_zero_route_status", "current_blocker", "effect_on_graph_zero"])}

Result: `Z_graph=False` in the current corpus. This is not a disproof of the route forever; it is a refusal to smuggle the graph signature.

## C_src vector basis

{md_table(vector, ["component_id", "symbol", "definition", "formula_or_import", "feeds", "required_inputs", "current_status", "valid_for_claim"])}

## Arena closure runner

{md_table(arenas, ["arena_id", "arena", "residual_symbol", "projection_law", "observable_or_bound", "required_projection_inputs", "missing_marker", "runner_status", "claim_allowed"])}

## Smoke runner result

{md_table(runner, ["run_id", "arena", "input_vector", "projection_fixed_before_scoring", "computed_residual", "comparison_status", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "requirement", "current_result", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "rationale", "next_target", "claim_allowed"])}

## Status

{md_table(statuses, ["status_id", "item", "status", "detail"])}

## Next target

{md_table(next_targets, ["target_id", "next_target", "question", "preferred_route", "derive_route", "fallback_route", "claim_allowed"])}

## Source register

{md_table(sources, ["source_id", "path_exists", "needle_found", "line_number", "role"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")

    post_doc = f"""# 4362 - parent-owned graph signature or C_src closure runner

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- Parent-owned graph zero route: rejected for the current corpus because the 1606 edge audit remains not parent-certified.
- C_src closure runner: instantiated as a nonclaim calculation scaffold.
- Public/local claims: all blocked.

## What moved

The coupling problem is no longer just "missing coupling". It is now a named vector and runner:

`R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open`.

That means the next useful attack is a real projection row or a real parent-owned graph edge.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Source register: `{SOURCE_DIR / "P8_Y5_R2FR_4362_SOURCE_REGISTER.csv"}`
- Graph audit: `{SOURCE_DIR / "P8_Y5_R2FR_4362_GRAPH_SIGNATURE_AUDIT.csv"}`
- C_src vector: `{SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv"}`
- Arena contract: `{SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv"}`
- Runner: `{SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_RUNNER.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups() -> None:
    spine_block = f"""

## 4362 Transition parent-owned graph signature or C_src runner

Marker: `{MARKER}`

4362 tests the graph-zero route instead of circling it. The current 1606 parent-owned edge audit does not sign the ordinary-matter graph: the electron/EM, EM/nuclear, quark/QCD, quark-mass, QCD/nuclear, measure/Jacobian and current/readout edges remain unsigned or partial. Therefore the current corpus cannot claim `Delta_w_component_vector=0` or `Xi_src_hidden=0` from graph ownership.

The nonzero branch is now a concrete runner:

`C_src_open=(Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open)`,

`R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open`.

The WEP, PPN, R10, clock, orbital, EM, Newton/source and local-GR rows all remain nonclaim until their projection matrices and vector components are numeric, source-backed and fixed before scoring. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4362 packet update: graph signature rejected, C_src runner instantiated

Marker: `{PACKET_MARKER}`

Packet update: the source-coupling route has a concrete fork. If a future parent action signs the ordinary-matter graph, measure owner and no-reentry clauses, the owner/no-wA theorem can kill the source-label leg. In the current corpus that graph signature is absent, so the packet must carry `C_src_open=(Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open)` into local residuals by `R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open`. This blocks WEP/PPN/R10/clock/orbital/EM/Newton/local-GR claims until one source-backed projection input or one parent-owned graph edge is actually supplied.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4362 tests the parent-owned graph signature route against the existing 1606 source-relevant edge audit and rejects promotion in the current corpus: the ordinary-matter graph, measure/Jacobian owner and current/readout no-reentry edges are not parent-certified. The checkpoint therefore instantiates the explicit C_src closure runner: C_src_open=(Delta_w_component_vector, Xi_open, tau_WEP product, epsilon_Gsrc_open), and each local arena must use R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open with fixed source-backed projection matrices before scoring. All WEP, PPN, R10, clock, orbital, EM, Newton/source and local-GR claims remain blocked.",
            "4362 source register, graph-signature audit, C_src vector basis, arena projection contract, closure runner, claim gates, decision, status, next target and validation CSV.",
            "graph_signature_rejected_current_corpus_Csrc_closure_runner_instantiated_nonclaim",
            "Fill one source-backed C_src projection row such as Pi_WEP/Pi_PPN, or parent-prove one ordinary-matter graph edge in the action grammar.",
            "Pretending unsigned graph ownership kills source coupling; scoring local tests with placeholder projection matrices; cancelling source-coupling components after seeing residuals.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    graph = graph_signature_rows()
    vector = csrc_vector_rows()
    arenas = arena_projection_rows()
    runner = runner_rows(arenas)
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_GRAPH_SIGNATURE_AUDIT.csv", graph)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv", vector)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv", arenas)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4362_NEXT_TARGET.csv", next_targets)

    write_docs(sources, graph, vector, arenas, runner, gates, decisions, statuses, next_targets)
    update_rollups()

    validations = validation_rows(sources, graph, vector, arenas, runner, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4362 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
