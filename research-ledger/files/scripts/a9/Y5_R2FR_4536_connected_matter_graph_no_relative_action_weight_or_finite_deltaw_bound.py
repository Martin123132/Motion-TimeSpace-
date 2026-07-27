from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4536"
CLAIM_ID = "L-378"
MARKER = "PPC4161_CONNECTED_MATTER_GRAPH_NO_RELATIVE_ACTION_WEIGHT_OR_FINITE_DELTAW_BOUND_4536"
PACKET_MARKER = "PPC4161_PACKET_CONNECTED_MATTER_GRAPH_NO_RELATIVE_ACTION_WEIGHT_OR_FINITE_DELTAW_BOUND_4536"
DECISION = "CONNECTED_GRAPH_RANK_THEOREM_DERIVED_GR_PARITY_BRANCH_AVAILABLE_BUT_MTS_PARENT_COMPONENT_GRAPH_UNSIGNED"
NEXT_TARGET = "4537-Y5-R2FR-component-graph-rank-matrix-or-adopt-GR-parity-import.md"

FORMAL_PATH = FORMAL / "552-PPC4161-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"
DOC_PATH = POST / "4536-Y5-R2FR-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4536_SOURCE_REGISTER.csv"
GRAPH_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_CONNECTED_GRAPH_RANK_THEOREM.csv"
RENORMALIZATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_COMPONENT_WEIGHT_RENORMALIZATION_AUDIT.csv"
GR_PARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_GR_PARITY_IMPORT_DECISION.csv"
FINITE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_FINITE_DELTAW_BOUND_REQUIREMENTS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4536_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4536_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC4536_00_4535_owner",
            "label": "4535 owner split",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4535_OWNER_DERIVATION_SPLIT.csv",
            "needle": "OWN4535_3_connected_graph_route",
            "role": "connected graph route target",
        },
        {
            "source_id": "SRC4536_01_4535_counter",
            "label": "4535 component countermodel",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4535_COMPONENT_WEIGHT_COUNTERMODEL_GATE.csv",
            "needle": "CCG4535_0_weighted_decomposition",
            "role": "weighted L_matter countermodel",
        },
        {
            "source_id": "SRC4536_02_4443_root",
            "label": "4443 nonEM root edge",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4443_DERIVATION_ROWS.csv",
            "needle": "NEDGE4443_0_root_hilbert_stress_edge",
            "role": "root edge already branch-signed",
        },
        {
            "source_id": "SRC4536_03_4443_species_edges",
            "label": "4443 species edge templates",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_SPECIES_EDGE_OUTPUT.csv",
            "needle": "EDGE4443_0_L_to_lepton_template",
            "role": "component graph edge templates not signed",
        },
        {
            "source_id": "SRC4536_04_4444_component",
            "label": "4444 component naturality",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4444_DERIVATION_ROWS.csv",
            "needle": "LMCE4444_1_component_naturality_contract",
            "role": "connected component theorem precursor",
        },
        {
            "source_id": "SRC4536_05_4445_gr_parity",
            "label": "4445 GR-parity import",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4445_DERIVATION_ROWS.csv",
            "needle": "SMIMP4445_0_GR_parity_import_principle",
            "role": "fair MTS-to-GR matter import principle",
        },
        {
            "source_id": "SRC4536_06_standard_import_doc",
            "label": "standard visible matter import contract",
            "path": FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
            "needle": "The Hilbert source is",
            "role": "calibrated visible matter branch",
        },
        {
            "source_id": "SRC4536_07_4533_pack",
            "label": "4533 source pack",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv",
            "needle": "SP4533_5_delta_w_species",
            "role": "finite Delta_w fallback",
        },
        {
            "source_id": "SRC4536_08_4535_finite",
            "label": "4535 finite Delta_w route",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv",
            "needle": "FBR4535_OVERALL",
            "role": "no claim-grade Delta_w bound yet",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in source_specs:
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


def graph_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CGRT4536_0_exact_rank_statement",
            "statement": "Relative component action weights are killed only when the fixed kinetic/vertex/readout constraint matrix has full rank on the non-common weight subspace.",
            "formal_condition": "Let delta l_i = delta ln w_i and P_perp remove the common mode. Let M_graph contain rows from canonical kinetic residues, fixed mass ratios, fixed charge/current normalizations, fixed interaction vertices, fixed binding/composite maps, and no readout reentry. If ker(M_graph) ∩ im(P_perp) = {0}, then P_perp delta l = 0.",
            "proof_move": "A component rescaling that keeps all nongravitational observables fixed must lie in ker(M_graph). Full rank on im(P_perp) leaves only common calibration; any nonzero kernel vector is a real Delta_w residual or measured-constant drift.",
            "result": "EXACT_CONDITIONAL_RANK_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CGRT4536_1_connected_not_sufficient",
            "statement": "Graph connectedness alone is not sufficient.",
            "formal_condition": "A connected graph with freely retunable vertex couplings or hidden readout maps can absorb non-common weights into theta_A or source-only spurions.",
            "proof_move": "Field rescalings can move weights from kinetic terms into vertices. If those vertex constants are not parent-fixed or measured, relative weights remain underdetermined.",
            "result": "CONNECTEDNESS_REDUCES_BUT_DOES_NOT_CLOSE",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CGRT4536_2_gr_parity_branch",
            "statement": "A GR-parity imported standard matter action can close the source-weight route without deriving all microphysics.",
            "formal_condition": "Import one standard S_matter[g, fields, theta_SM] with fixed internal constants, canonical normalization, Hilbert variation before readout, no SpeciesLabel/MaterialLabel -> Coeff_active_source Hom, and no readout reentry.",
            "proof_move": "GR itself does not derive the Standard Model; it assumes a matter action and couples universally to its Hilbert stress. MTS local reduction can use the same parity branch if it forbids extra MTS source-only weights.",
            "result": "GR_PARITY_IMPORT_CAN_SIGN_COMPONENT_SOURCE_UNIVERSALITY_IF_ADOPTED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CGRT4536_3_current_MTS_status",
            "statement": "Current MTS has the root edge and import contract, but no source-backed M_graph rank matrix.",
            "formal_condition": "4443/4444/4445 provide root edge, component templates and GR-parity theorem; they do not provide a parent-signed component graph rank matrix with fixed coupling/readout rows.",
            "proof_move": "Therefore local GR/Newton source coupling does not claim-pass yet; the next executable target is M_graph construction or explicit GR-parity adoption.",
            "result": "RANK_MATRIX_OR_ADOPTION_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def renormalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "REN4536_0_free_disconnected_sector",
            "case": "disconnected or free sector",
            "weight_effect": "relative w_i can be classically invisible while changing active source",
            "constraint_rank_effect": "kernel survives on P_perp",
            "verdict": "RETAIN_DELTAW_RESIDUAL",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "REN4536_1_connected_fixed_vertex",
            "case": "connected sector with fixed canonical kinetic residues and fixed vertex couplings",
            "weight_effect": "field rescalings move w_i into measured couplings/charges/mass ratios; fixed observables force non-common weights to zero",
            "constraint_rank_effect": "full rank possible if vertex/incidence rows span P_perp",
            "verdict": "ZERO_IF_RANK_TEST_PASSES",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "REN4536_2_connected_retargetable_couplings",
            "case": "connected sector but couplings are allowed to retune as hidden theta",
            "weight_effect": "non-common weights can be reabsorbed as changes in theta rather than source-only coefficients",
            "constraint_rank_effect": "rank test must include fixed measured theta rows; otherwise kernel is too large",
            "verdict": "NOT_SOURCE_ONLY_BUT_NOT_ZERO_WITHOUT_FIXED_THETA",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "REN4536_3_material_readout",
            "case": "Ti/Pt/material/orbital source inventory",
            "weight_effect": "material composition enters empirical readout tensors, not parent active-source coefficient",
            "constraint_rank_effect": "material projection rows score residuals only after source universality is fixed or Delta_w is bounded",
            "verdict": "READOUT_SCOPE_SEPARATED",
            "valid_for_claim": "False",
        },
    ]


