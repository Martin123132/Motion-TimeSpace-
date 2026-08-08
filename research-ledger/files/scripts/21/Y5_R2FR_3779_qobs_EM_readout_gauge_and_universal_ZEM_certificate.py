import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3779"
BRANCH = "MTS_R2FR_Y5_QOBS_EM_READOUT_GAUGE_AND_UNIVERSAL_ZEM_CERTIFICATE_3779"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3779_SOURCE_REGISTER.csv",
    "certificate_theorem": RESIDUALS / "P8_Y5_R2FR_3779_QOBS_EM_CERTIFICATE_THEOREM.csv",
    "qobs_extension": RESIDUALS / "P8_Y5_R2FR_3779_QOBS_EM_EXTENSION_MAP.csv",
    "certificate_audit": RESIDUALS / "P8_Y5_R2FR_3779_EM_CERTIFICATE_AUDIT.csv",
    "residual_coefficients": RESIDUALS / "P8_Y5_R2FR_3779_EM_QOBS_ZEM_RESIDUAL_COEFFICIENTS.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_3779_EM_QOBS_ZEM_BOUND_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3779_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3779_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3779_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3779_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3779_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3779_0_3778_doc": PCW / "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md",
        "SRC3779_1_3778_descent": RESIDUALS / "P8_Y5_R2FR_3778_MAXWELL_HILBERT_DESCENT_THEOREM.csv",
        "SRC3779_2_3778_clause_audit": RESIDUALS / "P8_Y5_R2FR_3778_MTS_EM_DESCENT_CLAUSE_AUDIT.csv",
        "SRC3779_3_3778_bounds": RESIDUALS / "P8_Y5_R2FR_3778_EM_DESCENT_AND_TAIL_BOUND_VECTOR.csv",
        "SRC3779_4_3765_qobs_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
        "SRC3779_5_3765_sector_residuals": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
        "SRC3779_6_3766_kernel_theorem": RESIDUALS / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv",
        "SRC3779_7_3768_kappa_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
        "SRC3779_8_3769_shadow_budget": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
        "SRC3779_9_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3779_10_3771_theta_theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
        "SRC3779_11_3760_em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3779_12_3759_wep_eval": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3779_13_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3779 q_obs EM readout/gauge and universal Z_EM certificate input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def imported_bounds() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3779_12_3759_wep_eval"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3779_13_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3779_13_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3779_7_3768_kappa_budget"], "budget_id", "KBB3768_0_Gdot_total")
    return {"wep": wep["bound_value"], "gamma": gamma["bound_value"], "beta": beta["bound_value"], "gdot": gdot["bound_value"]}


def certificate_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "QEC3779_0_qobs_em_readout",
            "Define an EM readout functor F_EM over q_obs only if A_obs and F_obs=dA_obs are functions of q_obs plus U(1) gauge orbit data, not representative MTS fibre data.",
            "Then sector EM readout factors as q_EM=F_EM o q_obs up to gauge, closing Delta q_EM at the readout level.",
            "EXACT_CONDITIONAL_QOBS_EM_READOUT_THEOREM",
        ),
        (
            "QEC3779_1_vertical_gauge_basicness",
            "For every vertical E_A in ker(Dq_obs), EM is q_obs-basic if Lie_EA A_obs=d lambda_A and hence Lie_EA F_obs=0.",
            "Gauge variation of A is harmless; any vertical change of F is physical EM leakage.",
            "EXACT_VERTICAL_GAUGE_CRITERION",
        ),
        (
            "QEC3779_2_gauge_current_certificate",
            "If the parent action is invariant under A -> A+d lambda and charged matter current descends through the same source action, the Noether/Ward identity gives nabla_a J^a=0 and internal EM/matter exchange.",
            "This is the q_obs-owned route to U(1) gauge redundancy and source-current conservation.",
            "EXACT_CONDITIONAL_GAUGE_WARD_THEOREM",
        ),
        (
            "QEC3779_3_universal_ZEM_zero",
            "Define beta_Z,A := Lie_EA ln Z_EM. Universal EM normalization is parent-signed only if beta_Z,A=0 for all q_obs-vertical directions, or Z_EM is superselected.",
            "This is the exact coefficient that would otherwise feed WEP, clocks, Gdot, PPN, and material response.",
            "EXACT_ZEM_SUPERSELECTION_CRITERION",
        ),
        (
            "QEC3779_4_same_metric_certificate",
            "EM uses the same local metric/coframe as matter/source only if its kinetic term contracts F_ab F_cd with g_eff^{ac}g_eff^{bd} from q_obs and no disformal/birefringent shadow remains.",
            "This is the local light-cone/gamma branch of the EM certificate.",
            "EXACT_NO_EM_SHADOW_METRIC_CRITERION",
        ),
        (
            "QEC3779_5_certificate_promotion",
            "If QEC3779_0 through QEC3779_4 hold and extra EM modes/tail-domain rows are zero or bounded, the 3778 Maxwell Hilbert descent route can use EM as ordinary total Hilbert stress.",
            "This promotes EM from an explicit mu_extra owner to the EM part of Pi_M_total, still conditional on parent signatures.",
            "EXACT_CONDITIONAL_EM_CERTIFICATE_PROMOTION",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation_or_meaning": derivation_or_meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, derivation_or_meaning, status in rows
    ]


