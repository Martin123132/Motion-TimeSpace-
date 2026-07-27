from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1512_validation": OUT / "P8_Y5_BRR545_1512_VALIDATION.csv",
    "1512_theorem": OUT / "P8_Y5_PARENT_EH_1512_SELECTION_THEOREM_ATTEMPT.csv",
    "1512_premises": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "1512_vector": OUT / "P8_Y5_PARENT_EH_1512_NON_EH_RESIDUAL_VECTOR.csv",
    "1512_decision": OUT / "P8_Y5_PARENT_EH_1512_OPERATOR_DECISION.csv",
    "1512_next": OUT / "P8_Y5_PARENT_EH_1512_NEXT_TARGET.csv",
    "413_no_marker": ROOT / "413-no-marker-parent-action-theorem-attempt.md",
    "414_invariant_algebra": ROOT / "414-local-quotient-invariant-algebra-triviality-gate.md",
    "423_no_extension": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
    "439_premise_ladder": ROOT / "439-EH-only-exterior-parent-premise-ladder.md",
    "440_second_order": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "962_r2fr_zero": OUT / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
    "963_runner_spec": OUT / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
    "964_template": OUT / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
    "965_doc": ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
    "965_theorem": OUT / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
    "965_next": OUT / "P8_Y5_R10_965_NEXT_TARGET.csv",
}

THEOREM_AUDIT = OUT / "P8_Y5_PARENT_MINIMALITY_1513_PRIMITIVE_THEOREM_AUDIT.csv"
GENERATOR_LOCK = OUT / "P8_Y5_PARENT_MINIMALITY_1513_LOCAL_INVARIANT_GENERATOR_LOCK.csv"
COUNTERMODEL_LEDGER = OUT / "P8_Y5_PARENT_MINIMALITY_1513_COUNTERMODEL_LEDGER.csv"
R2FR_STATUS = OUT / "P8_Y5_PARENT_MINIMALITY_1513_R2FR_HIGHER_CURVATURE_STATUS.csv"
R11_VECTOR_LOCK = OUT / "P8_Y5_PARENT_MINIMALITY_1513_R11_VECTOR_LOCK.csv"
BRANCH_DECISION = OUT / "P8_Y5_PARENT_MINIMALITY_1513_OPERATOR_BRANCH_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_MINIMALITY_1513_LOCAL_GR_NEWTON_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_MINIMALITY_1513_SCORE_READINESS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_MINIMALITY_1513_REJECTION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_MINIMALITY_1513_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1513_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1513"
QUAR_THEOREM = QUARANTINE / "PRIMITIVE_MINIMALITY_THEOREM_AUDIT_NONCLAIM.csv"
QUAR_GENERATORS = QUARANTINE / "LOCAL_INVARIANT_GENERATOR_LOCK_NONCLAIM.csv"
QUAR_R11 = QUARANTINE / "R11_VECTOR_LOCK_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "OPERATOR_BRANCH_DECISION_NONCLAIM.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "primitive_minimality_theorem_audit_nonclaim_1513.csv"
BRANCH_GENERATORS = BRANCH_RESIDUALS / "local_invariant_generator_lock_nonclaim_1513.csv"
BRANCH_R11 = BRANCH_RESIDUALS / "r11_vector_lock_nonclaim_1513.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "operator_branch_decision_nonclaim_1513.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("PM1513_0_target", "primitive minimal parent object", "Q_MTS is the free/minimal primitive quotient generated by motion-time-space, not a selected submodel of a larger parent", "NOT_DERIVED", "covariant extensions remain legal", source_list("423_no_extension", "965_theorem")),
        ("PM1513_1_fixed_spurion", "fixed active labels", "fixed non-orbit labels are not functions on a strict quotient", "CONDITIONAL_PASS_IF_STRICT_QUOTIENT", "kills only fixed labels, not transforming markers", source_list("423_no_extension", "965_theorem")),
        ("PM1513_2_no_natural_marker", "no-natural-marker functor", "no natural covariant construction creates nonconstant local scalars/source labels from Q_MTS, matter, or class data", "NOT_DERIVED", "finite-cell spectra, domain/class data, memory scalars, species constants remain admissible", source_list("413_no_marker", "414_invariant_algebra", "965_theorem")),
        ("PM1513_3_local_invariant_algebra", "local invariant algebra triviality", "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor universal constants on the local branch", "NOT_DERIVED", "extra generators can source marker-prefactors or local residuals", source_list("414_invariant_algebra", "965_theorem")),
        ("PM1513_4_no_integrated_tower", "no integrated-out higher-curvature tower", "hidden sectors cannot generate R2/fR/Ricci2/Weyl2/nonlocal metric operators after reduction", "NOT_DERIVED", "EH+R2 and auxiliary scalar countermodels remain legal", source_list("964_template", "965_doc")),
        ("PM1513_5_second_order_activation", "activate R2/fR relative zero theorem", "parent signs exact local second-order/no-extra-scalar premise, forcing f_RR=0", "RELATIVE_THEOREM_EXISTS_ABSOLUTE_PREMISE_UNSIGNED", "R2/fR zero cannot promote", source_list("962_r2fr_zero", "1512_premises")),
        ("PM1513_6_verdict", "primitive minimality/no-higher-derivative theorem", "PM1513_0 through PM1513_5 close with no live countermodel", "THEOREM_NOT_PROVEN_CURRENT_CORPUS", "lock R11 vector as active local operator branch", source_list("1512_decision", "965_theorem")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "theorem_piece": piece,
            "would_need_to_show": need,
            "current_status": status,
            "consequence": consequence,
            "source_paths": sources,
            **flags(),
        }
        for attempt_id, piece, need, status, consequence, sources in rows
    ]


