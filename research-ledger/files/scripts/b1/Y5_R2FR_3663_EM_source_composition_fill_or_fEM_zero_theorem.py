from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3663"
BRANCH_ID = "MTS_R2FR_Y5_EM_SOURCE_COMPOSITION_FILL_OR_FEM_ZERO_THEOREM_3663"
DOC = ROOT / "3663-Y5-R2FR-EM-source-composition-fill-or-fEM-zero-theorem.md"


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
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3662", RESIDUALS / "P8_Y5_R2FR_3662_NEXT_TARGET.csv", "f_EM=0", "3662 selected fEM/source composition branch"),
        ("theorem_3662", RESIDUALS / "P8_Y5_R2FR_3662_EM_ZERO_THEOREM_ATTEMPT.csv", "NONZERO_EM_BINDING_BRANCH_LIVE", "3662 EM zero theorem attempt"),
        ("elements_3662", RESIDUALS / "P8_Y5_R2FR_3662_ELEMENTAL_EM_BINDING_ROWS.csv", "EME3662_TiPt_delta", "3662 Ti/Pt numeric rows"),
        ("schemas_3662", RESIDUALS / "P8_Y5_R2FR_3662_SOURCE_BODY_SCHEMA_ROWS.csv", "SOLAR_COMPOSITION_REQUIRED_FOR_GAMMA", "3662 source body schema"),
        ("shared_3662", RESIDUALS / "P8_Y5_R2FR_3662_SHARED_COMPONENT_ROWS.csv", "GAMMA_SOURCE_SIDE_MISSING_NONCLAIM", "3662 shared EM status"),
        ("doc_3649", ROOT / "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md", "b_alpha=f_EM=0", "3649 conditional EM-lock theorem"),
        ("theorem_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_MAXWELL_THEOREM_ATTEMPT.csv", "FEM_SOURCE_FORMULA_DERIVED_CONDITIONALLY", "3649 fEM theorem row"),
        ("audit_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv", "MISSING_NO_FEM_THEOREM", "3649 EM-lock audit"),
        ("coeff_3649", RESIDUALS / "P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv", "FEM3649_1_fEM", "3649 fEM retained row"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def fem_zero_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("FZA3663_0_unique_F2_owner", "no independent f_X(X_N)F_Q^2 operator exists", "3649 EMA3649_1_unique_F2", "UNSIGNED"),
        ("FZA3663_1_same_frame_Hodge", "Hodge star/readout frame descends through the same observed coframe", "3649 EMA3649_3_Hodge_frame", "UNSIGNED"),
        ("FZA3663_2_charge_norm_owner", "charge generator and gauge kinetic normalization are fixed by one parent owner", "3649 EMA3649_0_TQ_owner", "UNSIGNED"),
        ("FZA3663_3_current_owner", "charge current/source normalization descends from the same owner", "3649 EMA3649_4_current_owner", "UNSIGNED"),
        ("FZA3663_4_no_radiative_leak", "radiative/optical readout does not regenerate an effective f_EM", "3649 EMA3649_5_radiative_readout", "UNSIGNED"),
        ("FZA3663_5_total", "all EM-lock clauses hold simultaneously", "3649 EMA3649_6_total", "NOT_SIGNED"),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "clause": clause,
            "source_anchor": source_anchor,
            "current_status": status,
            "accepted_as_zero": False,
            "meaning": "f_EM remains live unless this clause is parent-signed",
            "claim_allowed": False,
        }
        for audit_id, clause, source_anchor, status in specs
    ]


