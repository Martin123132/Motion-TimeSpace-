from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2685"
BRANCH_ID = "Y5_R2FR_PARENT_SOURCE_PREFACTOR_ZERO_THEOREM_MINIMAL_CONTRACT_OR_DELTA_W_FIRST_INPUT_2685"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2685-Y5-R2FR-parent-source-prefactor-zero-theorem-minimal-contract-or-delta-w-first-input.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2685_SOURCE_REGISTER.csv",
    "zero_contract": RESIDUALS / "P8_Y5_R2FR_2685_PARENT_SOURCE_PREFACTOR_ZERO_THEOREM_CONTRACT_NONCLAIM.csv",
    "proof_attempt": RESIDUALS / "P8_Y5_R2FR_2685_ZERO_THEOREM_PROOF_ATTEMPT_LEDGER.csv",
    "failure_clauses": RESIDUALS / "P8_Y5_R2FR_2685_ZERO_THEOREM_FAILURE_CLAUSES.csv",
    "delta_w_contract": RESIDUALS / "P8_Y5_R2FR_2685_DELTA_W_FIRST_INPUT_CONTRACT_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2685_ZERO_OR_DELTA_W_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2685_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2685_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2685_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2685_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2685_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_zero_contract": LOCAL_BOUNDS / "parent_source_prefactor_zero_theorem_contract_2685_NONCLAIM.csv",
    "local_delta_w_contract": LOCAL_BOUNDS / "delta_w_first_input_contract_2685_NONCLAIM.csv",
    "wep_zero_contract": WEP_COEFF / "parent_source_prefactor_zero_theorem_contract_2685_NONCLAIM.csv",
    "wep_delta_w_contract": WEP_COEFF / "delta_w_first_input_contract_2685_NONCLAIM.csv",
    "source_weight_delta_w_contract": SOURCE_WEIGHT / "DELTA_W_FIRST_INPUT_CONTRACT_2685_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2685_2684_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2684_NEXT_TARGET.csv",
        "required_needles": ["NEXT2684_0_selected", "no parent source-prefactor target", "Delta_w_AB remains nonclaim"],
        "purpose": "confirms selected derivation-first 2685 target",
    },
    {
        "source_id": "SRC2685_2679_LINE_OWNER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv",
        "required_needles": ["LOT2679_0_parent_density_line", "LOT2679_2_scalar_endomorphism_collapse", "CONTRACT_READY_PROOF_NOT_CLOSED"],
        "purpose": "imports action-density line-owner contract",
    },
    {
        "source_id": "SRC2685_2680_LINE_BUNDLE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2680_PARENT_LINE_BUNDLE_OBJECT_LANGUAGE_CONTRACT_NONCLAIM.csv",
        "required_needles": ["LBH2680_2_source_prefactor_target_absent", "TARGET_FORBIDDEN_ROUTE_UNSIGNED", "LBH2680_6_verdict"],
        "purpose": "imports line-bundle/source-prefactor target absence contract",
    },
    {
        "source_id": "SRC2685_1479_NO_SOURCE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv",
        "required_needles": ["NST1479_0_target", "TARGET_EXACT", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
        "purpose": "imports no-source-only prefactor typing theorem",
    },
    {
        "source_id": "SRC2685_1480_HOM",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv",
        "required_needles": ["CDH1480_2_target_forbidden", "CDH1480_3_scalar_counterexample", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED"],
        "purpose": "imports Hom exclusion and scalar counterexample",
    },
    {
        "source_id": "SRC2685_1488_CURRENT_CHAIN",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv",
        "required_needles": ["OMSCC1488_0_target", "OMSCC1488_3_prefactor_countermodel", "NOT_CLOSED_WA_RESIDUAL_LOCKED"],
        "purpose": "imports ordinary matter current-chain proof and source-weight countermodel",
    },
    {
        "source_id": "SRC2685_2682_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2682_SOURCE_PREFACTOR_TARGET_NORMAL_FORM_AUDIT.csv",
        "required_needles": ["NF2682_2_source_prefactor_target", "FORBIDDEN_TARGET_CANDIDATE_NOT_SIGNED", "NF2682_7_verdict"],
        "purpose": "imports source-prefactor target normal-form status",
    },
    {
        "source_id": "SRC2685_2683_ZERO_GATES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv",
        "required_needles": ["TZ2683_0_source_prefactor_target_absent", "TZ2683_2_action_line_owner", "THEOREM_ZERO_NOT_PROVED"],
        "purpose": "imports theorem-zero gates",
    },
    {
        "source_id": "SRC2685_2684_PROJECTION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2684_SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
        "required_needles": ["APM2684_0_WEP", "MISSING_WEP_MATERIAL_TENSOR_TAU_AND_PARENT_VALUES", "APM2684_6_total_envelope"],
        "purpose": "imports projection matrix blockers",
    },
    {
        "source_id": "SRC2685_2684_MAP",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2684_COEFFICIENT_TO_ARENA_MAP_NONCLAIM.csv",
        "required_needles": ["CAM2684_1_Delta_w_AB", "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W", "MISSING_TAU_K_QBAR_PROJECTIONS"],
        "purpose": "imports Delta_w coefficient-to-arena blockers",
    },
    {
        "source_id": "SRC2685_MOMS1486",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv",
        "required_needles": ["MOMS1088_4_no_species_weights", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
        "purpose": "imports parent ordinary-matter signature blockers",
    },
    {
        "source_id": "SRC2685_CURRENT1453",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_5_pre_variation_weight", "SURVIVES_PRE_VARIATION", "PARTIAL_THEOREM_NOT_CLOSED"],
        "purpose": "imports current-owner limitation",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def zero_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZTC2685_0_parent_action_domain",
            "zero_theorem_clause": "parent ordinary action domain admits only observable geometry, matter fields, gauge/current data, fixed representation constants and universal constants",
            "formal_role": "removes source-only species/readout/hidden labels from admissible active-source coefficient arguments",
            "if_signed_effect": "Coeff_source-prefactor is not an object of the parent action language",
            "current_status": "ROOT_OBJECT_LANGUAGE_ADMISSIBILITY_NOT_DERIVED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/no_source_only_prefactor_typing_theorem_nonclaim_1479.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive admissible argument list from q-descent/category primitives rather than adopt it",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_1_action_density_line",
            "zero_theorem_clause": "ordinary matter densities live in one parent action-density line before source/readout",
            "formal_role": "collapses relative action-line scalars to common calibration if object-language target is absent",
            "if_signed_effect": "Delta_w_AB becomes zero/common-mode rather than a relative source coupling",
            "current_status": "ACTION_DENSITY_LINE_NOT_PARENT_CONSTRUCTED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "construct A_ord from parent quotient/category primitives",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_2_no_hidden_visible_Hom",
            "zero_theorem_clause": "Hom(C_hid or species/readout labels, Coeff_source-prefactor) is absent or common-constant",
            "formal_role": "prevents c(I_hid), w_A, kappa_A and c_A from feeding active source normalization",
            "if_signed_effect": "hidden/scalar counterexample is killed syntactically rather than by tuning",
            "current_status": "HOM_EXCLUSION_CONDITIONAL_NOT_PARENT_DERIVED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive target absence or hidden invariant algebra triviality",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_3_ordinary_subaction_descent",
            "zero_theorem_clause": "S_ord descends through q_obs/coframe and fixed theta_A before source/readout",
            "formal_role": "makes vertical/local hidden variations invisible to ordinary source terms up to gauge/boundary terms",
            "if_signed_effect": "local source-prefactor variations cannot enter Hilbert source",
            "current_status": "ORDINARY_SUBACTION_DESCENT_EXACT_CONDITIONAL_NOT_SIGNED",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "parent-sign q_obs, matter lift, line object and boundary class together",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_4_variation_before_readout",
            "zero_theorem_clause": "Hilbert/current source is extracted before material selectors, source-worldtubes or readout calibration",
            "formal_role": "kills post-current c_A as parent-source redefinition but not pre-action weights by itself",
            "if_signed_effect": "post-current rescalings become readout bookkeeping",
            "current_status": "VARIATION_ORDER_CONDITIONAL_PRE_ACTION_WEIGHT_SURVIVES",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "combine with object-language no-source-slot theorem",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_5_no_reentry_no_extension",
            "zero_theorem_clause": "readout/radiative/effective maps do not enlarge coefficient domains or reenter before variation",
            "formal_role": "prevents C_eff_source_tail and arena-specific source legs",
            "if_signed_effect": "zero theorem survives WEP/R10/clock/PPN/orbital projection",
            "current_status": "READOUT_RADIATIVE_EXTENSION_NOT_SIGNED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive no-extension/no-reentry from parent readout construction",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_6_projection_silence",
            "zero_theorem_clause": "WEP/R10/PPN/clock/orbital projections carry no independent source-prefactor charge",
            "formal_role": "prevents arena-specific screens from reintroducing coupling",
            "if_signed_effect": "finite projection matrix becomes unnecessary for zero branch",
            "current_status": "PROJECTION_SILENCE_NOT_SIGNED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_PROJECTION_SILENCE_GATES_NONCLAIM.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "derive shared source-leg owner or keep projection matrix rows live",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "ZTC2685_7_verdict",
            "zero_theorem_clause": "all source-prefactor occupants vanish in parent branch",
            "formal_role": "would set c(I_hid), Delta_w_AB, c_A_pre/kappa_A and C_eff_source_tail to theorem-zero/common calibration",
            "if_signed_effect": "local coupling branch becomes a derived silence theorem instead of a finite-input programme",
            "current_status": "MINIMAL_ZERO_THEOREM_EXACT_CONDITIONAL_NOT_PROVED",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_NEXT_TARGET.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "next_action": "attack ZTC2685_0 root object-language admissibility, or fall back to Delta_w input contract",
            "timestamp_utc": stamp(),
        },
    ]


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_step": "PRF2685_0_state_theorem",
            "statement": "If ZTC2685_0..6 are parent-signed in the same branch, then every active source-prefactor occupant is absent or common-calibration only.",
            "proof_move": "conditional theorem assembly from typed object language, action-line owner, Hom exclusion, subaction descent, variation-before-readout, no-extension and projection-silence clauses",
            "result": "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "blocking_issue": "premises are not parent-signed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "proof_step": "PRF2685_1_domain_elimination",
            "statement": "If source-only labels are not admissible arguments of S_parent, there is no target slot for w_A, c_A, kappa_A or c(I_hid).",
            "proof_move": "type/domain exclusion rather than dynamical cancellation",
            "result": "CLEANEST_PROOF_MOVE_IDENTIFIED",
            "blocking_issue": "admissible argument list remains a grammar contract, not derived from MTS primitives",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "proof_step": "PRF2685_2_counterexample_test",
            "statement": "Same-action Hilbert variation, covariance, Ward identity or current ownership alone does not remove pre-action weights.",
            "proof_move": "test against S_matter=sum_A w_A S_A and hidden scalar c(I_hid) O_source",
            "result": "COUNTEREXAMPLE_SURVIVES_WITHOUT_DOMAIN_ELIMINATION",
            "blocking_issue": "must not smuggle Delta_w=0 from covariance",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "proof_step": "PRF2685_3_projection_survival",
            "statement": "Even if bare source-prefactor slots are absent, readout/radiative/projection maps must not reintroduce arena-specific source legs.",
            "proof_move": "append no-extension and projection-silence gates to the zero theorem",
            "result": "LOCAL_TEST_SURVIVAL_CLAUSE_REQUIRED",
            "blocking_issue": "projection silence is not parent-signed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "proof_step": "PRF2685_4_verdict",
            "statement": "The derivation path is not rejected; it is reduced to one root admissibility theorem plus projection/no-extension survival clauses.",
            "proof_move": "fail honestly at parent grammar/admissibility, not at data fitting",
            "result": "ZERO_THEOREM_NOT_PROVED_BUT_NOW_MINIMAL",
            "blocking_issue": "ZTC2685_0 is the first hard target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def failure_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("FC2685_0_root", "parent object-language admissibility", "without this, source-prefactor target remains legal", "derive from q-descent/category primitives"),
        ("FC2685_1_line", "parent action-density line construction", "without this, relative ordinary matter line weights remain possible", "construct A_ord and connected ordinary line owner"),
        ("FC2685_2_hidden", "hidden invariant algebra or target absence", "without this, c(I_hid) O_source counterexample survives", "prove hidden invariants trivial or forbid source coefficient target"),
        ("FC2685_3_variation", "variation before readout plus no pre-current slot", "without this, post/pre-current c_A can be conflated", "derive source extraction order and no source-current coefficient slot"),
        ("FC2685_4_reentry", "no readout/radiative coefficient-domain extension", "without this, C_eff_source_tail reappears", "derive no-extension/no-reentry theorem"),
        ("FC2685_5_projection", "shared source-leg/projection silence", "without this, local arenas can regain source-prefactor legs", "derive common source-leg owner across WEP/R10/PPN/clock/orbital"),
    ]
    return [
        {
            "failure_id": failure_id,
            "unsigned_clause": clause,
            "why_it_matters": why,
            "best_next_attack": attack,
            "current_status": "UNSIGNED_BLOCKS_ZERO_THEOREM",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for failure_id, clause, why, attack in rows
    ]


def delta_w_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "DW2685_0_theorem_zero_option",
            "quantity": "Delta_w_AB",
            "route": "derive_zero",
            "accepted_evidence": "ZTC2685_0..6 parent-signed in the same branch",
            "required_units": "dimensionless common source fraction",
            "required_projection": "none if true theorem-zero; otherwise all arena projections remain live",
            "current_value": "MISSING_THEOREM_ZERO",
            "source_path": str(OUTPUTS["zero_contract"]),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "attack root parent admissibility theorem",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "DW2685_1_first_finite_value",
            "quantity": "Delta_w_AB",
            "route": "finite_source_value",
            "accepted_evidence": "independent parent/source model value or bound not obtained by WEP/R10 inversion",
            "required_units": "dimensionless common source fraction",
            "required_projection": "K_WEP, tau_WEP, K_R10(lambda), tau_R10(lambda), M_PPN, K_orbital plus source/test composition",
            "current_value": "MISSING_NUMERIC_SOURCE_BACKED_DELTA_W",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_COEFFICIENT_TO_ARENA_MAP_NONCLAIM.csv")),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "do not fill unless zero theorem fails and independent source value exists",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "DW2685_2_common_normalizer",
            "quantity": "N_source_common",
            "route": "finite_branch_required_normalizer",
            "accepted_evidence": "declared Hilbert/source denominator shared by WEP, R10, PPN, clock and orbital rows",
            "required_units": "same denominator for all Delta_w projections",
            "required_projection": "must be referenced by every K/tau arena row",
            "current_value": "MISSING_COMMON_SOURCE_NORMALIZER",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_NONCLAIM.csv")),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "define only after parent source owner is fixed",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "DW2685_3_no_cancellation",
            "quantity": "abs(Delta_w_AB) contribution",
            "route": "absolute_envelope",
            "accepted_evidence": "componentwise positive envelope, not fitted cancellation against c_A, C_eff or hidden scalars",
            "required_units": "dimensionless common source fraction then arena-declared observable units",
            "required_projection": "absolute envelope per arena with no cross-arena cancellation",
            "current_value": "MISSING_ABSOLUTE_ENVELOPE",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_NONCLAIM.csv")),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "keep Delta_w row nonclaim until all signs and envelopes are declared",
            "timestamp_utc": stamp(),
        },
        {
            "input_id": "DW2685_4_refusal_rule",
            "quantity": "Delta_w_AB",
            "route": "forbidden_shortcuts",
            "accepted_evidence": "none",
            "required_units": "n/a",
            "required_projection": "n/a",
            "current_value": "REFUSE_WEP_R10_BOUND_INVERSION_REFUSE_DELTA_W_EQUALS_ZERO_BY_PREFERENCE",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2684_NEXT_TARGET.csv")),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "only theorem-zero or independent source value can move this row",
            "timestamp_utc": stamp(),
        },
    ]


