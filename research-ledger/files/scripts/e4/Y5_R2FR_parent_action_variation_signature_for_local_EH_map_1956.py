from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1956-Y5-R2FR-parent-action-variation-signature-for-local-EH-map.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1956_VALIDATION.csv"

SOURCES = {
    "1955_doc": {
        "path": ROOT / "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md",
        "needles": ["EH1955_2_same_source_map", "EH1955_6_zero_verdict", "NEXT1955_0_primary"],
    },
    "1955_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1955_VALIDATION.csv",
        "needles": ["VAL1955_OVERALL", "PASS"],
    },
    "956_spine": {
        "path": ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
        "needles": ["SSG956_2_total_Hilbert_source", "LHG956_0_EH_core_selection", "HCG956_2_nonHilbert_current"],
    },
    "957_local_gr_order": {
        "path": ROOT / "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
        "needles": ["PLG957_2_EH_operator", "PLG957_3_extra_sector_silence", "DEC957_0_branch_choice"],
    },
    "990_parent_contract": {
        "path": ROOT / "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md",
        "needles": ["PAC990_1_gravity_operator", "PAC990_2_matter_functor", "PAC990_5_Ward_Bianchi"],
    },
    "1008_variation_warning": {
        "path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["PVA1008_0_parent_action", "PVA1008_5_EH_import_limit"],
    },
    "1476_source_label": {
        "path": ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
        "needles": ["SLF1476_0_target", "SLP1476_4_nonHilbert_silence"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1956 parent action variation signature for local EH map",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def signature_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SIG1956_0_observed_geometry",
            "one observed metric/coframe for local matter, source variation, clocks, photons, and PPN/Cassini readout",
            "q(Phi)->g_obs,e_obs; all source/readout maps use same branch",
            "CONDITIONAL_SPINE_NOT_FULLY_SIGNED",
            "956/957/990 keep one-frame contract visible",
            "frame/readout theorem through PPN order remains unsigned",
        ),
        (
            "SIG1956_1_EH_operator",
            "local exterior gravity operator is EH-only, or every non-EH/R11 term is retained as an executable residual",
            "E_parent = G[g_obs]+Lambda g_obs + DeltaE_R11+DeltaE_extra",
            "UNSIGNED_PRIMARY_BLOCKER",
            "956/957/990 all mark EH/operator selection as not parent-derived",
            "derive metric-only second-order EH selection or fill residual coefficients",
        ),
        (
            "SIG1956_2_total_Hilbert_source",
            "ordinary source is total Hilbert/coframe derivative of one matter action",
            "T_parent=T_Hilbert_total if no species/source-label reentry and current owner is signed",
            "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "956 and 1476 give a clean conditional route",
            "source-functor domain, current owner, non-Hilbert silence, and readout no-reentry remain open",
        ),
        (
            "SIG1956_3_same_source_normalization",
            "same kappa/source normalization as EH/GR for ordinary matter",
            "DeltaJ_species=DeltaT_w=0 and kappa_A=kappa_univ",
            "UNSIGNED_SOURCE_WEIGHT_BLOCKER",
            "956/1476 retain source prefactor and delta_w rows",
            "prove source-label forgetting plus common measure/current owner or bound delta_w",
        ),
        (
            "SIG1956_4_extra_sector_silence",
            "motion/time/domain/memory/projector/boundary/connection sectors carry no independent projected local l=2 stress/charge",
            "P_2[R_extra]=0, or retained residual rows with units/sources/bounds",
            "UNSIGNED_PRIMARY_BLOCKER",
            "957 calls this an active primary obstruction; 990 keeps Ward/Bianchi open",
            "sector-specific no-hair/topological/gauge silence or residual envelopes",
        ),
        (
            "SIG1956_5_boundary_flux_zero",
            "no independent extra boundary/symplectic l=2 flux contaminates local EH source map",
            "Omega_boundary_extra|l=2=0 and delta B_extra|l=2=0",
            "UNSIGNED_BOUNDARY_BLOCKER",
            "1008 refuses EH import without parent theta/Q and boundary/extra pieces",
            "extract parent boundary term/symplectic flux or bound it",
        ),
        (
            "SIG1956_6_Ward_Bianchi_accounting",
            "all hidden/projector/domain/boundary variables are varied/on-shell/topological or retained, so conservation has no silent Euler leak",
            "nabla_mu(T_total+DeltaT+R_extra)^{mu nu}=0",
            "CONDITIONAL_CONSERVATION_GUARD",
            "990 supplies the Ward/Bianchi contract but not closure",
            "does not kill residual l=2 unless paired with source/boundary silence",
        ),
        (
            "SIG1956_7_verdict",
            "the parent-action signature needed for local EH same-source recovery is not signed yet",
            "local EH map blocked by EH operator, source normalization, extra-sector silence, and boundary flux",
            "SIGNATURE_AUDIT_FAILS_CLAIM",
            "the corpus has a coherent conditional spine, not a completed derivation",
            "next attack should sign source-map/current-owner clauses or emit residual current bounds",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, required_form, status, evidence, missing_for_claim in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "required_form": required_form,
                "status": status,
                "evidence": evidence,
                "missing_for_claim": missing_for_claim,
            }
        )
        rows.append(row)
    return rows


