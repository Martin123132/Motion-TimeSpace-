from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2852-Y5-R2FR-source-doublet-symmetry-owner-or-closure-demotion-under-AX1090.md"

SRC_2851_DOC = ROOT / "2851-Y5-R2FR-minimal-parent-amplitude-owner-ansatz-or-no-go-under-AX1090.md"
SRC_2851_PROOF = RESIDUALS / "P8_Y5_R2FR_2851_ALGEBRAIC_PROOF_ATTEMPT.csv"
SRC_2851_NOGO = RESIDUALS / "P8_Y5_R2FR_2851_NO_GO_TUNING_LEDGER.csv"
SRC_2851_REQ = RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv"
SRC_2851_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2851_VALIDATION.csv"
SRC_2850_ROUTES = RESIDUALS / "P8_Y5_R2FR_2850_DERIVATION_ROUTE_RANKING.csv"
SRC_2850_MANUAL = RESIDUALS / "P8_Y5_R2FR_2850_MANUAL_SOURCE_LEDGER.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_CANCEL = RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_974 = ROOT / "974-Y5-R10-zero-origin-evenness-theorem-or-boundary-flux-coefficient-fill.md"
SRC_980 = ROOT / "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2852_SOURCE_REGISTER.csv",
    "candidates": RESIDUALS / "P8_Y5_R2FR_2852_SYMMETRY_CANDIDATE_MATRIX.csv",
    "owner_test": RESIDUALS / "P8_Y5_R2FR_2852_OWNER_ACCEPTANCE_TEST.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2852_CLOSURE_DEMOTION_LEDGER.csv",
    "fallback": RESIDUALS / "P8_Y5_R2FR_2852_FINITE_AMPLITUDE_FALLBACK_CONTRACT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2852_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2852_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2852_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2852_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2852_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": LOCAL_BOUNDS / "RAB_SOURCE_DOUBLET_SYMMETRY_CANDIDATES_2852_NONCLAIM.csv",
    "demotion_copy": SOURCE_WEIGHT / "RAB_SHARED_CURRENT_CLOSURE_DEMOTION_2852_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2852_finite_amplitude_fallback_source_row_NEXT.csv",
    "fallback_copy": BETA_DOCS / "RAB_FINITE_AMPLITUDE_FALLBACK_CONTRACT_2852_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2852_0_2851_doc", SRC_2851_DOC, "NEXT2851_0_2852;VAL2851_OVERALL", "2851 selected source-doublet symmetry owner test"),
        ("SRC2852_1_2851_proof", SRC_2851_PROOF, "ALG2851_3_identity;ALG2851_4_no_free_lunch", "conditional common-current algebra"),
        ("SRC2852_2_2851_nogo", SRC_2851_NOGO, "NG2851_0_ratio_tuning;NG2851_1_current_rescaling", "2851 tuning and rescaling no-go rows"),
        ("SRC2852_3_2851_requirements", SRC_2851_REQ, "REQ2851_1_symmetry_owner;REQ2851_2_current_owner;REQ2851_3_operator_sign", "2851 parent signature requirements"),
        ("SRC2852_4_2851_validation", SRC_2851_VALIDATION, "VAL2851_OVERALL", "2851 validation"),
        ("SRC2852_5_2850_routes", SRC_2850_ROUTES, "ROUTE2850_0_shared_parent_current;ROUTE2850_4_absorb_into_GM", "2850 route ranking"),
        ("SRC2852_6_2850_manual", SRC_2850_MANUAL, "MAN2850_4_identity;MAN2850_5_boundary", "2850 manual source ledger"),
        ("SRC2852_7_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "exact symbolic suppression condition"),
        ("SRC2852_8_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "source-current and sign contract gaps"),
        ("SRC2852_9_2844_cancel", SRC_2844_CANCEL, "CANCEL2844_1_parent_source_identity;CANCEL2844_5_verdict", "amplitude cancellation parent proof still missing"),
        ("SRC2852_10_1078", SRC_1078, "OL1078_4_verdict;CO1078_4_verdict;CEK1078_1_current_rescaling", "object/current owner still unsigned"),
        ("SRC2852_11_974", SRC_974, "ZOE974_2_evenness_kills_linear;ZOE974_6_verdict", "relative evenness theorem exists but parent unsigned"),
        ("SRC2852_12_980", SRC_980, "NMF980_2_scalar_obstruction_lemma;NMF980_7_verdict", "broad no-marker theorem rejected for current corpus"),
        ("SRC2852_13_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full PPN vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def candidate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SYM2852_0_fixed_source_vector",
            "fixed source-doublet vector",
            "parent action contains J_star*kappa_star*(-sigma_R*C_AB+R_delta)",
            "would fix (a_C,a_R)=kappa_star*(-sigma_R,1)",
            "mathematically sufficient",
            "MISSING_PARENT_SOURCE_DOUBLET_TERM",
            "not accepted because the term is not sourced from an existing parent action",
        ),
        (
            "SYM2852_1_Z2_or_OE_evenness",
            "Z2/O(E) evenness owner",
            "a signed field-space symmetry forbids the orthogonal source covector",
            "could kill the tuning freedom by representation theory",
            "relative theorem shape exists in 974",
            "MISSING_PARENT_Z2_OR_OEX_SYMMETRY_FOR_THIS_DOUBLET",
            "not accepted because 974 is parent-unsigned and not specific to C_AB/R_delta",
        ),
        (
            "SYM2852_2_O11_or_symplectic_doublet",
            "O(1,1)/symplectic doublet",
            "operator metric pairs C_AB and R_delta with signature fixed by sigma_R",
            "could make the source vector a canonical null/eigen direction",
            "plausible ansatz",
            "MISSING_REPRESENTATION_AND_METRIC_OWNER",
            "not accepted because preserving a bilinear does not by itself choose the source vector",
        ),
        (
            "SYM2852_3_no_marker_object_language",
            "no-marker/object-language theorem",
            "forbid any independent covector in source-doublet space",
            "would make the ratio structural rather than fitted",
            "too broad in current corpus",
            "OBSTRUCTED_BY_980_AND_1078",
            "not accepted because broad no-marker fails and object-language/current owner are unsigned",
        ),
        (
            "SYM2852_4_auxiliary_constraint",
            "auxiliary amplitude constraint",
            "lambda_amp*(Q_CAB+sigma_R*q_R_eff)",
            "directly imposes the wanted identity",
            "closure mechanism only",
            "CLOSURE_AXIOM_RISK",
            "rejected unless lambda_amp descends from an existing parent gauge/constraint algebra",
        ),
    ]
    return [
        nonclaim(
            {
                "candidate_id": candidate_id,
                "candidate_owner": owner,
                "mathematical_form": form,
                "would_fix": would_fix,
                "status": status,
                "blocker": blocker,
                "verdict": verdict,
                "parent_signed": False,
                "accepted_owner": False,
                "control_only": True,
            }
        )
        for candidate_id, owner, form, would_fix, status, blocker, verdict in specs
    ]


def owner_test_rows() -> list[dict[str, Any]]:
    specs = [
        ("OWN2852_0_ratio_fixed_before_fit", "Does the parent fix a_C/a_R before local PPN fitting?", "required for derivation", "FAIL", "only conditional ansatz rows exist"),
        ("OWN2852_1_no_independent_rescaling", "Can one projection or current be rescaled independently?", "must be forbidden", "FAIL", "1078 current-rescaling counterexample survives"),
        ("OWN2852_2_operator_sign", "Is sigma_R fixed by the same parent operator/Green convention?", "required for sign-stable identity", "FAIL", "2844 sign contract remains missing"),
        ("OWN2852_3_marker_exclusion", "Are orthogonal source covectors/markers excluded?", "required to avoid hidden tuning", "FAIL", "974/980 show only relative or obstructed no-marker results"),
        ("OWN2852_4_boundary_inclusion", "Are boundary/corner fluxes zero or included in the identity?", "required for exact charge relation", "FAIL", "manual ledger still has boundary flux law missing"),
        ("OWN2852_5_verdict", "Source-doublet symmetry owner accepted?", "all owner tests must pass", "NOT_ACCEPTED", "no parent-signed symmetry/object-language owner found"),
    ]
    return [
        nonclaim(
            {
                "owner_test_id": test_id,
                "test": test,
                "needed_for": needed_for,
                "result": result,
                "reason": reason,
                "passed": False,
                "accepted_owner": False,
                "control_only": True,
            }
        )
        for test_id, test, needed_for, result, reason in specs
    ]


def demotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEM2852_0_keep_math", "Retain the algebraic identity as a closure theorem.", "A_total=0 iff a_C=-sigma_R*a_R for the shared-current ansatz", "CLOSURE_ONLY_RETAINED"),
        ("DEM2852_1_reject_claim", "Reject parent theorem-zero promotion.", "the ratio is not owned by symmetry/current/object language", "THEOREM_ZERO_NOT_ACCEPTED"),
        ("DEM2852_2_reject_auxiliary_shortcut", "Do not add lambda_amp solely to force the plateau.", "that would smuggle the result into the action", "AUXILIARY_SHORTCUT_REJECTED"),
        ("DEM2852_3_retain_fallback", "Keep finite amplitude fallback active.", "if derivation is not signed, Q_CAB/q_R_eff/sigma_R must be sourced and bounded", "FINITE_FALLBACK_RETAINED"),
        ("DEM2852_4_no_local_GR", "No local-GR/Newton/PPN claim.", "full vector and source-normalized Newton remain open", "CLAIM_LOCKED"),
    ]
    return [
        nonclaim(
            {
                "demotion_id": demotion_id,
                "action": action,
                "reason": reason,
                "result": result,
                "control_only": True,
            }
        )
        for demotion_id, action, reason, result in specs
    ]


def fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("FB2852_0_Q_CAB", "Q_CAB", "finite numeric charge or parent-signed zero theorem", "source_path;equation_anchor;Green_convention;boundary_policy;units", "MISSING_Q_CAB_VALUE_OR_THEOREM"),
        ("FB2852_1_q_R_eff", "q_R_eff", "finite numeric charge or parent-signed zero theorem", "source_path;equation_anchor;Green_convention;source_normalization;units", "MISSING_q_R_eff_VALUE_OR_THEOREM"),
        ("FB2852_2_sigma_R", "sigma_R", "parent action sign/operator convention", "source_path;operator_anchor;Green_kernel;sign", "MISSING_SIGMA_R_PARENT_SIGN"),
        ("FB2852_3_A_total", "A_total", "computed from source-backed Q_CAB,q_R_eff,sigma_R only", "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi); no tuned cancellation unless theorem-owned", "MISSING_CORE_INPUTS"),
        ("FB2852_4_GM", "M_source/GM", "same measured source charge used in U=GM/r", "worldtube/Hamiltonian/Noether charge source; metric 1/r readout; units", "MISSING_GM_PARENT_GLUE"),
        ("FB2852_5_full_vector", "full PPN residual vector", "all local channels finite or theorem-zero in one convention", "beta;preferred;source;endpoint;clock;orbital;q_loc rows", "MISSING_FULL_VECTOR_CLOSURE"),
    ]
    return [
        nonclaim(
            {
                "fallback_id": fallback_id,
                "quantity": quantity,
                "accepted_form": accepted_form,
                "required_provenance": provenance,
                "current_gap": gap,
                "accepted_ready": False,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for fallback_id, quantity, accepted_form, provenance, gap in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    specs = [
        ("CG2852_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2852_1_symmetry_owner", "source-doublet symmetry owner accepted", "BLOCKED", "all owner tests fail in current corpus", False),
        ("CG2852_2_shared_current_theorem", "shared-current route promoted to theorem-zero", "BLOCKED", "demoted to closure-only until owner is signed", False),
        ("CG2852_3_finite_fallback_ready", "finite amplitude fallback row score-ready", "BLOCKED", "source-backed values are not supplied", False),
        ("CG2852_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "full vector and measured-GM charge remain open", False),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "control_check_passed": control_passed,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason, control_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2852_0_symmetry_hunt", "No parent-signed source-doublet symmetry owner found.", "NOT_ACCEPTED", "candidate symmetries are plausible but unsigned or obstructed"),
        ("DEC2852_1_closure", "Shared-current amplitude identity is retained only as closure.", "DEMOTED_TO_CLOSURE_ONLY", "the ratio can still be tuned or rescaled"),
        ("DEC2852_2_auxiliary", "Auxiliary constraint shortcut is rejected for now.", "REJECTED_AS_SMUGGLING_RISK", "no existing parent constraint algebra owns lambda_amp"),
        ("DEC2852_3_fallback", "Finite amplitude fallback is the next executable route.", "SELECTED_2853", "derivation-first was attempted; without symmetry owner, testable finite rows are the honest fallback"),
        ("DEC2852_4_no_claim", "No R10, PPN, local-GR or Newton claim.", "LOCKED", "this checkpoint is a route demotion and fallback contract"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2852_0_2853",
                "status": "selected_primary",
                "target_doc": "2853-Y5-R2FR-finite-amplitude-fallback-source-row-or-parent-action-reentry-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_amplitude_fallback_source_row_or_parent_action_reentry_under_AX1090_2853.py",
                "mission": "build the first strict finite-amplitude fallback runner for Q_CAB, q_R_eff, sigma_R, A_total and GM, while preserving a parent-action reentry hook if a real symmetry/source equation appears",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2852_0_candidates", OUTPUTS["candidates"], BRANCH_OUTPUTS["candidate_copy"], "source-doublet symmetry candidates nonclaim copy"),
        ("COPY2852_1_demotion", OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"], "closure demotion nonclaim copy"),
        ("COPY2852_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2853"),
        ("COPY2852_3_fallback", OUTPUTS["fallback"], BRANCH_OUTPUTS["fallback_copy"], "finite amplitude fallback contract nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {"valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "parent_signed", "accepted_owner", "passed", "accepted_ready", "numeric_value_present", "gate_passed"}
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value", "A_total_value", "delta_p_value", "q_R_hat_value", "Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_prediction_present") is True or row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2852_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2852_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2852_2_no_symmetry_owner_accepted", not any(row["accepted_owner"] for row in rows_by_name["candidates"]) and not any(row["passed"] for row in rows_by_name["owner_test"]), "no parent-signed source-doublet owner accepted"),
        ("VAL2852_3_closure_demotion_present", any(row["demotion_id"] == "DEM2852_1_reject_claim" and row["result"] == "THEOREM_ZERO_NOT_ACCEPTED" for row in rows_by_name["demotion"]), "shared-current route demoted to closure-only"),
        ("VAL2852_4_finite_fallback_retained", len(rows_by_name["fallback"]) >= 6 and not any(row["accepted_ready"] for row in rows_by_name["fallback"]), "finite amplitude fallback contract retained and nonclaim"),
        ("VAL2852_5_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2852_6_next_target_2853", any(row["next_id"] == "NEXT2852_0_2853" and row["selected"] for row in rows_by_name["next"]), "2853 finite amplitude fallback target selected"),
        ("VAL2852_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2852_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2852_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2852_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2852_11_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2852_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2852_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2852_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2852_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2852_OVERALL",
            "passed": overall,
            "detail": "2852 tests candidate source-doublet symmetry owners, accepts none as parent-signed, demotes shared-current cancellation to closure-only, and selects finite amplitude fallback for 2853.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2852 - Y5 R2FR Source-Doublet Symmetry Owner Or Closure Demotion Under AX1090

Status: `Y5_R2FR_2852_source_doublet_symmetry_owner_not_signed_shared_current_demoted_nonclaim`

## Private Verdict

2852 tries to promote the clean 2851 identity from conditional algebra into parent-derived physics.

The best possible shape is still:

```text
(a_C,a_R)=kappa_star*(-sigma_R,1)
Q_CAB=-sigma_R*q_R_eff
A_total=0
```

But the current corpus does not yet contain a parent-signed symmetry, object-language rule, current owner, operator sign owner, or boundary certificate that forces this coupling vector. The broad no-marker route is also not available: 980 already proves the scalar-marker obstruction for the current corpus.

So the shared-current route is retained only as a closure theorem. It is not dead; it is just not allowed to pretend to be a derivation until a real source-doublet symmetry appears.

The honest next move is a finite-amplitude fallback runner: if the theorem route is unsigned, we source `Q_CAB`, `q_R_eff`, `sigma_R`, `A_total`, and `GM` as actual rows and let the local PPN comparator judge them.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Symmetry Candidate Matrix

{markdown_table(rows["candidates"], ["candidate_id", "candidate_owner", "status", "blocker", "verdict", "accepted_owner", "valid_for_claim"])}

## Owner Acceptance Test

{markdown_table(rows["owner_test"], ["owner_test_id", "test", "result", "reason", "passed", "accepted_owner", "valid_for_claim"])}

## Closure Demotion Ledger

{markdown_table(rows["demotion"], ["demotion_id", "action", "result", "reason", "valid_for_claim"])}

## Finite Amplitude Fallback Contract

{markdown_table(rows["fallback"], ["fallback_id", "quantity", "accepted_form", "current_gap", "required_provenance", "accepted_ready", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["candidates"] = candidate_rows()
    rows["owner_test"] = owner_test_rows()
    rows["demotion"] = demotion_rows()
    rows["fallback"] = fallback_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "candidates", "owner_test", "demotion", "fallback", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2852_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2852_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
