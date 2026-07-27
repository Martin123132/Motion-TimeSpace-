from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3676"
BRANCH_ID = "MTS_R2FR_Y5_NO_NATURAL_MARKER_NO_REENTRY_OR_CFXR_PRIOR_3676"
DOC = ROOT / "3676-Y5-R2FR-no-natural-marker-no-reentry-theorem-or-FXR-prior-row.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3675", RESIDUALS / "P8_Y5_R2FR_3675_NEXT_TARGET.csv", "no-natural-marker", "3675 selected this target"),
        ("doc_3675", ROOT / "3675-Y5-R2FR-quotient-descent-no-FXR-signature-or-finite-coefficient-source.md", "c_FXR = A_H*F0_prime/(1+A_H*F0)", "finite c_FXR branch definition"),
        ("signature_3675", RESIDUALS / "P8_Y5_R2FR_3675_NO_FXR_SIGNATURE_AUDIT.csv", "SIG3675_2_no_FXR_slot", "unsigned no-FXR slot"),
        ("coefficient_3675", RESIDUALS / "P8_Y5_R2FR_3675_FINITE_FXR_COEFFICIENT_SOURCE_ROWS.csv", "FCS3675_4_cFXR", "missing parent coefficient ledger"),
        ("bounds_3675", RESIDUALS / "P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv", "c_FXR", "inherited finite c_FXR bound rows"),
        ("doc_413", ROOT / "413-no-marker-parent-action-theorem-attempt.md", "co_moving_material_marker", "fixed-spurion-only partial no-marker result"),
        ("doc_423", ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md", "The current corpus does not yet prove the universal property or the no-natural-marker theorem.", "no-extension theorem attempt"),
        ("doc_965", ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md", "local invariant algebra", "primitive quotient/no-natural-marker sweep"),
        ("theorem_965", RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv", "PQ965_5_verdict", "primitive quotient theorem not proven"),
        ("algebra_965", RESIDUALS / "P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv", "ALG965_9_verdict", "local invariant algebra not derived"),
        ("markers_965", RESIDUALS / "P8_Y5_R10_965_MARKER_COUNTERMODEL_REVIEW.csv", "MC965_1_comoving_material_marker", "live marker countermodels"),
        ("nxhat_prior_2965", RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIRST_PRIOR_SLOT_NONCLAIM.csv", "NONCLAIM_UNTIL_SOURCE_BACKED", "prior slot policy precedent"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def no_natural_marker_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "NMM3676_0_fixed_spurion",
            "fixed active spurion exclusion",
            "a fixed non-orbit label cannot be a function on a strict quotient configuration space",
            "CONDITIONAL_PARTIAL_PASS",
            "413/965 conditionally kill fixed active labels if strict quotient parent space is already proven",
            "does not kill transforming material markers, class scalars, species constants, or readout markers",
            "useful anti-cheat result only; not enough to set c_FXR=0",
            "source-sign strict quotient parent field list and show the actual local branch uses it",
            "413;965",
            False,
        ),
        (
            "NMM3676_1_primitive_quotient",
            "primitive quotient object",
            "Q_MTS is the minimal/free object generated by motion, time, and space, not an arbitrary selected submodel",
            "NOT_DERIVED",
            "423 and 965 name this as the required universal-property theorem",
            "Q_tilde=(Q,m)/G_rel remains a covariant extension",
            "no-extension cannot be promoted from preference to theorem",
            "define the category, morphisms, allowed matter pullbacks, and prove initial/minimal object status",
            "423;965",
            False,
        ),
        (
            "NMM3676_2_material_marker",
            "co-moving material marker exclusion",
            "any matter-carried marker is pure gauge, universal auxiliary, stress-free topology, or absent",
            "NOT_PROVEN_LIVE_COUNTERMODEL",
            "413/423 classify transforming material markers as legal extended theories",
            "co-moving material marker can generate source charge, WEP pressure, or fifth-force numerator",
            "source-side zero remains closure-only",
            "prove parent no-extension theorem or retain explicit marker-coupling coefficients",
            "413;423;965",
            False,
        ),
        (
            "NMM3676_3_quotient_class_scalar",
            "quotient-invariant class scalar silence",
            "every quotient-invariant local scalar beyond observed geometry jets is constant, gauge, or locally silent",
            "NOT_DERIVED",
            "965 local invariant algebra keeps finite-cell, domain, memory, orientation/time-arrow, and class scalar generators live",
            "F(sigma)R is technically admissible and can masquerade as c_FXR",
            "no-natural-marker theorem fails at the local invariant algebra",
            "attack generator elimination one by one, starting with the one entering the F(X)R slot",
            "965",
            False,
        ),
        (
            "NMM3676_4_species_constants",
            "constant-sector universality",
            "matter constants and source coefficients cannot depend on species, domain, or marker class",
            "NOT_UNIVERSALIZED",
            "965 keeps species/source constants as live local generators",
            "WEP, source-charge, clock, and EM residual rows can reappear",
            "finite coefficient branches cannot be scored as universal",
            "derive constant-sector universality or retain product bounds for each source class",
            "965",
            False,
        ),
        (
            "NMM3676_5_readout_marker",
            "post-readout marker exclusion",
            "readout is performed after variation and cannot be varied as a reduced marker-dependent action",
            "NO_CHEAT_RULE_ONLY",
            "413/965 block this as policy, not as a parent theorem",
            "a reduced readout action can reintroduce active projector or Hessian terms",
            "readout-zero cannot be counted as theorem-zero",
            "prove exact parent readout-after-variation theorem",
            "413;965",
            False,
        ),
        (
            "NMM3676_6_verdict",
            "primitive quotient/no-natural-marker theorem",
            "NMM3676_0 through NMM3676_5 close with no live marker countermodels",
            "THEOREM_NOT_PROVED_CURRENT_CORPUS",
            "fixed active spurion exclusion is real but too narrow",
            "material marker, quotient class scalar, species constants, and readout marker remain live",
            "cannot set c_FXR=0 from no-natural-marker logic",
            "take finite c_FXR branch unless a specific generator-elimination proof closes",
            "3675;413;423;965",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "theorem_piece": theorem_piece,
            "attempted_statement": attempted_statement,
            "current_status": current_status,
            "evidence_summary": evidence_summary,
            "live_counterexample": live_counterexample,
            "consequence": consequence,
            "needed_to_close": needed_to_close,
            "source_refs": source_refs,
            "source_signed": source_signed,
        }
        for (
            audit_id,
            theorem_piece,
            attempted_statement,
            current_status,
            evidence_summary,
            live_counterexample,
            consequence,
            needed_to_close,
            source_refs,
            source_signed,
        ) in specs
    ]


def no_reentry_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RE3676_0_operator_grammar",
            "gravity operator grammar contains no F(X)R slot",
            "UNSIGNED",
            "3675 SIG3675_2 says the slot is not banned; 965 keeps quotient-invariant class scalars live",
            "marker-prefactor F(sigma)R or F(Xhat)R",
            "no c_FXR zero",
            "parent operator grammar or action derivation",
            False,
        ),
        (
            "RE3676_1_auxiliary_integrated_out",
            "integrated-out sectors cannot regenerate R times a local scalar",
            "UNSIGNED",
            "3675 SIG3675_3 keeps integrated-out scalar/projector re-entry live",
            "universal auxiliary or scalar mode that leaves an R*X effective term",
            "finite residual coefficient must be retained",
            "Delta S_eff no-reentry theorem with source-independent auxiliary solution",
            False,
        ),
        (
            "RE3676_2_memory_nonlocal",
            "nonlocal memory kernels cannot reduce to local F(X)R in the local branch",
            "UNSIGNED",
            "965 keeps memory/class scalar generators live",
            "local limit of nonlocal memory gives a scalar prefactor or Hessian-STF response",
            "local-GR branch remains bounded rather than proven",
            "local memory silence theorem or explicit memory coefficient bound",
            False,
        ),
        (
            "RE3676_3_readout_frame",
            "observed metric/readout has no conformal, disformal, derivative, or boundary Hessian X dependence",
            "UNSIGNED",
            "3675 SIG3675_4 states readout descent is a contract, not parent-signed",
            "g_obs=A(X)q(Phi)+B(X)gradX gradX plus boundary/readout Hessian terms",
            "PPN and clock residuals can re-enter",
            "single public metric theorem with readout-after-variation proof",
            False,
        ),
        (
            "RE3676_4_improved_stress",
            "improved stress/nonminimal matter terms cannot mimic Hessian-STF geometry source",
            "UNSIGNED",
            "3673 demoted ordinary minimal stress but kept improvement/nonminimal routes",
            "matter improvement term produces (g Box - nabla nabla)F",
            "stress route cannot be merged with geometric route",
            "matter action descent plus no-improvement theorem",
            False,
        ),
        (
            "RE3676_5_verdict",
            "no-reentry theorem",
            "THEOREM_NOT_PROVED_CURRENT_CORPUS",
            "operator grammar, auxiliary, memory, readout, and improvement slots remain unsigned",
            "at least one admissible re-entry channel can produce finite c_FXR",
            "c_FXR=0 is not claimed",
            "either close all RE3676_0..4 clauses or source/bound c_FXR",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "reentry_id": reentry_id,
            "clause": clause,
            "current_status": current_status,
            "evidence_summary": evidence_summary,
            "live_reentry_channel": live_reentry_channel,
            "consequence": consequence,
            "needed_to_close": needed_to_close,
            "source_signed": source_signed,
        }
        for (
            reentry_id,
            clause,
            current_status,
            evidence_summary,
            live_reentry_channel,
            consequence,
            needed_to_close,
            source_signed,
        ) in specs
    ]