def qobs_extension_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "QEX3779_0_EM_bundle_class",
            "EM bundle/gauge orbit class",
            "[A_obs]_{U(1)} over the same observed spacetime/coframe in q_obs",
            "must be added as a q_obs-owned readout class or recovered functorially from existing source fields",
            "MISSING_PARENT_EM_BUNDLE_CLASS",
        ),
        (
            "QEX3779_1_F_field_class",
            "field-strength class",
            "F_obs=dA_obs invariant under A_obs -> A_obs+d lambda",
            "physical stress depends on F_obs, not on representative A_obs",
            "MISSING_PARENT_F_BASICNESS_CERTIFICATE",
        ),
        (
            "QEX3779_2_charge_current_class",
            "descended current class",
            "J_obs^a from the same q_obs source action and same charged matter fields",
            "needed for Maxwell equations and Ward exchange cancellation",
            "MISSING_DESCENDED_CHARGED_CURRENT_CLASS",
        ),
        (
            "QEX3779_3_ZEM_class",
            "EM normalization class",
            "Z_EM in theta_univ or superselected constants",
            "must not depend on species, material, frame, environment, or vertical representative",
            "MISSING_ZEM_QOBS_OR_SUPERSELECTION_CLASS",
        ),
        (
            "QEX3779_4_EM_metric_class",
            "EM metric/coframe class",
            "g_EM=g_eff from q_obs",
            "excludes disformal/birefringent EM shadow metric",
            "MISSING_EM_SAME_METRIC_CERTIFICATE",
        ),
        (
            "QEX3779_5_tail_domain_class",
            "EM field-support domain class",
            "source_domain_id includes declared EM support/tail/flux convention",
            "needed so Pi_M_total knows what EM stress is included vs bounded",
            "MISSING_EM_TAIL_DOMAIN_QOBS_CLASS",
        ),
    ]
    return [
        {
            **base(timestamp),
            "extension_id": extension_id,
            "object": object_name,
            "qobs_form": qobs_form,
            "role": role,
            "current_status": current_status,
            "claim_allowed": False,
        }
        for extension_id, object_name, qobs_form, role, current_status in rows
    ]


def certificate_audit_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("ECA3779_0_qobs_A", "A_obs gauge orbit is q_obs-owned", "MISSING_PARENT_EM_BUNDLE_CLASS", False, "Delta q_EM remains live"),
        ("ECA3779_1_F_basic", "F_obs is vertical-invariant: Lie_EA F_obs=0", "MISSING_PARENT_F_BASICNESS_CERTIFICATE", False, "vertical EM field leakage remains live"),
        ("ECA3779_2_gauge_redundancy", "vertical A variation is pure gauge: Lie_EA A=d lambda_A", "MISSING_VERTICAL_GAUGE_ORBIT_PROOF", False, "longitudinal/non-gauge source leakage remains live"),
        ("ECA3779_3_current_conservation", "U(1) Ward identity gives nabla_a J^a=0 in the local branch", "MISSING_PARENT_GAUGE_INVARIANCE_CERTIFICATE", False, "charged source exchange is not internally certified"),
        ("ECA3779_4_same_source_current", "charged matter current descends from the same S_src", "MISSING_SAME_ACTION_CHARGED_MATTER_CURRENT", False, "Lorentz exchange may be external"),
        ("ECA3779_5_ZEM_basic", "beta_Z,A=Lie_EA ln Z_EM=0 or Z_EM is superselected", "MISSING_UNIVERSAL_ZEM_SUPERSELECTION", False, "EM normalization residual remains live"),
        ("ECA3779_6_same_metric", "g_EM equals g_eff from q_obs with no birefringent/disformal residue", "MISSING_EM_SAME_METRIC_CERTIFICATE", False, "PPN/light/frame residual remains live"),
        ("ECA3779_7_tail_domain", "EM support/tail/flux convention is q_obs-owned or bounded", "MISSING_EM_TAIL_DOMAIN_QOBS_CLASS", False, "field-domain residual remains live"),
        ("ECA3779_8_material_response", "EM material/binding response coefficients descend or are superselected", "MISSING_EM_MATERIAL_RESPONSE_DESCENT", False, "WEP/clock/source residual remains live"),
        ("ECA3779_9_verdict", "current branch has the full q_obs EM/Z_EM certificate", "CERTIFICATE_ROUTE_DERIVED_BUT_UNSIGNED", False, "do not claim EM Maxwell descent"),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "required_clause": required_clause,
            "current_status": current_status,
            "passes_clause": passes_clause,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for audit_id, required_clause, current_status, passes_clause, consequence in rows
    ]


