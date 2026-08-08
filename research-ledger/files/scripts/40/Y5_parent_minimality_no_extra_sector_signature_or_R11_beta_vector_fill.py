from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1586"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1586-Y5-parent-minimality-no-extra-sector-signature-or-R11-beta-vector-fill.md"

SOURCE_FILES = {
    "1585_doc": ROOT / "1585-Y5-EH-source-normalized-parent-action-owner-or-beta-residual-ledger.md",
    "1585_validation": OUT / "P8_Y5_BRR545_1585_VALIDATION.csv",
    "1585_beta_residual": OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv",
    "439_doc": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "964_doc": ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
    "964_minimality": OUT / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
    "964_countermodels": OUT / "P8_Y5_R10_964_COUNTERMODEL_LEDGER.csv",
    "423_minimality": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
    "413_marker": ROOT / "413-no-marker-parent-action-theorem-attempt.md",
    "1512_premises": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "local_eh_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "r11_status": OUT / "R11_EXECUTABLE_VECTOR_STATUS.csv",
    "r11_skeleton": OUT / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
    "r11_executable": OUT / "R11_nonEH_operator_vector_executable.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1585_doc": ["NEXT_1586_PARENT_MINIMALITY_NO_EXTRA_SECTOR_SIGNATURE_OR_R11_BETA_VECTOR_FILL", "BRL1585_1_delta_beta_R11"],
    "1585_validation": ["VAL1585_OVERALL", "PASS"],
    "1585_beta_residual": ["BRL1585_1_delta_beta_R11", "MISSING_R11_COEFFICIENT_VECTOR_OR_EH_NOHAIR"],
    "439_doc": ["P3_no_extra_local_propagating_fields", "P6_second_order_metric_equations"],
    "440_doc": ["If any sector or operator coefficient remains", "retained_R11_vector"],
    "964_doc": ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "Countermodels like"],
    "964_minimality": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
    "964_countermodels": ["CM964_0_EH_plus_R2", "CM964_3_nonlocal_memory_kernel"],
    "423_minimality": ["parent_universal_property_derived", "fail", "material_marker_extension_blocked"],
    "413_marker": ["material_marker_extension_blocked", "fail", "local_GR_promoted"],
    "1512_premises": ["PRE1512_4_no_extra_fields", "ACTIVE_PRIMARY_OBSTRUCTION", "PRE1512_6_parent_minimality", "THEOREM_NOT_PROVEN"],
    "local_eh_audit": ["R2_fR_scalar_mode", "source_normalization_operator"],
    "r11_status": ["template_only", "valid_for_claim"],
    "r11_skeleton": ["MTS_source_normalized_Newton_branch", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"],
    "r11_executable": ["MISSING_DOMAIN_VECTOR_ABSENCE_THEOREM_OR_NUMERIC_COEFFICIENTS", "0_IF_PARENT_OWNS_METRIC_INDEPENDENT_TOPOLOGICAL_P_D_ELSE_MISSING_PROJECTOR_STRESS_COEFFICIENT"],
    "r11_beta_vector": ["B530_1_R2_fR_scalar", "B530_11_readout_frame"],
    "local_bounds": ["Will_2014_PPN_beta_table", "beta_minus_1", "7.8e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1586_SOURCE_REGISTER.csv"
MINIMALITY_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1586_MINIMALITY_SIGNATURE_ATTEMPT.csv"
COUNTERMODEL_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1586_COUNTERMODEL_SURVIVAL_LEDGER.csv"
R11_BETA_FILL = OUT / "P8_Y5_PARENT_QLOC_1586_R11_BETA_VECTOR_FILL_REQUIREMENTS.csv"
BETA_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1586_BETA_VECTOR_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1586_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1586_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1586_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1586_VALIDATION.csv"

COPY_TARGETS = {
    MINIMALITY_ATTEMPT: [
        QUARANTINE / "MINIMALITY_SIGNATURE_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "minimality_signature_attempt_nonclaim_1586.csv",
    ],
    COUNTERMODEL_LEDGER: [
        QUARANTINE / "COUNTERMODEL_SURVIVAL_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "countermodel_survival_ledger_nonclaim_1586.csv",
    ],
    R11_BETA_FILL: [
        QUARANTINE / "R11_BETA_VECTOR_FILL_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R11_beta_vector_fill_requirements_nonclaim_1586.csv",
    ],
    BETA_RUNNER: [
        QUARANTINE / "BETA_VECTOR_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "beta_vector_runner_nonclaim_1586.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "minimality_or_R11_beta_fill_decision_nonclaim_1586.csv",
    ],
}


R11_AFFECTED_ROWS = {
    "source_normalization_operator": "R1;R4;R9;R10;R11",
    "R2_fR_scalar_mode": "R3;R4;R10;R11",
    "Ricci_Weyl_squared": "R3;R8;R11",
    "scalar_tensor_class_metric": "R2;R3;R4;R9;R10;R11",
    "boundary_topological_terms": "R3;R4;R7;R8;R11",
    "projector_domain_stress": "R5;R6;R7;R8;R11",
    "nonlocal_memory_kernel": "R7;R9;R10;R11",
    "q_loc_Gamma_Khat": "R3;R4;R7;R11",
    "torsion_nonmetricity": "R0;R1;R2;R11",
    "vector_preferred_frame": "R5;R6;R7;R8;R11",
    "bulk_X_force_law": "R1;R3;R4;R10;R11",
    "observed_readout_frame": "R0;R2;R3;R4;R11",
}

R11_CURRENT_STATUS = {
    "source_normalization_operator": "MISSING_A_B_SOURCE_EQUATION_OR_MEASURED_GM_OPERATOR_ZERO",
    "R2_fR_scalar_mode": "MISSING_C_R2_C_FR_ZERO_OR_FINITE_SCALAR_MAP",
    "Ricci_Weyl_squared": "MISSING_CURVATURE_SQUARED_ZERO_OR_WEAK_FIELD_MAP",
    "scalar_tensor_class_metric": "MISSING_SCALAR_CLASS_NOHAIR_OR_COUPLING_MAP",
    "boundary_topological_terms": "MISSING_BOUNDARY_TOPOLOGICAL_NOFLUX_OR_COEFFICIENT",
    "projector_domain_stress": "MISSING_PROJECTOR_DOMAIN_STRESS_ZERO_OR_COEFFICIENT",
    "nonlocal_memory_kernel": "MISSING_COMPACT_LOCAL_KERNEL_SILENCE_OR_KERNEL_NORM",
    "q_loc_Gamma_Khat": "PROVISIONAL_QLOC_U2_BUDGET_NOT_PARENT_SIGNED",
    "torsion_nonmetricity": "MISSING_LEVI_CIVITA_OR_CONNECTION_RESIDUAL_MAP",
    "vector_preferred_frame": "MISSING_VECTOR_ABSENCE_OR_PREFERRED_FRAME_MAP",
    "bulk_X_force_law": "MISSING_BULK_SOURCE_FREE_NOHAIR_OR_ALPHA_LAMBDA_MAP",
    "observed_readout_frame": "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1586_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "parent minimality/no-extra-sector signature attempt or R11 beta vector fill",
                **flags(),
            }
        )
    return rows


def minimality_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MIN1586_0_object_language",
            "primitive parent object language",
            "Arg(S_parent) is generated only by motion/time/space, observed metric/coframe, matter representations and universal constants",
            "would exclude extra local scalar/vector/domain/marker targets before variation",
            "TARGET_RESTATED_NOT_DERIVED",
            "423 and 964 both keep the universal-property/minimal quotient theorem open",
        ),
        (
            "MIN1586_1_no_marker_no_extension",
            "no natural marker or quotient extension",
            "no nonconstant natural marker functor, class scalar, material label or hidden-visible coefficient morphism exists on the local branch",
            "would kill marker-prefactor F(sigma)R and species/source-only couplings",
            "NOT_DERIVED",
            "co-moving markers and invariant scalars remain legal countermodels",
        ),
        (
            "MIN1586_2_no_integrated_out_tower",
            "no integrated-out higher-curvature tower",
            "solving hidden/auxiliary/projector/memory sectors cannot generate f(R), R^2, Ricci^2, Weyl^2, nonlocal kernels or finite scalar poles",
            "would protect the EH-only second-order operator",
            "NOT_DERIVED",
            "440 and 964 show auxiliary scalar and nonlocal countermodels remain legal",
        ),
        (
            "MIN1586_3_no_extra_stress_carriers",
            "no extra local propagating stress/source carriers",
            "scalar, vector, bulk-X, projector/domain, torsion, nonmetricity and memory sectors are absent, gauge/topological, harmless or explicitly residualized",
            "would remove non-EH beta leakage at source",
            "ACTIVE_PRIMARY_OBSTRUCTION",
            "1512 PRE1512_4 remains active and R11 rows are template-only",
        ),
        (
            "MIN1586_4_second_order_filter",
            "metric-only second-order exterior",
            "local tested exterior equations are second order in the observed metric/coframe and all higher derivative/nonlocal terms are theorem-zero or bounded",
            "would activate the Lovelock/EH selector route",
            "CENTRAL_BLOCKER_NOT_DERIVED",
            "R2/fR, Ricci/Weyl and nonlocal rows remain legal",
        ),
        (
            "MIN1586_5_verdict",
            "parent minimality/no-extra-sector signature",
            "MIN1586_0 through MIN1586_4 all parent-signed from MTS primitives",
            "would set the R11 beta vector to theorem-zero except retained harmless/topological rows",
            "FAIL_CURRENT_CLAIM_MINIMALITY_NOT_DERIVED",
            "minimality is a clean contract, not a current theorem",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "minimality_id": minimality_id,
            "theorem_piece": theorem_piece,
            "required_statement": required_statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for minimality_id, theorem_piece, required_statement, effect_if_signed, status, blocking_gap in rows
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM1586_0_EH_plus_R2", "S_EH + epsilon int sqrt(-g) R^2", "local 4D diffeo-invariant and Ward-compatible without no-higher-derivative theorem", "scalar trace pole/fourth-order response shifts gamma/beta/R10", "no-higher-derivative minimality or R2/fR coefficient row"),
        ("CM1586_1_auxiliary_scalar_integrated_out", "S_EH + int sqrt(-g)(-M^2 phi^2/2 + beta phi R)", "auxiliary scalar can look harmless before solving E_phi=0", "integrating out phi generates beta^2 R^2/(2M^2)", "no integrated-out tower theorem or finite scalar map"),
        ("CM1586_2_marker_prefactor", "int sqrt(-g) F(sigma_marker) R", "covariant marker/class scalar is legal unless no-extension is proven", "scalar-tensor/f(R)-like beta, clock, WEP and fifth-force leakage", "primitive no-marker/no-extension theorem"),
        ("CM1586_3_vector_domain", "domain/aether/vector selector stress", "covariant vector/domain structures can be added unless object-language excludes them", "preferred-frame alpha_i/xi and possible beta cross-terms", "vector absence/alignment theorem or preferred-frame coefficient map"),
        ("CM1586_4_torsion_nonmetricity", "independent connection/torsion/nonmetricity sector", "metric compatibility is not automatic before connection variation", "WEP/light/clock/source readout and possible beta leakage", "Levi-Civita compatibility theorem or connection residual map"),
        ("CM1586_5_nonlocal_memory", "R Box^{-1} R or compact history kernel", "memory language can remain covariant and source-owned", "finite-range/time-drift/source-normalization and beta tails", "compact-local kernel silence or kernel norm map"),
        ("CM1586_6_source_normalization_operator", "mu_extra or domain-dependent G_eff/M_eff operator", "measured GM is not fixed by EH operator alone", "source-denominator and beta source residuals", "source-normalization theorem or epsilon_SN residual score"),
        ("CM1586_7_projector_domain_stress", "metric-dependent projector/domain stress", "projector can vary with metric/domain unless topological independence is proven", "preferred-location/frame and beta stress residuals", "metric-independent topological projector or stress coefficient row"),
        ("CM1586_8_Gauss_Bonnet_safe_case", "4D exact Gauss-Bonnet/topological boundary term", "can be harmless only with exact combination and boundary flux control", "not a generic R11 rescue; boundary hair can still leak", "topological exactness plus boundary no-flux theorem"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_legal_without_gate": why_legal_without_gate,
            "damage": damage,
            "gate_that_kills_it": gate_that_kills_it,
            "currently_killed": False,
            **flags(),
        }
        for countermodel_id, countermodel, why_legal_without_gate, damage, gate_that_kills_it in rows
    ]