def strongest_bound() -> dict[str, str]:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv")
    return min(rows, key=lambda row: float(row["xi_H_max"]))


def cfxr_prior_rows(ts: str) -> list[dict[str, object]]:
    strongest = strongest_bound()
    inherited_bound = strongest["finite_coefficient_bound"]
    specs = [
        (
            "CFXRP3676_0_cFXR",
            "c_FXR=A_H*F0_prime/(1+A_H*F0)",
            "dimensionless",
            "finite nonminimal F(X)R Hessian-STF coefficient after EH normalization",
            "symbolic_wide_nonclaim_parent_prior_slot",
            "MISSING_PARENT_PRIOR_OR_OPERATOR_NORMALIZATION",
            "MISSING_PARENT_PRIOR_OR_OPERATOR_NORMALIZATION",
            "MISSING_PARENT_VALUE",
            inherited_bound,
            "A_H;F0;F0_prime;operator normalization;field normalization;no-reentry/readout floor",
            "3675 finite coefficient ledger plus 3676 failed zero theorem",
            "valid only as a named private coefficient slot, not as evidence",
            "derive natural size from parent action or assign an explicit prior before scoring",
        ),
        (
            "CFXRP3676_1_AH",
            "A_H",
            "dimensionless",
            "nonminimal curvature slot amplitude in S_H=(M_*^2/2) int sqrt(-g) A_H F(X) R",
            "component_parent_input",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_VALUE",
            inherited_bound,
            "parent action operator coefficient and normalization convention",
            "3675 FCS3675_0_AH",
            "not sourced",
            "derive from allowed operator grammar or declare nonclaim prior",
        ),
        (
            "CFXRP3676_2_F0",
            "F0",
            "dimensionless",
            "background value F(X0) entering the EH denominator",
            "component_parent_input",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_VALUE",
            inherited_bound,
            "background branch value and denominator positivity condition 1+A_H*F0 != 0",
            "3675 FCS3675_1_F0",
            "not sourced",
            "derive local branch background value or absorb into measured G only with stated policy",
        ),
        (
            "CFXRP3676_3_F0_prime",
            "F0_prime",
            "per normalized X_b",
            "first derivative of F at the local background in the chosen invariant field coordinate",
            "component_parent_input",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_VALUE",
            inherited_bound,
            "field coordinate, local background, and parent function F",
            "3675 FCS3675_2_F0_prime",
            "not sourced",
            "derive double-zero/no-linear-term law or keep finite branch",
        ),
        (
            "CFXRP3676_4_fEM_over_ZX",
            "f_EM/Z_X",
            "dimensionless product in xi_FXR",
            "EM stress-to-X transfer amplitude divided by X kinetic normalization",
            "component_parent_input",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_PRIOR",
            "MISSING_PARENT_VALUE",
            inherited_bound,
            "EM coupling, field normalization, and source transfer kernel",
            "3675 FCS3675_5_xiFXR",
            "not sourced",
            "source the EM/current coupling or bound the product directly",
        ),
    ]
    return [
        {
            **base(ts),
            "prior_id": prior_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "prior_type": prior_type,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "central_value": central_value,
            "inherited_strictest_bound": inherited_bound,
            "required_parent_inputs": required_parent_inputs,
            "source_basis": source_basis,
            "source_status": source_status,
            "valid_for_claim": False,
            "score_ready": False,
            "claim_allowed": False,
            "next_action": next_action,
        }
        for (
            prior_id,
            symbol,
            units,
            definition,
            prior_type,
            lower_bound,
            upper_bound,
            central_value,
            inherited_bound,
            required_parent_inputs,
            source_basis,
            source_status,
            next_action,
        ) in specs
    ]


