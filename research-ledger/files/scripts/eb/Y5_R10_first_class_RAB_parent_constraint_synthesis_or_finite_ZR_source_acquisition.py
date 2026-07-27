from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1267"
TITLE = "1267-Y5-R10-first-class-RAB-parent-constraint-synthesis-or-finite-ZR-source-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIRST_CLASS_SYNTHESIS_PATH = OUT_DIR / f"{PACK_ID}_FIRST_CLASS_SYNTHESIS_ATTEMPT.csv"
DIRAC_CLASSIFICATION_PATH = OUT_DIR / f"{PACK_ID}_DIRAC_CLASSIFICATION_AUDIT.csv"
AUX_SELECTOR_PATH = OUT_DIR / f"{PACK_ID}_AUXILIARY_VS_FIRST_CLASS_SELECTOR.csv"
AP_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_AP1265_CLOSURE_UPDATE.csv"
FINITE_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_ACQUISITION_START.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1267_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def live_intake_counts() -> tuple[int, int, int]:
    raw_dir = RAB_INTAKE_DIR / "raw"
    accepted_dir = RAB_INTAKE_DIR / "accepted"
    docs_dir = RAB_INTAKE_DIR / "docs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    raw_rows = sum(len(read_csv(path)) for path in raw_dir.glob("*.csv"))
    accepted_rows = sum(len(read_csv(path)) for path in accepted_dir.glob("*.csv"))
    docs_rows = sum(len(read_csv(path)) for path in docs_dir.glob("*.csv"))
    return raw_rows, accepted_rows, docs_rows


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        FIRST_CLASS_SYNTHESIS_PATH,
        DIRAC_CLASSIFICATION_PATH,
        AUX_SELECTOR_PATH,
        AP_UPDATE_PATH,
        FINITE_ACQUISITION_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_rows, accepted_rows, docs_rows = live_intake_counts()

    source_register = [
        {
            "source_id": "SRC1267_0_1266_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1266_NEXT_TARGET.csv",
            "needle": "NEXT1266_0_1267",
            "purpose": "handoff to first-class R_AB parent-constraint synthesis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_1_1266_scorecard",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1266_PARENT_ORIGIN_SCORECARD.csv",
            "needle": "MISSING_PARENT_MULTIPLIER_ORIGIN",
            "purpose": "parent-origin blockers to be attacked by 1267",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_2_1266_ap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1266_AP1265_CLAUSE_EVIDENCE_MAP.csv",
            "needle": "AP1265_0_auxiliary_signature",
            "purpose": "AP1265 clauses still needing parent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_3_1265_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_AUXILIARY_ELIMINATION_THEOREM.csv",
            "needle": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "purpose": "conditional auxiliary-elimination theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_4_1248_ansatz",
            "local_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "needle": "minimal `lambda_R C_R` parent-action ansatz",
            "purpose": "prior minimal action and Dirac failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_5_1248_dirac",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_DIRAC_CHECK.csv",
            "needle": "DIR1248_2_preservation",
            "purpose": "preservation and constraint-class blockers from previous Dirac check",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_6_1247_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1247_DIRAC_PARENT_CONTRACT.csv",
            "needle": "DC1247_3_constraint_class",
            "purpose": "Dirac parent contract requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_7_1238_first_class",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1238_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv",
            "needle": "FCR1238_5_verdict",
            "purpose": "earlier first-class route not constructed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_8_nonprop",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "clean closure/holonomic constraint route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_9_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "ordinary current gives Q_R hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_10_gauge_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "Noether structure can explain a constraint only after the parent action has",
            "purpose": "Noether route cannot invent constraint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1267_11_finite_template",
            "local_path": "source-intake/rab-sector/docs/ZR1264_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1264_TEMPLATE_DO_NOT_SCORE",
            "purpose": "finite-ZR nonclaim row template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    first_class_synthesis = [
        {
            "attempt_id": "FCS1267_0_target",
            "candidate": "first-class parent constraint directly setting C_R=R_AB=0",
            "construction": "seek G_R with first-class algebra, no Q_R charge, and matter/readout invariance",
            "test_result": "TARGET_SHARP",
            "why_not_closed": "requires more than lambda_R C_R; must exhibit gauge generator and invariant readout",
            "route_effect": "would derive local reciprocity if passed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCS1267_1_multiplier_constraint",
            "candidate": "S += integral lambda_R C_R",
            "construction": "variation of lambda_R gives C_R=0",
            "test_result": "HOLONOMIC_CONSTRAINT_NOT_FIRST_CLASS",
            "why_not_closed": "it imposes the closure but does not itself supply a gauge redundancy or parent necessity",
            "route_effect": "useful as second-class/auxiliary compatibility if parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCS1267_2_gauge_shift",
            "candidate": "make C_R a gauge coordinate and use C_R=0 as gauge fixing",
            "construction": "introduce a generator Pi_R so delta C_R=epsilon and physical variables are quotient-invariant",
            "test_result": "FAILS_CURRENT_MATTER_READOUT",
            "why_not_closed": "the current corpus does not prove clocks, rods, sources, and local metric readout are invariant under this split shift",
            "route_effect": "would make C_R=0 a gauge choice, not a physical equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCS1267_3_presymplectic_auxiliary",
            "candidate": "C_R has no symplectic direction and is eliminated as compatibility data",
            "construction": "treat R_AB/lambda_R as algebraic auxiliaries with no derivative, boundary, matter, or readout regeneration",
            "test_result": "PROMISING_BUT_NOT_PARENT_SIGNED",
            "why_not_closed": "this is the 1265 theorem route; it still needs AP1265_0 through AP1265_4 signed by the parent grammar",
            "route_effect": "best derivation route after first-class category failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCS1267_4_stueckelberg",
            "candidate": "add compensator sigma and impose C_R-sigma=0",
            "construction": "make a formal gauge pair with sigma absorbing the C_R shift",
            "test_result": "REJECT_AS_SMUGGLING_RISK",
            "why_not_closed": "adds an unowned field and moves the closure into sigma/readout unless a parent source for sigma exists",
            "route_effect": "not cleaner than finite residual acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCS1267_5_verdict",
            "candidate": "construct first-class R_AB zero theorem from current sources",
            "construction": "combine 1238/1247/1248/1266 sources and test the category",
            "test_result": "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
            "why_not_closed": "the direct hard constraint is second-class/auxiliary, while the gauge route requires new invariant readout and source functor",
            "route_effect": "shift derivation target to parent-signed second-class auxiliary compatibility, with finite-ZR fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dirac_classification = [
        {
            "check_id": "DIR1267_0_variables",
            "assumption": "if R_AB is admitted as an independent local coordinate R",
            "constraint_chain": "Pi_lambda≈0 from no dot(lambda_R); C_R=R≈0 from preserving Pi_lambda",
            "poisson_test": "{Pi_R(x), C_R(y)} = delta(x-y) if Pi_R exists",
            "classification": "SECOND_CLASS_OR_HOLONOMIC_NOT_FIRST_CLASS",
            "claim_effect": "C_R=0 can be an auxiliary compatibility condition but not a first-class theorem by itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1267_1_multiplier_only",
            "assumption": "lambda_R C_R is simply added to a schematic H_core",
            "constraint_chain": "Pi_lambda≈0 -> C_R≈0; preserving C_R requires {C_R,H_core}≈0 or fixes a multiplier",
            "poisson_test": "preservation cannot be evaluated without H_core and brackets for T,S/e_pub",
            "classification": "FORMAL_SECONDARY_ONLY",
            "claim_effect": "repeats 1248: primary/secondary work inside ansatz but do not parent-sign the route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1267_2_first_class_possibility",
            "assumption": "a true gauge generator G_R exists",
            "constraint_chain": "first-class constraint would be momentum-like generator Pi_C≈0; C_R=0 would be gauge fixing",
            "poisson_test": "{Pi_C, H_parent}≈0 and all matter/readout observables commute with Pi_C",
            "classification": "POSSIBLE_ONLY_WITH_NEW_GAUGE_READOUT",
            "claim_effect": "not in current corpus; would require new parent gauge symmetry and invariant public metric/readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1267_3_auxiliary_pair",
            "assumption": "R_AB/lambda_R are parent-owned algebraic auxiliaries, not physical coordinates",
            "constraint_chain": "E_lambda: C_R=0; E_R: lambda_R plus any R-source vanishes; no R symplectic sector remains after elimination",
            "poisson_test": "Dirac matrix may be nonzero; that is acceptable for second-class auxiliary elimination",
            "classification": "BEST_DERIVATION_CATEGORY_IF_PARENT_SIGNED",
            "claim_effect": "can close Z_R=0 without first-class gauge, but only after AP1265 protection clauses are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1267_4_boundary_current",
            "assumption": "R_AB is treated as a conserved-current field instead of auxiliary",
            "constraint_chain": "partial_r(W partial_r R_AB)=0 -> W R_AB'=Q_R",
            "poisson_test": "Q_R remains an exterior charge unless a boundary/source theorem kills it",
            "classification": "FINITE_RESIDUAL_BRANCH",
            "claim_effect": "requires Z_R/J_R/B_R and arena projection source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    aux_selector = [
        {
            "selector_id": "SEL1267_0_first_class",
            "route": "first-class gauge route",
            "required_signature": "gauge generator, bracket closure, invariant matter/readout, no boundary charge",
            "1267_status": "NOT_CONSTRUCTED",
            "next_if_selected": "write new parent gauge theory before any local-GR claim",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "selector_id": "SEL1267_1_second_class_auxiliary",
            "route": "second-class/algebraic auxiliary compatibility",
            "required_signature": "parent field list excludes R_AB as physical; lambda_R C_R is required; no D R_AB, matter source, boundary charge, or readout regeneration",
            "1267_status": "BEST_DERIVATION_ROUTE_NOT_YET_SIGNED",
            "next_if_selected": "prove parent-signed compatibility action and AP1265 clauses",
            "selected_now": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "selector_id": "SEL1267_2_finite_residual",
            "route": "finite or massive/suppressed R_AB residual",
            "required_signature": "source-backed Z_R, M_R^2, J_R, B_R, tau_R10, tau_PPN, tau_clock, tau_orbital rows",
            "1267_status": "FALLBACK_ACQUISITION_STARTED_NONCLAIM",
            "next_if_selected": "populate finite rows from parent coefficients or empirical bounds before scoring",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ap_update = [
        {
            "clause_id": "AP1265_0_auxiliary_signature",
            "1267_update": "first-class route fails as category, but auxiliary/second-class compatibility is the better target",
            "evidence": "DIR1267_3_auxiliary_pair",
            "remaining_gap": "parent must still require lambda_R C_R rather than insert it as closure",
            "updated_status": "REFOCUSED_TO_SECOND_CLASS_PARENT_SIGNATURE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_1_no_derivatives",
            "1267_update": "omitting D R_AB is consistent with auxiliary classification",
            "evidence": "FCS1267_3_presymplectic_auxiliary",
            "remaining_gap": "object-language operator ban is not derived",
            "updated_status": "NEEDS_TYPED_OPERATOR_EXCLUSION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_2_eliminability",
            "1267_update": "second-class/algebraic elimination is enough; first-class gauge is not necessary",
            "evidence": "DIR1267_0_variables; DIR1267_3_auxiliary_pair",
            "remaining_gap": "must prove no extra R-source in E_R and no determinant/readout remnant",
            "updated_status": "EXACT_IF_PARENT_AUXILIARY_BLOCK_COMPLETE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_3_boundary_silence",
            "1267_update": "boundary current route remains live if auxiliary proof fails",
            "evidence": "DIR1267_4_boundary_current",
            "remaining_gap": "Q_R=0 or B_R=0 still lacks theorem",
            "updated_status": "BOUNDARY_ZERO_STILL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_4_readout_stability",
            "1267_update": "gauge route would require invariant readout; auxiliary route requires no regeneration after elimination",
            "evidence": "FCS1267_2_gauge_shift; DIR1267_3_auxiliary_pair",
            "remaining_gap": "readout/EFT closure theorem is absent",
            "updated_status": "READOUT_CLOSURE_STILL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_acquisition = [
        {
            "row_id": "FZA1267_0_ZR",
            "needed_quantity": "Z_R",
            "meaning": "kinetic coefficient for finite R_AB residual if auxiliary proof fails",
            "units_required": "parent action normalized coefficient units or dimensionless normalized row",
            "source_requirement": "MISSING_SOURCE_BACKED_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_1_MR2",
            "needed_quantity": "M_R^2",
            "meaning": "local mass/Hessian for Yukawa or suppression branch",
            "units_required": "inverse length squared in stated convention",
            "source_requirement": "MISSING_PARENT_HESSIAN_OR_BOUND",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_2_JR",
            "needed_quantity": "J_R",
            "meaning": "bulk matter/source forcing of R_AB",
            "units_required": "same normalization as E_R equation",
            "source_requirement": "MISSING_MATTER_DESCENT_OR_SOURCE_COEFFICIENT",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_3_BR",
            "needed_quantity": "B_R or Pi_R^n",
            "meaning": "boundary/corner reciprocal charge source",
            "units_required": "boundary momentum/charge normalization",
            "source_requirement": "MISSING_BOUNDARY_ZERO_THEOREM_OR_FLUX_BOUND",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_4_tau_R10",
            "needed_quantity": "tau_R10",
            "meaning": "projection from finite R_AB residual to short-range force/R10 alpha-lambda arena",
            "units_required": "dimensionless transfer or stated kernel units",
            "source_requirement": "MISSING_R10_ARENA_PROJECTION",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_5_tau_PPN",
            "needed_quantity": "tau_PPN",
            "meaning": "projection to gamma/beta/light-bending/Shapiro/orbital residual vector",
            "units_required": "dimensionless transfer to PPN residuals",
            "source_requirement": "MISSING_PPN_ARENA_PROJECTION",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_6_tau_clock",
            "needed_quantity": "tau_clock",
            "meaning": "projection to clock/spectroscopy readout residual",
            "units_required": "dimensionless or Hz/fractional-frequency convention",
            "source_requirement": "MISSING_CLOCK_ARENA_PROJECTION",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FZA1267_7_tau_orbital",
            "needed_quantity": "tau_orbital",
            "meaning": "projection to perihelion/timing/local orbital systems",
            "units_required": "dimensionless transfer or acceleration convention",
            "source_requirement": "MISSING_ORBITAL_ARENA_PROJECTION",
            "current_status": "SOURCE_NEEDED_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1267_0_first_class",
            "claim": "first-class R_AB parent constraint is constructed",
            "status": "BLOCKED",
            "reason": "hard C_R=0 multiplier route is second-class/auxiliary; gauge route needs new invariant matter/readout structure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1267_1_auxiliary_zero",
            "claim": "second-class/auxiliary R_AB elimination proves Z_R=0",
            "status": "BLOCKED",
            "reason": "best route is identified but AP1265 parent signature, boundary silence, and readout closure are still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1267_2_finite_acquisition",
            "claim": "finite-ZR acquisition has started as nonclaim source checklist",
            "status": "PASS_NONCLAIM",
            "reason": "required Z_R/M_R2/J_R/B_R and arena projection rows are listed but no scoring row is accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1267_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither auxiliary theorem-zero nor finite residual inputs are claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1267_0_first_class_category",
            "decision": "do not keep calling the hard R_AB=0 condition first-class without a gauge generator",
            "because": "Dirac classification says lambda_R C_R is holonomic/second-class or auxiliary, not a first-class gauge theorem",
            "status": "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
            "next_action": "pursue second-class auxiliary compatibility instead of fake gauge language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1267_1_best_derivation_route",
            "decision": "the best derivation route is parent-signed auxiliary compatibility",
            "because": "a second-class auxiliary pair can eliminate R_AB exactly if parent field list, no-derivative grammar, matter descent, boundary silence, and readout closure are signed",
            "status": "ROUTE_REFOCUSED_NOT_CLAIMED",
            "next_action": "build a parent compatibility action certificate for AP1265_0..4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1267_2_finite_fallback",
            "decision": "finite-ZR acquisition starts but remains nonclaim",
            "because": "if auxiliary compatibility cannot be parent-signed, R_AB residuals need coefficient/source/projection rows",
            "status": "FALLBACK_CHECKLIST_READY",
            "next_action": "only populate raw/accepted rows from real parent coefficients or external source bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1267_0_1268",
            "target_file": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_second_class_auxiliary_compatibility_action_or_finite_ZR_source_row.py",
            "task": "try to construct a parent-signed second-class/algebraic R_AB compatibility action that closes AP1265_0 through AP1265_4; if any clause fails, create the first finite-ZR nonclaim source row template with explicit missing inputs",
            "success_condition": "either all AP1265 clauses are signed by a concrete compatibility-action certificate, or the finite-ZR source-row path is made ready without accepting placeholders",
            "do_not": "do not call a holonomic lambda_R constraint first-class and do not claim local GR from a closure benchmark",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (FIRST_CLASS_SYNTHESIS_PATH, first_class_synthesis),
        (DIRAC_CLASSIFICATION_PATH, dirac_classification),
        (AUX_SELECTOR_PATH, aux_selector),
        (AP_UPDATE_PATH, ap_update),
        (FINITE_ACQUISITION_PATH, finite_acquisition),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    first_class_verdict = any(
        row["attempt_id"] == "FCS1267_5_verdict" and row["test_result"] == "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED"
        for row in first_class_synthesis
    )
    dirac_second_class = any(
        row["check_id"] == "DIR1267_0_variables" and "SECOND_CLASS" in row["classification"]
        for row in dirac_classification
    )
    aux_selected = any(
        row["selector_id"] == "SEL1267_1_second_class_auxiliary"
        and str(row["selected_now"]).strip().lower() == "true"
        for row in aux_selector
    )
    ap_ids = {row["clause_id"] for row in ap_update}
    expected_ap_ids = {
        "AP1265_0_auxiliary_signature",
        "AP1265_1_no_derivatives",
        "AP1265_2_eliminability",
        "AP1265_3_boundary_silence",
        "AP1265_4_readout_stability",
    }
    finite_nonclaim_ready = all(
        "SOURCE_NEEDED" in str(row["current_status"]) and is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"])
        for row in finite_acquisition
    )
    claim_gates_safe = all(
        row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"])
        for row in claim_gates
    ) and any(row["gate_id"] == "GATE1267_0_first_class" and row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *first_class_synthesis,
        *dirac_classification,
        *aux_selector,
        *ap_update,
        *finite_acquisition,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1267_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1267_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1267_2_first_class_verdict",
            "first-class route is explicitly not constructed",
            first_class_verdict,
            "FCS1267_5_verdict=FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
        ),
        validation_row(
            "VAL1267_3_dirac_second_class",
            "Dirac audit identifies hard C_R=0 as second-class/holonomic unless new gauge readout exists",
            dirac_second_class,
            "DIR1267_0_variables classification contains SECOND_CLASS",
        ),
        validation_row(
            "VAL1267_4_auxiliary_route_selected",
            "best derivation route is refocused to auxiliary compatibility",
            aux_selected,
            "SEL1267_1_second_class_auxiliary selected_now=True",
        ),
        validation_row(
            "VAL1267_5_ap_clause_coverage",
            "all AP1265 clauses have a 1267 update",
            ap_ids == expected_ap_ids,
            f"covered={len(ap_ids)}; missing={sorted(expected_ap_ids - ap_ids)}",
        ),
        validation_row(
            "VAL1267_6_finite_acquisition_nonclaim",
            "finite-ZR acquisition rows exist but are not scoreable",
            finite_nonclaim_ready and raw_rows == 0 and accepted_rows == 0,
            f"finite_rows={len(finite_acquisition)}; raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}",
        ),
        validation_row(
            "VAL1267_7_claim_gates",
            "claim gates block first-class and local-test claims",
            claim_gates_safe,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1267_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1267_9_next_target_1268",
            "next target routes to auxiliary compatibility action or finite-ZR source row",
            next_target[0]["next_id"] == "NEXT1267_0_1268",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1267_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1267_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1267_12_overall",
            "overall 1267 validation",
            overall_pass,
            "1267 rejects the first-class label for the hard R_AB constraint, refocuses the derivation route to parent-signed second-class auxiliary compatibility, and starts finite-ZR acquisition as a nonclaim fallback",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1267 does not construct a first-class `R_AB=0` parent constraint. More importantly, it shows why that label is probably the wrong target: a hard `lambda_R C_R` condition is naturally holonomic/second-class or auxiliary, not first-class, unless a new gauge generator and invariant matter/readout map are supplied.

**Main progress:** the local-GR derivation route is sharper. The best route is now parent-signed second-class/algebraic auxiliary compatibility: prove `R_AB` is eliminated before readout with no derivative operator, matter source, boundary charge, or readout regeneration. That can still give an exact `Z_R=0` theorem if signed; it just should not be sold as first-class gauge magic.

**No-claim guard:** no `Z_R=0`, local-GR/Newton, R10, PPN, clock, or orbital claim is made. The finite-`Z_R` fallback is only a source-acquisition checklist, not a scored row.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## First-Class Synthesis Attempt
{markdown_table(first_class_synthesis, ["attempt_id", "candidate", "construction", "test_result", "why_not_closed", "route_effect", "valid_for_claim", "claim_allowed"])}

## Dirac Classification Audit
{markdown_table(dirac_classification, ["check_id", "assumption", "constraint_chain", "poisson_test", "classification", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Auxiliary vs First-Class Selector
{markdown_table(aux_selector, ["selector_id", "route", "required_signature", "1267_status", "next_if_selected", "selected_now", "valid_for_claim", "claim_allowed"])}

## AP1265 Closure Update
{markdown_table(ap_update, ["clause_id", "1267_update", "evidence", "remaining_gap", "updated_status", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Acquisition Start
{markdown_table(finite_acquisition, ["row_id", "needed_quantity", "meaning", "units_required", "source_requirement", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
