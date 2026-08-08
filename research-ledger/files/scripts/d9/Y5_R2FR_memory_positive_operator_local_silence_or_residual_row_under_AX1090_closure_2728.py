from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2728-Y5-R2FR-memory-positive-operator-local-silence-or-residual-row-under-AX1090-closure.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2728_SOURCE_REGISTER.csv",
    "activation": RESIDUALS / "P8_Y5_R2FR_2728_MEMORY_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2728_ENERGY_IDENTITY_THEOREM.csv",
    "jx": RESIDUALS / "P8_Y5_R2FR_2728_JX_ZERO_COMPONENT_AUDIT.csv",
    "boundary": RESIDUALS / "P8_Y5_R2FR_2728_BOUNDARY_ZERO_MODE_AUDIT.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2728_MEMORY_RESIDUAL_ROWS_NONCLAIM.csv",
    "ejeff": RESIDUALS / "P8_Y5_R2FR_2728_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2728_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2728_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2728_NEXT_TARGET.csv",
    "snapshot": RESIDUALS / "P8_Y5_R2FR_2728_PROJECT_STATUS_SNAPSHOT.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2728_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2728_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "memory_positive_operator_residual_rows_2728_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "memory_positive_operator_EJeff_update_2728_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2728_PARENT_MEMORY_SIGNATURE_PLUS_FINITE_RESIDUAL_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2728_0_2727_handoff",
            "description": "2727 selected the memory positive-operator route after readout remained conditional",
            "path": DOC.parent / "2727-Y5-R2FR-readout-after-variation-no-reduced-action-backreaction-or-generator-row-under-AX1090-closure.md",
            "needles": ["NEXT2727_0_selected", "memory positive-operator", "VAL2727_OVERALL"],
            "use": "current handoff and no-claim discipline",
        },
        {
            "source_id": "SRC2728_1_967_relative_lemma",
            "description": "relative positive-operator energy identity and amplitude law",
            "path": DOC.parent / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict", "MB967_0_gap"],
            "use": "mathematical theorem form and finite-bound fallback",
        },
        {
            "source_id": "SRC2728_2_968_input_audit",
            "description": "memory operator activation inputs missing",
            "path": DOC.parent / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
            "needles": ["MOI968_0_X_variable", "MOI968_8_verdict", "MZG968_7_verdict"],
            "use": "parent X/domain/operator/source/boundary/coupling blockers",
        },
        {
            "source_id": "SRC2728_3_2626_owner_gate",
            "description": "parent memory operator owner hunt and residual template",
            "path": DOC.parent / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md",
            "needles": ["MOA2626_9_verdict", "ZPT2626_4_current_verdict", "MRI2626_0_lambda_gap"],
            "use": "latest owner audit and template rows",
        },
        {
            "source_id": "SRC2728_4_2627_source_boundary",
            "description": "J_X component and boundary zero audit",
            "path": DOC.parent / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md",
            "needles": ["JX2627_6_total_verdict", "BZ2627_5_current_verdict", "RBP2627_5_score_gate"],
            "use": "component source/boundary failure map",
        },
        {
            "source_id": "SRC2728_5_1980_positivity_sign",
            "description": "parent memory positivity lemma and exact missing signs",
            "path": DOC.parent / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md",
            "needles": ["GATE1980_0_Zm", "GATE1980_1_M2", "DEC1980_2_best_next"],
            "use": "Z_m and M_X^2 sign requirements",
        },
        {
            "source_id": "SRC2728_6_573_generator_debt",
            "description": "memory scalar generator debt ledger",
            "path": RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
            "needles": ["IG573_3_memory_scalar", "not_silenced_as_theorem"],
            "use": "generator debt lineage",
        },
        {
            "source_id": "SRC2728_7_574_attempts",
            "description": "earlier memory scalar elimination attempt",
            "path": RESIDUALS / "P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv",
            "needles": ["GE574_4_memory_scalar", "conditional_interior_silence_boundary_open"],
            "use": "historical failure mode to avoid repeating",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path: Path = spec["path"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "description": spec["description"],
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "valid_for_claim": False,
            }
        )
    return rows