def generator_rows() -> list[dict[str, Any]]:
    rows = [
        ("GEN1513_0_observed_geometry", "observed geometry jets J^k(e_obs)", "ALLOWED_GEOMETRY", False, "EH operator selection remains separate", "use in same-frame EH/Newton branch"),
        ("GEN1513_1_universal_constants", "universal constants", "ALLOWED_IF_SOURCE_INDEPENDENT", False, "common calibration only if constant and universal", "GM/source-normalization theorem still needed"),
        ("GEN1513_2_finite_cell_spectrum", "finite-cell/fibre spectrum", "NOT_ELIMINATED", True, "can become scalar/class marker or source-dependent prefactor", "derive spectral universality or no-local-gradient silence"),
        ("GEN1513_3_domain_selector", "domain selector chi_D", "NOT_ELIMINATED", True, "can become projector/source switch or local/cosmology branch axiom", "derive selector theorem separating local vacuum from cosmology"),
        ("GEN1513_4_memory_class_scalar", "memory/class scalar", "NOT_ELIMINATED", True, "can produce nonlocal/Gdot/fifth-force or prefactor leakage", "prove local kernel silence or retain memory residual"),
        ("GEN1513_5_species_constants", "species constants theta_A(I_Q)", "NOT_ELIMINATED", True, "WEP/source-charge residuals", "constant-sector universality theorem"),
        ("GEN1513_6_orientation_time_arrow", "orientation/time-arrow marker", "NOT_CLASSIFIED", True, "preferred-frame/parity/time-asymmetry residuals", "show contained in e_obs, constant, or pure gauge"),
        ("GEN1513_7_readout_projector", "post-readout projector/reduced-action marker", "POLICY_BLOCKED_NOT_THEOREM_BLOCKED", True, "closure-zero can be mistaken for theorem-zero", "exact readout-after-variation theorem"),
        ("GEN1513_8_boundary_topological_marker", "boundary/topological marker", "CONDITIONALLY_SAFE_NOT_DERIVED", True, "can carry boundary/domain class data", "stress-free topological no-flux theorem"),
        ("GEN1513_9_verdict", "I_loc(Q_MTS)=I_geom plus constants", "NOT_DERIVED", True, "marker couplings remain technically admissible", "attack generators one by one before local-GR claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "generator_id": generator_id,
            "generator": generator,
            "local_status": status,
            "blocks_no_marker": blocks,
            "possible_damage": damage,
            "required_elimination": required,
            **flags(),
        }
        for generator_id, generator, status, blocks, damage, required in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM1513_0_EH_plus_R2", "S=S_EH+epsilon int sqrt(-g) R^2", "LIVE", "adds scalar trace pole/fourth-order metric equation unless epsilon=0 or decoupled", "parent second-order/minimality theorem"),
        ("CM1513_1_auxiliary_scalar", "hidden auxiliary scalar integrated out into f(R)", "LIVE", "can re-enter as higher-curvature or scalar-tensor operator after reduction", "no-integrated-out-tower theorem"),
        ("CM1513_2_marker_prefactor", "F(sigma)R with quotient-invariant scalar sigma", "LIVE", "variable effective G, scalar force, clock/PPN leakage", "local invariant algebra triviality"),
        ("CM1513_3_comoving_marker", "co-moving material marker m varied with matter", "LIVE", "source charge, WEP pressure, fifth-force numerator", "primitive universal-property no-extension theorem"),
        ("CM1513_4_domain_selector", "domain selector chi_D in local/cosmology split", "LIVE", "projector stress and preferred-frame/source-switch leakage", "domain selector theorem"),
        ("CM1513_5_nonlocal_memory", "R Box^-1 R or history kernel", "LIVE", "Gdot, alpha3, finite-range/memory leakage", "compact-local memory silence theorem"),
        ("CM1513_6_topological_marker", "boundary/topological marker", "CONDITIONALLY_SAFE", "safe only if no local stress/flux/readout vertex", "topological stress-free no-flux theorem"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "counter_id": counter_id,
            "countermodel": countermodel,
            "current_status": status,
            "damage": damage,
            "required_blocker": blocker,
            **flags(),
        }
        for counter_id, countermodel, status, damage, blocker in rows
    ]


