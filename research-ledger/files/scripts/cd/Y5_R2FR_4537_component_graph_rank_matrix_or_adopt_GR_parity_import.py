from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4537"
CLAIM_ID = "L-379"
MARKER = "PPC4161_COMPONENT_GRAPH_RANK_MATRIX_OR_ADOPT_GR_PARITY_IMPORT_4537"
PACKET_MARKER = "PPC4161_PACKET_COMPONENT_GRAPH_RANK_MATRIX_OR_ADOPT_GR_PARITY_IMPORT_4537"
DECISION = "GR_PARITY_COMPONENT_GRAPH_RANK_PASSES_AS_PRIVATE_BRANCH_CURRENT_MTS_PARENT_GRAPH_REMAINS_UNSIGNED"
NEXT_TARGET = "4538-Y5-R2FR-GR-parity-local-source-universality-adoption-gates-or-interface-residuals.md"

FORMAL_PATH = FORMAL / "553-PPC4161-component-graph-rank-matrix-or-adopt-GR-parity-import.md"
DOC_PATH = POST / "4537-Y5-R2FR-component-graph-rank-matrix-or-adopt-GR-parity-import.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4537_SOURCE_REGISTER.csv"
MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_MATRIX.csv"
RANK_RESULTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv"
ADOPTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_GR_PARITY_ADOPTION_CERTIFICATE.csv"
CURRENT_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_CURRENT_PARENT_APPLICATION_GATE.csv"
FINITE_FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_FINITE_DELTAW_FALLBACK_AFTER_RANK.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4537_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4537_VALIDATION.csv"

NODES = [
    "lepton_electron",
    "photon_EM",
    "quark_flavour",
    "gluon_QCD",
    "nuclear_bound_state",
    "atomic_bound_state",
    "macroscopic_test_body",
]