def residual_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RES1956_0_DeltaE_R11",
            "DeltaE_R11_l2",
            "non-EH/R11 local operator l=2 residual",
            "MISSING_EXECUTABLE_COEFFICIENTS",
            "left-hand/Cassini/PPN",
            "fill coefficient vector or prove EH-only operator",
        ),
        (
            "RES1956_1_DeltaT_w",
            "DeltaT_w_l2",
            "source prefactor/species/source-label l=2 residual",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "source-side/WEP/Newton/Cassini",
            "prove source-label forgetting or retain delta_w bound",
        ),
        (
            "RES1956_2_DeltaT_NH",
            "DeltaT_nonHilbert_l2",
            "spin/torsion/boundary/non-Hilbert current bypass residual",
            "MISSING_NONHILBERT_SILENCE_OR_BOUND",
            "source-side/local GR",
            "prove absent/exact/projected-silent or source numeric envelope",
        ),
        (
            "RES1956_3_R_extra_l2",
            "P_2[R_extra]",
            "extra-sector local l=2 stress/charge residual",
            "MISSING_EXTRA_SECTOR_SILENCE_OR_BOUND",
            "Cassini/PPN/local GR",
            "sector no-hair/topological/gauge silence or residual bound",
        ),
        (
            "RES1956_4_boundary_flux_l2",
            "Omega_boundary_extra_l2",
            "extra boundary/symplectic l=2 flux residual",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "Hamiltonian charge/Newton/Cassini",
            "extract parent theta/Q/boundary term or bound flux",
        ),
        (
            "RES1956_5_readout_norm",
            "W_STF",
            "Cassini residual STF readout norm for any retained l=2 residual",
            "MISSING_READOUT_NORM",
            "Cassini scoring",
            "source after residual amplitudes exist",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, status, arena, next_action in entries:
        row = base(row_id)
        row.update(
            {
                "symbol": symbol,
                "definition": definition,
                "status": status,
                "arena": arena,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1956_0_full_signature",
            "all signature clauses signed -> local EH same-source residual l=2 zero",
            "S_TF_extra=0",
            "MISSING_EH_OPERATOR;MISSING_SOURCE_NORMALIZATION;MISSING_EXTRA_SILENCE;MISSING_BOUNDARY_FLUX",
            "BLOCKED_SIGNATURE_INCOMPLETE",
            "no local EH/Cassini claim",
        ),
        (
            "RUN1956_1_source_side_partial",
            "total Hilbert source route is conditionally clean",
            "not a claim without source-functor/current/non-Hilbert signatures",
            "MISSING_SOURCE_FUNCTOR_DOMAIN;MISSING_CURRENT_OWNER;MISSING_NONHILBERT_SILENCE",
            "PASS_NONCLAIM_PARTIAL_ROUTE",
            "best narrow derivation target is source-map signing",
        ),
        (
            "RUN1956_2_residual_bound",
            "retained residual vector can be scored if each component has units, source path, and envelope",
            "abs(S_TF_extra)<=6.7e-5",
            "MISSING_RESIDUAL_AMPLITUDES;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "fallback empirical route remains unavailable",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CG1956_0_signature_audit",
            "Parent action variation signature audit exists.",
            "PASS_NONCLAIM",
            "audit only; no full clause signing",
        ),
        (
            "CG1956_1_source_side_conditional",
            "Source-side same-source route is clean conditionally.",
            "PASS_NONCLAIM",
            "still missing parent signatures",
        ),
        (
            "CG1956_2_EH_operator_signed",
            "EH operator selection is parent-signed.",
            "FAIL_BLOCKED",
            "EH/operator branch remains not parent-derived",
        ),
        (
            "CG1956_3_source_map_signed",
            "ordinary matter same-source map is parent-signed.",
            "FAIL_BLOCKED",
            "source-functor/current/non-Hilbert clauses remain open",
        ),
        (
            "CG1956_4_extra_boundary_silent",
            "extra-sector and boundary l=2 residuals are zero.",
            "FAIL_BLOCKED",
            "extra-sector silence and boundary flux zero remain unsigned",
        ),
        (
            "CG1956_5_Cassini_pass",
            "MTS passes Cassini gamma residual gate.",
            "FAIL_BLOCKED",
            "signature incomplete and residual bound missing",
        ),
        (
            "CG1956_6_local_GR_Newton",
            "MTS derives local GR/Newton.",
            "FAIL_BLOCKED",
            "EH operator, measured source mass, PPN vector, and residual gates remain open",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1956_0_verdict",
            "CONDITIONAL_LOCAL_EH_SPINE_CONFIRMED_NOT_SIGNED",
            "the existing corpus supports the route but not the claim",
            "do not promote local GR; attack source-map/current-owner signatures or fill residual bounds",
        ),
        (
            "DEC1956_1_best_next",
            "SOURCE_MAP_SIGNATURE_OR_RESIDUAL_CURRENT_BOUND",
            "the source-side route is narrower and more mature than the full EH operator branch, while still directly feeding residual l=2",
            "prove source-functor domain/current owner/non-Hilbert silence together, or emit residual current envelopes",
        ),
        (
            "DEC1956_2_parallel_debt",
            "EH_OPERATOR_REMAINS_UPSTREAM_LOCAL_GR_DEBT",
            "even perfect source-map signing would not finish local GR without EH/operator and measured-GM gates",
            "keep EH/R11 residual vector in the local-GR spine rather than pretending Cassini source-side closes everything",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1956_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md",
            "target_script": "scripts/Y5_R2FR_source_map_signature_or_residual_current_bound_1957.py",
            "objective": "prove or bound the ordinary-matter source-map residual: source-functor domain, current owner, non-Hilbert silence, and source-label forgetting",
            "acceptance_output": "signed same-source clauses or residual current envelope rows for DeltaT_w and DeltaT_nonHilbert",
            "nonclaim_rule": "no local GR/Cassini claim unless source residuals and left-hand l2 residuals are zero or bounded",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1956_0_project_position")
    row.update(
        {
            "strongest_result": "The current corpus has a coherent conditional local-EH/source-map spine, but the parent-action variation signature is incomplete.",
            "what_improved": "the exact signed/unsigned clauses are now separated: EH operator, ordinary source map, extra silence, boundary flux, Ward/Bianchi",
            "still_missing": "parent signatures or numeric envelopes for EH/R11 residuals, source-label/current residuals, extra-sector l2, boundary flux, and W_STF",
            "claim_status": "not a Cassini/local-GR/Newton pass; a sharper action-signature audit",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_SOURCE_REGISTER.csv",
    "signature": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_ACTION_VARIATION_SIGNATURE_LEDGER.csv",
    "residuals": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_RESIDUAL_OPERATOR_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1956_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ACTION_VARIATION_SIGNATURE_1956_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1956_SOURCE_MAP_SIGNATURE_OR_RESIDUAL_CURRENT_BOUND_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1956_0_nonclaim_weight"),
            "artifact": "1956 parent-action variation signature audit",
            "weight": "CLAUSE_AUDIT_NOT_EVIDENCE",
            "reason": "existing spine is conditional; no full parent signature or numeric residual bound exists",
        }
    ]
    queue = [
        {
            **base("AQ1956_0_source_functor"),
            "target": "source-functor domain and current owner",
            "needed_inputs": "parent matter action; Hilbert current owner; variation-before-readout; no readout reentry",
            "priority": "HIGH",
        },
        {
            **base("AQ1956_1_nonHilbert"),
            "target": "non-Hilbert current silence",
            "needed_inputs": "spin/torsion/boundary current theorem or residual envelope",
            "priority": "HIGH",
        },
        {
            **base("AQ1956_2_EH_R11"),
            "target": "EH operator / R11 residual vector",
            "needed_inputs": "EH normalization, non-EH operator coefficients, weak-field maps",
            "priority": "PARALLEL_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "signature": signature_rows(),
        "residuals": residual_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1956-", "*_1956_*", "*Y5*1956*", "*VAL1956*", "*P8*1956*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1956_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    signature_ok = any(row["row_id"] == "SIG1956_7_verdict" and row["status"] == "SIGNATURE_AUDIT_FAILS_CLAIM" for row in tables["signature"])
    rows.append(validation_row("VAL1956_01_signature_verdict", "PASS" if signature_ok else "FAIL", "signature audit verdict recorded"))

    source_partial_ok = any(row["row_id"] == "SIG1956_2_total_Hilbert_source" and row["status"] == "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED" for row in tables["signature"])
    rows.append(validation_row("VAL1956_02_source_partial", "PASS" if source_partial_ok else "FAIL", "conditional source-side route retained"))

    blockers = {"SIG1956_1_EH_operator", "SIG1956_4_extra_sector_silence", "SIG1956_5_boundary_flux_zero"}
    blocker_ok = blockers.issubset({row["row_id"] for row in tables["signature"] if "UNSIGNED" in str(row["status"])})
    rows.append(validation_row("VAL1956_03_unsigned_blockers", "PASS" if blocker_ok else "FAIL", "primary unsigned blockers retained"))

    residual_symbols = {"DeltaE_R11_l2", "DeltaT_w_l2", "DeltaT_nonHilbert_l2", "P_2[R_extra]", "Omega_boundary_extra_l2"}
    residual_ok = residual_symbols.issubset({row["symbol"] for row in tables["residuals"]})
    rows.append(validation_row("VAL1956_04_residual_ledger", "PASS" if residual_ok else "FAIL", "residual operator ledger covers source/operator/extra/boundary channels"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"BLOCKED_SIGNATURE_INCOMPLETE", "PASS_NONCLAIM_PARTIAL_ROUTE", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1956_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks claims and preserves partial source route"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1956_0_signature_audit" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1956_06_claim_gates", "PASS" if gate_ok else "FAIL", "only nonclaim audit gates pass"))

    decision_ok = any(row["decision"] == "SOURCE_MAP_SIGNATURE_OR_RESIDUAL_CURRENT_BOUND" for row in tables["decision"])
    rows.append(validation_row("VAL1956_07_decision", "PASS" if decision_ok else "FAIL", "source-map residual target selected"))

    next_ok = tables["next"][0]["target_doc"] == "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md"
    rows.append(validation_row("VAL1956_08_next_target", "PASS" if next_ok else "FAIL", "1957 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1956_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1956_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1956_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1956_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1956_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1956_OVERALL", overall, "1956 parent action variation signature for local EH map"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Action Variation Signature Ledger", tables["signature"]),
        ("Residual Operator Ledger", tables["residuals"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1956 Y5 R2FR: Parent Action Variation Signature For Local EH Map",
        "",
        "Private checkpoint. This audits whether existing corpus evidence signs the local EH same-source map needed by the residual l=2/Cassini branch.",
        "",
        "Verdict: the route is coherent but still conditional. Source-side Hilbert current structure is the cleanest partial route, but EH operator selection, source normalization/current ownership, extra-sector silence, and boundary flux are not parent-signed. No local-GR, Newton, or Cassini claim is promoted.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for name, path in OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1956_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
