import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3791"
BRANCH = "MTS_R2FR_Y5_ZEM_FIXED_NORMALIZATION_OR_BETAZ_BOUND_3791"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3791_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3791_ZEM_FIXED_NORMALIZATION_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3791_CURRENT_CORPUS_ZEM_SIGNATURE_AUDIT.csv",
    "counterterms": RESIDUALS / "P8_Y5_R2FR_3791_OPERATOR_BASIS_COUNTEREXAMPLE_GUARD.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3791_BETAZ_LAMBDA_ZERO_OR_BOUND_COMPONENTS.csv",
    "action_update": RESIDUALS / "P8_Y5_R2FR_3791_EM_ACTION_ALPHA_UPDATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3791_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3791_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3791_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3791_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3791_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
    PCW / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
    PCW / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
    PCW / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
    PCW / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "ZEM_betaZ_unique_F2_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def theorem_rows(timestamp):
    rows = [
        {
            "theorem_id": "ZFT3791_0_definition",
            "claim_piece": "Z_EM vertical coefficient",
            "mathematical_form": "beta_Z,A := Lie_EA ln Z_EM, with Z_EM=Z_Pi/q_*^2 or Z_EM=C_P N_Q/q_*^2 plus retained counterterms if allowed.",
            "derivation_status": "DEFINITION_FROM_3784_3790",
            "missing_for_current_claim": "parent-owned Z_Pi/C_P/N_Q and no independent F^2 coefficient",
            "if_unsigned": "retain beta_Z,A and lambda_A rows",
        },
        {
            "theorem_id": "ZFT3791_1_conditional_zero",
            "claim_piece": "beta_Z,A=0",
            "mathematical_form": "If q_* is superselected, C_P is quotient-owned/superselected, N_Q is fixed by a nonrescalable parent generator norm, and no independent lambda_A F^2 or f(Xhat)F^2 operator exists, then Lie_EA Z_EM=0.",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "fixed parent generator norm; unique Maxwell subblock; operator-domain exhaustion; readout/current owner",
            "if_unsigned": "Z_EM remains a finite coefficient branch",
        },
        {
            "theorem_id": "ZFT3791_2_lambda_counterterm",
            "claim_piece": "independent Maxwell kinetic coefficient",
            "mathematical_form": "If DeltaS=-lambda_A/4 int sqrt(-g_eff) F_obs^2 is legal, then Z_EM=Z_parent+lambda_A and beta_Z,A receives Lie_EA ln(Z_parent+lambda_A).",
            "derivation_status": "COUNTEREXAMPLE_GUARD",
            "missing_for_current_claim": "no-independent-F2 proof",
            "if_unsigned": "lambda_A and beta_Z,A must be bounded, not set to zero",
        },
        {
            "theorem_id": "ZFT3791_3_alpha_readout",
            "claim_piece": "alpha_EM ownership",
            "mathematical_form": "Even beta_Z,A=0 is not a full alpha_EM theorem unless observed Hodge/coframe, hbar*c, current normalization, and spectroscopy/readout also descend through q_obs.",
            "derivation_status": "OVERCLAIM_GUARD",
            "missing_for_current_claim": "readout descent and same-current/source ownership",
            "if_unsigned": "retain b_alpha/readout/current residuals",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def audit_rows(timestamp):
    rows = [
        {
            "audit_id": "ZA3791_0_3784_ZEM",
            "source_signal": "3784 names Z_EM=Z_Pi/q_*^2=C_Q N_Q and keeps Z_EM zero condition unsigned",
            "current_result": "ZEM_OWNER_UNSIGNED",
            "impact": "cannot promote beta_Z,A=0 in strict current-corpus mode",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ZA3791_1_3790_qstar",
            "source_signal": "3790 conditionally zeroes q_* drift but explicitly says this does not derive Z_EM/alpha",
            "current_result": "QSTAR_HELPFUL_BUT_INSUFFICIENT",
            "impact": "q_* branch removes denominator drift only; numerator normalization remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ZA3791_2_1056_norm",
            "source_signal": "1056 says compact U(1) fixes charge labels but not continuous Maxwell kinetic coefficient",
            "current_result": "COMPACTNESS_NOT_ENOUGH",
            "impact": "requires fixed generator norm plus unique F2 inheritance",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ZA3791_3_1057_unique_F2",
            "source_signal": "1057 states exact no-independent-F2 theorem but current corpus fails because gauge/diffeomorphism allow F2",
            "current_result": "UNIQUE_F2_NOT_DERIVED",
            "impact": "lambda_A/f(Xhat)F2 counterterms remain legal",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ZA3791_4_1049_operator",
            "source_signal": "1049 operator classification says ordinary symmetries do not forbid f_X F2; stronger product/sequester rule is unsigned",
            "current_result": "OPERATOR_DOMAIN_EXHAUSTION_MISSING",
            "impact": "cannot remove beta_Z/lambda by ordinary covariance or gauge invariance",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ZA3791_5_verdict",
            "source_signal": "sources jointly support theorem shape and jointly block current promotion",
            "current_result": "CONDITIONAL_THEOREM_PLUS_RETAINED_BOUND_BRANCH",
            "impact": "emit zero branch only as parent-extension theorem; retain bound rows for current corpus",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def counterterm_rows(timestamp):
    rows = [
        {
            "guard_id": "CTG3791_0_covariant_F2",
            "operator": "lambda_A F_obs^2",
            "ordinary_symmetry_status": "ALLOWED_BY_DIFF_AND_U1",
            "effect": "adds an independent contribution to Z_EM and can carry vertical drift",
            "repair_needed": "parent operator-domain exhaustion or unique curvature-norm inheritance",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CTG3791_1_hidden_scalar_F2",
            "operator": "f(Xhat) F_obs^2",
            "ordinary_symmetry_status": "ALLOWED_IF_XHAT_IS_VISIBLE_SCALAR_OR_COEFFICIENT_MARKER",
            "effect": "direct beta_Z,A/b_alpha leakage and WEP/clock/R10 pressure",
            "repair_needed": "hidden-visible product/sequester theorem plus radiative closure",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CTG3791_2_generator_rescale",
            "operator": "T_Q -> s T_Q, A_Q -> A_Q/s, current labels compensate",
            "ordinary_symmetry_status": "CONVENTIONAL_UNLESS_PARENT_NORM_FIXED",
            "effect": "N_Q and current normalization are not physical until parent norm/current owner is fixed",
            "repair_needed": "nonrescalable parent generator norm and same-current owner",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CTG3791_3_readout_leak",
            "operator": "Hodge/coframe/hbar*c/spectroscopy readout drift",
            "ordinary_symmetry_status": "SEPARATE_FROM_ABSTRACT_ZEM",
            "effect": "alpha_EM can drift even if abstract Z_EM is fixed",
            "repair_needed": "q_obs-owned observed readout and clock/source descent",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def component_rows(timestamp):
    rows = [
        {
            "component_id": "BZ3791_0_beta_ZA",
            "symbol": "beta_Z,A",
            "definition": "Lie_EA ln Z_EM",
            "zero_if": "q_* superselected, parent C_P/N_Q fixed, no independent F^2 operator, and readout/current normalization does not reintroduce vertical drift",
            "conditional_value": "0",
            "fallback_value": "MISSING_BETA_ZA_OR_PARENT_ZERO_THEOREM",
            "feeds": "delta_A S_EM;epsilon_alpha_source;WEP;clock;Gdot;PPN",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "BZ3791_1_lambda_A",
            "symbol": "lambda_A",
            "definition": "coefficient of independent observed/pullback Maxwell kinetic operator outside parent curvature norm",
            "zero_if": "operator-domain exhaustion forbids lambda_A F_obs^2 including effective/radiative re-entry",
            "conditional_value": "0",
            "fallback_value": "MISSING_LAMBDA_A_PRIOR_OR_OPERATOR_BAN",
            "feeds": "delta_A S_EM;alpha_EM;clock;WEP;R10",
            "status": "LEGAL_UNLESS_PARENT_DOMAIN_EXCLUDES",
            "valid_for_claim": False,
        },
        {
            "component_id": "BZ3791_2_fX_F2",
            "symbol": "b_Z_hidden",
            "definition": "vertical derivative of hidden scalar gauge kinetic function f(Xhat)F_obs^2",
            "zero_if": "hidden-visible product/sequester theorem forbids Xhat-dependent visible kinetic coefficients",
            "conditional_value": "0",
            "fallback_value": "MISSING_FX_F2_PRIOR_OR_SEQUESTER_THEOREM",
            "feeds": "beta_Z,A;b_alpha;WEP;clock;R10",
            "status": "LEGAL_UNLESS_PRODUCT_FUNCTOR_SIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "BZ3791_3_b_alpha_readout",
            "symbol": "b_alpha_readout",
            "definition": "residual vertical derivative of observed dimensionless alpha readout after abstract Z_EM is fixed",
            "zero_if": "observed coframe/Hodge/hbar*c/spectroscopy readout descends through q_obs",
            "conditional_value": "0",
            "fallback_value": "MISSING_ALPHA_READOUT_DESCENT_OR_BOUND",
            "feeds": "clock;atomic_spectra;WEP_source_alpha",
            "status": "SEPARATE_READOUT_GATE",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def action_update_rows(timestamp):
    rows = [
        {
            "update_id": "EAU3791_0_current_action_leak",
            "branch": "finite_current_corpus",
            "formula": "delta_A S_EM contains beta_Z,A F^2, dR_A, J_Q dot R_A, and lambda_A contributions",
            "conditions": "Z_EM owner and no-independent-F2 are unsigned",
            "status": "RETAINED_BOUND_FORM",
            "valid_for_claim": False,
        },
        {
            "update_id": "EAU3791_1_ZEM_zero_branch",
            "branch": "ZEM_fixed_parent_extension",
            "formula": "beta_Z,A=0 removes the universal Maxwell-normalization leak from delta_A S_EM",
            "conditions": "q_* superselected, C_P/N_Q fixed, no independent F^2, no readout/current re-entry",
            "status": "CONDITIONAL_SIMPLIFICATION",
            "valid_for_claim": False,
        },
        {
            "update_id": "EAU3791_2_lambda_block",
            "branch": "operator_domain_unsigned",
            "formula": "Z_EM=Z_parent+lambda_A or Z_parent+f(Xhat), so beta_Z,A is not zero by compactness/topology alone",
            "conditions": "independent F^2 slot remains legal",
            "status": "CURRENT_CORPUS_BLOCKER",
            "valid_for_claim": False,
        },
        {
            "update_id": "EAU3791_3_alpha_status",
            "branch": "alpha_readout",
            "formula": "alpha_EM silence requires Z_EM silence plus observed readout descent; Z_EM theorem alone is not enough",
            "conditions": "Hodge/coframe/hbar*c/spectroscopy/current normalization separate",
            "status": "ALPHA_REMAINS_NONCLAIM",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_1_ZEM_theorem_shape",
            "pass": True,
            "claim_allowed": False,
            "details": "exact conditional Z_EM fixed-normalization theorem emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_2_current_ZEM_signed",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus lacks fixed generator norm, unique F2 operator-domain exhaustion, and readout/current owner",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_3_independent_F2_banned",
            "pass": False,
            "claim_allowed": False,
            "details": "ordinary covariance and U1 gauge invariance allow F2; stronger parent domain theorem is unsigned",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_4_betaZ_bound_rows",
            "pass": True,
            "claim_allowed": False,
            "details": "beta_Z/lambda_A/fX/readout bound rows emitted as nonclaim fallbacks",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_5_alpha_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "alpha_EM ownership is not derived from Z_EM theorem alone",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3791_6_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; Maxwell normalization remains finite unless upstream operator-domain gates close",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3791_0_theorem_shape",
            "decision": "Z_EM can be theorem-zero only under fixed parent normalization plus no independent F2.",
            "action": "Keep the exact conditional theorem, but do not promote it in strict current-corpus mode.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3791_1_current_failure",
            "decision": "The current corpus cannot ban lambda_A F^2 or f(Xhat)F^2 using ordinary symmetry.",
            "action": "Retain beta_Z,A, lambda_A, and hidden scalar F2 rows as finite residuals.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3791_2_alpha_honesty",
            "decision": "Even a Z_EM zero theorem would not by itself derive observed alpha_EM.",
            "action": "Keep readout/current/Hodge/spectroscopy descent as separate gates.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3791_3_next",
            "decision": "The next concrete route is same-current owner or operator-domain exhaustion; same-current is closer to local GR/Newton source coupling.",
            "action": "Try the same-source charged-current/Ward/Hilbert-stress owner before returning to the harder B_Q owner.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md",
            "target_script": "scripts/Y5_R2FR_3792_same_current_Ward_Hilbert_stress_owner_or_epsilonJ_bound.py",
            "objective": "Try to prove J_Q, charged matter, EM stress, and binding stress descend from the same q_obs total source action so epsilon_J_Q=0 and EM Hilbert stress can enter Pi_M_total; if it fails, emit source-ready epsilon_J_Q/source-current bound rows.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "ZEM_ZERO_CONDITIONAL_UNIQUE_F2_NOT_DERIVED_BETAZ_LAMBDA_RETAINED",
            "plain_verdict": "3791 isolates the exact Z_EM theorem: beta_Z,A vanishes only if q_* is superselected, the parent generator norm/Maxwell subblock is fixed, and independent F^2 operators are forbidden. Current corpus does not ban F^2, so beta_Z,A and lambda_A remain nonclaim finite residuals. Alpha_EM is still not derived.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3791 markdown document written"),
        (
            "zem_theorem",
            any(row["theorem_id"] == "ZFT3791_1_conditional_zero" for row in grouped["theorem"]),
            "conditional Z_EM theorem emitted",
        ),
        (
            "f2_counterterm_guard",
            any(row["guard_id"] == "CTG3791_0_covariant_F2" for row in grouped["counterterms"]),
            "independent F2 counterterm guard emitted",
        ),
        (
            "current_failure_retained",
            any(row["audit_id"] == "ZA3791_3_1057_unique_F2" and row["current_result"] == "UNIQUE_F2_NOT_DERIVED" for row in grouped["audit"]),
            "current no-independent-F2 failure retained",
        ),
        (
            "betaz_rows",
            all(
                any(row["symbol"] == symbol for row in grouped["components"])
                for symbol in ["beta_Z,A", "lambda_A", "b_Z_hidden", "b_alpha_readout"]
            ),
            "beta_Z/lambda/readout rows emitted",
        ),
        (
            "alpha_claim_closed",
            any(row["gate_id"] == "CG3791_5_alpha_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "alpha claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3792-"),
            "3792 same-current target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3791 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3791 - Z_EM Fixed Normalization or beta_Z Bound",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3791 takes the dangerous Maxwell-normalization step and refuses the easy lie. `Z_EM` can be fixed only if the parent branch supplies a nonrescalable generator norm, a unique Maxwell kinetic subblock, no independent `F^2` slot, and no readout/current re-entry. The current corpus does not have that: ordinary covariance and U(1) gauge invariance allow `F^2`, and prior checkpoints already kept this as a counterexample. So `beta_Z,A`, `lambda_A`, hidden `f(Xhat)F^2`, and alpha-readout leakage stay live finite residuals.",
        "",
        "## Compact Result",
        "",
        "`beta_Z,A := Lie_EA ln Z_EM`.",
        "",
        "Conditional zero: `beta_Z,A=0` if `q_*` is fixed, parent `C_P/N_Q` are fixed, no independent `F^2` operator exists, and readout/current normalization descends.",
        "",
        "Current-corpus verdict: ordinary symmetries allow `lambda_A F^2` and `f(Xhat)F^2`, so `beta_Z,A` is not claim-zero.",
        "",
        "Alpha guard: even abstract `Z_EM` silence does not prove observed `alpha_EM` unless Hodge/coframe, `hbar*c`, spectroscopy, and current normalization descend too.",
        "",
        render_section("Z_EM Fixed-Normalization Theorem", grouped["theorem"], ["theorem_id", "claim_piece"]),
        render_section("Current Corpus Z_EM Signature Audit", grouped["audit"], ["audit_id"]),
        render_section("Operator-Basis Counterexample Guard", grouped["counterterms"], ["guard_id", "operator"]),
        render_section("beta_Z/lambda Zero or Bound Components", grouped["components"], ["component_id", "symbol"]),
        render_section("EM Action and Alpha Update", grouped["action_update"], ["update_id", "branch"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "audit": audit_rows(timestamp),
        "counterterms": counterterm_rows(timestamp),
        "components": component_rows(timestamp),
        "action_update": action_update_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["counterterms"], grouped["counterterms"])
    write_csv(OUTPUTS["components"], grouped["components"])
    write_csv(OUTPUTS["action_update"], grouped["action_update"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3791 validation failed: {failures}")
    print("wrote 3791 checkpoint: Z_EM theorem shape and beta_Z/lambda fallback emitted")


if __name__ == "__main__":
    main()
