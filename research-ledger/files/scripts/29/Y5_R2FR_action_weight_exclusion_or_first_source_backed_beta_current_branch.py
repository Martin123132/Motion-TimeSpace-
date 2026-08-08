from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1694"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1694-Y5-R2FR-action-weight-exclusion-or-first-source-backed-beta-current-branch.md"

SOURCE_FILES = {
    "1693_doc": ROOT / "1693-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-current-branch.md",
    "1693_validation": OUT / "P8_Y5_BRR545_1693_VALIDATION.csv",
    "1693_next": OUT / "P8_Y5_PARENT_QLOC_1693_NEXT_TARGET.csv",
    "1594_doc": ROOT / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
    "1594_action_weight": OUT / "P8_Y5_PARENT_QLOC_1594_ACTION_WEIGHT_EXCLUSION_THEOREM_ATTEMPT.csv",
    "1594_validator_spec": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv",
    "1594_validator_results": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
    "1594_queue": OUT / "P8_Y5_PARENT_QLOC_1594_BETA_SOURCE_ACQUISITION_QUEUE.csv",
    "1595_doc": ROOT / "1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md",
    "1595_validation": OUT / "P8_Y5_BRR545_1595_VALIDATION.csv",
    "1595_action_owner": OUT / "P8_Y5_PARENT_QLOC_1595_ACTION_MEASURE_OWNER_REOPEN.csv",
    "1595_bound_candidate": OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv",
    "1595_next_inputs": OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv",
    "local_bound_claims": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
    "1066_wep_bound": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
}