def countermodel_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CMC3676_0_fixed_active_spurion", "fixed active label/projector", "CONDITIONALLY_EXCLUDED_ONLY", "strict quotient kills fixed non-orbit labels if signed", "not enough for no-marker theorem"),
        ("CMC3676_1_comoving_material_marker", "co-moving material marker", "LIVE", "transforms covariantly and descends to an extended quotient", "blocks source-side zero"),
        ("CMC3676_2_quotient_scalar", "quotient-invariant scalar sigma(Q)", "LIVE", "already a quotient function, so covariance does not remove it", "can produce F(sigma)R and c_FXR"),
        ("CMC3676_3_domain_selector", "domain/class selector chi_D", "LIVE", "local trivial class is not derived", "can turn local/cosmology split into an axiom"),
        ("CMC3676_4_species_constant", "species/source constants", "LIVE", "constant-sector universality is not proven", "WEP/source-charge/clock pressure"),
        ("CMC3676_5_post_readout_EFT", "post-readout reduced action marker", "POLICY_BLOCKED_NOT_THEOREM_BLOCKED", "no-cheat rule exists but parent theorem is absent", "closure-zero can be mistaken for theorem-zero"),
        ("CMC3676_6_universal_auxiliary", "universal auxiliary", "CONDITIONALLY_SAFE_NOT_DERIVED", "safe only if unique source-independent solution reduces to constants", "otherwise regenerates scalar force or non-EH operator"),
        ("CMC3676_7_topological_marker", "topological/boundary marker", "CONDITIONALLY_SAFE_NOT_DERIVED", "safe only if no local stress, no matter vertex, no exchange leakage", "can carry boundary/domain information"),
    ]
    return [
        {
            **base(ts),
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "current_status": current_status,
            "why_survives_or_is_killed": why_survives_or_is_killed,
            "damage": damage,
            "required_blocker": "derive blocker or retain explicit nonclaim coefficient",
        }
        for countermodel_id, countermodel, current_status, why_survives_or_is_killed, damage in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3676_0_no_marker_zero", "set c_FXR=0 by no-natural-marker theorem", "BLOCKED_NONCLAIM", "NMM3676_6 theorem verdict is not proved"),
        ("CG3676_1_no_reentry_zero", "set c_FXR=0 by no-reentry theorem", "BLOCKED_NONCLAIM", "RE3676_5 theorem verdict is not proved"),
        ("CG3676_2_finite_cFXR_score", "score finite c_FXR branch", "BLOCKED_NONCLAIM", "c_FXR prior row has MISSING_PARENT_PRIOR and no numeric value"),
        ("CG3676_3_local_GR", "claim local-GR/PPN pass", "BLOCKED_NONCLAIM", "finite source coupling remains symbolic and zero theorem unsigned"),
        ("CG3676_4_github_or_public", "public claim or GitHub promotion", "BLOCKED_PRIVATE", "this is a private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str, priors: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "NO_NATURAL_MARKER_AND_NO_REENTRY_THEOREMS_NOT_PROVED_CFXR_NONCLAIM_PRIOR_ROW_STAGED",
            "summary": "3676 tests the two possible zero routes for c_FXR. Fixed spurions remain conditionally excluded, but material markers, quotient scalars, species constants, readout markers, auxiliary sectors, memory kernels, and improvement terms stay live. Therefore c_FXR=0 is not claimed and a finite nonclaim c_FXR prior/source slot is staged.",
            "claim_ceiling": "no local-GR, PPN, WEP/R10, fifth-force, EH/Newton, c_FXR zero, or finite c_FXR evidence claim is made",
            "useful_result": f"c_FXR is now the explicit parent-owned coupling to derive/source; strictest inherited template remains {priors[0]['inherited_strictest_bound']}",
            "next_missing_piece": "derive a parent normalization/natural-size law for c_FXR or eliminate one live local invariant generator",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3676_0",
            "target_doc": "3677-Y5-R2FR-cFXR-parent-normalization-scale-or-local-generator-elimination.md",
            "target_script": "scripts/Y5_R2FR_3677_cFXR_parent_normalization_scale_or_local_generator_elimination.py",
            "objective": "derive a principled parent scale/prior for c_FXR from operator normalization, or eliminate the specific quotient-scalar/readout generator that feeds the F(X)R slot",
            "success_gate": "either c_FXR gets a source-backed/naturalness-prior row without MISSING markers, or a named live generator is theorem-killed with all re-entry clauses signed",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    nmm: list[dict[str, object]],
    reentry: list[dict[str, object]],
    priors: list[dict[str, object]],
    counters: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3676 - No-natural-marker / no-reentry theorem or F(X)R prior row",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint is the anti-circling move: it does not merely say a coupling is missing. It tests the two clean ways the coupling could vanish, rejects promotion where live countermodels remain, and names the exact finite coefficient the parent theory must now own.",
        "",
        "## Result",
        "",
        "- Fixed active spurions are still conditionally excluded by strict quotient logic.",
        "- That exclusion is too narrow: co-moving material markers, quotient-invariant class scalars, species constants, readout markers, auxiliary sectors, memory kernels, and improvement terms remain legal unless extra theorems close.",
        "- Therefore `c_FXR=0` is **not proved**.",
        "- The finite branch is staged as a nonclaim parent coefficient:",
        "",
        "`c_FXR = A_H*F0_prime/(1+A_H*F0)`",
        "",
        f"Strictest inherited private template: `{priors[0]['inherited_strictest_bound']}`.",
        "",
        "## No-natural-marker audit",
    ]
    for row in nmm:
        lines.append(f"- `{row['audit_id']}`: {row['current_status']} - {row['theorem_piece']} -> {row['consequence']}")
    lines.extend(["", "## No-reentry audit"])
    for row in reentry:
        lines.append(f"- `{row['reentry_id']}`: {row['current_status']} - {row['clause']} -> {row['consequence']}")
    lines.extend(["", "## c_FXR prior/source slot"])
    for row in priors:
        lines.append(f"- `{row['prior_id']}`: `{row['symbol']}` [{row['units']}] - {row['source_status']}; next: {row['next_action']}")
    lines.extend(["", "## Live countermodels"])
    for row in counters:
        lines.append(f"- `{row['countermodel_id']}`: {row['current_status']} - {row['countermodel']} ({row['damage']})")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    nmm: list[dict[str, object]],
    reentry: list[dict[str, object]],
    priors: list[dict[str, object]],
    counters: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + nmm + reentry + priors + counters + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3676*", "3676-Y5-R2FR-*", "P8_Y5*3676*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    nmm_ids = {str(row["audit_id"]) for row in nmm}
    reentry_ids = {str(row["reentry_id"]) for row in reentry}
    prior_symbols = {str(row["symbol"]) for row in priors}
    missing_markers = [row for row in priors if "MISSING_" not in str(row["lower_bound"]) and row["prior_id"] != "CFXRP3676_0_cFXR"]

    add("VAL3676_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3676_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3676_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3676 outputs written")
    add("VAL3676_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3676_4_nmm_coverage", {"NMM3676_0_fixed_spurion", "NMM3676_1_primitive_quotient", "NMM3676_2_material_marker", "NMM3676_3_quotient_class_scalar", "NMM3676_4_species_constants", "NMM3676_5_readout_marker", "NMM3676_6_verdict"}.issubset(nmm_ids), "no-natural-marker audit covers required clauses")
    add("VAL3676_5_nmm_not_proved", any(row["audit_id"] == "NMM3676_6_verdict" and row["current_status"] == "THEOREM_NOT_PROVED_CURRENT_CORPUS" for row in nmm), "no-natural-marker theorem is not promoted")
    add("VAL3676_6_reentry_coverage", {"RE3676_0_operator_grammar", "RE3676_1_auxiliary_integrated_out", "RE3676_2_memory_nonlocal", "RE3676_3_readout_frame", "RE3676_4_improved_stress", "RE3676_5_verdict"}.issubset(reentry_ids), "no-reentry audit covers operator, auxiliary, memory, readout, improvement")
    add("VAL3676_7_reentry_not_proved", any(row["reentry_id"] == "RE3676_5_verdict" and row["current_status"] == "THEOREM_NOT_PROVED_CURRENT_CORPUS" for row in reentry), "no-reentry theorem is not promoted")
    add("VAL3676_8_prior_slot", "c_FXR=A_H*F0_prime/(1+A_H*F0)" in prior_symbols and "f_EM/Z_X" in prior_symbols, "c_FXR and transfer product prior slots present")
    add("VAL3676_9_parent_inputs_named", all("MISSING_" in str(row["lower_bound"]) and "MISSING_" in str(row["upper_bound"]) and "MISSING_" in str(row["central_value"]) for row in priors), "all finite prior/source rows explicitly carry missing parent inputs")
    add("VAL3676_10_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3676_11_countermodels_live", any(row["countermodel_id"] == "CMC3676_1_comoving_material_marker" and row["current_status"] == "LIVE" for row in counters) and any(row["countermodel_id"] == "CMC3676_2_quotient_scalar" and row["current_status"] == "LIVE" for row in counters), "material marker and quotient scalar countermodels remain live")
    add("VAL3676_12_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates) and any(row["claim_gate_id"] == "CG3676_3_local_GR" and row["status"] == "BLOCKED_NONCLAIM" for row in gates), "claim gates remain blocked")
    add("VAL3676_13_doc_written", "anti-circling move" in doc_text and "c_FXR=0" in doc_text and "not proved" in doc_text and "nonclaim" in doc_text, "doc records theorem failure and finite nonclaim coefficient")
    add("VAL3676_14_no_formalization_leak", not leaks, "no 3676 checkpoint files in formalization-workbench")
    add("VAL3676_15_next_target", next_target[0]["target_doc"].startswith("3677-") and "cFXR-parent-normalization" in next_target[0]["target_doc"], "3677 parent normalization/generator elimination target selected")
    add("VAL3676_16_no_accidental_numeric_prior", not missing_markers, "no component prior row gained an accidental numeric bound")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    nmm = no_natural_marker_rows(ts)
    reentry = no_reentry_rows(ts)
    priors = cfxr_prior_rows(ts)
    counters = countermodel_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, priors)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3676_SOURCE_REGISTER.csv",
        "nmm": RESIDUALS / "P8_Y5_R2FR_3676_NO_NATURAL_MARKER_THEOREM_AUDIT.csv",
        "reentry": RESIDUALS / "P8_Y5_R2FR_3676_NO_REENTRY_THEOREM_AUDIT.csv",
        "priors": RESIDUALS / "P8_Y5_R2FR_3676_CFXR_PRIOR_SOURCE_ROW.csv",
        "counters": RESIDUALS / "P8_Y5_R2FR_3676_MARKER_COUNTERMODEL_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3676_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3676_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3676_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3676_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["nmm"], nmm)
    write_csv(outputs["reentry"], reentry)
    write_csv(outputs["priors"], priors)
    write_csv(outputs["counters"], counters)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, nmm, reentry, priors, counters, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, nmm, reentry, priors, counters, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3676 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3676 checkpoint with {len(validation)} validation checks; c_FXR zero unsigned, finite nonclaim prior row staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