def gr_parity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "GRP4536_0_import_allowed",
            "branch": "GR-parity standard matter import",
            "status": "AVAILABLE_PRIVATE_BRANCH",
            "meaning": "MTS can aim to reduce to GR using the same imported standard matter action GR uses; it need not derive all SM sectors to pass local GR.",
            "requirement": "adopt single S_matter with fixed theta_SM, canonical normalization, no source-only prefactor, Hilbert variation before readout.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "GRP4536_1_not_yet_adopted",
            "branch": "current MTS parent derivation",
            "status": "NOT_PARENT_SIGNED",
            "meaning": "The corpus has component templates and import contract, but not an explicit adoption/rank certificate for source-universality.",
            "requirement": "write M_graph rank matrix or explicit GR-parity adoption certificate with no hidden/readout reentry.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "GRP4536_2_if_not_adopted",
            "branch": "finite Delta_w route",
            "status": "BOUND_ROUTE_REQUIRED",
            "meaning": "If source universality is not adopted/derived, Delta_w is a physical residual vector to project into WEP/R10/PPN/orbital tests.",
            "requirement": "numeric/material source vector, tau/projection coefficient, bound, no-cancellation norm and source path.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "FDB4536_0_vector",
            "quantity": "Delta_w_perp vector",
            "required_for_bound": "dimensionless component/source weight vector after common-mode projection",
            "current_status": "SYMBOLIC_ONLY",
            "source_hint": str(SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv"),
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "FDB4536_1_projection",
            "quantity": "tau_WEP/R10/PPN/material projection",
            "required_for_bound": "arena-specific transfer from Delta_w_perp to observable residual",
            "current_status": "MISSING_CLAIM_GRADE_PROJECTION",
            "source_hint": str(SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv"),
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "FDB4536_2_nocancel",
            "quantity": "no-cancellation norm",
            "required_for_bound": "absolute/envelope norm so component cancellations are not used as evidence",
            "current_status": "NOT_SOURCED",
            "source_hint": "future material/readout source pack",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "FDB4536_OVERALL",
            "quantity": "finite Delta_w bound branch",
            "required_for_bound": "all rows above plus comparator bound",
            "current_status": "NOT_READY",
            "source_hint": str(SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv"),
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4536_0_rank_theorem",
            "gate": "connected graph rank theorem",
            "status": "PASS_CONDITIONAL_THEOREM",
            "meaning": "full-rank fixed-observable graph constraints kill non-common source weights",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4536_1_connectedness_only",
            "gate": "connectedness alone",
            "status": "REJECT_AS_INSUFFICIENT",
            "meaning": "connected graph without fixed couplings/rank can still hide weights",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4536_2_current_MTS_application",
            "gate": "current MTS component graph",
            "status": "BLOCKED_RANK_MATRIX_OR_ADOPTION_MISSING",
            "meaning": "component templates exist but are not parent-signed/rank-scored",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4536_3_GR_parity_import",
            "gate": "GR-parity matter import",
            "status": "AVAILABLE_NOT_PROMOTED",
            "meaning": "fair local-GR branch if explicitly adopted with no source-prefactor/no reentry",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4536_4_finite_bound",
            "gate": "finite Delta_w bound",
            "status": "BLOCKED_VALUES_MISSING",
            "meaning": "symbolic vector/projection/no-cancel requirements remain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4536_0",
            "decision": DECISION,
            "meaning": "4536 turns the component-coupling problem into an exact rank theorem. A connected, fixed-observable matter graph kills invisible relative source weights only if its constraint matrix is full-rank on the non-common subspace. GR-parity standard matter import is an available fair branch, but current MTS has not adopted/rank-scored it. The next concrete work is an M_graph rank matrix or explicit GR-parity adoption certificate; otherwise build finite Delta_w bounds.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4536_0",
            "target": NEXT_TARGET,
            "objective": "Build the actual component graph rank matrix for the imported standard visible matter branch, or explicitly adopt GR-parity import as a local-reduction branch with no-source-prefactor/no-reentry clauses.",
            "derive_first": "construct M_graph rows for canonical kinetic residues, masses, charges, gauge/Yukawa/QCD vertices, binding/composite maps and readout no-reentry; test rank on P_perp.",
            "fallback": "if rank/adoption is not possible, create finite Delta_w vector/projection/no-cancellation source-pack rows.",
            "avoid": "claiming connectedness alone kills source weights.",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    renorm: list[dict[str, Any]],
    gr_parity: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4536_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    theorem_ids = {row["theorem_id"] for row in theorem}
    theorem_ok = {"CGRT4536_0_exact_rank_statement", "CGRT4536_1_connected_not_sufficient", "CGRT4536_3_current_MTS_status"}.issubset(theorem_ids)
    checks.append({"validation_id": "VAL4536_01_rank_theorem", "status": "PASS" if theorem_ok else "FAIL", "detail": "rank theorem, connectedness guard and current-status rows present"})

    renorm_ok = {"REN4536_1_connected_fixed_vertex", "REN4536_2_connected_retargetable_couplings"}.issubset({row["audit_id"] for row in renorm})
    checks.append({"validation_id": "VAL4536_02_renormalization", "status": "PASS" if renorm_ok else "FAIL", "detail": "renormalization audit separates fixed-vertex and retargetable-coupling cases"})

    gr_ok = any(row["branch_id"] == "GRP4536_0_import_allowed" for row in gr_parity) and any(row["branch_id"] == "GRP4536_1_not_yet_adopted" for row in gr_parity)
    checks.append({"validation_id": "VAL4536_03_gr_parity", "status": "PASS" if gr_ok else "FAIL", "detail": "GR-parity branch available but not promoted"})

    finite_ok = any(row["requirement_id"] == "FDB4536_OVERALL" and row["current_status"] == "NOT_READY" for row in finite)
    checks.append({"validation_id": "VAL4536_04_finite_bound", "status": "PASS" if finite_ok else "FAIL", "detail": "finite Delta_w bound requirements remain explicit"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    checks.append({"validation_id": "VAL4536_05_claims_blocked", "status": "PASS" if gates_ok else "FAIL", "detail": "all claim gates remain nonclaim"})

    csv_paths = [SOURCE_REGISTER, GRAPH_THEOREM_CSV, RENORMALIZATION_CSV, GR_PARITY_CSV, FINITE_BOUND_CSV, GATES_CSV, DECISION_CSV, NEXT_CSV]
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
    checks.append({"validation_id": "VAL4536_06_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4536_07_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4536_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4536 connected matter graph rank theorem and GR-parity/finiteness branch split"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    renorm: list[dict[str, Any]],
    gr_parity: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4536 - connected matter graph no-relative-action-weight or finite Delta-w bound

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains internal, conditional and nonclaim.

## What Moved

- 4536 does not make the lazy move "connected graph therefore solved". It derives the sharper condition: the graph constraint matrix must be full rank on the non-common action-weight subspace.
- This is progress because `Delta_w_A` is now an executable rank/bound target, not a vague coupling worry.
- The GR-parity route is fair: MTS can reduce to GR by importing the same standard matter action GR uses, provided no MTS-only source prefactor/readout reentry is added.
- Current MTS still does not claim local GR/Newton source universality: component graph rank/adoption and finite `Delta_w` bounds remain open.

## Connected Graph Rank Theorem

{markdown_table(theorem)}

### Compact Derivation

Let `delta l_i = delta ln w_i` be infinitesimal component action-weight shifts and let `P_perp` remove the common calibration mode. Every fixed nongravitational datum contributes a row to `M_graph`: canonical kinetic residues, mass ratios, charge/current normalization, gauge/Yukawa/QCD vertices, binding/composite maps, and readout no-reentry. A source-only relative weight must leave all those rows unchanged, so it lies in `ker(M_graph)`.

If `ker(M_graph) ∩ im(P_perp) = {{0}}`, the only allowed action-weight shift is common calibration, so `P_perp Delta_w=0`. If the intersection is nonzero, that surviving vector is a real finite `Delta_w` residual and must be bounded. Thus connectedness is useful but not enough; full rank is the actual condition.

## Component Weight Renormalization Audit

{markdown_table(renorm)}

## GR-Parity Import Decision

{markdown_table(gr_parity)}

## Finite Delta-w Bound Requirements

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
        "claim_name": "local_gr_newton_r2fr_connected_graph_rank_theorem",
        "statement": "4536 derives the connected matter graph rank condition for killing relative source weights, while keeping GR-parity import and finite Delta_w bounds nonclaim until rank/adoption/source rows exist.",
        "evidence": "Generated connected graph rank theorem, renormalization audit, GR-parity import decision, finite Delta_w requirements, claim gates and validation P8_Y5_BRR545_4536_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_rank_theorem_component_graph_unsigned",
        "next_target": NEXT_TARGET,
        "blocker": "No source-backed M_graph rank matrix or explicit GR-parity adoption certificate exists yet.",
        "sector": "local_gr_newton",
        "source_path": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "failure_mode": "Treating graph connectedness alone as proof that source-only weights vanish.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = graph_theorem_rows()
    renorm = renormalization_rows()
    gr_parity = gr_parity_rows()
    finite = finite_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(GRAPH_THEOREM_CSV, theorem)
    write_csv(RENORMALIZATION_CSV, renorm)
    write_csv(GR_PARITY_CSV, gr_parity)
    write_csv(FINITE_BOUND_CSV, finite)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, renorm, gr_parity, finite, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, renorm, gr_parity, finite, gates, decisions, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4536 Connected Matter Graph No Relative Action Weight Or Finite Delta-w Bound

Marker: `{MARKER}`  
4536 derives the exact connected-graph rank condition: source-only relative component weights vanish only if the fixed kinetic/vertex/readout constraint matrix has full rank on the non-common weight subspace. Connectedness alone is rejected as insufficient. The fair GR-parity standard matter import branch is available but not promoted until explicitly adopted/rank-scored with no source-prefactor and no readout reentry. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4536 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now treats component source universality as a rank/adoption problem: either `ker(M_graph) ∩ im(P_perp)=0`, or the surviving kernel vector becomes a finite `Delta_w` residual to bound.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