NEEDLES = {
    "1693_doc": ["w_A", "NEXT1693_0_primary"],
    "1693_validation": ["VAL1693_OVERALL", "PASS"],
    "1693_next": ["NEXT1693_0_primary", "action-weight-exclusion"],
    "1594_doc": ["AWT1594_7_verdict", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED"],
    "1594_action_weight": ["AWT1594_7_verdict", "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_VALIDATOR_REQUIRED"],
    "1594_validator_spec": ["BVS1594_9_verdict", "current 1593 beta rows are expected to fail"],
    "1594_validator_results": ["BVR1594_VERDICT", "NO_ACCEPTED_BETA_ROWS"],
    "1594_queue": ["BSQ1594_2_Delta_w_A", "BSQ1594_7_verdict"],
    "1595_doc": ["AMR1595_5_verdict", "SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor"],
    "1595_validation": ["VAL1595_OVERALL", "PASS"],
    "1595_action_owner": ["AMR1595_5_verdict", "ACTION_MEASURE_OWNER_STILL_NOT_DERIVED"],
    "1595_bound_candidate": ["SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor", "2.8e-15"],
    "1595_next_inputs": ["NIR1595_0_tau_WEP", "NIR1595_5_verdict"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
    "1066_wep_bound": ["BOUND1066_0_WEP_source_charge", "2.8e-15"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_REGISTER.csv"
OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1694_ACTION_MEASURE_OWNER_PROOF_GATE.csv"
VARIATION_IDENTITY = OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv"
BOUND_ROWS = OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv"
VALIDATOR_RECHECK = OUT / "P8_Y5_PARENT_QLOC_1694_VALIDATOR_RECHECK.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1694_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1694_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1694_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1694_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OWNER_GATE,
    VARIATION_IDENTITY,
    BOUND_ROWS,
    VALIDATOR_RECHECK,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    OWNER_GATE,
    VARIATION_IDENTITY,
    BOUND_ROWS,
    VALIDATOR_RECHECK,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    OWNER_GATE: [
        QUARANTINE / "ACTION_MEASURE_OWNER_PROOF_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_action_measure_owner_proof_gate_1694.csv",
        QUEUE / "JR1694_ACTION_MEASURE_OWNER_PROOF_GATE.csv",
    ],
    VARIATION_IDENTITY: [
        QUARANTINE / "SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
        BRANCH_RESIDUALS / "R2FR_source_weight_variation_identity_1694.csv",
        QUEUE / "JR1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    ],
    BOUND_ROWS: [
        QUARANTINE / "SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
        BRANCH_RESIDUALS / "R2FR_source_backed_beta_DeltaW_current_rows_1694.csv",
        QUEUE / "JR1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1694.csv",
        QUEUE / "JR1694_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1694": "action-weight exclusion proof gate and first source-backed beta/Delta_w current-branch row",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "OWG1694_0_countermodel",
            "pre-variation relative weight countermodel",
            "S_matter=sum_A w_A(phi) S_A[Psi_A,e_obs,theta_A]",
            "COUNTERMODEL_SURVIVES",
            "covariance, additivity and isolated classical matter equations do not remove w_A",
            "parent grammar/action-measure theorem or finite Delta_w/beta_w rows",
        ),
        (
            "OWG1694_1_no_source_only_slot",
            "forbid source-only matter weights",
            "Allowed[S_matter]=sum_A S_A[Psi_A,e_obs(q),theta_A] with no independent w_A argument",
            "UNSIGNED_PARENT_GRAMMAR",
            "would make partial S_matter/partial w_A undefined rather than tuned",
            "object-language/no-extra-slot theorem from MTS primitives",
        ),
        (
            "OWG1694_2_single_action_measure",
            "one parent action measure/phase scale",
            "one hbar/action measure owns the whole matter path weight, not species-indexed exp(i w_A S_A/hbar)",
            "UNSIGNED_PARENT_MEASURE",
            "cleanest route to kill relative action weights",
            "parent measure owner, not merely a convention",
        ),
        (
            "OWG1694_3_current_owner",
            "Hilbert/source current before readout",
            "T_H is the coframe/metric variation of the already-fixed total matter action",
            "PARTIAL_ONLY_PREVARIATION_SURVIVES",
            "post-variation rescalings are controlled, but pre-variation w_A is inherited by T_H",
            "combine with no-source-only-slot and common action measure",
        ),
        (
            "OWG1694_4_label_forgetting",
            "source functor forgets species/source labels",
            "ordinary source charge depends on observed coframe and representation data, not source labels as active multipliers",
            "UNSIGNED_LABEL_FORGETTING",
            "would collapse relative source couplings to one calibrated common mode",
            "parent ordinary-matter functor exhaustion theorem",
        ),
        (
            "OWG1694_5_nonhilbert_silence",
            "no non-Hilbert or hidden spurion source bypass",
            "zeta_A J_NH,A, marker/domain/boundary source weights and readout rescalings are absent or projected silent",
            "UNSIGNED_BYPASS_SILENCE",
            "prevents w_A from re-entering through a different source-current channel",
            "hidden-current/no-spurion theorem or explicit residual rows",
        ),
        (
            "OWG1694_6_common_mode_guard",
            "common constant mode only",
            "w_A=w_common for all A and partial_phi w_common=0 can be absorbed into calibrated G/kappa",
            "CONDITIONAL_COMMON_MODE_ONLY",
            "relative or phi-dependent weights remain physical",
            "do not use measured-G absorption for Delta_w_A or beta_w_A",
        ),
        (
            "OWG1694_7_verdict",
            "action-weight exclusion theorem",
            "no-source-only-slot + single action measure + current owner + label forgetting + bypass silence",
            "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_BOUND_ANCHOR_RETAINED",
            "current corpus sharpens the theorem but does not parent-sign it",
            "retain MICROSCOPE bound anchor and move to no-slot/tau_WEP projection gate",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "clause": clause,
            "formal_statement": statement,
            "current_status": status,
            "effect": effect,
            "required_next_input": required,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, clause, statement, status, effect, required in rows
    ]


def variation_identity_rows() -> list[dict[str, object]]:
    rows = [
        (
            "VAR1694_0_matter_EOM",
            "matter field equation",
            "delta(w_A S_A)/delta Psi_A = w_A E_A when w_A is Psi_A-independent",
            "isolated classical equations can look unchanged",
            "does not prove source universality",
        ),
        (
            "VAR1694_1_Hilbert_source",
            "metric/coframe source",
            "T_obs = sum_A w_A T_A after varying the weighted matter action",
            "relative w_A changes the active gravitational source",
            "blocks Newton/common-matter reduction unless forbidden or bounded",
        ),
        (
            "VAR1694_2_canonical_source",
            "canonical field source",
            "J_phi contains sum_A (partial_phi w_A) S_A + w_A delta_phi S_A",
            "beta_w_source and beta_w_test are real finite-exchange legs if w_A(phi) survives",
            "blocks g_c=0 and beta_source beta_test=0 claims",
        ),
        (
            "VAR1694_3_common_mode",
            "common derivative-silent weight",
            "w_A=w_common and partial_phi w_common=0 rescales the whole matter source",
            "can be absorbed into calibrated G only as a common constant mode",
            "not a WEP/R10/PPN residual by itself",
        ),
        (
            "VAR1694_4_relative_mode",
            "relative or phi-dependent weight",
            "Delta_w_AB != 0 or beta_w,A != 0 remains after G calibration",
            "maps to WEP/source-normalization and finite beta rows",
            "must be theorem-zero or source-backed",
        ),
        (
            "VAR1694_5_identity_verdict",
            "source-weight variation identity",
            "the algebra proves why w_A is the right seam",
            "classical-looking dynamics are not enough; source variation is the load path",
            "derive no-slot owner or keep finite rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": identity_id,
            "object": obj,
            "identity": identity,
            "meaning": meaning,
            "local_gr_impact": impact,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for identity_id, obj, identity, meaning, impact in rows
    ]


def bound_rows() -> list[dict[str, object]]:
    local_bound_path = SOURCE_FILES["local_bound_claims"]
    rows = [
        (
            "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "P_WEP_relative_source_weight",
            "source_backed_bound_anchor",
            "absolute product bound for relative source/action-weight channel, P=abs(Delta_w_TiPt*tau_WEP)",
            "2.8e-15",
            "dimensionless",
            str(local_bound_path),
            "R1_WEP_source_charge",
            "imported from 1595/1066 MICROSCOPE source-charge bound anchor",
            "Delta_w_TiPt*tau_WEP product convention",
            "R1_WEP_source_charge; Newton/common-matter guard; no R10/PPN score",
            "tau_WEP;source_worldtube;material_map;readout_kernel;MTS prediction",
            True,
        ),
        (
            "BDW1694_1_beta_w_source_template",
            "beta_w_source",
            "current_branch_template",
            "source leg partial_phi ln w_source in canonical phi convention",
            "MISSING",
            "1/canonical_phi",
            "MISSING_SOURCE_PATH",
            "MISSING_SOURCE_ANCHOR",
            "not extracted",
            "canonical_phi_required",
            "R10;PPN;WEP;Newton source",
            "parent coefficient or theorem-zero certificate",
            False,
        ),
        (
            "BDW1694_2_beta_w_test_template",
            "beta_w_test",
            "current_branch_template",
            "test leg partial_phi ln w_test in canonical phi convention",
            "MISSING",
            "1/canonical_phi",
            "MISSING_SOURCE_PATH",
            "MISSING_SOURCE_ANCHOR",
            "not extracted",
            "canonical_phi_required",
            "R10;WEP;clock;orbital",
            "parent coefficient or theorem-zero certificate",
            False,
        ),
        (
            "BDW1694_3_Delta_w_material_template",
            "Delta_w_A",
            "current_branch_template",
            "relative constant/source-weight split after common-mode calibration",
            "MISSING",
            "dimensionless",
            "MISSING_SOURCE_PATH",
            "MISSING_SOURCE_ANCHOR",
            "not extracted",
            "Delta_w_AB convention required",
            "Newton;common matter;WEP",
            "no-slot theorem or source-backed material map",
            False,
        ),
        (
            "BDW1694_4_verdict",
            "beta/Delta_w current branch",
            "validator_status",
            "one source-backed bound anchor exists, but no MTS beta/Delta_w prediction row exists",
            "NONCLAIM_ONLY",
            "mixed",
            str(local_bound_path),
            "R1_WEP_source_charge",
            "schema/provenance pass for bound anchor only",
            "canonical_phi_and_Delta_w_conventions_still_required",
            "all local arenas blocked",
            "tau_WEP;beta_source;beta_test;Delta_w prediction or theorem-zero",
            False,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "row_type": row_type,
            "definition": definition,
            "value_or_bound": value,
            "units": units,
            "source_path": source_path,
            "source_anchor": anchor,
            "extraction_method": method,
            "beta_convention": convention,
            "arena_map": arena_map,
            "missing_before_score": missing,
            "schema_provenance_pass": schema_pass,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, row_type, definition, value, units, source_path, anchor, method, convention, arena_map, missing, schema_pass in rows
    ]


def validator_recheck_rows() -> list[dict[str, object]]:
    rows = [
        (
            "VRC1694_0_bound_anchor_schema",
            "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "P_WEP_relative_source_weight",
            "ACCEPT_SCHEMA_PROVENANCE_ONLY",
            "none",
            "BOUND_ANCHOR_ONLY_NO_MTS_PREDICTION",
            "source-backed bound anchor can be used as external constraint once tau_WEP exists",
        ),
        (
            "VRC1694_1_beta_w_source",
            "BDW1694_1_beta_w_source_template",
            "beta_w_source",
            "REJECT_SCORE",
            "source_path;source_anchor;numeric_or_theorem_zero_value;arena_map",
            "MISSING",
            "no source leg exists",
        ),
        (
            "VRC1694_2_beta_w_test",
            "BDW1694_2_beta_w_test_template",
            "beta_w_test",
            "REJECT_SCORE",
            "source_path;source_anchor;numeric_or_theorem_zero_value;arena_map",
            "MISSING",
            "no test leg exists",
        ),
        (
            "VRC1694_3_Delta_w",
            "BDW1694_3_Delta_w_material_template",
            "Delta_w_A",
            "REJECT_SCORE",
            "source_path;source_anchor;material_map;tau_WEP",
            "MISSING",
            "no material/source projection exists",
        ),
        (
            "VRC1694_4_verdict",
            "all_1694_current_rows",
            "beta/Delta_w package",
            "ONE_BOUND_ANCHOR_SCHEMA_PASS_NO_PREDICTION_ROWS_ACCEPTED",
            "tau_WEP;source_worldtube;material_map;readout_kernel;MTS beta rows",
            "NONCLAIM",
            "validator-readable plumbing exists, but scoring remains blocked",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "validation_id": validation_id,
            "input_row_id": input_row_id,
            "quantity": quantity,
            "validator_result": result,
            "missing_required_fields": missing,
            "bad_markers": markers,
            "effect": effect,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for validation_id, input_row_id, quantity, result, missing, markers, effect in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1694_0_wA_zero", "claim w_A absent/theorem-zero", "REJECT_ACTION_WEIGHT_ZERO_CLAIM", "no-source-only slot and action-measure owner are not parent-signed"),
        ("RUN1694_1_measured_G_absorb", "absorb all w_A into measured G", "REJECT_RELATIVE_WEIGHT_ABSORPTION", "only common derivative-silent mode is calibratable"),
        ("RUN1694_2_bound_anchor_score", "treat MICROSCOPE anchor as MTS prediction", "REJECT_BOUND_AS_PREDICTION", "tau_WEP/source/readout projection and MTS Delta_w are missing"),
        ("RUN1694_3_beta_score", "score beta_w_source beta_w_test", "REJECT_FINITE_BETA_SCORE", "beta_w source/test values are missing"),
        ("RUN1694_4_local_GR", "claim derived local GR/Newton/common matter", "BLOCKED_NO_CLAIM", "source-weight theorem and source-normalized Newton remain open"),
        ("RUN1694_5_R10_PPN_clock_orbit", "export bound anchor to R10/PPN/clock/orbital arenas", "REJECT_ARENA_EXPORT", "arena projection kernels are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1694_0_primary",
            "1695-Y5-R2FR-no-source-only-slot-theorem-or-tau-WEP-projection-current-branch.md",
            "scripts/Y5_R2FR_no_source_only_slot_theorem_or_tau_WEP_projection_current_branch.py",
            "derive the parent no-source-only-slot/object-language theorem for ordinary matter; failing that, derive/source tau_WEP, source-worldtube, material-map and readout-kernel rows so the MICROSCOPE bound anchor becomes a usable nonclaim constraint",
            "this attacks the derivation-first route while preserving the first real bound anchor as pressure data",
            "selected",
        ),
        (
            "NEXT1694_1_fallback",
            "1695b-Y5-R2FR-beta-w-prior-chain-and-arena-kernel-source-pack.md",
            "scripts/Y5_R2FR_beta_w_prior_chain_and_arena_kernel_source_pack.py",
            "only if the theorem route stalls, build beta_w_source/beta_w_test/Delta_w prior-chain source rows and then arena kernels",
            "finite route is honest but less fundamental than proving the source slot absent",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1694_0_action_weight_zero", "w_A absent/theorem-zero", "BLOCKED_NO_CLAIM", "parent no-source-only-slot/action-measure theorem is unsigned"),
        ("CG1694_1_common_matter", "common matter/source normalization", "BLOCKED_NO_CLAIM", "relative source weights remain legal until forbidden or bounded"),
        ("CG1694_2_delta_w_bound", "Delta_w numeric bound", "BLOCKED_NO_CLAIM", "MICROSCOPE anchor is only abs(Delta_w_TiPt*tau_WEP), tau_WEP is missing"),
        ("CG1694_3_finite_beta", "beta_w finite exchange score", "BLOCKED_NO_CLAIM", "beta_w_source and beta_w_test are missing"),
        ("CG1694_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-side GR and common measured-G bridge do not close"),
        ("CG1694_5_public_result", "public/GitHub-ready physics claim", "BLOCKED_NO_CLAIM", "private plumbing checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    bound_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_verdict = any(
        row["gate_id"] == "OWG1694_7_verdict"
        and row["current_status"] == "ACTION_WEIGHT_EXCLUSION_NOT_DERIVED_BOUND_ANCHOR_RETAINED"
        for row in owner_rows
    )
    countermodel_present = any(row["gate_id"] == "OWG1694_0_countermodel" and row["current_status"] == "COUNTERMODEL_SURVIVES" for row in owner_rows)
    variation_complete = {"matter field equation", "metric/coframe source", "canonical field source", "common derivative-silent weight", "relative or phi-dependent weight"}.issubset(
        {str(row["object"]) for row in variation_rows}
    )
    bound_anchor_imported = any(
        row["row_id"] == "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor"
        and row["value_or_bound"] == "2.8e-15"
        and row["source_anchor"] == "R1_WEP_source_charge"
        and bool_cell(row["schema_provenance_pass"])
        and not bool_cell(row["valid_prediction_row"])
        for row in bound_rows_
    )
    templates_blocked = all(
        not bool_cell(row["accepted_for_scoring"])
        for row in bound_rows_
        if str(row["row_id"]).startswith("BDW1694_")
    )
    validator_blocks = any(
        row["validation_id"] == "VRC1694_4_verdict"
        and row["validator_result"] == "ONE_BOUND_ANCHOR_SCHEMA_PASS_NO_PREDICTION_ROWS_ACCEPTED"
        for row in validator_rows
    )
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(
        row["route_id"] == "NEXT1694_0_primary"
        and row["selection_status"] == "selected"
        and "no-source-only-slot" in row["next_target"]
        for row in next_rows
    )
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1694*"))) == 0 if FORMALIZATION.exists() else True

    checks = [
        ("VAL1694_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1694_1_owner_countermodel", countermodel_present and owner_verdict, "action-weight countermodel survives and theorem verdict remains nonclaim"),
        ("VAL1694_2_variation_identity", variation_complete, "variation identity covers matter EOM, Hilbert source, canonical source, common mode and relative mode"),
        ("VAL1694_3_bound_anchor_imported", bound_anchor_imported, "MICROSCOPE 2.8e-15 bound anchor is imported as schema-only nonprediction row"),
        ("VAL1694_4_templates_blocked", templates_blocked, "all beta/Delta_w rows remain blocked for scoring"),
        ("VAL1694_5_validator_blocks", validator_blocks, "validator accepts only bound-anchor plumbing and no prediction rows"),
        ("VAL1694_6_runner_blocks", runner_blocks, "runner blocks action-weight zero, measured-G absorption, local scores and arena exports"),
        ("VAL1694_7_next_selected", next_selected, "next target selects no-source-only-slot theorem or tau_WEP projection"),
        ("VAL1694_8_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1694_9_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1694_10_csv_parse", csv_parse, "all generated 1694 CSVs parse"),
        ("VAL1694_11_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1694_12_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1694_13_formalization_untouched", formalization_untouched, "no 1694 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1694_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1694 action-weight exclusion or first source-backed beta/Delta_w current-branch validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    bound_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1694 - Action-Weight Exclusion Or First Source-Backed Beta Current Branch

## Verdict

1694 takes the current 1693 branch straight into the source-side gremlin: the pre-variation action/source weight `w_A`. The derivation attempt is now exact enough to be useful, but it still does **not** close. Classical-looking matter equations cannot kill `w_A`; the Hilbert/source variation still sees it.

The result is not a retreat. It is a cleaner fork. Either the parent action forbids source-only matter weights by object-language/action-measure ownership, or `Delta_w_A`, `beta_w_source`, and `beta_w_test` must stay as finite local rows.

The one concrete progress item is retained: the MICROSCOPE `R1_WEP_source_charge` anchor gives `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15` as a source-backed **bound anchor only**. It is schema-readable, but not an MTS prediction and not a local-GR/WEP/R10/PPN pass.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1694"])}

## Action-Measure Owner Proof Gate

{markdown_table(owner_rows, ["gate_id", "clause", "current_status", "effect", "required_next_input"])}

## Source-Weight Variation Identity

{markdown_table(variation_rows, ["identity_id", "object", "identity", "meaning", "local_gr_impact"])}

## Source-Backed Beta/Delta-w Current Rows

{markdown_table(bound_rows_, ["row_id", "quantity", "row_type", "value_or_bound", "source_anchor", "schema_provenance_pass", "missing_before_score"])}

## Validator Recheck

{markdown_table(validator_rows, ["validation_id", "input_row_id", "validator_result", "missing_required_fields", "effect"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a useful ugly result. The theory is not failing randomly here; it is pointing to one precise load-bearing contract. If MTS can derive the no-source-only-slot/action-measure owner, the source side can start looking GR-like for a real reason. If it cannot, the finite branch is still testable, but it becomes a constrained residual theory rather than a clean local-GR derivation.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    owner_rows = owner_gate_rows()
    variation_rows = variation_identity_rows()
    bound_rows_ = bound_rows()
    validator_rows = validator_recheck_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1694", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_GATE, owner_rows, ["branch_id", "gate_id", "clause", "formal_statement", "current_status", "effect", "required_next_input", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(VARIATION_IDENTITY, variation_rows, ["branch_id", "identity_id", "object", "identity", "meaning", "local_gr_impact", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(BOUND_ROWS, bound_rows_, ["branch_id", "row_id", "quantity", "row_type", "definition", "value_or_bound", "units", "source_path", "source_anchor", "extraction_method", "beta_convention", "arena_map", "missing_before_score", "schema_provenance_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(VALIDATOR_RECHECK, validator_rows, ["branch_id", "validation_id", "input_row_id", "quantity", "validator_result", "missing_required_fields", "bad_markers", "effect", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, owner_rows, variation_rows, bound_rows_, validator_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, variation_rows, bound_rows_, validator_rows, runner_rows_, next_rows, claim_rows, validation_rows)

    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1694 validation PASS")


if __name__ == "__main__":
    main()
