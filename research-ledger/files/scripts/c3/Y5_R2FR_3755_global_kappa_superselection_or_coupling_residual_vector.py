from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3755"
BRANCH = "MTS_R2FR_Y5_GLOBAL_KAPPA_SUPERSELECTION_OR_COUPLING_RESIDUAL_VECTOR_3755"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3755-Y5-R2FR-global-kappa-superselection-or-coupling-residual-vector.md"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(stamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": stamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3755_0_3754_next": RESIDUALS / "P8_Y5_R2FR_3754_NEXT_TARGET.csv",
        "SRC3755_1_3754_poisson": RESIDUALS / "P8_Y5_R2FR_3754_POISSON_CALIBRATION_ROWS.csv",
        "SRC3755_2_3754_residuals": RESIDUALS / "P8_Y5_R2FR_3754_COUPLING_RESIDUAL_ROWS.csv",
        "SRC3755_3_3754_gates": RESIDUALS / "P8_Y5_R2FR_3754_CLAIM_GATES.csv",
        "SRC3755_4_global_contract": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
        "SRC3755_5_constant_gm_attempt": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "SRC3755_6_constant_gm_bounds": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "SRC3755_7_delta_kappa": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
        "SRC3755_8_pg_map": RESIDUALS / "P8_PG_calibration_residual_MAP.csv",
        "SRC3755_9_newton_bounds": RESIDUALS / "P8_Y5_R2FR_3530_NEWTON_PPN_BOUND_ROWS.csv",
    }


def source_register(stamp: str) -> list[dict[str, object]]:
    purpose = {
        "SRC3755_0_3754_next": "imports exact 3755 target",
        "SRC3755_1_3754_poisson": "imports G_eff := kappa_eff c^4/(8*pi) bridge",
        "SRC3755_2_3754_residuals": "imports coupling residual vector from 3754",
        "SRC3755_3_3754_gates": "imports still-open constant-G/local-GR gates",
        "SRC3755_4_global_contract": "imports global coupling superselection contract GS0-GS8",
        "SRC3755_5_constant_gm_attempt": "imports constant-GM zero theorem attempt Z0-Z8",
        "SRC3755_6_constant_gm_bounds": "imports local coupling residual bound matrix",
        "SRC3755_7_delta_kappa": "imports Bianchi/kappa exchange residual row",
        "SRC3755_8_pg_map": "imports Poisson/Gauss residual activation map",
        "SRC3755_9_newton_bounds": "imports numeric local bound anchors for Gdot/WEP/beta/gamma/R10",
    }
    return [
        {
            **base(stamp),
            "source_id": source_id,
            "source_path": str(path),
            "purpose": purpose[source_id],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for source_id, path in source_paths().items()
    ]


def bound_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(source_paths()["SRC3755_9_newton_bounds"])
    return {row["bound_id"]: row for row in rows}


def theorem_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "KT3755_0_configuration_split",
            "Superselection signature",
            "Assume Q_parent = Q_dyn x K_global, with kappa_eff in K_global and not in Gamma(E_local). Compact-support variations act only on Q_dyn.",
            "SIGNATURE_REQUIRED_NOT_SOURCED",
            "would give delta_local kappa_eff=0 and no local Euler equation for kappa",
        ),
        (
            "KT3755_1_global_parameter",
            "Global coupling derivative silence",
            "If kappa_eff is a global parameter, then partial_t kappa_eff=partial_r kappa_eff=partial_A kappa_eff=partial_lambda kappa_eff=partial_frame kappa_eff=0 inside the local branch.",
            "EXACT_IF_K_GLOBAL",
            "kills Gdot/source/range/frame coupling derivatives",
        ),
        (
            "KT3755_2_bianchi_arbitrary_source",
            "Bianchi arbitrary-source lemma",
            "For E_mn=kappa(x)T_mn, nabla^m E_mn=0, nabla^m T_mn=0, and arbitrary same-frame conserved T_mn, one gets (nabla^m kappa)T_mn=0 for arbitrary T, hence nabla kappa=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "can prove derivative silence if same-frame separate conservation and arbitrary-source premises are signed",
        ),
        (
            "KT3755_3_exchange_fallback",
            "Bianchi exchange fallback",
            "If matter is not separately conserved or exchange owners remain, the identity is nabla E=0 -> kappa q_exchange + T nabla kappa + nabla DeltaE = 0, not nabla kappa=0.",
            "NO_OVERCLAIM_COUNTERBRANCH",
            "activates delta_kappa_source and q_exchange rows",
        ),
        (
            "KT3755_4_source_blindness",
            "Species/source-label silence",
            "If kappa_eff in K_global and K_global has no material/source-label action, partial_A kappa_eff=partial_source kappa_eff=0.",
            "EXACT_IF_K_GLOBAL_SOURCE_BLIND",
            "kills active-gravitational-source composition dependence from kappa itself",
        ),
        (
            "KT3755_5_range_blindness",
            "Range/radius silence",
            "If kappa_eff is not a propagating scalar or range field, no Yukawa alpha(lambda) branch is generated by kappa_eff.",
            "EXACT_IF_NOT_LOCAL_FIELD",
            "kills kappa-owned R10/radial coupling hair; other mu_extra range channels remain separate",
        ),
        (
            "KT3755_6_constant_offset",
            "Absolute G policy",
            "A constant kappa_eff still only calibrates G_eff unless the parent action predicts its absolute value; derivative silence is not a numerical prediction of G.",
            "ANTI_OVERCLAIM_POLICY",
            "allows GR-like Newton limit without claiming measured G is derived",
        ),
    ]
    return [
        {
            **base(stamp),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement_or_derivation": statement,
            "status": status,
            "impact": impact,
            "claim_allowed": False,
        }
        for theorem_id, claim_piece, statement, status, impact in rows
    ]


