from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1979-Y5-R2FR-M2-Z-domain-theorem-or-first-finite-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1979_VALIDATION.csv"

SOURCES = {
    "1978_doc": {
        "path": ROOT / "1978-Y5-R2FR-memory-mass-gap-and-mL-derivative-bound-pack.md",
        "needles": ["MG1978_5_inverse_bound", "MLE1978_5_mL_derivative", "NEXT1978_0_primary"],
    },
    "1978_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1978_VALIDATION.csv",
        "needles": ["VAL1978_OVERALL", "PASS"],
    },
    "1304_gap_map": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_ZM_POSITIVE_GAP_MAP_NONCLAIM.csv",
        "needles": ["ZPG1304_0_Zm_positive", "ZPG1304_2_mass_gap", "VALUE_MISSING"],
    },
    "1304_operator": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
        "needles": ["OO1304_1_static_local_operator_map", "M_m^2=partial_m^2 V_R"],
    },
    "968_operator_inputs": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
        "needles": ["MOI968_4_mass_gap", "MOI968_6_boundary_data"],
    },
    "1348_memory": {
        "path": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["OPS1348_3_M2_gap", "GATE1348_1_operator_owned"],
    },
    "1977_identity": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1977_MOVING_EXTREMUM_VM_A_IDENTITY.csv",
        "needles": ["ME1977_0_identity", "V_mA=-V_mm m_L,A"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_SOURCE_REGISTER.csv",
    "theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_M2_Z_DOMAIN_THEOREM.csv",
    "proof_steps": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_COERCIVITY_PROOF_STEPS.csv",
    "finite_template": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_FIRST_FINITE_ROW_TEMPLATE.csv",
    "parent_signature": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_PARENT_SIGNATURE_REQUIRED.csv",
    "eh_impact": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_EH_R2FR_IMPACT.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1979_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MEMORY_MASS_GAP_COERCIVITY_THEOREM_1979_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1979_PARENT_MEMORY_POSITIVITY_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(base: dict[str, object]) -> dict[str, str]:
    defaults = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**defaults, **base}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, config in SOURCES.items():
        path = config["path"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing_needles = [needle for needle in config["needles"] if needle not in text]
        rows.append(
            row(
                {
                    "id": f"SRC1979_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "required_needles": "; ".join(config["needles"]),
                    "exists": str(path.exists()).lower(),
                    "needle_status": "PASS" if not missing_needles else "MISSING: " + "; ".join(missing_needles),
                    "role": "source continuity for memory mass-gap, kinetic sign, domain, and 1978 inverse-bound pack",
                }
            )
        )
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    theorem = [
        row(
            {
                "id": "THM1979_0_domain",
                "object": "D_loc",
                "statement": "Choose a compact local domain D_loc with smooth boundary and a fixed admissible boundary class: H_0^1(D_loc), or Neumann with the constant zero mode projected out.",
                "mathematical_status": "STANDARD_ASSUMPTION_NOT_PARENT_SELECTED",
                "claim_blocker": "MISSING_PARENT_SELECTED_DOMAIN_AND_BOUNDARY_CLASS",
                "needed_for": "positive lambda_1(D_loc) and an inverse bound for H_m",
            }
        ),
        row(
            {
                "id": "THM1979_1_lambda1",
                "object": "lambda_1(D_loc)",
                "statement": "For the selected domain and boundary class, require lambda_1(D_loc)>0, where lambda_1 is the first positive eigenvalue of -Delta_h on D_loc.",
                "mathematical_status": "STANDARD_SPECTRAL_FACT_ONCE_DOMAIN_IS_SELECTED",
                "claim_blocker": "MISSING_DOMAIN_GEOMETRY_OR_ZERO_MODE_PROJECTION",
                "needed_for": "G_m=Z_min lambda_1+M2_min-Eta_H",
            }
        ),
        row(
            {
                "id": "THM1979_2_Z_bounds",
                "object": "Z_m",
                "statement": "Assume 0<Z_min<=Z_m(x;X_B)<=Z_bar<infinity on D_loc.",
                "mathematical_status": "PARENT_SIGNATURE_REQUIRED",
                "claim_blocker": "MISSING_PARENT_PROOF_OF_POSITIVE_MEMORY_KINETIC_COEFFICIENT",
                "needed_for": "ellipticity, coercivity, and finite current Schur bound",
            }
        ),
        row(
            {
                "id": "THM1979_3_M2_bounds",
                "object": "M_m^2",
                "statement": "Assume 0<M2_min<=partial_m^2 V_R(m_L;X_B)<=M2_bar<infinity on D_loc.",
                "mathematical_status": "PARENT_SIGNATURE_REQUIRED",
                "claim_blocker": "MISSING_PARENT_PROOF_OF_UNIFORM_MEMORY_MASS_GAP",
                "needed_for": "H_m inverse, moving-extremum bound, and V_mA_bar",
            }
        ),
        row(
            {
                "id": "THM1979_4_eta",
                "object": "Eta_H",
                "statement": "Collect representative, boundary, source, and X_B correction terms into an operator-norm envelope Eta_H.",
                "mathematical_status": "BOOKKEEPING_READY_VALUES_MISSING",
                "claim_blocker": "MISSING_BOUND_FOR_SOURCE_BOUNDARY_XB_CORRECTIONS",
                "needed_for": "strict positivity of corrected local memory Hessian",
            }
        ),
        row(
            {
                "id": "THM1979_5_gap",
                "object": "G_m",
                "statement": "If G_m:=Z_min*lambda_1(D_loc)+M2_min-Eta_H>0, then the corrected local memory operator has a positive spectral floor.",
                "mathematical_status": "THEOREM_READY_PARENT_CONSTANTS_MISSING",
                "claim_blocker": "MISSING_NUMERIC_OR_SYMBOLIC_PARENT_LOWER_BOUNDS",
                "needed_for": "||H_m^{-1}||<=1/G_m",
            }
        ),
        row(
            {
                "id": "THM1979_6_inverse_bound",
                "object": "H_m^{-1}",
                "statement": "For f in L^2(D_loc), the solution u=H_m^{-1}f obeys ||u||_2 <= ||f||_2/G_m, and an H^1 bound follows from the same coercive bilinear form.",
                "mathematical_status": "COERCIVITY_PROOF_CONSTRUCTED_CONDITIONAL",
                "claim_blocker": "NO_CLAIM_UNTIL_THM1979_0_TO_5_ARE_PARENT_SIGNED",
                "needed_for": "Delta c_R2[V_R] and local-GR residual suppression",
            }
        ),
        row(
            {
                "id": "THM1979_7_stability_warning",
                "object": "stable_extremum",
                "statement": "A stable branch extremum gives non-negative second variation at best; it does not by itself give a uniform positive mass gap, because zero modes, criticality, and flat directions can make M2_min vanish.",
                "mathematical_status": "IMPORTANT_REJECTION_OF_TOO_WEAK_SHORTCUT",
                "claim_blocker": "MUST_NOT_SMUGGLE_M2_MIN_GT_0_FROM_STABILITY_WORDING_ALONE",
                "needed_for": "prevents accidental closure axiom masquerading as derivation",
            }
        ),
    ]

    proof_steps = [
        row(
            {
                "id": "PRF1979_0_form",
                "proof_step": "Define the local quadratic form B[u,u]=integral_Dloc Z_m h^{ij} nabla_i u nabla_j u + M_m^2 u^2 dmu_h plus correction form E_H[u,u].",
                "status": "FORMULA_CONSTRUCTED",
                "depends_on": "OO1304_1_static_local_operator_map; THM1979_2_Z_bounds; THM1979_3_M2_bounds",
            }
        ),
        row(
            {
                "id": "PRF1979_1_gradient_floor",
                "proof_step": "Using Z_m>=Z_min and the selected boundary class, integral Z_m|nabla u|^2 >= Z_min*lambda_1(D_loc)*||u||_2^2.",
                "status": "STANDARD_ONCE_DOMAIN_SIGNED",
                "depends_on": "THM1979_0_domain; THM1979_1_lambda1; THM1979_2_Z_bounds",
            }
        ),
        row(
            {
                "id": "PRF1979_2_mass_floor",
                "proof_step": "Using M_m^2>=M2_min, integral M_m^2 u^2 >= M2_min*||u||_2^2.",
                "status": "PARENT_GAP_REQUIRED",
                "depends_on": "THM1979_3_M2_bounds",
            }
        ),
        row(
            {
                "id": "PRF1979_3_corrections",
                "proof_step": "Bound the absolute value of the correction form by Eta_H*||u||_2^2.",
                "status": "CORRECTION_NORM_REQUIRED",
                "depends_on": "THM1979_4_eta",
            }
        ),
        row(
            {
                "id": "PRF1979_4_coercivity",
                "proof_step": "Combine the previous three lines to get B_corrected[u,u] >= G_m*||u||_2^2.",
                "status": "THEOREM_READY_PARENT_CONSTANTS_MISSING",
                "depends_on": "THM1979_5_gap",
            }
        ),
        row(
            {
                "id": "PRF1979_5_inverse",
                "proof_step": "Lax-Milgram/spectral theorem gives a unique inverse on the selected local function space and ||H_m^{-1}||_{L2->L2}<=1/G_m.",
                "status": "CONDITIONAL_PROOF_COMPLETE",
                "depends_on": "PRF1979_4_coercivity",
            }
        ),
    ]

    finite_template = [
        row(
            {
                "id": "FIN1979_0_domain",
                "quantity": "D_loc",
                "placeholder_value": "MISSING_DOMAIN_SELECTION",
                "units": "length domain / coordinate patch",
                "source_or_theorem_required": "parent local-vacuum branch must select D_loc and boundary class",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_1_lambda1",
                "quantity": "lambda_1(D_loc)",
                "placeholder_value": "MISSING_EIGENVALUE_OR_GEOMETRY_BOUND",
                "units": "1/length^2",
                "source_or_theorem_required": "spectral bound for chosen local geometry",
                "status": "MISSING_ARENA_PROJECTION",
            }
        ),
        row(
            {
                "id": "FIN1979_2_Zmin",
                "quantity": "Z_min",
                "placeholder_value": "MISSING_POSITIVE_LOWER_BOUND",
                "units": "memory kinetic normalization",
                "source_or_theorem_required": "parent kinetic-sign lemma",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_3_Zbar",
                "quantity": "Z_bar",
                "placeholder_value": "MISSING_FINITE_UPPER_BOUND",
                "units": "memory kinetic normalization",
                "source_or_theorem_required": "parent regularity or compact-domain bound",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_4_M2min",
                "quantity": "M2_min",
                "placeholder_value": "MISSING_POSITIVE_MEMORY_MASS_GAP",
                "units": "memory potential curvature",
                "source_or_theorem_required": "parent local branch Hessian lower-bound lemma",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_5_M2bar",
                "quantity": "M2_bar",
                "placeholder_value": "MISSING_FINITE_HESSIAN_UPPER_BOUND",
                "units": "memory potential curvature",
                "source_or_theorem_required": "parent regularity/compact-domain bound",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_6_EtaH",
                "quantity": "Eta_H",
                "placeholder_value": "MISSING_CORRECTION_NORM",
                "units": "same spectral units as Z_min lambda_1 + M2_min",
                "source_or_theorem_required": "source/boundary/X_B correction audit",
                "status": "MISSING_PARENT_INPUT",
            }
        ),
        row(
            {
                "id": "FIN1979_7_Gm",
                "quantity": "G_m",
                "placeholder_value": "Z_min*lambda_1(D_loc)+M2_min-Eta_H",
                "units": "spectral floor",
                "source_or_theorem_required": "derived after FIN1979_0_to_6",
                "status": "FORMULA_READY_VALUES_MISSING",
            }
        ),
    ]

    parent_signature = [
        row(
            {
                "id": "SIG1979_0_kinetic",
                "signature_clause": "The parent action must contain a memory kinetic quadratic sector whose pullback to the local branch has positive coefficient Z_m.",
                "why_it_matters": "without positive Z_m the local memory operator is not elliptic",
                "route": "derive from parent action sign or mark as explicit closure",
                "status": "OPEN_PARENT_SIGNATURE",
            }
        ),
        row(
            {
                "id": "SIG1979_1_potential",
                "signature_clause": "The parent action must make the selected local branch a strict non-degenerate minimum in the m direction.",
                "why_it_matters": "this is the real M2_min>0 source; ordinary extremum only gives partial_m V_R=0",
                "route": "derive from branch stability, convexity, or local vacuum selection principle",
                "status": "OPEN_PARENT_SIGNATURE",
            }
        ),
        row(
            {
                "id": "SIG1979_2_zero_modes",
                "signature_clause": "Any exact zero mode from gauge, translation, or memory-shift symmetry must be projected out before claiming lambda_1 or M2_min.",
                "why_it_matters": "zero modes collapse G_m even when the potential looks stable",
                "route": "define quotient/local projection explicitly",
                "status": "OPEN_PROJECTION_SIGNATURE",
            }
        ),
        row(
            {
                "id": "SIG1979_3_corrections",
                "signature_clause": "Boundary, representative, source, and X_B correction terms must be smaller than the positive floor.",
                "why_it_matters": "large corrections can destroy coercivity and revive local R^2/f(R) residuals",
                "route": "bound Eta_H or impose a local silent-boundary branch",
                "status": "OPEN_CORRECTION_BOUND",
            }
        ),
    ]

    eh_impact = [
        row(
            {
                "id": "IMPACT1979_0_leap_forward",
                "result": "The local-GR/R2-fR obstruction is reduced to a precise coercivity contract rather than a vague missing coupling.",
                "impact": "If 1980 signs Z_m>0 and M2_min>0 from the parent action, the V_R contribution becomes quantitatively suppressible.",
                "claim_status": "NO_CLAIM_YET",
            }
        ),
        row(
            {
                "id": "IMPACT1979_1_failure_mode",
                "result": "If M2_min cannot be made positive without hand insertion, the local branch becomes closure-only.",
                "impact": "MTS could still be phenomenological, but the GR-reduction claim would not be derivable in the strong sense the project wants.",
                "claim_status": "RISK_EXPLICIT",
            }
        ),
        row(
            {
                "id": "IMPACT1979_2_next_math",
                "result": "The next derivation is not another scan; it is a parent action signature test.",
                "impact": "Find the memory kinetic sign and strict branch Hessian, or demote this local transition route.",
                "claim_status": "NEXT_GATE_SELECTED",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "id": "GATE1979_0_R2FR",
                "gate": "local EH / R2-fR suppression",
                "status": "BLOCKED",
                "reason": "coercivity theorem is conditional; parent constants missing",
                "required_to_open": "Z_min, M2_min, lambda_1, Eta_H with G_m>0",
            }
        ),
        row(
            {
                "id": "GATE1979_1_local_GR",
                "gate": "derived local GR limit",
                "status": "BLOCKED",
                "reason": "H_m inverse and V_mA_bar not source-backed",
                "required_to_open": "parent memory positivity lemma plus correction norms",
            }
        ),
        row(
            {
                "id": "GATE1979_2_first_finite_row",
                "gate": "first finite nonclaim row",
                "status": "READY_TEMPLATE_ONLY",
                "reason": "all required row slots are named but contain missing placeholders",
                "required_to_open": "real sourced or theorem-backed values",
            }
        ),
    ]

    decision = [
        row(
            {
                "id": "DEC1979_0_result",
                "decision": "CONDITIONAL_THEOREM_CONSTRUCTED",
                "rationale": "The coercivity proof is mathematically standard once the parent supplies Z_m>0, M2_min>0, a domain, and bounded corrections.",
                "next_action": "do not claim; attack the parent signature directly",
            }
        ),
        row(
            {
                "id": "DEC1979_1_rejection",
                "decision": "STABILITY_ALONE_REJECTED",
                "rationale": "stable extremum is too weak because it permits zero curvature and flat directions",
                "next_action": "require strict non-degenerate minimum or explicit closure",
            }
        ),
        row(
            {
                "id": "DEC1979_2_best_next",
                "decision": "PARENT_MEMORY_POSITIVITY_FIRST",
                "rationale": "the coupling problem has collapsed to the sign and strictness of the memory quadratic sector",
                "next_action": "try to prove Z_m>0 and M2_min>0 from the parent action before adding phenomenological bounds",
            }
        ),
    ]

    next_rows = [
        row(
            {
                "id": "NEXT1979_0_primary",
                "status": "selected",
                "target_doc": "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md",
                "target_script": "scripts/Y5_R2FR_parent_memory_positivity_lemma_or_closure_1980.py",
                "task": "derive the parent memory positivity lemma: Z_m>0, strict M2_min>0, zero-mode projection, and Eta_H smallness; otherwise mark local branch closure-only",
                "success_condition": "parent-signed coercivity inputs or explicit demotion",
            }
        )
    ]

    snapshot = [
        row(
            {
                "id": "SNAP1979_0_position",
                "area": "local GR / EH reduction",
                "status": "CLOSER_BUT_NOT_CLAIMED",
                "summary": "1979 supplies the actual operator theorem needed by 1978, but it still depends on a parent memory positivity lemma.",
            }
        ),
        row(
            {
                "id": "SNAP1979_1_missing",
                "area": "core missing item",
                "status": "SHARPENED",
                "summary": "The missing object is now precise: a parent-signed positive elliptic memory operator with a strict mass gap on the selected local domain.",
            }
        ),
        row(
            {
                "id": "SNAP1979_2_not_circling",
                "area": "route discipline",
                "status": "FORWARD_STEP",
                "summary": "This is not another equivalent blocker list; it proves the exact theorem that will make the later local residual estimate legitimate if the parent signs its hypotheses.",
            }
        ),
    ]

    source_weight = [
        row(
            {
                "id": "SW1979_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_theorem",
                "claim_safety": "all public/claim flags false",
                "use": "conditional local coercivity contract for R2-fR/local-GR gate",
            }
        )
    ]

    queue = [
        row(
            {
                "id": "Q1979_0_parent_memory_positivity",
                "quantity": "Z_m>0 and M2_min>0",
                "priority": "highest",
                "why": "without this, H_m^{-1} is not claimable and local GR remains blocked",
                "target": "1980 parent memory positivity lemma",
            }
        ),
        row(
            {
                "id": "Q1979_1_domain_projection",
                "quantity": "D_loc, boundary class, zero-mode projection, lambda_1",
                "priority": "high",
                "why": "domain/projection is needed for the lambda_1 floor",
                "target": "1980 or first finite row",
            }
        ),
    ]

    return {
        "source_register": source_register_rows(),
        "theorem": theorem,
        "proof_steps": proof_steps,
        "finite_template": finite_template,
        "parent_signature": parent_signature,
        "eh_impact": eh_impact,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    for table_rows in tables.values():
        for table_row in table_rows:
            if table_row.get("valid_for_claim") != "false" or table_row.get("public_claim") != "false":
                return False
    return True


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            parsed_rows = list(csv.DictReader(handle))
        if not parsed_rows:
            return False
    return True


def formalization_1979_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1979*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    source_ok = all(
        table_row["exists"] == "true" and table_row["needle_status"] == "PASS"
        for table_row in tables["source_register"]
    )
    theorem_by_id = {table_row["id"]: table_row for table_row in tables["theorem"]}
    proof_by_id = {table_row["id"]: table_row for table_row in tables["proof_steps"]}
    claim_gate_safe = all(table_row["status"] in {"BLOCKED", "READY_TEMPLATE_ONLY"} for table_row in tables["claim_gate"])
    finite_template_safe = all(
        table_row["valid_for_claim"] == "false"
        and ("MISSING" in table_row["status"] or table_row["id"] == "FIN1979_7_Gm")
        for table_row in tables["finite_template"]
    )
    next_selected = tables["next"][0]["target_doc"] == "1980-Y5-R2FR-parent-memory-positivity-lemma-or-closure.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1979_artifact_count()

    validation_specs = [
        ("VAL1979_00_sources", source_ok, "all source paths exist and continuity needles found"),
        (
            "VAL1979_01_gap_theorem",
            theorem_by_id["THM1979_5_gap"]["mathematical_status"] == "THEOREM_READY_PARENT_CONSTANTS_MISSING",
            "G_m theorem stated with missing parent constants",
        ),
        (
            "VAL1979_02_inverse_proof",
            proof_by_id["PRF1979_5_inverse"]["status"] == "CONDITIONAL_PROOF_COMPLETE",
            "conditional inverse proof completed",
        ),
        (
            "VAL1979_03_stability_shortcut_rejected",
            theorem_by_id["THM1979_7_stability_warning"]["mathematical_status"] == "IMPORTANT_REJECTION_OF_TOO_WEAK_SHORTCUT",
            "stable extremum alone does not imply strict gap",
        ),
        ("VAL1979_04_finite_template", finite_template_safe, "finite row template remains nonclaim and missing-valued"),
        ("VAL1979_05_claim_gates", claim_gate_safe, "all claim gates remain blocked or template-only"),
        ("VAL1979_06_decision", tables["decision"][-1]["decision"] == "PARENT_MEMORY_POSITIVITY_FIRST", "decision selects parent positivity"),
        ("VAL1979_07_next_target", next_selected, "1980 target selected"),
        ("VAL1979_08_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1979_09_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1979_10_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1979_11_formalization_untouched", formalization_count == 0, f"formalization_1979_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in validation_specs
    ]
    rows.append(
        {
            "validation_id": "VAL1979_OVERALL",
            "status": "PASS" if all(row_data["status"] == "PASS" for row_data in rows) else "FAIL",
            "detail": "1979 conditional memory coercivity theorem pack",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for table_row in rows:
        escaped = [table_row.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def proof_text() -> str:
    return "\n".join(
        [
            "## Coercivity Proof",
            "",
            "Let `H_m` be the local memory fluctuation operator from the 1304 operator map, restricted to the selected local function space. For an admissible fluctuation `u`, define the corrected quadratic form",
            "",
            "`B_H[u,u] = integral_Dloc Z_m h^{ij} nabla_i u nabla_j u dmu_h + integral_Dloc M_m^2 u^2 dmu_h + E_H[u,u]`.",
            "",
            "If `Z_m>=Z_min>0`, `M_m^2>=M2_min>0`, the selected domain/projection gives `integral |nabla u|^2 >= lambda_1(D_loc)||u||_2^2`, and `|E_H[u,u]|<=Eta_H||u||_2^2`, then",
            "",
            "`B_H[u,u] >= (Z_min lambda_1(D_loc)+M2_min-Eta_H)||u||_2^2 = G_m||u||_2^2`.",
            "",
            "Therefore, when `G_m>0`, the local memory operator is coercive and the spectral/Lax-Milgram inverse obeys",
            "",
            "`||H_m^{-1}||_{L2->L2} <= 1/G_m`.",
            "",
            "This is a real theorem, but not yet a physics claim: the parent action still has to sign `Z_m`, the strict branch Hessian `M2_min`, the domain/projection, and the correction envelope.",
            "",
        ]
    )


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("M2 Z Domain Theorem", tables["theorem"]),
        ("Coercivity Proof Steps", tables["proof_steps"]),
        ("First Finite Row Template", tables["finite_template"]),
        ("Parent Signature Required", tables["parent_signature"]),
        ("EH R2FR Impact", tables["eh_impact"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1979 Y5 R2FR: M2 Z Domain Theorem Or First Finite Row",
        "",
        "Private checkpoint. This is the clean leap after 1978: prove the exact local memory coercivity theorem needed for the local EH/R2-fR gate, while refusing to pretend the parent-signature inputs are already known.",
        "",
        "Verdict: the operator step now has a conditional proof. If the parent action signs `Z_m>0`, a strict memory gap `M2_min>0`, a selected local domain/projection with `lambda_1>0`, and small corrections `Eta_H`, then `H_m^{-1}` is bounded and the `V_R` Schur contribution can be made quantitative. Stable extremum alone is rejected as too weak because it permits zero modes and flat directions.",
        "",
        "No local-GR, EH, R10, PPN, clock, orbital, or public claim follows from 1979.",
        "",
        proof_text(),
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1979_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