def fem_theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "theorem_id": "FEMT3663_0_conditional_zero",
            "claim": "f_EM=0 follows from a unique same-frame Maxwell owner.",
            "formula": "unique_F2_owner and same_frame_Hodge and charge_norm_owner and current_owner and no_radiative_leak => f_EM=0",
            "result_status": "CONDITIONAL_ZERO_THEOREM_RESTATED_FROM_3649",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "FEMT3663_1_current_verdict",
            "claim": "Current MTS proves f_EM=0.",
            "formula": "3649 EM-lock clauses are unsigned, so f_EM stays in the Q_X basis as B_source_EM*f_EM",
            "result_status": "FAIL_CURRENT_CLAIM_FEM_ZERO_UNSIGNED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def source_composition_acquisition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("SCA3663_0_solar_gamma", "solar_source_for_gamma", "Sun/Cassini gamma", "mass_fraction_H;mass_fraction_He;mass_fraction_metals;metal mixture;source_reference", "B_Sun_EM=sum_i w_i B_i^EM", "SOLAR_COMPOSITION_SOURCE_REQUIRED"),
        ("SCA3663_1_earth_WEP", "Earth_source_for_WEP", "Earth/MICROSCOPE source proxy", "core/mantle/crust mass fractions or accepted bulk-Earth elemental model;source_reference", "B_Earth_EM=sum_i w_i B_i^EM", "EARTH_COMPOSITION_SOURCE_REQUIRED"),
        ("SCA3663_2_lab_R10", "lab_source_for_R10", "short-range attractor/source material", "experiment/source material;Z;A;mass_fraction;geometry;source_reference", "B_lab_EM=sum_i w_i B_i^EM", "LAB_ATTRACTOR_COMPOSITION_REQUIRED"),
        ("SCA3663_3_generic_source", "generic_source_body", "shared source composition schema", "component_id;element;Z;A_effective;mass_fraction;B_A_EM;source_reference", "B_source_EM=sum_i w_i B_i^EM", "GENERIC_SOURCE_SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            **base(ts),
            "composition_id": cid,
            "source_body": source_body,
            "arena": arena,
            "required_columns": required,
            "formula": formula,
            "current_status": status,
            "score_ready": False,
            "placeholder_refused_as_claim": True,
            "claim_allowed": False,
        }
        for cid, source_body, arena, required, formula, status in specs
    ]


def branch_status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "branch_id_row": "EBS3663_0_fEM_zero_branch",
            "branch": "parent f_EM zero",
            "status": "PREFERRED_BUT_UNSIGNED",
            "required_next_input": "parent unique F2/no f_XF2 theorem plus Hodge/current/radiative lock",
            "effect_if_closed": "B_source_EM*f_EM drops out of Q_X in every shared arena",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "branch_id_row": "EBS3663_1_source_composition_branch",
            "branch": "live f_EM bound branch",
            "status": "SOURCE_COMPOSITION_ACQUISITION_READY",
            "required_next_input": "B_Sun_EM, B_Earth_EM, lab/source B_EM provenance rows",
            "effect_if_closed": "EM component becomes scoreable in WEP/R10/gamma once f_EM/Z_X/profile inputs are supplied",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3663_0_fEM_zero_audit", "f_EM zero theorem audited", "PASSED_AUDIT", "same-frame Maxwell route exists but remains unsigned"),
        ("CG3663_1_no_fEM_claim", "f_EM=0 not claimed", "ACTIVE_GUARD", "3649 EM-lock clauses still unsigned"),
        ("CG3663_2_source_composition", "Sun/Earth/lab source composition acquisition rows staged", "PASSED_SCHEMA_GATE", "source-body values are required before score"),
        ("CG3663_3_no_score", "EM component still not score-ready", "ACTIVE_GUARD", "source composition and f_EM/profile inputs missing"),
        ("CG3663_4_next", "next step should source one source-body composition or prove unique F2", "SOURCE_BODY_OR_UNIQUE_F2_NEXT", "turns EM component from proxy to shared test input"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "FEM_ZERO_UNSIGNED_SOURCE_COMPOSITION_ACQUISITION_ROWS_READY",
            "summary": "3663 audits the f_EM=0 route against the 3649 EM-lock clauses, refuses the unsigned zero, and stages Sun/Earth/lab source-composition acquisition rows for the live EM-binding branch.",
            "claim_ceiling": "no f_EM zero, EM-binding pass, WEP, R10, gamma, local-GR, PPN, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The EM component now has a clean fork: prove unique same-frame Maxwell ownership, or source B_source_EM rows for each shared arena.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3663_0",
            "target_doc": "3664-Y5-R2FR-unique-F2-parent-proof-or-solar-BsourceEM-first-row.md",
            "target_script": "scripts/Y5_R2FR_3664_unique_F2_parent_proof_or_solar_BsourceEM_first_row.py",
            "objective": "try to prove the parent unique-F2/no-f_XF2 theorem; if not, source a solar B_source_EM first row for Cassini/gamma as nonclaim evidence plumbing",
            "success_gate": "either f_EM is parent-zero through unique-F2 ownership or solar B_source_EM has a sourced nonclaim row with placeholders refused as claims",
        }
    ]