def residual_coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("ERZ3779_0_Delta_q_EM", "Delta_q_EM", "|q_EM - F_EM o q_obs|", "sector readout mismatch", "MISSING_PARENT_INPUT"),
        ("ERZ3779_1_vertical_F", "epsilon_F_vertical", "sup_A ||Lie_EA F_obs||/||F_obs||", "physical EM field changes along q_obs fibre", "MISSING_F_VERTICAL_BASICNESS_NORM"),
        ("ERZ3779_2_vertical_A_nongauge", "epsilon_A_nongauge", "inf_lambda sup_A ||Lie_EA A_obs-dlambda_A||", "vertical A variation not pure gauge", "MISSING_A_GAUGE_ORBIT_NORM"),
        ("ERZ3779_3_beta_Z", "beta_Z,A", "Lie_EA ln Z_EM", "EM normalization varies along hidden fibre", "MISSING_ZEM_VERTICAL_COEFFICIENT"),
        ("ERZ3779_4_current_leak", "epsilon_J_EM", "||nabla_a J^a|| + ||J - J_qobs||", "charged current not conserved/descended", "MISSING_EM_CURRENT_DESCENT_NORM"),
        ("ERZ3779_5_shadow_metric", "epsilon_gEM", "||g_EM-g_eff||", "EM light cone differs from source metric", "MISSING_EM_SHADOW_METRIC_NORM"),
        ("ERZ3779_6_material_response", "epsilon_EM_material", "sum_I |K_I^EM delta ln theta_I|", "material response not q_obs/superselected", "MISSING_EM_MATERIAL_RESPONSE_COEFFICIENTS"),
        ("ERZ3779_7_tail_domain", "epsilon_EM_domain", "epsilon_EM_tail + epsilon_flux + epsilon_domain_wall", "tail/flux/domain not q_obs-owned or bounded", "MISSING_EM_TAIL_DOMAIN_COMPONENTS"),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "current_value": current_value,
            "claim_allowed": False,
        }
        for residual_id, symbol, formula, meaning, current_value in rows
    ]