def superselection_clause_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "SC3755_0_factorization",
            "Q_parent = Q_dyn x K_global",
            "kappa_eff is not a local dynamical field",
            "UNSIGNED_PARENT_SIGNATURE",
            "derive from parent action/category or retain scalar-kappa residuals",
        ),
        (
            "SC3755_1_no_local_variation",
            "delta_local kappa_eff = 0",
            "compact local variations cannot move the coupling",
            "PASS_IF_SC3755_0_SIGNED",
            "blocks scalar-tensor local force",
        ),
        (
            "SC3755_2_trivial_MTS_action",
            "partial_Z/IQ/C/D kappa_eff = 0",
            "motion/memory/domain/projector variables do not label G",
            "PASS_IF_K_GLOBAL_TRIVIAL",
            "blocks domain/range/preferred-location coupling hair",
        ),
        (
            "SC3755_3_no_species_label",
            "partial_A/source kappa_eff = 0",
            "species/material/source labels do not label the coupling",
            "PASS_IF_K_GLOBAL_SOURCE_BLIND",
            "blocks kappa contribution to eta_source_AB",
        ),
        (
            "SC3755_4_no_range_time_radial",
            "partial_t,r,lambda kappa_eff = 0",
            "no Gdot, radial G, or kappa-owned fifth force",
            "PASS_IF_K_GLOBAL_NOT_LOCAL_FIELD",
            "blocks local Gdot/R10 from kappa",
        ),
        (
            "SC3755_5_bianchi_same_frame",
            "nabla T_obs=0 for arbitrary same-frame matter",
            "Bianchi can force nabla kappa=0 if kappa is allowed as a scalar coefficient",
            "CONDITIONAL_UNSIGNED",
            "backup theorem, not replacement for parent signature",
        ),
        (
            "SC3755_6_exchange_owned",
            "q_exchange=0 or mapped",
            "Bianchi proof cannot ignore exchange terms",
            "OPEN",
            "delta_kappa_source row remains live if not signed",
        ),
    ]
    return [
        {
            **base(stamp),
            "clause_id": clause_id,
            "required_clause": clause,
            "mathematical_role": role,
            "status": status,
            "fallback_or_next_action": action,
            "claim_allowed": False,
        }
        for clause_id, clause, role, status, action in rows
    ]