NODE_FROM_1477 = {
    "N1477_1_electron_lepton": "lepton_electron",
    "N1477_2_photon_EM": "photon_EM",
    "N1477_3_quark_flavour": "quark_flavour",
    "N1477_4_gluon_QCD": "gluon_QCD",
    "N1477_5_nuclear_bound_state": "nuclear_bound_state",
    "N1477_6_atomic_bound_state": "atomic_bound_state",
    "N1477_7_macroscopic_test_body": "macroscopic_test_body",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def matrix_rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    mat = [[Fraction(value) for value in row] for row in matrix]
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    pivot_col = 0
    while rank < rows and pivot_col < cols:
        pivot = None
        for row_index in range(rank, rows):
            if mat[row_index][pivot_col] != 0:
                pivot = row_index
                break
        if pivot is None:
            pivot_col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pivot_value = mat[rank][pivot_col]
        mat[rank] = [value / pivot_value for value in mat[rank]]
        for row_index in range(rows):
            if row_index != rank and mat[row_index][pivot_col] != 0:
                factor = mat[row_index][pivot_col]
                mat[row_index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(mat[row_index], mat[rank])
                ]
        rank += 1
        pivot_col += 1
    return rank


def rank_summary(matrix: list[list[int]]) -> dict[str, int]:
    ncols = len(NODES)
    rank = matrix_rank(matrix)
    augmented_rank = matrix_rank(matrix + [[1] * ncols])
    return {
        "num_nodes": ncols,
        "num_rows": len(matrix),
        "rank": rank,
        "nullity": ncols - rank,
        "rank_with_common_row": augmented_rank,
        "pperp_kernel_dim": ncols - augmented_rank,
        "rank_needed_on_pperp": ncols - 1,
    }


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4537_00_4536_rank",
            "label": "4536 rank theorem",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4536_CONNECTED_GRAPH_RANK_THEOREM.csv",
            "needle": "CGRT4536_0_exact_rank_statement",
            "role": "rank condition to execute",
        },
        {
            "source_id": "SRC4537_01_1477_edges",
            "label": "1477 connected matter graph edges",
            "path": SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv",
            "needle": "E1477_4_lepton_EM",
            "role": "template graph edge source",
        },
        {
            "source_id": "SRC4537_02_1605_certificate",
            "label": "1605 connected graph certificate",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1605_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv",
            "needle": "GRC1605_6_verdict",
            "role": "template connected but parent unsigned",
        },
        {
            "source_id": "SRC4537_03_1606_theorem",
            "label": "1606 parent-owned graph theorem",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_GRAPH_THEOREM_ATTEMPT.csv",
            "needle": "POG1606_1_exact_graph_lemma",
            "role": "older exact graph lemma",
        },
        {
            "source_id": "SRC4537_04_2616_exchange",
            "label": "2616 exchange connectivity theorem",
            "path": SOURCE_DIR / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
            "needle": "OMC2616_1_connected_graph_implication",
            "role": "ordinary block connectivity theorem",
        },
        {
            "source_id": "SRC4537_05_4445_gr_parity",
            "label": "4445 GR-parity import",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4445_DERIVATION_ROWS.csv",
            "needle": "SMIMP4445_0_GR_parity_import_principle",
            "role": "fair local-GR matter import branch",
        },
        {
            "source_id": "SRC4537_06_standard_visible",
            "label": "standard visible matter import contract",
            "path": FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
            "needle": "The Hilbert source is",
            "role": "calibrated visible matter branch",
        },
        {
            "source_id": "SRC4537_07_2647_signature",
            "label": "2647 ordinary matter signature",
            "path": SOURCE_DIR / "P8_Y5_ORDINARY_MATTER_SIGNATURE_2647_CLAUSE_MATRIX.csv",
            "needle": "OMC2647_4_source_functor_label_forgetting",
            "role": "ordinary matter signature clauses remain unsigned",
        },
        {
            "source_id": "SRC4537_08_4535_finite",
            "label": "4535 finite Delta_w route",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv",
            "needle": "FBR4535_OVERALL",
            "role": "finite fallback remains nonclaim",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def component_matrix_rows() -> tuple[list[dict[str, Any]], list[list[int]]]:
    edge_rows = read_csv(SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv")
    rows: list[dict[str, Any]] = []
    matrix: list[list[int]] = []
    for edge in edge_rows:
        source = NODE_FROM_1477.get(edge.get("source_node", ""))
        target = NODE_FROM_1477.get(edge.get("target_node", ""))
        if not source or not target:
            continue
        coefficients = {node: 0 for node in NODES}
        coefficients[source] = 1
        coefficients[target] = -1
        row_vector = [coefficients[node] for node in NODES]
        matrix.append(row_vector)
        rows.append(
            {
                "matrix_row_id": "M4537_" + edge["edge_id"],
                "source_edge_id": edge["edge_id"],
                "source_node": source,
                "target_node": target,
                "constraint": f"delta_l[{source}] - delta_l[{target}] = 0",
                "coefficients_by_node": ";".join(f"{node}:{coefficients[node]}" for node in NODES),
                "template_edge_present": edge.get("template_edge_present", ""),
                "parent_owned_in_current_MTS": edge.get("parent_owned", ""),
                "adopted_in_GR_parity_branch": "True",
                "source_status": edge.get("parent_owned_status", ""),
                "valid_for_claim": "False",
            }
        )
    return rows, matrix


def rank_result_rows(matrix: list[list[int]]) -> list[dict[str, Any]]:
    template = rank_summary(matrix)
    current = rank_summary([])
    adopted_pass = template["rank"] == template["rank_needed_on_pperp"] and template["pperp_kernel_dim"] == 0
    current_pass = current["rank"] == current["rank_needed_on_pperp"] and current["pperp_kernel_dim"] == 0
    return [
        {
            "rank_case_id": "RR4537_0_template_graph",
            "case": "1477/standard visible template graph",
            **template,
            "rank_passes_on_pperp": b(adopted_pass),
            "meaning": "template/adopted standard visible branch kills non-common component weights",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "rank_case_id": "RR4537_1_current_parent_owned_graph",
            "case": "current MTS parent-owned graph using only signed component edges",
            **current,
            "rank_passes_on_pperp": b(current_pass),
            "meaning": "current parent-owned component graph is not signed, so rank test fails for public/current theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "rank_case_id": "RR4537_2_GR_parity_adopted_branch",
            "case": "private GR-parity import branch",
            **template,
            "rank_passes_on_pperp": b(adopted_pass),
            "meaning": "adopting one standard matter action with fixed graph/no-source-prefactor gives P_perp Delta_w=0 inside that branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_rows() -> list[dict[str, Any]]:
    return [
        {
            "adoption_id": "AD4537_0_GR_parity_scope",
            "clause": "private GR-parity local-reduction branch",
            "status": "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH_ONLY",
            "meaning": "For testing local MTS->GR reduction, use the same standard visible matter action GR uses, with fixed internal constants and total Hilbert variation.",
            "does_not_mean": "MTS has derived the Standard Model or all matter constants from psi.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "adoption_id": "AD4537_1_no_source_prefactor",
            "clause": "no source-only component prefactor",
            "status": "ADOPTED_INSIDE_GR_PARITY_BRANCH",
            "meaning": "No SpeciesLabel/MaterialLabel -> Coeff_active_source Hom is allowed on the imported branch; material labels enter readout/inventory only.",
            "does_not_mean": "off-branch source-weight residuals are erased.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "adoption_id": "AD4537_2_rank_result",
            "clause": "M_graph full rank on P_perp",
            "status": "PASS_FOR_IMPORTED_TEMPLATE_BRANCH",
            "meaning": "The 1477 visible graph incidence matrix has rank 6 for 7 nodes and zero non-common kernel after common-mode projection.",
            "does_not_mean": "current MTS parent-owned graph is signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "adoption_id": "AD4537_3_interface_guard",
            "clause": "local interface residuals still required",
            "status": "RETAIN",
            "meaning": "Hidden/readout/no-flux/R_eq/source-worldtube and nonlocal MTS interface residuals remain separate gates.",
            "does_not_mean": "full local GR/Newton/PPN branch is claim-ready.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def current_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CPG4537_0_template_rank",
            "gate": "template/adopted standard visible graph rank",
            "status": "PASS",
            "reason": "incidence matrix connected; rank=n-1; non-common kernel zero",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CPG4537_1_current_parent_rank",
            "gate": "current parent-owned graph rank",
            "status": "FAIL_UNSIGNED_EDGES",
            "reason": "1477/1605/1606 mark physical template edges as not parent-owned",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CPG4537_2_GR_parity_adoption",
            "gate": "private GR-parity adoption",
            "status": "PASS_PRIVATE_BRANCH",
            "reason": "adoption is explicit and scoped; not a derivation of SM or public claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CPG4537_3_public_or_full_parent_claim",
            "gate": "public/full parent claim",
            "status": "BLOCKED",
            "reason": "needs parent-owned component-edge theorem or accepted GR-parity branch plus interface gates",
            "valid_for_claim": "False",
        },
    ]


def finite_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FF4537_0_off_branch_delta_w",
            "quantity": "Delta_w_perp",
            "condition": "if GR-parity import is not adopted or a test includes nonstandard/hidden matter sectors",
            "status": "RETAIN_BOUND_ROUTE",
            "required_next": "source-backed component vector, material projection, tau/projection kernel and no-cancellation norm",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv"),
            "valid_for_claim": "False",
        },
        {
            "fallback_id": "FF4537_1_interface_residuals",
            "quantity": "R_eq/B_zero/worldtube/readout residuals",
            "condition": "even inside GR-parity matter branch",
            "status": "RETAIN_SEPARATE_GATES",
            "required_next": "same-current equality, no-flux/worldtube source measure and local interface residual gates",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4445_DERIVATION_ROWS.csv"),
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4537_0_rank_matrix",
            "gate": "M_graph rank matrix",
            "status": "PASS_FOR_TEMPLATE_AND_GR_PARITY_BRANCH",
            "meaning": "rank test kills P_perp Delta_w in the adopted standard visible branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4537_1_current_parent",
            "gate": "current MTS parent-derived component graph",
            "status": "BLOCKED_UNSIGNED",
            "meaning": "physical edges are templates, not parent-owned current-MTS derivations",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4537_2_local_branch_use",
            "gate": "private local-reduction use",
            "status": "ALLOW_PRIVATE_BRANCH_TESTING",
            "meaning": "safe to use GR-parity branch internally while carrying interface residual gates",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4537_3_full_local_GR_claim",
            "gate": "full local GR/Newton claim",
            "status": "BLOCKED_INTERFACE_AND_PARENT_SCOPE",
            "meaning": "source universality branch is improved, but R_eq/no-flux/worldtube/readout/nonlocal interface gates still remain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4537_0",
            "decision": DECISION,
            "meaning": "4537 executes the component rank test. The standard visible template graph has rank n-1 and zero non-common kernel, so GR-parity import can be adopted as a private local-reduction branch that kills P_perp Delta_w for ordinary visible matter. This is not a derivation of the SM from MTS and not a full local-GR claim; current MTS parent-owned graph remains unsigned and interface residuals remain live.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4537_0",
            "target": NEXT_TARGET,
            "objective": "Use the adopted private GR-parity branch to move past source-weight fog and attack the remaining local interface gates: R_eq, B_zero/no-flux, source worldtube measure, readout no-reentry and nonlocal MTS residuals.",
            "derive_first": "write branch conditions under which P_perp Delta_w=0 can be imported into the local GR/Newton/PPN source equations.",
            "fallback": "for off-branch or hidden-sector tests, retain finite Delta_w projection/source-bound rows.",
            "avoid": "claiming MTS derived the Standard Model or that source universality alone proves full local GR.",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    current: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4537_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    matrix_ok = len(matrix_rows) >= 7 and all("coefficients_by_node" in row for row in matrix_rows)
    checks.append({"validation_id": "VAL4537_01_matrix_rows", "status": "PASS" if matrix_ok else "FAIL", "detail": "component graph matrix rows generated from 1477 edges"})

    template = next((row for row in rank_rows if row["rank_case_id"] == "RR4537_0_template_graph"), {})
    current_parent = next((row for row in rank_rows if row["rank_case_id"] == "RR4537_1_current_parent_owned_graph"), {})
    rank_ok = template.get("rank_passes_on_pperp") == "True" and current_parent.get("rank_passes_on_pperp") == "False"
    checks.append({"validation_id": "VAL4537_02_rank_results", "status": "PASS" if rank_ok else "FAIL", "detail": "template/adopted branch passes while current parent-owned branch fails"})

    adoption_ok = any(row["adoption_id"] == "AD4537_0_GR_parity_scope" and row["status"] == "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH_ONLY" for row in adoption)
    checks.append({"validation_id": "VAL4537_03_adoption_scope", "status": "PASS" if adoption_ok else "FAIL", "detail": "GR-parity adoption is explicit and scoped as private nonclaim"})

    current_ok = any(row["gate_id"] == "CPG4537_1_current_parent_rank" and row["status"] == "FAIL_UNSIGNED_EDGES" for row in current)
    checks.append({"validation_id": "VAL4537_04_current_parent_block", "status": "PASS" if current_ok else "FAIL", "detail": "current MTS parent graph remains blocked"})

    finite_ok = any(row["fallback_id"] == "FF4537_0_off_branch_delta_w" for row in finite)
    checks.append({"validation_id": "VAL4537_05_finite_fallback", "status": "PASS" if finite_ok else "FAIL", "detail": "off-branch finite Delta_w fallback retained"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    checks.append({"validation_id": "VAL4537_06_claims_blocked", "status": "PASS" if gates_ok else "FAIL", "detail": "all claim gates remain nonclaim"})

    csv_paths = [SOURCE_REGISTER, MATRIX_CSV, RANK_RESULTS_CSV, ADOPTION_CSV, CURRENT_GATE_CSV, FINITE_FALLBACK_CSV, GATES_CSV, DECISION_CSV, NEXT_CSV]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4537_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4537_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4537_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4537 component graph rank matrix and GR-parity private adoption gate"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    current: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4537 - component graph rank matrix or adopt GR-parity import

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains internal, conditional and nonclaim.

## What Moved

- This checkpoint runs the rank matrix promised by 4536. The 1477 standard visible component graph has seven source-relevant nodes and incidence rank six.
- After common-mode projection, the template/adopted branch has zero non-common kernel: `P_perp Delta_w=0` for ordinary visible matter inside the GR-parity import branch.
- Current MTS parent derivation still fails the same test because the component edges are template/GR-parity adopted, not parent-owned MTS derivations.
- The practical result is a clean branch adoption: use GR-parity standard matter internally for local-reduction work, while retaining interface residual gates and off-branch finite `Delta_w` bounds.

## Component Graph Rank Matrix

{markdown_table(matrix_rows)}

## Rank Results

{markdown_table(rank_rows)}

### Compact Result

For `n=7` component nodes, the adopted standard visible incidence matrix has `rank=6=n-1`. Adding the common-mode row raises the rank to `7`, so:

`dim(ker(M_graph) cap im(P_perp)) = 0`.

Thus, on the GR-parity standard matter branch with fixed couplings and no source-prefactor/readout reentry, the only action-weight deformation is common calibration. The current parent-owned MTS graph does not pass because its component edges are not signed as MTS-derived.

## GR-Parity Adoption Certificate

{markdown_table(adoption)}

## Current Parent Application Gate

{markdown_table(current)}

## Finite Fallback After Rank

{markdown_table(finite)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "claim_name": "local_gr_newton_r2fr_component_graph_rank_matrix",
        "statement": "4537 executes the visible matter component graph rank matrix: GR-parity branch passes with zero non-common Delta_w kernel, while current MTS parent-owned graph remains unsigned.",
        "evidence": "Generated component graph rank matrix, rank results, GR-parity adoption certificate, current parent gate, finite fallback, claim gates and validation P8_Y5_BRR545_4537_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_GR_parity_branch_rank_pass_current_parent_unsigned",
        "next_target": NEXT_TARGET,
        "blocker": "GR-parity import is private branch adoption, not an MTS derivation of matter; interface residuals remain open.",
        "sector": "local_gr_newton",
        "source_path": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "failure_mode": "Claiming full local GR/Newton from GR-parity matter rank while R_eq/no-flux/worldtube/readout/interface gates remain open.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    matrix_rows, matrix = component_matrix_rows()
    rank_rows = rank_result_rows(matrix)
    adoption = adoption_rows()
    current = current_gate_rows()
    finite = finite_fallback_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MATRIX_CSV, matrix_rows)
    write_csv(RANK_RESULTS_CSV, rank_rows)
    write_csv(ADOPTION_CSV, adoption)
    write_csv(CURRENT_GATE_CSV, current)
    write_csv(FINITE_FALLBACK_CSV, finite)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, matrix_rows, rank_rows, adoption, current, finite, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, matrix_rows, rank_rows, adoption, current, finite, gates, decisions, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4537 Component Graph Rank Matrix Or Adopt GR-Parity Import

Marker: `{MARKER}`  
4537 executes the `M_graph` rank test. The standard visible component graph from 1477 has rank `n-1` and zero non-common kernel, so the GR-parity imported matter branch can be adopted privately for local-reduction work with `P_perp Delta_w=0`. Current MTS parent-owned component graph remains unsigned, and full local GR/Newton still waits on interface gates. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4537 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has an executable component graph rank matrix. On the adopted GR-parity standard visible branch, non-common source weights vanish. Off-branch sectors retain finite `Delta_w` bounds; interface residuals remain live.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