def r2fr_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "R2FR1513_0_relative_zero",
            "object": "R2/fR scalar-mode zero theorem",
            "current_status": "RELATIVE_THEOREM_ONLY",
            "evidence": "962 proves f_RR=0 if parent signs exact second-order/no-extra-scalar premise",
            "claim_effect": "cannot set c_R2=c_fR=0 until primitive minimality/second-order premise is parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "R2FR1513_1_finite_branch",
            "object": "finite R2/fR scalar branch",
            "current_status": "NONCLAIM_RUNNER_ONLY",
            "evidence": "963/964 runner specs reject missing parent coefficient, missing full curve, and unsigned zero theorem",
            "claim_effect": "no R10/PPN/local-GR score",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "R2FR1513_2_operator_branch",
            "object": "higher-curvature leakage",
            "current_status": "LOCK_IN_R11_VECTOR",
            "evidence": "1512 retained non-EH vector; 1513 minimality theorem not proven",
            "claim_effect": "EH operator remains conditional",
            **flags(),
        },
    ]


def r11_lock_rows() -> list[dict[str, Any]]:
    locked = []
    for row in read_csv(SOURCE_FILES["1512_vector"]):
        locked.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "lock_id": f"R11LOCK1513_{len(locked):02d}",
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "current_coefficient": row["coefficient_value"],
                "lock_status": "ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND",
                "unlock_condition": "parent zero theorem, topological/no-flux theorem, double-zero selector, or sourced numeric coefficient/bound",
                "induced_observable": row["induced_observable"],
                "source_vector_row": row["vector_id"],
                **flags(),
            }
        )
    return locked


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1513_0_minimality",
            "decision": "primitive minimality/no-higher-derivative theorem not proven",
            "rationale": "fixed spurions are conditionally excluded, but covariant material markers and local invariant generators remain live",
            "result": "NO_EH_OPERATOR_PROMOTION",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1513_1_R11_lock",
            "decision": "lock non-EH vector as active local operator branch",
            "rationale": "higher-curvature, connection, scalar, vector, memory, boundary, source-normalization, and projector families cannot be silently dropped",
            "result": "R11_VECTOR_ACTIVE",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1513_2_next",
            "decision": "attack local invariant generators directly",
            "rationale": "the no-natural-marker theorem failed because specific generators remain; the next derivation should eliminate or lock them one by one",
            "result": "NEXT_1514_GENERATOR_ELIMINATION",
            **flags(),
        },
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1513_0",
            "object": "primitive minimality / no higher derivative",
            "status": "NOT_PARENT_DERIVED",
            "effect": "does not activate absolute EH/R2-fR zero claim",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1513_1",
            "object": "local operator branch",
            "status": "R11_VECTOR_ACTIVE_NONCLAIM",
            "effect": "local GR/Newton derivation must either eliminate each vector family or bound it",
            **flags(),
        },
    ]