def bound_vector_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("EQB3779_0_EM_readout", "Delta_q_EM", "|q_EM-F_EM o q_obs|", "MISSING_QOBS_EM_READOUT_BOUND", "dimensionless", "EM descent; PPN; WEP"),
        ("EQB3779_1_F_basic", "epsilon_F_vertical", "sup ||Lie_EA F_obs||/||F_obs||", "MISSING_F_BASICNESS_BOUND", "dimensionless", "EM stress; Newton GM"),
        ("EQB3779_2_A_gauge", "epsilon_A_nongauge", "inf_lambda ||Lie_EA A-dlambda_A||", "MISSING_A_GAUGE_ORBIT_BOUND", "field_norm", "gauge/current conservation"),
        ("EQB3779_3_ZEM", "epsilon_ZEM", "|beta_Z,A zeta^A| plus material/species dependence", "MISSING_UNIVERSAL_ZEM_BOUND", "dimensionless", "WEP; clocks; Gdot"),
        ("EQB3779_4_current", "epsilon_J_EM", "||nabla J|| + ||J-J_qobs||", "MISSING_EM_CURRENT_CONSERVATION_BOUND", "current_norm", "same-source; Ward exchange"),
        ("EQB3779_5_shadow_metric", "epsilon_EM_shadow_metric", "||g_EM-g_eff||", "MISSING_EM_SHADOW_METRIC_BOUND", "dimensionless", "PPN gamma; light"),
        ("EQB3779_6_material_response", "epsilon_EM_material_response", "sum_I |K_I^EM delta ln theta_I|", "MISSING_EM_MATERIAL_RESPONSE_COEFFICIENTS", "dimensionless", "WEP; clocks"),
        ("EQB3779_7_WEP", "eta_EM_AB", "C_Z epsilon_ZEM + C_mat epsilon_EM_material + C_J epsilon_J_EM", bounds["wep"], "dimensionless", "WEP"),
        ("EQB3779_8_gamma", "delta_gamma_EM", "C_g epsilon_EM_shadow_metric + C_q Delta_q_EM", bounds["gamma"], "dimensionless", "PPN gamma"),
        ("EQB3779_9_beta", "delta_beta_EM", "C_beta_Z epsilon_ZEM + C_beta_mat epsilon_EM_material + C_beta_extra epsilon_extra", bounds["beta"], "dimensionless", "PPN beta"),
        ("EQB3779_10_Gdot", "dln_Geff_dt_EM", "|d_t ln Z_EM| + |d_t Delta_q_EM| + source exchange rate", bounds["gdot"], "yr^-1", "Gdot"),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "bound_or_value": bound_or_value,
            "units": units,
            "feeds": feeds,
            "claim_allowed": False,
        }
        for bound_id, target, formula, bound_or_value, units, feeds in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    theorem = any(row["theorem_id"] == "QEC3779_5_certificate_promotion" for row in grouped["certificate_theorem"])
    extension = len(grouped["qobs_extension"]) == 6
    audit = len(grouped["certificate_audit"]) == 10
    beta_row = any(row["symbol"] == "beta_Z,A" for row in grouped["residual_coefficients"])
    verdict = any(row["audit_id"] == "ECA3779_9_verdict" and row["passes_clause"] is True for row in grouped["certificate_audit"])
    missing_bounds = any(str(row["bound_or_value"]).startswith("MISSING_") for row in grouped["bound_vector"])
    rows = [
        ("CG3779_0_sources", "all 3779 source paths exist", sources_exist, "path hygiene"),
        ("CG3779_1_certificate_theorem", "q_obs EM/Z_EM certificate theorem emitted", theorem, "constructive certificate route exists"),
        ("CG3779_2_qobs_extension", "q_obs EM extension map emitted", extension, "A/F/current/Z_EM/metric/tail-domain owners named"),
        ("CG3779_3_clause_audit", "all q_obs EM certificate clauses audited", audit, "no EM certificate clause skipped"),
        ("CG3779_4_beta_Z", "beta_Z,A residual coefficient emitted", beta_row, "Z_EM vertical leakage is exact coefficient"),
        ("CG3779_5_current_certificate", "current branch signs q_obs EM/Z_EM certificate", verdict, "expected false until parent signatures exist"),
        ("CG3779_6_missing_bounds_nonclaim", "missing EM certificate bounds remain blockers", missing_bounds, "no pass from placeholder EM certificate rows"),
        ("CG3779_7_EM_descent_claim", "MTS-to-Maxwell Hilbert descent claim allowed", False, "blocked until q_obs EM and Z_EM certificate closes"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3779_0", "The EM parent signature is now an exact q_obs-basicness problem: vertical changes of A must be pure gauge and vertical changes of F must vanish.", "use Lie_EA A=d lambda_A and Lie_EA F=0 as the EM readout certificate"),
        ("DEC3779_1", "Z_EM is the coupling throat: beta_Z,A=Lie_EA ln Z_EM is the exact leakage coefficient if EM normalization is not q_obs-owned or superselected.", "derive beta_Z,A=0 or feed WEP/clock/Gdot bounds"),
        ("DEC3779_2", "Gauge invariance and current conservation are not optional decorations; without them, longitudinal/source leakage can masquerade as EM stress or source mass.", "make U(1) Ward identity a parent-signature target"),
        ("DEC3779_3", "The next target should test the vertical-basicness equations directly rather than widening the audit.", "attempt the parent vertical variation calculation for A, F, and Z_EM"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3779_0",
            "target_doc": "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
            "target_script": "scripts/Y5_R2FR_3780_vertical_EM_basicness_calculation_A_F_ZEM.py",
            "objective": "attempt the explicit vertical variation calculation Lie_EA A=d lambda_A, Lie_EA F=0, and Lie_EA ln Z_EM=0; if it fails, emit the corresponding EM readout and coupling residuals",
            "reason": "3779 reduces the EM parent signature to a direct vertical-basicness calculation, which is a better forward move than adding more audit rows",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "QOBS_EM_READOUT_GAUGE_AND_ZEM_CERTIFICATE_DERIVED_NOT_PARENT_SIGNED",
            "summary": "3779 derives the q_obs EM certificate: EM descends only if A_obs is q_obs-owned up to U(1) gauge, F_obs is vertical-invariant, gauge symmetry gives current conservation, Z_EM is q_obs-owned or superselected with beta_Z,A=0, and EM uses the same g_eff without shadow metric. The current branch has not signed those parent clauses, so Delta q_EM, vertical F leakage, non-gauge A leakage, beta_Z,A, current leakage, EM shadow metric, material response, and tail-domain residuals remain explicit.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3779 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3779 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("certificate_theorem", "q_obs EM certificate theorem emitted", any(row["theorem_id"] == "QEC3779_5_certificate_promotion" for row in grouped["certificate_theorem"])),
        ("qobs_extension", "q_obs EM extension rows emitted", len(grouped["qobs_extension"]) == 6),
        ("audit_complete", "ten certificate audit rows emitted", len(grouped["certificate_audit"]) == 10),
        ("vertical_gauge", "vertical gauge criterion emitted", any(row["theorem_id"] == "QEC3779_1_vertical_gauge_basicness" for row in grouped["certificate_theorem"])),
        ("beta_Z", "beta_Z,A coefficient emitted", any(row["symbol"] == "beta_Z,A" for row in grouped["residual_coefficients"])),
        ("no_certificate_claim", "current branch does not claim EM certificate", any(row["audit_id"] == "ECA3779_9_verdict" and row["passes_clause"] is False for row in grouped["certificate_audit"])),
        ("bounds_nonclaim", "missing EM certificate bounds remain nonclaim", any(str(row["bound_or_value"]).startswith("MISSING_") and row["claim_allowed"] is False for row in grouped["bound_vector"])),
        ("numeric_envelopes", "WEP/PPN/Gdot envelopes imported", all(any(str(row["bound_or_value"]) == value for row in grouped["bound_vector"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"})),
        ("claim_gates_closed", "EM descent claim remains closed", any(row["gate_id"] == "CG3779_7_EM_descent_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3780 vertical EM basicness target emitted", grouped["next_target"][0]["target_doc"] == "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md"),
        ("no_formalization_leak", "no 3779 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3779*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3779 - q_obs EM Readout, Gauge, And Universal Z_EM Certificate",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3779 turns the EM parent signature into a direct certificate. EM is safe only if the observed field is q_obs-basic: vertical changes of `A` are pure gauge, vertical changes of `F` vanish, gauge symmetry gives current conservation, and `Z_EM` is universal/superselected. If not, the theory gets explicit `Delta q_EM`, `epsilon_F_vertical`, `epsilon_A_nongauge`, `beta_Z,A`, current, shadow-metric, material-response, and tail-domain residuals.",
        "",
        "## q_obs EM Certificate Theorem",
    ]
    for row in grouped["certificate_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Meaning: {row['derivation_or_meaning']}")
    lines.extend(["", "## q_obs EM Extension Map"])
    for row in grouped["qobs_extension"]:
        lines.append(f"- `{row['extension_id']}` `{row['object']}`: {row['qobs_form']} Role: {row['role']}. Status: `{row['current_status']}`.")
    lines.extend(["", "## Certificate Audit"])
    for row in grouped["certificate_audit"]:
        lines.append(f"- `{row['audit_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Status: `{row['current_status']}`. Consequence: {row['consequence']}.")
    lines.extend(["", "## Residual Coefficients"])
    for row in grouped["residual_coefficients"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['formula']} = `{row['current_value']}`. Meaning: {row['meaning']}.")
    lines.extend(["", "## Bound Vector"])
    for row in grouped["bound_vector"]:
        lines.append(f"- `{row['bound_id']}` `{row['target']}`: {row['formula']} <= `{row['bound_or_value']}` `{row['units']}`. Feeds: {row['feeds']}.")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    bounds = imported_bounds()

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "certificate_theorem": certificate_theorem_rows(timestamp),
        "qobs_extension": qobs_extension_rows(timestamp),
        "certificate_audit": certificate_audit_rows(timestamp),
        "residual_coefficients": residual_coefficient_rows(timestamp),
        "bound_vector": bound_vector_rows(timestamp, bounds),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["certificate_theorem"], grouped["certificate_theorem"])
    write_csv(OUTPUTS["qobs_extension"], grouped["qobs_extension"])
    write_csv(OUTPUTS["certificate_audit"], grouped["certificate_audit"])
    write_csv(OUTPUTS["residual_coefficients"], grouped["residual_coefficients"])
    write_csv(OUTPUTS["bound_vector"], grouped["bound_vector"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3779 validation failed: {failures}")
    print("wrote 3779 checkpoint: q_obs EM gauge/Z_EM certificate emitted")


if __name__ == "__main__":
    main()