def write_doc(sources, theorem, audit, compositions, branches, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3663 - EM source composition fill or fEM zero theorem",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The clean route is still `f_EM=0`, but it is not free. From 3649, it requires unique same-frame Maxwell ownership: no independent `f_X(X_N)F_Q^2`, same Hodge/readout frame, fixed charge normalization, same current owner, and no radiative/optical leak.",
        "",
        "Those clauses remain unsigned, so the EM-binding branch stays live. Therefore the practical fallback is source composition: `B_source_EM=sum_i w_i B_i^EM` for the Sun/Cassini gamma branch, Earth/WEP branch, and lab/R10 branch.",
        "",
        "## f_EM theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['result_status']} - `{row['formula']}`")
    lines.extend(["", "## f_EM zero audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['current_status']} - {row['clause']}")
    lines.extend(["", "## Source-composition acquisition rows"])
    for row in compositions:
        lines.append(f"- `{row['composition_id']}`: `{row['source_body']}` - {row['current_status']}")
    lines.extend(["", "## Branch status"])
    for row in branches:
        lines.append(f"- `{row['branch_id_row']}`: {row['status']} - {row['branch']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, theorem, audit, compositions, branches, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3663_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3663_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3663_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3663 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3663_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3663_4_fEM_zero_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in theorem + audit), "f_EM zero not accepted")
    add("VAL3663_5_audit_complete", len(audit) >= 6 and any(row["audit_id"] == "FZA3663_5_total" for row in audit), "all key EM-lock clauses audited")
    add("VAL3663_6_composition_rows", {"solar_source_for_gamma", "Earth_source_for_WEP", "lab_source_for_R10"}.issubset({row["source_body"] for row in compositions}), "source composition acquisition rows present")
    add("VAL3663_7_composition_nonclaim", all(str(row["placeholder_refused_as_claim"]).lower() == "true" and str(row["score_ready"]).lower() == "false" for row in compositions), "composition placeholders refused as claims")
    add("VAL3663_8_branch_rows", {"parent f_EM zero", "live f_EM bound branch"}.issubset({row["branch"] for row in branches}), "branch status rows present")
    add("VAL3663_9_claim_gates_present", {"CG3663_0_fEM_zero_audit", "CG3663_1_no_fEM_claim", "CG3663_2_source_composition", "CG3663_3_no_score", "CG3663_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + theorem + audit + compositions + branches + gates + status_rows_ + next_target
    add("VAL3663_10_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3663_11_doc_written", "f_EM=0" in doc_text and "B_source_EM=sum_i w_i B_i^EM" in doc_text and "unsigned" in doc_text, "doc records fEM/source composition fork")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3663*", "3663-Y5-R2FR-*", "Y5_R2FR_3663_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3663_12_no_formalization_leak", not leaks, "no 3663 checkpoint files in formalization-workbench")
    add("VAL3663_13_next_target", next_target[0]["target_doc"].startswith("3664-") and "unique-F2" in next_target[0]["target_doc"], "3664 unique-F2/solar row target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = fem_theorem_rows(ts)
    audit = fem_zero_audit_rows(ts)
    compositions = source_composition_acquisition_rows(ts)
    branches = branch_status_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3663_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3663_FEM_ZERO_THEOREM_ROWS.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3663_FEM_ZERO_AUDIT_ROWS.csv",
        "compositions": RESIDUALS / "P8_Y5_R2FR_3663_SOURCE_COMPOSITION_ACQUISITION_ROWS.csv",
        "branches": RESIDUALS / "P8_Y5_R2FR_3663_BRANCH_STATUS_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3663_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3663_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3663_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3663_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["compositions"], compositions)
    write_csv(outputs["branches"], branches)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, audit, compositions, branches, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, audit, compositions, branches, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3663 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3663 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