def activation_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "MPOA2728_0_parent_X",
            "gate": "parent-owned memory/class scalar X",
            "required_to_activate": "X is a parent configuration variable or quotient scalar with an Euler-Lagrange equation owner",
            "current_status": "MISSING_PARENT_OWNER",
            "source_evidence": "MOI968_0_X_variable; MOA2626_0_parent_X",
            "consequence": "no theorem-zero; X remains a retained generator/residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_1_domain_D",
            "gate": "selected compact local exterior D",
            "required_to_activate": "D and its boundary class are selected by the same parent structure, not by posthoc local scoring",
            "current_status": "MISSING_PARENT_SELECTED_DOMAIN",
            "source_evidence": "MOI968_1_domain_D; MOA2626_1_domain_D",
            "consequence": "domain selector/wall terms can still source X",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_2_operator_LX",
            "gate": "parent-derived operator L_X",
            "required_to_activate": "L_X=-nabla_i(A^ij nabla_j)+m_X^2 is extracted from parent variation, not introduced as a useful ansatz",
            "current_status": "CANDIDATE_EXISTS_NOT_PARENT_SIGNED",
            "source_evidence": "MPO967_1_operator; MOA2626_2_operator_LX; QMA970 lineage in 2626",
            "consequence": "energy identity is mathematically shaped but not parent-owned",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_3_positive_principal_symbol",
            "gate": "positive A^ij",
            "required_to_activate": "A^ij is symmetric and bounded below by a_min h^ij with a_min>0 on D, or a controlled semidefinite kernel is quotient-removed",
            "current_status": "MISSING_SIGN_CERTIFICATE",
            "source_evidence": "MOI968_3_positivity; MOA2626_3_positive_A; GATE1980_0_Zm",
            "consequence": "integral identity cannot force grad X=0",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_4_gap_zero_mode",
            "gate": "mass/gap and zero-mode package",
            "required_to_activate": "m_X^2>=0 plus lambda_gap>0 after Dirichlet/mean/topological/quotient zero-mode removal",
            "current_status": "MISSING_GAP_INPUTS",
            "source_evidence": "MOI968_4_mass_gap; MOA2626_4_mass_gap; GATE1980_1_M2",
            "consequence": "constant or flat memory modes remain legal",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_5_JX_zero",
            "gate": "J_X=0 component theorem",
            "required_to_activate": "kinetic affine, matter, observed-slot, chi-wall, boundary, history and readout components all vanish",
            "current_status": "JX_ZERO_NOT_PROVED",
            "source_evidence": "JX2627_6_total_verdict; MOA2626_5_JX_source_map",
            "consequence": "any live component produces a finite memory residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_6_boundary_zero",
            "gate": "boundary and zero-mode silence",
            "required_to_activate": "Dirichlet, zero-flux plus zero mean, exact/topological boundary primitive, or universal constant calibration is parent-signed",
            "current_status": "BOUNDARY_ZERO_NOT_PARENT_DERIVED",
            "source_evidence": "BZ2627_5_current_verdict; MOA2626_6_boundary_zero_mode",
            "consequence": "boundary hair can carry local PPN/clock/R10 leakage",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_7_observable_projection",
            "gate": "arena couplings K_i",
            "required_to_activate": "R10, PPN, clock, Gdot, orbital and WEP projections from X and grad X are sourced with units",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "source_evidence": "MOI968_7_observable_couplings; MOA2626_7_observable_couplings",
            "consequence": "finite residual cannot yet be scored against data",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPOA2728_8_verdict",
            "gate": "memory positive-operator local silence",
            "required_to_activate": "MPOA2728_0 through MPOA2728_7 all pass with parent source paths",
            "current_status": "RELATIVE_THEOREM_READY_ACTIVATION_FAILS",
            "source_evidence": "967 proves relative identity; 968/2626/2627/1980 show missing inputs",
            "consequence": "do not claim local-GR/PPN/R10 memory silence; retain explicit memory residual vector",
            "valid_for_claim": False,
        },
    ]


def identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "EID2728_0_setup",
            "statement": "On a selected local exterior D, suppose X obeys L_X X=J_X with L_X=-nabla_i(A^ij nabla_j)+m_X^2.",
            "status": "CONDITIONAL_SETUP",
            "required_inputs": "parent X; parent D; parent L_X",
            "result": "setup is usable only as a theorem contract",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EID2728_1_energy_identity",
            "statement": "Multiplying by X and integrating gives int_D A^ij grad_i X grad_j X + m_X^2 X^2 = int_D X J_X plus boundary term.",
            "status": "RELATIVE_DERIVATION_OK",
            "required_inputs": "symmetric A^ij; controlled boundary term; regularity for integration by parts",
            "result": "not a plateau axiom; this is the legitimate no-hair route if premises sign",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EID2728_2_zero_theorem",
            "statement": "If A^ij is positive, m_X^2>=0, J_X=0, and boundary/zero modes are removed, then X=0 on D up to allowed universal constants.",
            "status": "RELATIVE_ZERO_THEOREM",
            "required_inputs": "positive symbol; nonnegative gap; zero source; zero boundary; zero-mode handling",
            "result": "mathematically clean but not activated by current parent corpus",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EID2728_3_amplitude_law",
            "statement": "If zero fails but lambda_gap>0, ||X||_L2 <= (||J_X||_L2 + boundary_lift_norm)/lambda_gap, with analogous gradient/pointwise estimates.",
            "status": "FINITE_BOUND_LAW_READY_NONCLAIM",
            "required_inputs": "lambda_gap; J_X norm; boundary lift; elliptic constants",
            "result": "turns a failed proof into explicit local-bound input rows",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EID2728_4_constant_mode_exception",
            "statement": "If m_X=0 and boundary/mean/topology do not remove constants, X may be constant; this is harmless only if universal and source-independent.",
            "status": "EXCEPTION_RETAINED",
            "required_inputs": "constant sector universality and source-independence",
            "result": "constant memory calibration cannot be silently counted as local-GR derivation",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EID2728_5_current_verdict",
            "statement": "The local-vacuum memory plateau lemma is derivable only relative to parent-signed operator/source/boundary premises.",
            "status": "DO_NOT_PROMOTE",
            "required_inputs": "MPOA2728_0..7",
            "result": "E_memory_scalar_generator remains active as a source-ready nonclaim residual",
            "valid_for_claim": False,
        },
    ]


def jx_rows() -> list[dict[str, Any]]:
    components = [
        ("JX2728_0_kinetic_affine", "J_X^kin_affine", "zero origin/evenness of the X kinetic block", "NOT_PARENT_SIGNED", "shifted origin or hidden representative marker"),
        ("JX2728_1_matter", "J_X^matter", "ordinary matter is quotient-blind to X and uses descended observed slots only", "CONDITIONAL_ONLY", "Weyl/disformal/mass/source-label channel"),
        ("JX2728_2_observed_slot", "J_X^obs", "observed/source coupling vanishes on local branch origin and is parent-owned", "RELATIVE_ZERO_UNSIGNED", "double-zero gate becomes closure choice"),
        ("JX2728_3_chi_wall", "J_X^chi_wall", "domain selector has no moving wall source and f'(0)=0 if relevant", "CONDITIONAL_ONLY", "selector/domain wall surface source"),
        ("JX2728_4_boundary", "J_X^boundary", "boundary current is fixed, exact/topological, or zero-flux with zero-mode removal", "NOT_DERIVED", "boundary hair drives local residuals"),
        ("JX2728_5_history", "J_X^history", "memory kernel has no local tail in compact exterior domain", "NOT_DERIVED", "history tail leaks cosmology/global memory into local tests"),
        ("JX2728_6_readout", "J_X^readout", "readout enters only after variation and cannot source parent X", "RELATIVE_SCHEMA_ONLY", "readout remains conditional because parent-domain signature is unsigned"),
    ]
    rows = [
        {
            "component_id": cid,
            "component": comp,
            "zero_condition": cond,
            "current_status": status,
            "failure_mode": fail,
            "next_action": "derive zero from parent action/domain signature or retain component norm",
            "valid_for_claim": False,
        }
        for cid, comp, cond, status, fail in components
    ]
    rows.append(
        {
            "component_id": "JX2728_7_total_verdict",
            "component": "J_X_total",
            "zero_condition": "all components JX2728_0..6 vanish under a single parent-owned local domain",
            "current_status": "JX_ZERO_NOT_PROVED",
            "failure_mode": "nonzero memory source implies finite residual instead of local silence",
            "next_action": "do not rerun theorem; build finite residual/source norm interface unless a new parent action signs the clauses",
            "valid_for_claim": False,
        }
    )
    return rows


def boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "BZ2728_0_variational_term",
            "gate": "identify X boundary term",
            "condition": "boundary contribution from integration by parts is fixed, cancelled, nonnegative, or zero",
            "current_status": "TERM_IDENTIFIED_NOT_SELECTED",
            "gap": "parent boundary condition for X is not selected",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BZ2728_1_dirichlet",
            "gate": "Dirichlet/local calibration",
            "condition": "X|partialD=0 or fixed universal value",
            "current_status": "CONDITIONAL_ROUTE",
            "gap": "could be imposed as closure; not parent-derived",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BZ2728_2_neumann_zero_mean",
            "gate": "zero flux plus zero mean",
            "condition": "n_i A^ij grad_j X=0 and constant mode removed or universal",
            "current_status": "CONDITIONAL_ROUTE",
            "gap": "zero-mode class and parent-selected mean condition unsigned",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BZ2728_3_exact_topological",
            "gate": "exact/topological primitive",
            "condition": "boundary current is exact/pure bookkeeping with zero local representative",
            "current_status": "CONDITIONAL_NOT_DERIVED",
            "gap": "boundary primitive and Bianchi/no-secular-drift lock remain unsigned",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BZ2728_4_wall_stress",
            "gate": "no selector wall stress",
            "condition": "metric/domain selector variation creates no local stress or is Ward-owned",
            "current_status": "NOT_DERIVED",
            "gap": "domain wall stress could source local geometry",
            "valid_for_claim": False,
        },
        {
            "boundary_id": "BZ2728_5_verdict",
            "gate": "boundary zero package",
            "condition": "one boundary route passes from parent action, or finite boundary_lift_norm is retained",
            "current_status": "BOUNDARY_ZERO_NOT_PARENT_DERIVED",
            "gap": "no memory zero/local-GR claim",
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EMEM2728_0_E_memory_parent_owner",
            "quantity": "E_memory_parent_owner",
            "definition": "residual from no source-backed parent X / memory-class scalar owner",
            "feeds": "E_memory_scalar_generator;E_local_invariant_algebra",
            "source_path": str(DOC.parent / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"),
            "missing": "MISSING_PARENT_X_OWNER",
            "next_action": "parent field/quotient certificate or retained residual input",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_1_E_memory_operator_sign",
            "quantity": "E_memory_operator_sign",
            "definition": "residual from unsigned A^ij positivity, Z_X normalization, m_X^2/gap, and zero-mode package",
            "feeds": "E_memory_scalar_generator;R2FR_local_leakage",
            "source_path": str(DOC.parent / "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md"),
            "missing": "MISSING_ZX_SIGN;MISSING_MX2_GAP;MISSING_LAMBDA1_D",
            "next_action": "source parent field-space metric and strict Hessian or keep finite lambda_gap row",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_2_E_memory_JX_source",
            "quantity": "E_memory_JX_source",
            "definition": "residual from unproved J_X=0 across kinetic, matter, observed-slot, chi-wall, boundary, history and readout channels",
            "feeds": "E_memory_scalar_generator;source_side_residuals",
            "source_path": str(DOC.parent / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md"),
            "missing": "MISSING_JX_COMPONENT_ZERO_THEOREMS",
            "next_action": "component source norms with units or parent zero theorem",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_3_E_memory_boundary_lift",
            "quantity": "E_memory_boundary_lift",
            "definition": "residual from missing boundary no-hair / zero flux / exact primitive / zero-mode class",
            "feeds": "E_memory_scalar_generator;PPN;clock;R10;orbital",
            "source_path": str(DOC.parent / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md"),
            "missing": "MISSING_BOUNDARY_ZERO_PACKAGE",
            "next_action": "boundary_lift_norm and projection coefficients or parent no-hair theorem",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_4_E_memory_arena_projection",
            "quantity": "E_memory_arena_projection",
            "definition": "residual from missing K_i, K_i_grad map from memory amplitude/gradient to local observables",
            "feeds": "R10;PPN;clock;Gdot;orbital;WEP",
            "source_path": str(DOC.parent / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md"),
            "missing": "MISSING_K_R10;MISSING_K_PPN;MISSING_K_CLOCK;MISSING_K_GDOT;MISSING_K_ORBITAL;MISSING_K_WEP",
            "next_action": "finite local residual interface before any empirical score",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_5_E_memory_tower_return",
            "quantity": "E_memory_tower_return",
            "definition": "residual from integrated-out memory/scalar tower returning as R2/f(R)/R11-like leakage",
            "feeds": "EH_operator_selection;R2FR_scalar;local_GR",
            "source_path": str(DOC.parent / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md"),
            "missing": "MISSING_NO_TOWER_CERTIFICATE",
            "next_action": "effective-action after-elimination audit or retained tower residual rows",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMEM2728_6_E_memory_scalar_generator",
            "quantity": "E_memory_scalar_generator",
            "definition": "combined memory/class scalar generator residual retained because positive-operator local silence is relative-only",
            "feeds": "local_GR_gate;Newton_limit;R10;PPN;clock;orbital",
            "source_path": str(DOC),
            "missing": "PARENT_OWNER_PLUS_SIGN_PLUS_SOURCE_PLUS_BOUNDARY_PLUS_PROJECTION",
            "next_action": "use 2729 finite residual/signature interface; do not claim theorem-zero",
            "valid_for_claim": False,
        },
    ]


def ejeff_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2728_0_memory_scalar_generator",
            "formula": "E_memory_scalar_generator := E_memory_parent_owner + E_memory_operator_sign + E_memory_JX_source + E_memory_boundary_lift + E_memory_arena_projection + E_memory_tower_return",
            "status": "ACTIVE_NONCLAIM_RESIDUAL",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2728_1_positive_operator_contract",
            "formula": "X=0 follows only if parent signs X,D,L_X,A>=0,m_X^2/gap,J_X=0,boundary zero,zero-mode handling and no tower/projection leak",
            "status": "RELATIVE_THEOREM_CONTRACT_NOT_ACTIVATED",
            "claim_allowed": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE2728_0_memory_zero", "gate": "memory scalar theorem-zero", "status": "BLOCKED", "reason": "activation gates MPOA2728_0..7 are not parent-signed", "opened": False, "valid_for_claim": False},
        {"gate_id": "GATE2728_1_finite_bound", "gate": "finite memory residual bound score", "status": "BLOCKED", "reason": "lambda_gap, J_X norm, boundary_lift_norm and K_i projections are not numeric/sourced", "opened": False, "valid_for_claim": False},
        {"gate_id": "GATE2728_2_local_GR", "gate": "derived local GR/Newton promotion", "status": "BLOCKED", "reason": "memory generator remains active and EH/no-extension gates are not fully closed", "opened": False, "valid_for_claim": False},
        {"gate_id": "GATE2728_3_public_claim", "gate": "public local-test claim", "status": "BLOCKED", "reason": "this is private derivation plumbing only", "opened": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2728_0_theorem",
            "decision": "KEEP_RELATIVE_POSITIVE_OPERATOR_THEOREM",
            "because": "the integration-by-parts identity is real and non-circular once the parent premises are signed",
            "consequence": "do not discard the route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2728_1_no_promotion",
            "decision": "DO_NOT_CLAIM_MEMORY_LOCAL_SILENCE",
            "because": "parent X, D, L_X signs, J_X=0, boundary and projection inputs are still unsigned",
            "consequence": "no local-GR/Newton/R10/PPN/clock/orbital pass",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2728_2_no_looping",
            "decision": "STOP_RERUNNING_THE_SAME_POSITIVITY_PROOF",
            "because": "the proof shape is already known; the missing item is signature evidence or finite residual inputs",
            "consequence": "next checkpoint must be parent-signature contract plus finite residual interface",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2728_0_selected",
            "status": "selected_primary",
            "target_doc": "2729-Y5-R2FR-parent-memory-signature-contract-plus-finite-local-residual-interface-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_parent_memory_signature_contract_plus_finite_local_residual_interface_under_AX1090_closure_2729.py",
            "mission": "write the exact parent action/signature contract that would activate the memory no-hair theorem, and in parallel produce the finite residual input interface for R10/PPN/clocks/Gdot/orbital/WEP if the contract remains unsigned",
            "acceptance": "either source-backed Z_X/M_X^2/J_X/boundary clauses exist, or all finite residual rows remain explicit, unit-tagged, source-needed, and valid_for_claim=false",
            "forbidden": "another generic positive-operator proof without new parent signature evidence; plateau axiom; invented coefficients; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2728_0_project",
            "area": "local GR/Newton derivation",
            "status": "SHARPER_BUT_NOT_CLOSED",
            "summary": "positive memory no-hair is a valid relative theorem, but activation inputs remain unsigned",
            "next_pressure_point": "parent memory signature or finite residual interface",
            "valid_for_claim": False,
        },
        {
            "snapshot_id": "SNAP2728_1_testing",
            "area": "empirical readiness",
            "status": "NOT_SCOREABLE_YET",
            "summary": "memory residual has explicit rows, but no sourced lambda_gap/J_X/boundary/K_i values",
            "next_pressure_point": "prepare local-bound interface without pretending it is evidence",
            "valid_for_claim": False,
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2728_0_local_bounds",
            "source_table": str(OUTPUTS["residuals"]),
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "local/R10/PPN branches ingest memory residual vector without claim credit",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2728_1_source_weight",
            "source_table": str(OUTPUTS["ejeff"]),
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "source-weight branch receives active E_memory_scalar_generator vector",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2728_2_next_queue",
            "source_table": str(OUTPUTS["next"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues parent signature plus finite residual interface target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    jx: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    activation_blocked = activation[-1]["current_status"] == "RELATIVE_THEOREM_READY_ACTIVATION_FAILS"
    identity_contract = any(row["theorem_id"] == "EID2728_2_zero_theorem" and row["status"] == "RELATIVE_ZERO_THEOREM" for row in identity)
    jx_blocked = jx[-1]["current_status"] == "JX_ZERO_NOT_PROVED"
    boundary_blocked = boundary[-1]["current_status"] == "BOUNDARY_ZERO_NOT_PARENT_DERIVED"
    residual_nonclaim = len(residuals) == 7 and all(row["valid_for_claim"] is False for row in residuals)
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_closed = all(row["opened"] is False and row["valid_for_claim"] is False for row in gates)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0

    csv_parse_details = []
    csv_parse_ok = True
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    rows = [
        {"validation_id": "VAL2728_0_sources", "passed": source_ok, "detail": "all cited source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_1_activation_blocked", "passed": activation_blocked, "detail": "memory no-hair activation remains blocked, not promoted", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_2_identity_contract", "passed": identity_contract, "detail": "relative zero theorem and amplitude law are recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_3_JX_blocked", "passed": jx_blocked, "detail": "J_X=0 is not proved", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_4_boundary_blocked", "passed": boundary_blocked, "detail": "boundary zero package is not parent-derived", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_5_residual_nonclaim", "passed": residual_nonclaim, "detail": "memory residual vector is complete and valid_for_claim=false", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_6_ejeff_nonclaim", "passed": ejeff_nonclaim, "detail": "E_memory_scalar_generator update remains nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_7_claim_gates_false", "passed": gates_closed, "detail": "no memory/local-GR/test/public claim opened", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_8_branch_outputs", "passed": branch_ok, "detail": "local_bounds, source_weight and RAB queue copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2728_9_csv_parse", "passed": csv_parse_ok, "detail": "; ".join(csv_parse_details), "timestamp_utc": ts()},
        {"validation_id": "VAL2728_10_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2728_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2728 keeps memory positive-operator as a relative theorem, blocks theorem-zero, and selects parent-signature plus finite residual interface next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 2728 — Y5 R2/f(R): Memory Positive-Operator Local Silence Or Residual Row Under AX1090 Closure

Status: `Y5_R2FR_2728_memory_positive_operator_relative_theorem_activation_fails_residual_vector_nonclaim`

## Private Verdict

The memory/class scalar route still has a real mathematical spine: if the parent action gives a signed positive operator, zero source, and zero boundary/zero-mode package, then the local memory scalar is forced to vanish by an energy identity rather than by a plateau axiom.

But 2728 does **not** claim that result for MTS. The parent corpus still does not sign the actual `X`, local domain `D`, active `L_X`, positive `A^ij`/`Z_X`, mass/gap, `J_X=0`, boundary zero package, no-tower clause, or local observable couplings. So this checkpoint preserves the theorem as a contract and keeps `E_memory_scalar_generator` alive as a nonclaim residual vector.

Key discipline:
- No memory theorem-zero, no local-GR/Newton/PPN/R10/clock/orbital/WEP pass is opened.
- No plateau axiom is used.
- The next move is not to rerun the same positivity proof; it is to write the exact parent-signature contract and finite residual interface.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "use", "valid_for_claim"])}

## Memory Positive-Operator Activation Audit

{markdown_table(data["activation"], ["audit_id", "gate", "required_to_activate", "current_status", "source_evidence", "consequence", "valid_for_claim"])}

## Energy Identity Theorem Contract

{markdown_table(data["identity"], ["theorem_id", "statement", "status", "required_inputs", "result", "valid_for_claim"])}

## J_X Zero Component Audit

{markdown_table(data["jx"], ["component_id", "component", "zero_condition", "current_status", "failure_mode", "next_action", "valid_for_claim"])}

## Boundary And Zero-Mode Audit

{markdown_table(data["boundary"], ["boundary_id", "gate", "condition", "current_status", "gap", "valid_for_claim"])}

## Memory Residual Rows

{markdown_table(data["residuals"], ["row_id", "quantity", "definition", "feeds", "source_path", "missing", "next_action", "valid_for_claim"])}

## EJeff Update Vector

{markdown_table(data["ejeff"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(data["gates"], ["gate_id", "gate", "status", "reason", "opened", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "consequence", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Project Snapshot

{markdown_table(data["snapshot"], ["snapshot_id", "area", "status", "summary", "next_pressure_point", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is useful but not triumphant. The good news: we do have the right kind of mathematical weapon. Multiply the memory equation by `X`, integrate by parts, and a positive operator with zero source/boundary kills the local memory field cleanly. That is exactly the non-handwave route we want.

The bad news, or really the honest engineering news, is that the parent theory has not yet supplied the signed parts. So the memory branch is not dead; it is now boxed into a precise residual vector. Next we either find/write the exact parent action signature that signs `Z_X`, `M_X^2`, `J_X=0`, and boundary zero, or we move the same quantities into a finite local residual interface for actual tests.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()

    sources = source_rows()
    activation = activation_rows()
    identity = identity_rows()
    jx = jx_rows()
    boundary = boundary_rows()
    residuals = residual_rows()
    ejeff = ejeff_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    snapshot = snapshot_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["activation"], activation)
    write_csv(OUTPUTS["identity"], identity)
    write_csv(OUTPUTS["jx"], jx)
    write_csv(OUTPUTS["boundary"], boundary)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["ejeff"], ejeff)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["snapshot"], snapshot)

    write_csv(BRANCH_OUTPUTS["local_bounds"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, activation, identity, jx, boundary, residuals, ejeff, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "activation": activation,
        "identity": identity,
        "jx": jx,
        "boundary": boundary,
        "residuals": residuals,
        "ejeff": ejeff,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "snapshot": snapshot,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2728 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