def residual_vector_rows(stamp: str) -> list[dict[str, object]]:
    bounds = bound_lookup()
    gdot = bounds.get("KB3530_0_Gdot_product", {})
    wep = bounds.get("KB3530_1_WEP_source_charge", {})
    gamma = bounds.get("KB3530_2_gamma", {})
    beta = bounds.get("KB3530_3_beta", {})
    r10 = bounds.get("KB3530_4_fifth_force_R10", {})
    rows = [
        (
            "KRV3755_0_Gdot",
            "dln_Geff_dt",
            "P8_Geff_time_drift",
            "LLR/Gdot",
            "d/dt ln(kappa_eff)",
            gdot.get("bound_value", "9.6e-15"),
            gdot.get("units", "yr^-1"),
            gdot.get("source_path", ""),
            "MISSING_DTLN_KAPPA_EFF_OR_SUPERSELECTION_ZERO",
        ),
        (
            "KRV3755_1_species_source",
            "eta_source_AB",
            "P8_species_source_charge",
            "MICROSCOPE/WEP",
            "composition/source-label dependence of kappa_eff or k_M",
            wep.get("bound_value", "2.8e-15"),
            wep.get("units", "dimensionless"),
            wep.get("source_path", ""),
            "MISSING_SOURCE_BLIND_KAPPA_OR_ETA_SOURCE_VALUE",
        ),
        (
            "KRV3755_2_range",
            "alpha(lambda)",
            "P8_range_dependence",
            "R10 inverse-square",
            "finite-range coupling branch from local kappa scalar or source-range hair",
            r10.get("bound_value", "alpha(lambda)"),
            r10.get("units", "range-dependent"),
            r10.get("source_path", ""),
            "MISSING_NO_RANGE_THEOREM_OR_ALPHA_LAMBDA_CURVE",
        ),
        (
            "KRV3755_3_radial",
            "partial_r_ln_mu_obs",
            "P8_radial_source_hair",
            "orbital/R10/radial source profile",
            "radial dependence of G_eff*M_eff*(1+epsilon_mu)",
            "zero_or_mapped_bound",
            "inverse_length_or_dimensionless_envelope",
            "source-intake\\mts_residuals\\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
            "MISSING_RADIAL_PROFILE_OR_NO_RADIAL_HAIR_THEOREM",
        ),
        (
            "KRV3755_4_delta_kappa_exchange",
            "delta_kappa_source",
            "P8_Bianchi_kappa_exchange",
            "PPN/R10/local exchange",
            "kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]",
            "same-frame theorem or explicit exchange coefficient",
            "projected_force_density_or_dimensionless_normalized_residual",
            str(source_paths()["SRC3755_7_delta_kappa"]),
            "MISSING_ARENA_PROJECTION_OR_DERIVED_ZERO_EXCHANGE",
        ),
        (
            "KRV3755_5_frame",
            "delta_frame_source",
            "P8_frame_calibration_split",
            "WEP/clock/preferred-frame",
            "source frame differs from orbital/clock frame",
            "zero_or_row_locks",
            "dimensionless",
            "source-intake\\mts_residuals\\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
            "MISSING_SAME_FRAME_SOURCE_THEOREM_OR_FRAME_RESIDUAL",
        ),
        (
            "KRV3755_6_gamma",
            "gamma_minus_1",
            "R3_gamma",
            "Cassini/Shapiro",
            "metric/source/readout/non-EH vector after coupling calibration",
            gamma.get("bound_value", "2.3e-05"),
            gamma.get("units", "dimensionless"),
            gamma.get("source_path", ""),
            "MISSING_FULL_PPN_VECTOR_PROJECTION",
        ),
        (
            "KRV3755_7_beta",
            "delta_beta_source",
            "P8_nonlinear_beta_source_residue",
            "PPN beta",
            "second-order source-normalization residue",
            beta.get("bound_value", "7.8e-05"),
            beta.get("units", "dimensionless"),
            beta.get("source_path", ""),
            "MISSING_SECOND_ORDER_SOURCE_THEOREM_OR_VALUE",
        ),
    ]
    return [
        {
            **base(stamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "component_id": component_id,
            "arena": arena,
            "prediction_formula_or_meaning": formula,
            "bound_value": bound,
            "units": units,
            "bound_source_path": source_path,
            "prediction_status": prediction_status,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, component_id, arena, formula, bound, units, source_path, prediction_status in rows
    ]


def claim_gate_rows(stamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(bool(row["exists"]) for row in grouped["sources"])
    bianchi = any(row["theorem_id"] == "KT3755_2_bianchi_arbitrary_source" for row in grouped["theorems"])
    residuals = len(grouped["residuals"]) == 8
    gates = [
        ("CG3755_0_sources", "all 3755 source paths exist", all_sources, "path hygiene"),
        ("CG3755_1_superselection_signature", "parent K_global signature sourced", False, "contract exists but parent action has not signed it"),
        ("CG3755_2_bianchi_lemma", "Bianchi arbitrary-source lemma written", bianchi, "conditional theorem recorded"),
        ("CG3755_3_same_frame_conservation", "same-frame separate conservation signed", False, "still conditional"),
        ("CG3755_4_exchange_zero", "kappa exchange owners zero/mapped", False, "delta_kappa_source remains live"),
        ("CG3755_5_derivative_silence", "all local derivatives of G_eff vanish by proof", False, "requires CG3755_1 or 3+4"),
        ("CG3755_6_residual_vector", "coupling residual vector emitted", residuals, "Gdot/WEP/R10/radial/frame/gamma/beta rows"),
        ("CG3755_7_newton_claim", "Newton source calibration claim allowed", False, "constant coupling and mu_extra still open"),
        ("CG3755_8_local_gr_claim", "local GR/PPN claim allowed", False, "second-order and full residual vector still open"),
    ]
    return [
        {
            **base(stamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3755_0_theorem_status",
            "BIANCHI_LEMMA_DERIVED_PARENT_SUPERSELECTION_UNSIGNED",
            "3755 derives the conditional Bianchi route to nabla kappa=0, but parent K_global superselection is not signed by the corpus.",
        ),
        (
            "DEC3755_1_residual_status",
            "COUPLING_RESIDUAL_VECTOR_EMITTED",
            "Failed kappa premises now activate Gdot, WEP/source charge, R10 alpha(lambda), radial hair, frame, gamma, and beta rows.",
        ),
        (
            "DEC3755_2_best_next",
            "NO_FLUX_EXCHANGE_OR_EXECUTABLE_RUNNER",
            "The next highest-leverage target is either proving q_exchange/Phi_side vanish or building the residual runner that scores the emitted rows.",
        ),
        (
            "DEC3755_3_G_policy",
            "DO_NOT_CLAIM_NUMERICAL_G",
            "Even if kappa is derivative-silent, absolute G remains a calibration unless parent normalization predicts it.",
        ),
    ]
    return [
        {
            **base(stamp),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def next_target_rows(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(stamp),
            "next_id": "NEXT3755_0",
            "target_doc": "3756-Y5-R2FR-no-flux-projected-exchange-or-coupling-runner.md",
            "target_script": "scripts/Y5_R2FR_3756_no_flux_projected_exchange_or_coupling_runner.py",
            "objective": "prove Phi_side=0 and Pi_M q_exchange=0 for the source-charge Ward balance, or create a dry-run coupling residual runner over the 3755 Gdot/WEP/R10/radial/frame/gamma/beta rows",
            "why_this_next": "3755 shows constant coupling alone is not enough; Newton calibration also needs no projected exchange/source flux or executable residual scoring",
            "claim_allowed": False,
        }
    ]


def status_rows(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(stamp),
            "status_id": "STATUS3755_0",
            "status": "BIANCHI_KAPPA_LEMMA_DERIVED_SUPERSELECTION_UNSIGNED_RESIDUAL_VECTOR_EMITTED",
            "summary": "3755 derives the conditional Bianchi arbitrary-source route to derivative-silent kappa and emits executable nonclaim coupling residual rows. Parent K_global superselection remains unsigned, so no Newton/local-GR claim is allowed.",
            "claim_allowed": False,
        }
    ]


def validation_rows(stamp: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    checks = [
        ("sources_exist", "all 3755 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("csv_parse", "all generated CSVs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("bianchi_lemma", "Bianchi arbitrary-source lemma emitted", any(row["theorem_id"] == "KT3755_2_bianchi_arbitrary_source" for row in grouped["theorems"])),
        ("exchange_counterbranch", "exchange fallback retained", any(row["theorem_id"] == "KT3755_3_exchange_fallback" for row in grouped["theorems"])),
        ("superselection_unsigned", "K_global signature remains unsigned", any(row["clause_id"] == "SC3755_0_factorization" and row["status"] == "UNSIGNED_PARENT_SIGNATURE" for row in grouped["clauses"])),
        ("residual_vector", "eight residual rows emitted", len(grouped["residuals"]) == 8),
        ("gdot_bound", "Gdot bound row carries numeric bound", any(row["residual_id"] == "KRV3755_0_Gdot" and row["bound_value"] == "9.6e-15" for row in grouped["residuals"])),
        ("wep_bound", "WEP source row carries numeric bound", any(row["residual_id"] == "KRV3755_1_species_source" and row["bound_value"] == "2.8e-15" for row in grouped["residuals"])),
        ("local_claim_blocked", "local GR claim remains false", any(row["gate_id"] == "CG3755_8_local_gr_claim" and row["passed"] is False for row in grouped["gates"])),
        ("next_target", "3756 target emitted", grouped["next"][0]["target_doc"] == "3756-Y5-R2FR-no-flux-projected-exchange-or-coupling-runner.md"),
        ("no_formalization_leak", "no 3755 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3755*"))),
    ]
    return [
        {
            **base(stamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3755 — Global Kappa Superselection Or Coupling Residual Vector",
        "",
        "## Status",
        "",
        "`BIANCHI_KAPPA_LEMMA_DERIVED_SUPERSELECTION_UNSIGNED_RESIDUAL_VECTOR_EMITTED`.",
        "",
        "This checkpoint separates the honest theorem from the claim. Bianchi can force derivative-silent coupling only under same-frame, separately conserved, arbitrary-source conditions; otherwise the kappa exchange term is physical and must be scored.",
        "",
        "## Kappa Theorem Rows",
    ]
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['claim_piece']} — {row['impact']}")
    lines.extend(["", "## Superselection Clauses"])
    for row in grouped["clauses"]:
        lines.append(f"- `{row['clause_id']}` `{row['status']}`: {row['required_clause']} -> {row['fallback_or_next_action']}")
    lines.extend(["", "## Coupling Residual Vector"])
    for row in grouped["residuals"]:
        lines.append(
            f"- `{row['residual_id']}` `{row['prediction_status']}`: `{row['symbol']}` arena `{row['arena']}` bound `{row['bound_value']} {row['units']}`"
        )
    lines.extend(["", "## Claim Gates"])
    for row in grouped["gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}`: {row['meaning']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["sources"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    stamp = ts()
    paths = {
        "doc": DOC_PATH,
        "sources": RESIDUALS / "P8_Y5_R2FR_3755_SOURCE_REGISTER.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv",
        "clauses": RESIDUALS / "P8_Y5_R2FR_3755_SUPERSELECTION_CLAUSES.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3755_COUPLING_RESIDUAL_VECTOR.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3755_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3755_DECISION_ROWS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3755_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3755_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3755_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(stamp),
        "theorems": theorem_rows(stamp),
        "clauses": superselection_clause_rows(stamp),
        "residuals": residual_vector_rows(stamp),
        "decisions": decision_rows(stamp),
        "next": next_target_rows(stamp),
        "status": status_rows(stamp),
    }
    grouped["gates"] = claim_gate_rows(stamp, grouped)
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(stamp, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3755 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3755 checkpoint: Bianchi kappa lemma derived conditionally; coupling residual vector emitted")


if __name__ == "__main__":
    main()