def score_rows(r11_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1513_0",
            "status": "NOT_SCORE_READY",
            "reason": "R11 vector is locked but all rows still require zero/bound sources before empirical scoring",
            "active_r11_rows": len(r11_rows),
            **flags(),
        }
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1513_0", "claim primitive minimality from aesthetic simplicity", "minimality must be a parent theorem, not a preference"),
        ("REJ1513_1", "claim no higher derivatives because EH is desired", "EH+R2 and auxiliary scalar countermodels remain legal"),
        ("REJ1513_2", "treat fixed-spurion exclusion as no-marker theorem", "fixed labels are not covariant material markers; live natural markers remain"),
        ("REJ1513_3", "treat local invariant generators as harmless by naming them closure", "closure labels are not theorem-zero; residual tax remains"),
        ("REJ1513_4", "promote R2/fR zero from the relative theorem", "962 needs parent second-order/no-extra-scalar premise, still unsigned"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "rejected_shortcut": shortcut,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1513_0_1514",
            "next_target": "1514-Y5-parent-local-invariant-generator-elimination-or-domain-selector-lock.md",
            "script": "scripts/Y5_parent_local_invariant_generator_elimination_or_domain_selector_lock.py",
            "objective": "attack the surviving local invariant generators directly, starting with the domain selector chi_D / projector branch; prove it is geometry/gauge/constant/silent, or lock it as an explicit R11 residual family",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (THEOREM_AUDIT, QUAR_THEOREM),
        (GENERATOR_LOCK, QUAR_GENERATORS),
        (R11_VECTOR_LOCK, QUAR_R11),
        (BRANCH_DECISION, QUAR_DECISION),
        (THEOREM_AUDIT, BRANCH_THEOREM),
        (GENERATOR_LOCK, BRANCH_GENERATORS),
        (R11_VECTOR_LOCK, BRANCH_R11),
        (BRANCH_DECISION, BRANCH_DECISION_COPY),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], generators: list[dict[str, Any]], counters: list[dict[str, Any]], r11_rows: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    theorem_not_proven = any(row["attempt_id"] == "PM1513_6_verdict" and row["current_status"] == "THEOREM_NOT_PROVEN_CURRENT_CORPUS" for row in theorem)
    live_generators = sum(1 for row in generators if str(row["blocks_no_marker"]) == "True") >= 6
    live_countermodels = sum(1 for row in counters if row["current_status"] == "LIVE") >= 5
    r2fr_locked = read_csv(R2FR_STATUS)[-1]["current_status"] == "LOCK_IN_R11_VECTOR"
    r11_locked = len(r11_rows) >= 10 and all(row["lock_status"] == "ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND" for row in r11_rows)
    next_generator = any(row["decision_id"] == "DEC1513_2_next" and row["result"] == "NEXT_1514_GENERATOR_ELIMINATION" for row in decisions)
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_THEOREM, QUAR_GENERATORS, QUAR_R11, QUAR_DECISION, BRANCH_THEOREM, BRANCH_GENERATORS, BRANCH_R11, BRANCH_DECISION_COPY])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1513_0_sources", source_paths_exist, "all cited minimality/no-marker/R11 source paths exist"),
        ("VAL1513_1_theorem_not_proven", theorem_not_proven, "primitive minimality theorem remains explicitly unproven"),
        ("VAL1513_2_live_generators", live_generators, "local invariant generator blockers remain live"),
        ("VAL1513_3_live_countermodels", live_countermodels, "live countermodels remain recorded"),
        ("VAL1513_4_r2fr_locked", r2fr_locked, "R2/fR higher-curvature leakage is locked into R11 vector"),
        ("VAL1513_5_r11_locked", r11_locked, "R11 vector lock covers at least 10 operator families"),
        ("VAL1513_6_next_generator", next_generator, "next target attacks generator elimination"),
        ("VAL1513_7_csv_parse", csv_parse_ok, "all generated 1513 CSVs parse cleanly"),
        ("VAL1513_8_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
        ("VAL1513_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1513_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1513_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1513_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1513 refused primitive-minimality overclaim, locked the R11 vector, and selected local invariant generator elimination next"
            if overall
            else "1513 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    theorem: list[dict[str, Any]],
    generators: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    r2fr: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1513 - Parent Primitive Minimality / No-Higher-Derivative Theorem or R11 Vector Lock",
                "",
                "## Verdict",
                "- The primitive minimality/no-natural-marker theorem still does not close: fixed spurions are conditionally excluded, but covariant material markers and local invariant generators remain live.",
                "- Therefore the higher-curvature/R2-fR leak is not theorem-zero; the non-EH R11 vector is now the active local operator branch until each family is zeroed or bounded.",
                "- The next derivation target is local invariant generator elimination, starting with the domain selector chi_D / projector branch.",
                "",
                "## Primitive Theorem Audit",
                md_table(theorem, ["attempt_id", "theorem_piece", "current_status", "consequence"]),
                "",
                "## Local Invariant Generator Lock",
                md_table(generators, ["generator_id", "generator", "local_status", "blocks_no_marker"]),
                "",
                "## Countermodel Ledger",
                md_table(counters, ["counter_id", "countermodel", "current_status", "required_blocker"]),
                "",
                "## R2/fR Higher-Curvature Status",
                md_table(r2fr, ["status_id", "object", "current_status", "claim_effect"]),
                "",
                "## R11 Vector Lock",
                md_table(r11_rows, ["lock_id", "operator_family", "lock_status"]),
                "",
                "## Operator Branch Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    theorem = theorem_rows()
    generators = generator_rows()
    counters = countermodel_rows()
    r2fr = r2fr_rows()
    r11_rows = r11_lock_rows()
    decisions = decision_rows()
    local_status = local_status_rows()
    score = score_rows(r11_rows)
    rejections = rejection_rows()
    next_rows = next_target_rows()

    write_csv(THEOREM_AUDIT, theorem)
    write_csv(GENERATOR_LOCK, generators)
    write_csv(COUNTERMODEL_LEDGER, counters)
    write_csv(R2FR_STATUS, r2fr)
    write_csv(R11_VECTOR_LOCK, r11_rows)
    write_csv(BRANCH_DECISION, decisions)
    write_csv(LOCAL_STATUS, local_status)
    write_csv(SCORE_READINESS, score)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        THEOREM_AUDIT,
        GENERATOR_LOCK,
        COUNTERMODEL_LEDGER,
        R2FR_STATUS,
        R11_VECTOR_LOCK,
        BRANCH_DECISION,
        LOCAL_STATUS,
        SCORE_READINESS,
        REJECTION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, generators, counters, r11_rows, decisions)
    write_csv(VALIDATION, validation)
    write_doc(theorem, generators, counters, r2fr, r11_rows, decisions, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