def runner_rows(zero_contract: list[dict[str, Any]], proof: list[dict[str, Any]], delta_w: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    unsigned = [row["clause_id"] for row in zero_contract if row["parent_signed"] != "true"]
    rows.append(
        {
            "runner_id": "RUN2685_ZERO_THEOREM",
            "stage": "parent_source_prefactor_zero",
            "input_target": "ZTC2685_0..6",
            "all_parent_signed": "false",
            "theorem_zero_available": "false",
            "finite_delta_w_available": "false",
            "bound_inversion_used": "false",
            "missing_blocker": ";".join(unsigned),
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": "ZERO_THEOREM_EXACT_CONDITIONAL_NOT_PROVED",
            "timestamp_utc": stamp(),
        }
    )
    for row in proof:
        rows.append(
            {
                "runner_id": f"RUN2685_{row['proof_step']}",
                "stage": "proof_attempt",
                "input_target": row["proof_step"],
                "all_parent_signed": "false",
                "theorem_zero_available": "false",
                "finite_delta_w_available": "false",
                "bound_inversion_used": "false",
                "missing_blocker": row["blocking_issue"],
                "score_ready": "false",
                "valid_for_claim": "false",
                "runner_verdict": row["result"],
                "timestamp_utc": stamp(),
            }
        )
    for row in delta_w:
        rows.append(
            {
                "runner_id": f"RUN2685_{row['input_id']}",
                "stage": "delta_w_first_input",
                "input_target": row["quantity"],
                "all_parent_signed": "false",
                "theorem_zero_available": "false",
                "finite_delta_w_available": "false",
                "bound_inversion_used": "false",
                "missing_blocker": row["current_value"],
                "score_ready": row["score_ready"],
                "valid_for_claim": row["valid_for_claim"],
                "runner_verdict": "DELTA_W_INPUT_REMAINS_NONCLAIM",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2685_0_zero_theorem_proved", "all zero theorem clauses parent-signed", "FAIL", "minimal theorem is exact conditional but not parent-signed"),
        ("CG2685_1_delta_w_source_ready", "Delta_w_AB has independent source value, units, projection and normalizer", "FAIL", "Delta_w fallback is only a contract"),
        ("CG2685_2_no_bound_inversion", "no WEP/R10 bound is used as Delta_w value", "PASS_GUARD_ONLY", "refusal rule is explicit"),
        ("CG2685_3_no_cancellation", "absolute no-cancellation envelope is available", "FAIL", "envelope policy exists but component values are missing"),
        ("CG2685_4_local_GR_or_WEP_claim", "local GR/WEP/R10/PPN/clock/orbital promotion", "REFUSED", "2685 is a theorem/input contract, not a claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": "true" if status == "PASS_GUARD_ONLY" else "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2685_0_private_verdict",
            "decision": "ZERO_THEOREM_NOT_PROVED_BUT_MINIMAL",
            "rationale": "the clean route now has a compact theorem contract; the root missing item is parent object-language admissibility, not a vague coupling mystery",
            "claim_allowed": "false",
            "next_action": "attack admissibility from q-descent/category primitives",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2685_1_delta_w_fallback",
            "decision": "DELTA_W_FIRST_INPUT_STAGED_ONLY_AS_FALLBACK",
            "rationale": "if the theorem route fails, Delta_w_AB is the first finite coupling to source because it touches the most local arenas",
            "claim_allowed": "false",
            "next_action": "do not source c_A or C_eff before Delta_w/common normalizer discipline",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2685_2_best_route",
            "decision": "NEXT_ATTACK_PARENT_ADMISSIBILITY_RULE",
            "rationale": "deriving the admissible parent action arguments would kill the source-prefactor target in the least scrutiny-prone way",
            "claim_allowed": "false",
            "next_action": "2686 parent action admissibility from q-descent or Delta_w row",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2685_0_selected",
            "kind": "selected",
            "target_doc": "2686-Y5-R2FR-parent-action-admissibility-from-q-descent-or-delta-w-first-row.md",
            "target_script": "scripts/Y5_R2FR_parent_action_admissibility_from_q_descent_or_delta_w_first_row_2686.py",
            "purpose": "try to derive the admissible parent action argument list from q-descent/category primitives; if it fails, keep Delta_w_AB as the first finite nonclaim source row",
            "acceptance_gate": "either source-only labels are proved nonarguments of S_parent, or Delta_w_AB remains nonclaim with explicit independent source-value requirements",
            "forbidden_shortcuts": "adopting object-language admissibility as an axiom; assuming Delta_w=0; using WEP/R10 bounds as Delta_w; treating covariance/Ward identity as pre-action weight exclusion; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2685_0_derivation", "GR/Newton coupling derivation", "ROOT_OBJECT_LANGUAGE_TARGET_IDENTIFIED", "the first hard theorem is parent action admissibility: source-only labels must be nonarguments of S_parent"),
        ("STATUS2685_1_finite_branch", "Delta_w_AB fallback", "FIRST_INPUT_CONTRACT_STAGED_NONCLAIM", "if derivation fails, Delta_w_AB is the first finite coefficient to source, not c_A or readout tails"),
        ("STATUS2685_2_claims", "local tests", "NO_LOCAL_CLAIM", "WEP/R10/PPN/clock/orbital comparisons remain blocked until theorem-zero or independent finite inputs exist"),
    ]
    return [
        {
            "status_id": status_id,
            "sector": sector,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "false",
            "next_action": "run 2686 admissibility derivation target",
            "timestamp_utc": stamp(),
        }
        for status_id, sector, status, meaning in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2685_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(source_rows: list[dict[str, Any]], zero_contract: list[dict[str, Any]], proof: list[dict[str, Any]], failures: list[dict[str, Any]], delta_w: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    zero_nonclaim = all(row["parent_signed"] == "false" and row["valid_for_claim"] == "false" for row in zero_contract)
    exact_conditional_written = any(row["proof_step"] == "PRF2685_0_state_theorem" and row["result"] == "EXACT_CONDITIONAL_THEOREM_WRITTEN" for row in proof)
    counterexamples_retained = any(row["proof_step"] == "PRF2685_2_counterexample_test" and "COUNTEREXAMPLE_SURVIVES" in row["result"] for row in proof)
    root_identified = any(row["clause_id"] == "ZTC2685_0_parent_action_domain" and row["current_status"] == "ROOT_OBJECT_LANGUAGE_ADMISSIBILITY_NOT_DERIVED" for row in zero_contract)
    failures_block = all(row["current_status"] == "UNSIGNED_BLOCKS_ZERO_THEOREM" and row["claim_allowed"] == "false" for row in failures)
    delta_w_nonclaim = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in delta_w)
    delta_w_refusal = any("REFUSE_WEP_R10_BOUND_INVERSION" in row["current_value"] for row in delta_w)
    runner_refuses = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner)
    claim_blocked = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    guard_pass_only = any(row["gate_id"] == "CG2685_2_no_bound_inversion" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2686" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2685_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2685_zero_contract_nonclaim", zero_nonclaim, "zero theorem clauses remain unsigned/nonclaim"),
        ("VAL2685_exact_conditional_written", exact_conditional_written, "minimal exact conditional theorem is written"),
        ("VAL2685_counterexamples_retained", counterexamples_retained, "source-prefactor counterexamples are retained"),
        ("VAL2685_root_admissibility_identified", root_identified, "root object-language admissibility clause identified"),
        ("VAL2685_failure_clauses_block_claim", failures_block, "unsigned clauses explicitly block zero theorem"),
        ("VAL2685_delta_w_contract_nonclaim", delta_w_nonclaim, "Delta_w fallback rows remain nonclaim"),
        ("VAL2685_bound_inversion_refused", delta_w_refusal and guard_pass_only, "WEP/R10 bound inversion refusal is explicit"),
        ("VAL2685_runner_refuses_unsigned_rows", runner_refuses, "runner refuses zero and Delta_w rows"),
        ("VAL2685_claim_gates_block_claims", claim_blocked, "all claim gates block promotion"),
        ("VAL2685_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2685_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2685_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2685_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2685_next_target_selected", next_target_ok, "2686 admissibility target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2685_OVERALL",
            "passed": as_bool(overall),
            "detail": "2685 writes the minimal source-prefactor zero theorem, identifies parent admissibility as root debt, and stages Delta_w_AB as fallback nonclaim",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(source_rows: list[dict[str, Any]], zero_contract: list[dict[str, Any]], proof: list[dict[str, Any]], failures: list[dict[str, Any]], delta_w: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_target: list[dict[str, Any]], status: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2685 — Y5/R2FR Parent Source-Prefactor Zero Theorem Minimal Contract or Delta-w First Input",
                "",
                "## Private Verdict",
                "",
                "This is the cleanest formulation so far: the source-coupling problem reduces to a parent action admissibility theorem. If source-only labels are not arguments of `S_parent`, then `Coeff_source-prefactor` is not a parent target and `c(I_hid)`, `Delta_w_AB`, `c_A_pre/kappa_A`, and `C_eff_source_tail` become theorem-zero/common-calibration candidates.",
                "",
                "The proof is not closed. The exact conditional theorem is written, but the root admissibility rule is not derived from MTS primitives yet. Same-action variation, covariance, Ward identities, and current ownership do not kill pre-action weights by themselves.",
                "",
                "Fallback is disciplined: `Delta_w_AB` is the first finite input only if the zero theorem fails, and it remains nonclaim unless it has an independent source value, common normalizer, K/tau projections, units, and no-cancellation envelope. WEP/R10 bounds cannot be inverted into `Delta_w_AB`.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Minimal Zero-Theorem Contract",
                "",
                markdown_table(zero_contract),
                "",
                "## Proof Attempt Ledger",
                "",
                markdown_table(proof),
                "",
                "## Failure Clauses",
                "",
                markdown_table(failures),
                "",
                "## Delta-w First Input Contract",
                "",
                markdown_table(delta_w),
                "",
                "## Runner Results",
                "",
                markdown_table(runner),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    zero_contract = zero_contract_rows()
    proof = proof_attempt_rows()
    failures = failure_clause_rows()
    delta_w = delta_w_contract_rows()
    runner = runner_rows(zero_contract, proof, delta_w)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["zero_contract"], zero_contract)
    write_csv(OUTPUTS["proof_attempt"], proof)
    write_csv(OUTPUTS["failure_clauses"], failures)
    write_csv(OUTPUTS["delta_w_contract"], delta_w)
    write_csv(OUTPUTS["runner_results"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_zero_contract"], zero_contract)
    write_csv(BRANCH_OUTPUTS["local_delta_w_contract"], delta_w)
    write_csv(BRANCH_OUTPUTS["wep_zero_contract"], zero_contract)
    write_csv(BRANCH_OUTPUTS["wep_delta_w_contract"], delta_w)
    write_csv(BRANCH_OUTPUTS["source_weight_delta_w_contract"], delta_w)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, zero_contract, proof, failures, delta_w, runner, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, zero_contract, proof, failures, delta_w, runner, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
