from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1407-Y5-R10-RAB-NoSourceOnlySpeciesSlot-proof-or-sector-beta-source-schema.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1407_SOURCE_REGISTER.csv"
SLOT_PROOF_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1407_NOSOURCEONLYSPECIESSLOT_PROOF_AUDIT.csv"
COUNTEREXAMPLE_PATH = SRC_DIR / "P8_Y5_R10_1407_SOURCE_ONLY_SLOT_COUNTEREXAMPLE_TEST.csv"
SCHEMA_PATH = SRC_DIR / "P8_Y5_R10_1407_SECTOR_BETA_SOURCE_SCHEMA.csv"
SCHEMA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1407_SCHEMA_ACCEPTANCE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1407_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1407_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1407_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1407_VALIDATION.csv"

STATUS = (
    "Y5_R10_1407_NoSourceOnlySpeciesSlot_not_proved_"
    "strict_sector_beta_source_schema_written_nonclaim"
)
CLAIM_CEILING = (
    "NoSourceOnlySpeciesSlot_proof_or_sector_beta_schema_only_no_WEP_pass_"
    "no_clock_transfer_no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1407_0_1406_doc",
            "source_path": "1406-Y5-R10-RAB-common-matter-owner-WEP-zero-theorem-or-sector-beta-acquisition.md",
            "anchor": "NEXT1406_0_1407",
            "role": "prior checkpoint selecting NoSourceOnlySpeciesSlot or sector beta source schema",
        },
        {
            "source_id": "SRC1407_1_1406_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_COMMON_MATTER_OWNER_WEP_ZERO_AUDIT.csv",
            "anchor": "CMO1406_1_single_matter_functional",
            "role": "declares single matter functional and no source-only weights unsigned",
        },
        {
            "source_id": "SRC1407_2_1406_counter",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_WEP_OWNER_COUNTERMODEL_LEDGER.csv",
            "anchor": "CTR1406_0_pre_action_weight",
            "role": "imports pre-action species weight countermodel",
        },
        {
            "source_id": "SRC1407_3_1406_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_SECTOR_BETA_SOURCE_ACQUISITION.csv",
            "anchor": "SBAQ1406_7_verdict",
            "role": "imports strict sector beta acquisition target",
        },
        {
            "source_id": "SRC1407_4_1338_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv",
            "anchor": "THMSTAT1338_0_no_source_slot",
            "role": "states NoSourceOnlySpeciesSlot is an explicit closure condition",
        },
        {
            "source_id": "SRC1407_5_1332_premises",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv",
            "anchor": "PREM1332_3_no_relative_source_prefactors",
            "role": "common-mode premise requiring no relative source prefactors",
        },
        {
            "source_id": "SRC1407_6_1332_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
            "anchor": "CMT1332_2_countermodel",
            "role": "relative source prefactor countermodel survives unless parent-forbidden",
        },
        {
            "source_id": "SRC1407_7_1077_WEP_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "WCO1077_5_verdict",
            "role": "parent WEP owner theorem not closed",
        },
        {
            "source_id": "SRC1407_8_1079_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "NCO1079_5_species_action_weight",
            "role": "Hilbert current owner does not remove pre-variation species weights",
        },
        {
            "source_id": "SRC1407_9_1087_descent",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
            "anchor": "PMD1087_4_pre_action_weights",
            "role": "pre-action weight leak survives parent matter descent",
        },
        {
            "source_id": "SRC1407_10_1310_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_OWNER_SIGNATURE_REPAIR_ATTEMPT.csv",
            "anchor": "OSA1310_3_source_weight_exclusion",
            "role": "source-weight exclusion remains unsigned",
        },
        {
            "source_id": "SRC1407_11_1405_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_SECTOR_RESPONSE_VECTOR_MAP.csv",
            "anchor": "SVP1405_6_vector_verdict",
            "role": "sector response vector map that schema must fill",
        },
        {
            "source_id": "SRC1407_12_1402_isolation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv",
            "anchor": "ISO1402_1_WEP",
            "role": "arena isolation remains active",
        },
        {
            "source_id": "SRC1407_13_this_script",
            "source_path": "scripts/Y5_R10_RAB_NoSourceOnlySpeciesSlot_proof_or_sector_beta_source_schema.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def slot_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NSS1407_0_target",
            "claim_piece": "NoSourceOnlySpeciesSlot",
            "proof_test": "show Arg(S_parent) excludes w_A(X)S_A, kappa_A(X)T_A, inert material labels, and source-only multipliers",
            "evidence": "1406/1338 identify this as the clean blocker",
            "result": "TARGET_SHARPENED",
            "gap": "proof must come from parent grammar/action-domain certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_1_allowed_parent_arguments",
            "claim_piece": "allowed ordinary matter arguments",
            "proof_test": "S_matter[Psi,e_obs(q(Phi)),omega_obs(q(Phi)),theta_rep] only",
            "evidence": "1310 gives candidate signature; 1045/1087 give functor/descent contracts",
            "result": "CANDIDATE_SIGNATURE_EXISTS",
            "gap": "candidate signature is not derived from MTS primitives as exhaustive grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_2_counterexample_locality",
            "claim_piece": "locality/covariance/additivity exclusion",
            "proof_test": "test whether w_A(X)S_A violates locality, covariance, or additivity",
            "evidence": "1332 countermodel and 1406 countermodel ledger",
            "result": "COUNTEREXAMPLE_SURVIVES_BASIC_SYMMETRIES",
            "gap": "basic field-theory constraints do not remove source-only slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_3_hilbert_current_insufficiency",
            "claim_piece": "Hilbert current/source ownership",
            "proof_test": "test whether variation-before-readout kills w_A already inside S_matter",
            "evidence": "1079 NCO1079_5 says pre-variation species weights survive",
            "result": "NOT_DERIVED_BY_CURRENT_OWNER_ALONE",
            "gap": "Hilbert stress inherits pre-action weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_4_measure_action_scale",
            "claim_piece": "species-blind action measure/scale",
            "proof_test": "show one hbar/action measure forbids w_A as a separate coefficient",
            "evidence": "1077 and 1310 require action-measure/object-language ownership",
            "result": "UNSIGNED_MEASURE_ACTION_SCALE_OWNER",
            "gap": "measure owner is still a closure/contract not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_5_material_spectrum",
            "claim_piece": "source-only slot vs material-spectrum slot",
            "proof_test": "exclude hidden X-dependence in masses, binding, alpha_EM, and readouts",
            "evidence": "1310 matter spectrum owner remains not parent-signed",
            "result": "RELATED_SPECTRUM_SLOT_STILL_LIVE",
            "gap": "even if source weights are forbidden, material spectrum betas need ownership or source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_6_exact_conditional",
            "claim_piece": "conditional theorem",
            "proof_test": "if Arg(S_parent) is exhaustively signed and contains no source-only species slots, then w_A/kappa_A branch is forbidden",
            "evidence": "1077 conditional theorem; 1338 common-mode route",
            "result": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "gap": "exhaustive parent grammar is unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "NSS1407_7_current_verdict",
            "claim_piece": "current NoSourceOnlySpeciesSlot status",
            "proof_test": "derive or demote",
            "evidence": "counterexample survives current corpus",
            "result": "NOSOURCEONLYSPECIESSLOT_NOT_PROVED_SCHEMA_REQUIRED",
            "gap": "strict sector beta/source schema required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "SLOT1407_0_wA_action",
            "candidate": "S_matter = sum_A w_A(X) S_A[Psi_A,e_obs,theta_A]",
            "checks_passed": "local;diffeomorphism-covariant;if w_A scalar;additive by species",
            "why_dangerous": "Hilbert source becomes sum_A w_A T_A and WEP/source universality fails",
            "blocked_by_current_corpus": "False",
            "required_blocker": "NoSourceOnlySpeciesSlot parent grammar certificate",
            "status": "LIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "SLOT1407_1_kappaA_source",
            "candidate": "source map uses kappa_A(X) T_A after material labelling but before gravity coupling",
            "checks_passed": "can be written as a source selection rule unless source functor forgets labels",
            "why_dangerous": "composition-dependent gravitational source without changing ordinary equations of motion",
            "blocked_by_current_corpus": "False",
            "required_blocker": "label-forgetting source quotient plus no source-only slot",
            "status": "LIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "SLOT1407_2_hidden_marker",
            "candidate": "material marker M_A(X) enters readout/worldtube/source kernel",
            "checks_passed": "can be downstream of equations unless readout/source ordering is signed",
            "why_dangerous": "reopens WEP after common Hilbert current",
            "blocked_by_current_corpus": "False",
            "required_blocker": "no marker/readout radiative closure plus source-kernel owner",
            "status": "LIVE_COUNTEREXAMPLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "SLOT1407_3_post_variation_selector",
            "candidate": "F(T_A,A) after variation redefines measured source",
            "checks_passed": "not allowed if readout is strictly downstream of variational source",
            "why_dangerous": "less dangerous than pre-action w_A but still a reporting/kernel issue",
            "blocked_by_current_corpus": "Conditional",
            "required_blocker": "readout order/source kernel theorem",
            "status": "PARTIALLY_BLOCKED_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "SLOT1407_4_verdict",
            "candidate": "source-only species slot family",
            "checks_passed": "at least one pre-variation counterexample survives",
            "why_dangerous": "prevents theorem-zero WEP/local source universality",
            "blocked_by_current_corpus": "False",
            "required_blocker": "explicit grammar proof or finite coefficient bounds",
            "status": "SLOT_PROOF_FAILS_USE_SCHEMA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def schema_rows() -> list[dict[str, Any]]:
    base = [
        ("SCHEMA1407_0_beta_e", "beta_e^a", "electronic/atomic sector response", "partial ln E_e / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "clock/fine-structure;WEP;R10"),
        ("SCHEMA1407_1_beta_nuc", "beta_nuc^a", "nuclear/QCD binding response", "partial ln E_nuc / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;orbital;R10"),
        ("SCHEMA1407_2_beta_EM", "beta_EM^a", "EM binding/charge/fine-structure response", "partial ln E_EM / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;clock;R10"),
        ("SCHEMA1407_3_beta_other", "beta_other^a", "other binding/readout guard response", "partial ln E_other / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;PPN;readout"),
        ("SCHEMA1407_4_U_source", "U_a", "WEP source/kernel contraction", "K_ab(lambda,lab) alpha_source^b", "inverse response-coordinate or arena-normalized source factor", "WEP only until transfer theorem"),
        ("SCHEMA1407_5_Delta_f", "Delta f_s,AB", "full material contrast tensor", "f_s,A - f_s,B for each material pair and sector", "dimensionless fraction", "WEP material scoring"),
        ("SCHEMA1407_6_P_s", "P_s", "compressed sector pressure coefficient", "P_s := beta_s^a U_a", "dimensionless Eotvos-response coefficient", "WEP pressure only"),
        ("SCHEMA1407_7_slot_certificate", "NoSourceOnlySpeciesSlot_certificate", "parent grammar/action-domain certificate", "Arg(S_parent) excludes w_A(X)S_A and kappa_A(X)T_A", "boolean theorem certificate", "WEP/local source universality"),
    ]
    rows = []
    required_columns = (
        "coefficient_id;quantity;parent_definition;units;dimension_basis;value;"
        "uncertainty;sign_convention;source_path;source_anchor;arena_projection;"
        "lambda_or_domain;valid_for_claim;claim_allowed"
    )
    for coefficient_id, quantity, role, parent_definition, units, arena in base:
        rows.append(
            {
                "coefficient_id": coefficient_id,
                "quantity": quantity,
                "role": role,
                "parent_definition": parent_definition,
                "required_units": units,
                "required_columns": required_columns,
                "current_value": "MISSING_SOURCE_VALUE",
                "current_source_path": "MISSING_SOURCE_PATH",
                "current_source_anchor": "MISSING_SOURCE_ANCHOR",
                "arena_projection": arena,
                "valid_for_claim": False,
                "claim_allowed": False,
                "status": "SCHEMA_ROW_NONCLAIM",
            }
        )
    rows.append(
        {
            "coefficient_id": "SCHEMA1407_8_verdict",
            "quantity": "sector_beta_source_schema",
            "role": "strict finite-branch source contract",
            "parent_definition": "every finite sector coefficient must be theorem-zero or source-valued before scoring",
            "required_units": "declared per row",
            "required_columns": required_columns,
            "current_value": "SCHEMA_ONLY",
            "current_source_path": "not_applicable",
            "current_source_anchor": "not_applicable",
            "arena_projection": "WEP pressure only until transfer gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
            "status": "STRICT_SCHEMA_READY_NO_VALUES",
        }
    )
    return rows


def schema_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SG1407_0_no_missing_values",
            "requirement": "no finite coefficient row may have MISSING_SOURCE_VALUE when valid_for_claim=true",
            "current_status": "ALL_ROWS_NONCLAIM",
            "failure_action": "keep WEP branch blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SG1407_1_units",
            "requirement": "units and parent-coordinate dimension basis must be declared",
            "current_status": "SCHEMA_DECLARED_VALUES_MISSING",
            "failure_action": "do not compare coefficients across sectors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SG1407_2_source_paths",
            "requirement": "source_path and source_anchor must be real local/provenance-backed rows",
            "current_status": "MISSING_FOR_ALL_VALUE_ROWS",
            "failure_action": "no claim-ready coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SG1407_3_arena_projection",
            "requirement": "WEP rows cannot transfer to clocks/R10/PPN without arena projection theorem",
            "current_status": "BLOCKED_BY_1402_ARENA_ISOLATION",
            "failure_action": "WEP pressure only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SG1407_4_no_pair_cancellation",
            "requirement": "no coefficient set may be accepted only because it cancels one material pair",
            "current_status": "PAIR_CANCELLATION_FORBIDDEN",
            "failure_action": "require all-material theorem or multi-material evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SG1407_5_verdict",
            "requirement": "schema acceptance status",
            "current_status": "SCHEMA_READY_VALUES_MISSING_NO_PASS",
            "failure_action": "move to source acquisition/fill queue",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1407_0_slot_proof",
            "claim": "NoSourceOnlySpeciesSlot is proved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "w_A(X)S_A pre-action counterexample survives current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1407_1_WEP_zero",
            "claim": "common matter-owner WEP zero is proved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "slot proof, matter spectrum owner, binding inheritance, and source kernel remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1407_2_schema_values",
            "claim": "sector beta/source coefficients are claim-ready",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1407 creates schema only; all finite values remain missing/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1407_3_transfer",
            "claim": "WEP coefficients transfer to clocks, R10, PPN, or orbital arenas",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 arena isolation remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1407_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "schema does not close q_loc, lambda_A, EM residuals, source kernel, or PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1407_0_slot_status",
            "decision": "do not promote NoSourceOnlySpeciesSlot",
            "basis": "basic symmetries and Hilbert current do not kill pre-action species weights",
            "action": "retain as explicit closure condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1407_1_schema_status",
            "decision": "strict schema is now the finite-branch contract",
            "basis": "sector beta values need units, source anchors, arena projections, and no pair-cancellation credit",
            "action": "next checkpoint should create fill queue/source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1407_2_best_next",
            "decision": "source acquisition should prioritize U_a and beta_EM/beta_nuc blockers",
            "basis": "U_a is needed for every WEP coefficient; EM/nuclear sectors are the most entangled with prior blockers",
            "action": "build 1408 coefficient fill queue and first source-ready templates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1407_0_1408",
            "target_doc": "1408-Y5-R10-RAB-sector-beta-source-fill-queue-and-Ua-kernel-contract.md",
            "target_script": "scripts/Y5_R10_RAB_sector_beta_source_fill_queue_and_Ua_kernel_contract.py",
            "task": "build the fill queue for beta_e, beta_nuc, beta_EM, beta_other, U_a, Delta f_s,AB, and P_s; prioritize deriving or sourcing U_a and the beta_EM/beta_nuc blockers",
            "success_condition": "each finite WEP coefficient has either a theorem-zero gate or a source-ready nonclaim template with units, source path, anchor, arena projection, sign convention, and no pair-cancellation credit",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    schema_gate: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()

    def row(check_id: str, status: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "timestamp_utc": now,
        }

    all_sources_ok = all(r["path_exists"] and r["anchor_found"] for r in sources)
    proof_ok = (
        any(r["audit_id"] == "NSS1407_6_exact_conditional" and r["result"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED" for r in proof)
        and any(r["audit_id"] == "NSS1407_7_current_verdict" and r["result"] == "NOSOURCEONLYSPECIESSLOT_NOT_PROVED_SCHEMA_REQUIRED" for r in proof)
        and all(str(r["claim_allowed"]) == "False" for r in proof)
    )
    counter_ok = (
        any(r["test_id"] == "SLOT1407_0_wA_action" and r["status"] == "LIVE_COUNTEREXAMPLE" for r in counters)
        and any(r["test_id"] == "SLOT1407_4_verdict" and r["status"] == "SLOT_PROOF_FAILS_USE_SCHEMA" for r in counters)
        and all(str(r["valid_for_claim"]) == "False" for r in counters)
    )
    schema_ok = (
        any(r["quantity"] == "beta_e^a" and r["current_value"] == "MISSING_SOURCE_VALUE" for r in schema)
        and any(r["quantity"] == "U_a" and r["current_value"] == "MISSING_SOURCE_VALUE" for r in schema)
        and any(r["coefficient_id"] == "SCHEMA1407_8_verdict" and r["status"] == "STRICT_SCHEMA_READY_NO_VALUES" for r in schema)
        and all(str(r["claim_allowed"]) == "False" for r in schema)
    )
    schema_gate_ok = (
        any(r["gate_id"] == "SG1407_5_verdict" and r["current_status"] == "SCHEMA_READY_VALUES_MISSING_NO_PASS" for r in schema_gate)
        and all(str(r["valid_for_claim"]) == "False" for r in schema_gate)
    )
    claim_ok = all(str(r["claim_allowed"]) == "False" and "NO_CLAIM" in r["status"] for r in claims)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        SLOT_PROOF_AUDIT_PATH,
        COUNTEREXAMPLE_PATH,
        SCHEMA_PATH,
        SCHEMA_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all(str((ROOT / path).resolve()).startswith(str(ROOT.resolve())) for path in output_paths)

    checks = [
        row("VAL1407_0_sources", all_sources_ok, "all cited local source paths exist and anchors are present"),
        row("VAL1407_1_slot_proof", proof_ok, "NoSourceOnlySpeciesSlot remains exact conditional only and not proved"),
        row("VAL1407_2_counterexamples", counter_ok, "source-only slot counterexamples remain live"),
        row("VAL1407_3_schema", schema_ok, "strict sector beta/source schema is present with missing values nonclaim"),
        row("VAL1407_4_schema_gate", schema_gate_ok, "schema acceptance gates block claims until values/sources exist"),
        row("VAL1407_5_claim_refusal", claim_ok, "slot, WEP, transfer, and local-GR claims are refused"),
        row("VAL1407_6_scope", scope_ok, "outputs are confined to post-checkpoint-work paths"),
    ]
    overall = all(check["status"] == "PASS" for check in checks)
    checks.append(
        row(
            "VAL1407_7_overall",
            overall,
            "1407 rejects the slot proof as unsigned and writes strict nonclaim sector beta source schema",
        )
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    schema_gate: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 1407 — NoSourceOnlySpeciesSlot Proof Or Sector-Beta Source Schema

**Status:** `{STATUS}`

**Current verdict:** `NoSourceOnlySpeciesSlot` is not proved. The pre-action counterexample `S_matter = sum_A w_A(X) S_A` remains compatible with the currently signed corpus unless the parent grammar/action-domain explicitly forbids source-only species slots.

**Discipline move:** the WEP zero route stays exact-conditional only. The finite route now has a strict schema: no `beta_s`, `U_a`, `Delta f_s,AB`, or `P_s` row can become claim-ready without units, source path, source anchor, arena projection, sign convention, and no pair-cancellation credit.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## NoSourceOnlySpeciesSlot Proof Audit

{md_table(proof)}

## Source-Only Slot Counterexample Test

{md_table(counters)}

## Sector Beta Source Schema

{md_table(schema)}

## Schema Acceptance Gate

{md_table(schema_gate)}

## Claim Gate

{md_table(claims)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    proof = slot_proof_rows()
    counters = counterexample_rows()
    schema = schema_rows()
    schema_gate = schema_gate_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, proof, counters, schema, schema_gate, claims)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(SLOT_PROOF_AUDIT_PATH, proof)
    write_csv(COUNTEREXAMPLE_PATH, counters)
    write_csv(SCHEMA_PATH, schema)
    write_csv(SCHEMA_GATE_PATH, schema_gate)
    write_csv(CLAIM_GATE_PATH, claims)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, proof, counters, schema, schema_gate, claims, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1407 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
