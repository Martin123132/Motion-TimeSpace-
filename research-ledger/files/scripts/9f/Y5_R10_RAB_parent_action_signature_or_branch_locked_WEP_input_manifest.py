from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1427-Y5-R10-RAB-parent-action-signature-or-branch-locked-WEP-input-manifest.md"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1427_SOURCE_REGISTER.csv"
PARENT_SIGNATURE_CANDIDATE = OUT / "P8_Y5_R10_1427_PARENT_ACTION_SIGNATURE_CANDIDATE.csv"
SIGNATURE_DECISION_GATE = OUT / "P8_Y5_R10_1427_SIGNATURE_DECISION_GATE.csv"
BRANCH_LOCKED_MANIFEST = OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv"
MANIFEST_SCHEMA = OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_SCHEMA.csv"
LOCAL_DIRECTORY_AUDIT = OUT / "P8_Y5_R10_1427_LOCAL_INPUT_DIRECTORY_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1427_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1427_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1427_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1427_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1427_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    schema_1336_doc = ROOT / "1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md"
    specs = [
        ("SRC1427_0_1426_next", OUT / "P8_Y5_R10_1426_NEXT_TARGET.csv", "NEXT1426_0_1427", "1426 handoff selecting parent signature or branch-locked WEP manifest."),
        ("SRC1427_1_1426_validation", OUT / "P8_Y5_BRR545_1426_VALIDATION.csv", "VAL1426_9_overall", "1426 validation summary."),
        ("SRC1427_2_1426_admissibility", OUT / "P8_Y5_R10_1426_ACTIVE_SOURCE_PREFACTOR_ADMISSIBILITY_AUDIT.csv", "ADM1426_5_verdict", "active-source-prefactor theorem remains unsigned."),
        ("SRC1427_3_1426_pack", OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv", "PACK1426_0_C_parent", "finite WEP coefficient/input pack."),
        ("SRC1427_4_1426_branch_lock", OUT / "P8_Y5_R10_1426_SAME_BRANCH_WEP_LOCK.csv", "LOCK1426_5_verdict", "same-branch WEP lock."),
        ("SRC1427_5_1336_readout_schema_doc", schema_1336_doc, "READSCHEMA1336_4_gx_m_s2", "official MICROSCOPE readout schema recorded in the 1336 checkpoint document."),
        ("SRC1427_6_1336_source_schema_doc", schema_1336_doc, "SRCSCHEMA1336_2_density_kg_m3", "source worldtube schema recorded in the 1336 checkpoint document."),
        ("SRC1427_7_1336_product_schema_doc", schema_1336_doc, "PRODSCHEMA1336_2_tau_eff_definition", "product convention schema recorded in the 1336 checkpoint document."),
        ("SRC1427_8_1336_branch_schema_doc", schema_1336_doc, "BRANCHSCHEMA1336_0_same_parent_branch_id", "branch classifier schema recorded in the 1336 checkpoint document."),
        ("SRC1427_9_1082_parent_DD", OUT / "P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv", "PTD1082_4_verdict", "parent-to-DD coefficient map remains unsigned."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "SIG1427_0_action_shape",
            "clause": "ordinary matter action descends only through one observed quotient metric/coframe",
            "candidate_signature": "S_matter = S_matter[psi, e_obs(q(Phi)), theta_obs]",
            "purpose": "make ordinary matter blind to representative/source-only labels",
            "status": "DECLARED_CLOSURE_CANDIDATE_NOT_DERIVED",
            "what_would_promote": "derive q, e_obs descent, and allowed argument list from parent MTS primitives",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "SIG1427_1_no_active_source_prefactors",
            "clause": "no active source-only species prefactors before variation",
            "candidate_signature": "forbid terms sum_A w_A S_A when w_A is not a nongravitational measured theta_A",
            "purpose": "kill the pre-variation w_A countermodel and restore common-mode WEP zero",
            "status": "DECLARED_CLOSURE_CANDIDATE_NOT_DERIVED",
            "what_would_promote": "parent admissibility/type theorem proving source-only scalars are ill-typed",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "SIG1427_2_variation_before_readout",
            "clause": "variation happens before readout/material projection",
            "candidate_signature": "T_obs := delta S_matter / delta e_obs before K_readout or material-channel projection",
            "purpose": "retain 1079 Hilbert-current subtheorem and block post-variation selectors",
            "status": "CONDITIONAL_SUBTHEOREM_DEPENDS_ON_SIGNATURE",
            "what_would_promote": "parent readout-order axiom or derived measurement functor order",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "SIG1427_3_single_measure_owner",
            "clause": "one action-scale/measure owner for ordinary matter",
            "candidate_signature": "relative sector action scales are either measured nongravitational constants or inadmissible as active-source weights",
            "purpose": "prevent action normalization from reappearing as WEP source charge",
            "status": "CLOSURE_CANDIDATE_MEASURE_OWNER_UNSIGNED",
            "what_would_promote": "derive hbar/measure owner and radiative stability in parent action",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "SIG1427_4_verdict",
            "clause": "parent action signature adoption status",
            "candidate_signature": "signature is useful as a closure option, not a derived theorem",
            "purpose": "separate derivation path from explicit closure path",
            "status": "NOT_ADOPTED_IN_1427",
            "what_would_promote": "user/theory decision to mark closure axiom plus later empirical stress tests, or a real derivation from primitives",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signature_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "SGD1427_0_derivation_route",
            "route": "continue deriving the parent admissibility theorem",
            "current_status": "OPEN_BUT_UNSIGNED",
            "benefit": "would give GR-like WEP/common-mode zero without finite source coefficients",
            "risk": "may require a primitive object-language axiom rather than a derivation",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "SGD1427_1_closure_route",
            "route": "declare the parent action signature as explicit closure",
            "current_status": "AVAILABLE_BUT_NOT_ADOPTED",
            "benefit": "clean minimal theory spine and direct common-mode WEP zero route",
            "risk": "less derivable; must be advertised as an axiom/closure, not proof",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "SGD1427_2_finite_manifest_route",
            "route": "build branch-locked finite WEP input manifest",
            "current_status": "SELECTED_NOW_NONCLAIM",
            "benefit": "keeps empirical route alive without pretending closure is derivation",
            "risk": "more phenomenological until C_parent and source/readout inputs are parent-owned",
            "selected_now": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def branch_manifest_rows() -> list[dict[str, Any]]:
    base = MICROSCOPE / "branch_locked_wep"
    rows = [
        ("MAN1427_0_branch_id", base / "branch_id.csv", "same_parent_branch_id;forbidden_mixing_rule;signature_option;source_basis;readout_basis", "locks every finite-WEP input into one branch"),
        ("MAN1427_1_C_parent", base / "coefficients" / "C_parent.csv", "coefficient_id;component;value;uncertainty;units;sign_convention;basis;source_path;parent_status", "parent or source-backed coefficient vector"),
        ("MAN1427_2_epsilon_e", base / "coefficients" / "epsilon_e.csv", "coefficient_id;value_or_bound;units;tau_eff_status;source_path;zero_certificate_status;validity_scope", "electron residual coefficient branch"),
        ("MAN1427_3_DD_coefficients", base / "coefficients" / "dd_alpha_surface.csv", "component;proxy_bound;physical_value;units;MTS_to_DD_map_status;source_path;claim_policy", "optional external DD comparator branch"),
        ("MAN1427_4_R_source", base / "source" / "R_source_Earth.csv", "component;value;uncertainty;units;profile_weighting;worldtube_support;source_path;basis", "Earth/source vector in same basis as C_parent"),
        ("MAN1427_5_R_material", base / "material" / "R_TA6V_minus_PtRh10.csv", "component;value;uncertainty;units;material_model;basis;source_path;parent_status", "full Ti/Pt material response tensor"),
        ("MAN1427_6_K_CMSM", base / "readout" / "K_CMSM.csv", "time_s;session_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;source_path;units", "official/validated MICROSCOPE readout kernel"),
        ("MAN1427_7_product_convention", base / "product" / "eta_product_convention.csv", "eta_formula;sign_convention;tau_eff_definition;orbit_average_rule;units;source_path", "maps coefficient/source/material/readout product to eta"),
        ("MAN1427_8_measured_G_guard", base / "guards" / "measured_G_guard.csv", "guard_id;allowed_common_mode;forbidden_relative_absorption;calibration_equation;source_path", "prevents measured-G absorption shortcut"),
    ]
    manifest: list[dict[str, Any]] = []
    for manifest_id, path, required_fields, purpose in rows:
        path.parent.mkdir(parents=True, exist_ok=True)
        manifest.append(
            {
                "manifest_id": manifest_id,
                "target_path": str(path),
                "required_fields": required_fields,
                "purpose": purpose,
                "current_status": "WAITING_FOR_SOURCE_FILE",
                "file_exists_now": path.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    manifest.append(
        {
            "manifest_id": "MAN1427_9_verdict",
            "target_path": str(base),
            "required_fields": "all MAN1427_0 through MAN1427_8 files populated and mutually branch-consistent",
            "purpose": "first branch-locked finite WEP scorepack",
            "current_status": "MANIFEST_READY_FILES_MISSING",
            "file_exists_now": base.exists(),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return manifest


def manifest_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "SCHEMA1427_0_branch_lock",
            "object": "same_parent_branch_id",
            "required_in_files": "all branch_locked_wep CSVs",
            "rule": "all finite product rows must share one branch id or be refused",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SCHEMA1427_1_units",
            "object": "units/sign convention",
            "required_in_files": "C_parent; R_source; R_material; K_CMSM; product convention",
            "rule": "no dimensionless product unless every factor declares units and conversion to eta",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SCHEMA1427_2_provenance",
            "object": "source_path",
            "required_in_files": "all claim-input files",
            "rule": "every numeric row needs a local source path or URL/DOI provenance string",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SCHEMA1427_3_no_shortcut",
            "object": "shortcut guards",
            "required_in_files": "measured_G_guard; product convention; branch_id",
            "rule": "forbid tau=1, DD-as-MTS, unit source proxy, surrogate arrays as official, and measured-G absorption",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def directory_audit_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dirs = sorted({Path(row["target_path"]).parent for row in manifest if row["manifest_id"] != "MAN1427_9_verdict"})
    rows: list[dict[str, Any]] = []
    for index, directory in enumerate(dirs):
        rows.append(
            {
                "audit_id": f"DIR1427_{index}",
                "absolute_path": str(directory),
                "exists": directory.exists(),
                "file_count": len([path for path in directory.glob("*") if path.is_file()]) if directory.exists() else 0,
                "status": "DIRECTORY_READY_FILES_PENDING",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1427_0_signature_closure",
            "target": "parent action signature/admissibility closure",
            "input_status": "CLOSURE_CANDIDATE_NOT_ADOPTED",
            "runner_status": "REFUSED_AS_DERIVATION",
            "score_ready": False,
            "reason": "signature is not derived and not adopted as an explicit closure axiom in 1427",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1427_1_branch_manifest",
            "target": "branch-locked finite WEP product",
            "input_status": "MANIFEST_READY_FILES_MISSING",
            "runner_status": "WAITING_FOR_SOURCE_INPUTS",
            "score_ready": False,
            "reason": "C_parent/R_source/R_material/K_CMSM/product convention files are not populated",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1427_0_parent_signature",
            "claim_component": "parent action signature forbids w_A",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "closure candidate only; not derived/adopted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1427_1_branch_manifest",
            "claim_component": "branch-locked finite WEP input manifest",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "manifest exists, but inputs are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1427_2_finite_WEP_score",
            "claim_component": "finite WEP score",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no populated C_parent/R_source/R_material/K_CMSM/product convention rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1427_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "neither common-mode closure nor finite WEP prediction proves local GR",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1427_0_signature",
            "decision": "record the parent action signature as a closure candidate only",
            "because": "it would solve the w_A problem, but the corpus does not derive it from primitives",
            "effect": "common-mode route remains available without being claimed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1427_1_manifest",
            "decision": "build the branch-locked finite WEP input manifest now",
            "because": "it is the honest next empirical route if closure is not adopted",
            "effect": "future input files have exact locations and schemas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1427_2_next",
            "decision": "next work should either populate one manifest row or decide closure adoption explicitly",
            "because": "1427 has separated derivation, closure, and finite-input branches",
            "effect": "1428 should fill the branch classifier/manifest first or write a closure-adoption consequences ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1427_0_1428",
            "next_target": "1428-Y5-R10-RAB-branch-classifier-first-row-or-closure-adoption-consequence-ledger.md",
            "script": "scripts/Y5_R10_RAB_branch_classifier_first_row_or_closure_adoption_consequence_ledger.py",
            "objective": "either create the first branch-classifier row for the finite WEP manifest, or write a closure-adoption consequence ledger for the parent action signature without pretending it is derived.",
            "include": "branch id row; no-mixing rule; finite WEP manifest status; closure consequence ledger; runner refusal",
            "exclude": "WEP/local-GR claim; tau=1; DD as MTS ontology; component fitting; measured-G absorption; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        PARENT_SIGNATURE_CANDIDATE,
        SIGNATURE_DECISION_GATE,
        BRANCH_LOCKED_MANIFEST,
        MANIFEST_SCHEMA,
        LOCAL_DIRECTORY_AUDIT,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    for path in csvs:
        try:
            _ = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
    signature_not_adopted = any(
        row["signature_id"] == "SIG1427_4_verdict" and row["status"] == "NOT_ADOPTED_IN_1427"
        for row in signature
    )
    manifest_ready = any(
        row["manifest_id"] == "MAN1427_9_verdict" and row["current_status"] == "MANIFEST_READY_FILES_MISSING"
        for row in manifest
    )
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims)
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1427_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1427 cited source paths and anchors resolve"),
        ("VAL1427_1_signature_not_adopted", signature_not_adopted, "parent action signature is closure candidate only"),
        ("VAL1427_2_manifest_ready", manifest_ready, "branch-locked finite WEP manifest paths and schemas are written"),
        ("VAL1427_3_claim_gates", claims_safe, "all claim gates keep claim_allowed=false"),
        ("VAL1427_4_csv_parse", parse_ok, "all generated 1427 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1427_5_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1427_6_next_target", True, "1428 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1427_7_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1427 records parent action signature as non-adopted closure candidate and builds branch-locked finite WEP manifest as nonclaim",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1427 - Parent action signature or branch-locked WEP input manifest",
            "**Current verdict:** 1427 does not derive or adopt the parent action signature. It records the exact closure signature that would kill `w_A`, then keeps it nonclaim and builds the branch-locked finite WEP input manifest instead.",
            "**Main progress:** the finite WEP route now has concrete local target paths and schemas for `C_parent`, `epsilon_e`, DD comparator coefficients, `R_source`, `R_material`, `K_CMSM`, product convention, branch lock, and measured-G guard.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Parent action signature candidate\n" + md_table(sections["signature"]),
            "## Signature decision gate\n" + md_table(sections["signature_gate"]),
            "## Branch-locked WEP input manifest\n" + md_table(sections["manifest"]),
            "## Branch-locked WEP schema\n" + md_table(sections["schema"]),
            "## Local input directory audit\n" + md_table(sections["directories"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    signature = parent_signature_rows()
    signature_gate = signature_decision_rows()
    manifest = branch_manifest_rows()
    schema = manifest_schema_rows()
    directories = directory_audit_rows(manifest)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_SIGNATURE_CANDIDATE, signature)
    write_csv(SIGNATURE_DECISION_GATE, signature_gate)
    write_csv(BRANCH_LOCKED_MANIFEST, manifest)
    write_csv(MANIFEST_SCHEMA, schema)
    write_csv(LOCAL_DIRECTORY_AUDIT, directories)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, signature, manifest, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "signature": signature,
            "signature_gate": signature_gate,
            "manifest": manifest,
            "schema": schema,
            "directories": directories,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1427_signature_closure_not_adopted_branch_locked_WEP_manifest_written_nonclaim")


if __name__ == "__main__":
    main()