def r11_beta_fill_rows() -> list[dict[str, Any]]:
    beta_rows = read_csv(SOURCE_FILES["r11_beta_vector"])
    rows = []
    for beta_row in beta_rows:
        operator_family = beta_row["operator_family"]
        component = beta_row["component"]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "fill_id": f"FILL1586_{len(rows)}_{component}",
                "source_component_id": beta_row["component_id"],
                "operator_family": operator_family,
                "component": component,
                "formal_map": beta_row["formal_map"],
                "zero_or_safe_condition": beta_row["zero_or_safe_condition"],
                "affected_rows": R11_AFFECTED_ROWS.get(operator_family, "R11"),
                "required_real_input": "theorem-zero parent signature or numeric coefficient with units, normalization, weak-field beta map and source path",
                "current_status": R11_CURRENT_STATUS.get(operator_family, "MISSING_THEOREM_OR_NUMERIC_INPUT"),
                "bound_or_target": "abs(component) included in Delta_beta_total_abs <= 7.8e-05 with no cancellation",
                "valid_for_claim": False,
                "claim_allowed": False,
                "parent_signed": False,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
            }
        )
    return rows


def beta_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1586_0_minimality_zero", "set R11 beta vector to zero by parent minimality", "REFUSE_UNSIGNED_MINIMALITY", "minimality/no-extra-sector signature is not derived"),
        ("RUN1586_1_R11_beta_score", "score R11 beta vector against beta bound", "NOT_RUN_COMPONENTS_MISSING", "R11 components are theorem/numeric-input templates, not valid predictions"),
        ("RUN1586_2_GB_shortcut", "use Gauss-Bonnet/topological safe case to silence all R11 rows", "REFUSE_OVERBROAD_TOPOLOGY", "topological safe case does not kill R2/fR, scalar, vector, source, connection, q_loc or readout rows"),
        ("RUN1586_3_EH_mass_family", "use conditional EH mass family as proof of no R11 beta leakage", "REFUSE_REFERENCE_PROMOTION", "EH mass family needs R11 silence as a premise, not a substitute"),
        ("RUN1586_4_beta_total", "run Delta_beta_total_abs", "NOT_RUN_COMPONENTS_MISSING", "delta_beta_source/R11/q_loc/boundary/readout/conservation/source-denominator rows are not filled"),
        ("RUN1586_5_local_gr", "claim local GR reduction", "BLOCKED_NO_CLAIM", "minimality, R11 beta vector, source normalization, common matter and conservation remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            **flags(),
        }
        for runner_id, case, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1586_0_minimality", "parent minimality/no-extra-sector theorem", "BLOCKED_NO_CLAIM", "universal property, no-marker, no integrated-out tower and no-extra-stress clauses are unsigned"),
        ("GATE1586_1_R11_zero", "R11 beta vector theorem-zero", "BLOCKED_NO_CLAIM", "minimality theorem is not derived and R11 coefficients are not filled"),
        ("GATE1586_2_beta_score", "beta residual score", "BLOCKED_NO_CLAIM", "R11 and other beta residual components are missing"),
        ("GATE1586_3_EH_operator", "EH-only local operator", "BLOCKED_NO_CLAIM", "R11/non-EH operator family rows remain active"),
        ("GATE1586_4_local_gr", "derived local GR branch", "BLOCKED_NO_CLAIM", "local GR requires EH/source/matter/conservation/beta gates under one parent action"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1586_0_derivation_attempt",
            "MINIMALITY_SIGNATURE_NOT_DERIVED",
            "current evidence from 423/413/440/964/1512 leaves legal marker, higher-curvature, vector, connection, nonlocal and source-normalization countermodels",
            "do not set R11 beta vector to zero by taste",
        ),
        (
            "DEC1586_1_fallback",
            "R11_BETA_VECTOR_FILL_REQUIREMENTS_ACTIVE",
            "the executable beta vector already lists each component; 1586 now turns it into fill requirements with explicit no-cancellation beta target",
            "each component needs theorem-zero or numeric coefficient/source path before scoring",
        ),
        (
            "DEC1586_2_priority",
            "START_WITH_HIGHER_CURVATURE_AND_SCALAR_SOURCE_ROWS",
            "R2/fR and Ricci/Weyl directly violate the second-order EH selector, while scalar/class and source normalization can feed beta and fifth-force tests",
            "attack the highest-leverage R11 rows first",
        ),
        (
            "DEC1586_3_next",
            "NEXT_1587_R11_BETA_VECTOR_FIRST_COMPONENT_FILL_R2FR_RICCIWEYL_OR_NOHAIR",
            "the next useful step is to fill or theorem-zero the first R11 beta components rather than repeating minimality as an assumption",
            "derive no-higher-curvature/no-scalar leakage first; if unsigned, create source-backed coefficient rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md",
            "script": "scripts/Y5_R11_beta_vector_first_component_fill_R2FR_RicciWeyl_or_nohair.py",
            "objective": "try to derive no R2/fR and no Ricci/Weyl beta leakage from the parent branch; if that fails, create first source-backed nonclaim coefficient rows for the R11 beta vector",
            "do_not": "do not use minimality, Gauss-Bonnet, EH reference family, or first-order Newton as a theorem-zero substitute for R11 beta components",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1586_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1586" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    minimality = read_csv(MINIMALITY_ATTEMPT)
    countermodels = read_csv(COUNTERMODEL_LEDGER)
    fills = read_csv(R11_BETA_FILL)
    runner = read_csv(BETA_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    beta_components = read_csv(SOURCE_FILES["r11_beta_vector"])
    required_components = {row["component"] for row in beta_components}
    required_claims = {
        "parent minimality/no-extra-sector theorem",
        "R11 beta vector theorem-zero",
        "beta residual score",
        "EH-only local operator",
        "derived local GR branch",
    }
    checks = [
        ("VAL1586_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1586 source paths exist"),
        ("VAL1586_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1586 source needles found"),
        (
            "VAL1586_2_minimality_fails_open",
            any(row["minimality_id"] == "MIN1586_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_MINIMALITY_NOT_DERIVED" for row in minimality),
            "minimality/no-extra-sector route is attempted but not promoted",
        ),
        (
            "VAL1586_3_countermodels_live",
            len(countermodels) >= 8 and all(row["currently_killed"] == "False" for row in countermodels),
            "countermodel ledger keeps non-EH leakage live unless a gate kills it",
        ),
        (
            "VAL1586_4_R11_fill_schema",
            {row["component"] for row in fills} == required_components
            and all(row["valid_for_claim"] == "False" and row["current_status"].startswith(("MISSING", "PROVISIONAL")) for row in fills),
            "R11 beta vector fill requirements cover every beta component as nonclaim rows",
        ),
        (
            "VAL1586_5_runner_blocks",
            all(row["can_score"] == "False" for row in runner)
            and any(row["runner_id"] == "RUN1586_5_local_gr" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks minimality shortcut, beta scoring and local GR",
        ),
        (
            "VAL1586_6_claim_gates_closed",
            {row["claim"] for row in gates} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all 1586 claim gates remain closed",
        ),
        (
            "VAL1586_7_decision_next",
            any(row["decision"] == "NEXT_1587_R11_BETA_VECTOR_FIRST_COMPONENT_FILL_R2FR_RICCIWEYL_OR_NOHAIR" for row in decisions),
            "decision selects first R11 beta component fill/nohair target",
        ),
        ("VAL1586_8_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1586 CSVs parse cleanly"),
        ("VAL1586_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1586_10_no_raw_accepted", not has_1586_rows(RAB_RAW) and not has_1586_rows(RAB_ACCEPTED), "no 1586 rows written to raw/accepted finite directories"),
        ("VAL1586_11_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1586_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1586_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1586 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1586_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1586 parent minimality/no-extra-sector signature or R11 beta vector fill validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    minimality: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1586 - Parent Minimality No-Extra-Sector Signature Or R11 Beta Vector Fill",
                "## Verdict\n"
                "- The derivation-first route was tested: parent minimality/no-extra-sector would be powerful enough to kill the non-EH R11 beta vector, but the current corpus does not derive it.\n"
                "- `minimality` is therefore not allowed to function as a magic word: marker, higher-curvature, vector/domain, torsion/nonmetricity, nonlocal, source-normalization and projector countermodels remain live until killed by theorem or coefficient rows.\n"
                "- The fallback is now explicit: every R11 beta component must be theorem-zero or filled with numeric/source-backed coefficient, units, normalization and weak-field beta map before beta can be scored.\n"
                "- The no-cancellation target remains `Delta_beta_total_abs <= 7.8e-05`, but the runner does not score because the component rows are missing.\n"
                "- No beta, EH, Newton, PPN, local-GR, R10, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Minimality Signature Attempt",
                md_table(minimality, ["minimality_id", "theorem_piece", "required_statement", "effect_if_signed", "status", "blocking_gap"]),
                "## Countermodel Survival Ledger",
                md_table(countermodels, ["countermodel_id", "countermodel", "why_legal_without_gate", "damage", "gate_that_kills_it", "currently_killed"]),
                "## R11 Beta Vector Fill Requirements",
                md_table(fills, ["fill_id", "source_component_id", "operator_family", "component", "current_status", "affected_rows", "bound_or_target"]),
                "## Beta Vector Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    minimality = minimality_attempt_rows()
    countermodels = countermodel_ledger_rows()
    fills = r11_beta_fill_rows()
    runner = beta_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        MINIMALITY_ATTEMPT,
        COUNTERMODEL_LEDGER,
        R11_BETA_FILL,
        BETA_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(MINIMALITY_ATTEMPT, minimality)
    write_csv(COUNTERMODEL_LEDGER, countermodels)
    write_csv(R11_BETA_FILL, fills)
    write_csv(BETA_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, minimality, countermodels, fills, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
