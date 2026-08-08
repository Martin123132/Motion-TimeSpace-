from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3664"
BRANCH_ID = "MTS_R2FR_Y5_UNIQUE_F2_PARENT_PROOF_OR_SOLAR_BSOURCEEM_FIRST_ROW_3664"
DOC = ROOT / "3664-Y5-R2FR-unique-F2-parent-proof-or-solar-BsourceEM-first-row.md"

A_C_MEV = 0.711
U_MEV = 931.49410242
SOLAR_SOURCE = "Asplund, Grevesse, Sauval, Scott 2009 solar composition; bulk X=0.7154,Y=0.2703,Z=0.0142; https://arxiv.org/abs/0909.0948"
SEMF_SOURCE = "semi_empirical_mass_formula_convention; a_C≈0.711 MeV; https://en.wikipedia.org/wiki/Semi-empirical_mass_formula"


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


def em_fraction(z: int, atomic_weight: float) -> tuple[float, float, float]:
    e_c = A_C_MEV * z * (z - 1) * atomic_weight ** (-1.0 / 3.0)
    mass_e = atomic_weight * U_MEV
    return e_c, mass_e, e_c / mass_e


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3663", RESIDUALS / "P8_Y5_R2FR_3663_NEXT_TARGET.csv", "unique-F2", "3663 selected unique-F2/solar row target"),
        ("fem_audit_3663", RESIDUALS / "P8_Y5_R2FR_3663_FEM_ZERO_AUDIT_ROWS.csv", "FZA3663_0_unique_F2_owner", "3663 fEM zero audit"),
        ("composition_3663", RESIDUALS / "P8_Y5_R2FR_3663_SOURCE_COMPOSITION_ACQUISITION_ROWS.csv", "solar_source_for_gamma", "3663 source-composition rows"),
        ("branch_3663", RESIDUALS / "P8_Y5_R2FR_3663_BRANCH_STATUS_ROWS.csv", "SOURCE_COMPOSITION_ACQUISITION_READY", "3663 branch status"),
        ("doc_3649", ROOT / "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md", "FAIL_CURRENT_CLAIM_COUNTERTERM_LEGAL", "3649 unique-F2 obstruction"),
        ("audit_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "3649 EM-lock audit"),
        ("coeff_3649", RESIDUALS / "P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv", "MISSING_FEM_OR_ZERO_THEOREM", "3649 fEM retained row"),
        ("elements_3662", RESIDUALS / "P8_Y5_R2FR_3662_ELEMENTAL_EM_BINDING_ROWS.csv", "EME3662_TiPt_delta", "3662 SEMF element method"),
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
    rows.extend(
        [
            {
                **base(ts),
                "source_id": "external_solar_composition_Asplund2009",
                "path": SOLAR_SOURCE,
                "exists": True,
                "needle": "X=0.7154,Y=0.2703,Z=0.0142",
                "needle_found": True,
                "role": "bulk solar H/He/metals mass fractions for first nonclaim solar source row",
            },
            {
                **base(ts),
                "source_id": "external_SEMF_aC",
                "path": SEMF_SOURCE,
                "exists": True,
                "needle": "a_C≈0.711 MeV",
                "needle_found": True,
                "role": "Coulomb coefficient convention reused from 3662",
            },
        ]
    )
    return rows


def unique_f2_proof_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "proof_id": "UF23664_0_operator_question",
            "object": "unique Maxwell kinetic operator",
            "statement": "The desired theorem is that the parent action admits one same-frame Maxwell F_Q^2 block and no independent scalar gauge-kinetic function f_X(X_N)F_Q^2.",
            "formula": "S_EM=-(C_P/4) int mu_obs <F_QT_Q,F_QT_Q>_P and no DeltaS=-(1/4)int mu_obs f_X(X_N)F_Q^2",
            "proof_status": "TARGET_THEOREM_STATED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "UF23664_1_counterterm_test",
            "object": "legal scalar counterterm",
            "statement": "A scalar gauge-kinetic function is diffeomorphism and gauge invariant unless the parent grammar/symmetry excludes it.",
            "formula": "f_X(X_N)F_Q^2 is allowed by ordinary gauge/diffeomorphism symmetry",
            "proof_status": "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "UF23664_2_current_verdict",
            "object": "f_EM zero from unique-F2",
            "statement": "Current MTS does not yet supply the stronger parent uniqueness/superselection rule needed to exclude f_XF^2.",
            "formula": "unique_F2_parent_proof not closed => f_EM remains live",
            "proof_status": "UNIQUE_F2_PROOF_NOT_CLOSED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def solar_component_rows(ts: str) -> list[dict[str, object]]:
    h_mass_fraction = 0.7154
    he_mass_fraction = 0.2703
    metal_mass_fraction = 0.0142
    h_b = 0.0
    he_e_c, he_mass_e, he_b = em_fraction(2, 4.002602)
    hhe_b_source = h_mass_fraction * h_b + he_mass_fraction * he_b
    return [
        {
            **base(ts),
            "row_id": "SOL3664_0_H",
            "source_body": "Sun_bulk",
            "component": "H",
            "mass_fraction": h_mass_fraction,
            "Z": 1,
            "A_effective": 1.008,
            "B_A_EM": h_b,
            "contribution_to_B_source_EM": h_mass_fraction * h_b,
            "source_reference": SOLAR_SOURCE,
            "method": "SEMF Coulomb term vanishes for Z=1",
            "current_status": "SOURCE_BACKED_NUMERIC_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3664_1_He",
            "source_body": "Sun_bulk",
            "component": "He",
            "mass_fraction": he_mass_fraction,
            "Z": 2,
            "A_effective": 4.002602,
            "B_A_EM": round(he_b, 12),
            "E_C_MeV": round(he_e_c, 9),
            "mass_energy_MeV": round(he_mass_e, 9),
            "contribution_to_B_source_EM": round(he_mass_fraction * he_b, 12),
            "source_reference": SOLAR_SOURCE,
            "method": "SEMF Coulomb fraction from a_C=0.711 MeV and CIAAW He atomic weight proxy",
            "current_status": "SOURCE_BACKED_NUMERIC_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3664_2_metals_retained",
            "source_body": "Sun_bulk",
            "component": "metals_Z",
            "mass_fraction": metal_mass_fraction,
            "Z": "mixture",
            "A_effective": "mixture",
            "B_A_EM": "MISSING_METAL_MIXTURE",
            "contribution_to_B_source_EM": "MISSING_METAL_MIXTURE_CONTRIBUTION",
            "source_reference": SOLAR_SOURCE,
            "method": "metal mixture must be expanded before claim or score",
            "current_status": "METAL_MIXTURE_RETAINED_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3664_3_BsourceEM_HHe_partial",
            "source_body": "Sun_bulk",
            "component": "HHe_partial_sum",
            "mass_fraction": h_mass_fraction + he_mass_fraction,
            "Z": "H+He",
            "A_effective": "H+He",
            "B_A_EM": round(hhe_b_source, 12),
            "contribution_to_B_source_EM": round(hhe_b_source, 12),
            "source_reference": f"{SOLAR_SOURCE}; {SEMF_SOURCE}",
            "method": "bulk solar H/He partial B_source_EM; metals retained",
            "current_status": "SOLAR_BSOURCE_EM_PARTIAL_HHE_NONCLAIM_METALS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def solar_gamma_status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "SGS3664_0_gamma_use",
            "object": "solar_B_source_EM_for_Cassini_gamma",
            "formula": "Q_X^EM_solar = B_Sun_EM*f_EM enters A_X ~= Q_X/(4*pi Z_X)",
            "current_status": "PARTIAL_HHE_ROW_READY_METALS_AND_fEM_ZX_PROFILE_MISSING",
            "missing_for_score": "solar metal mixture; f_EM; Z_X; lambda_X; k_H; k_G; gamma kernel",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "status_id": "SGS3664_1_fEM_zero_route",
            "object": "f_EM_zero",
            "formula": "unique_F2_owner => f_EM=0",
            "current_status": "PREFERRED_ROUTE_BUT_UNIQUE_F2_UNSIGNED",
            "missing_for_score": "parent unique-F2/no-f_XF2 theorem",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3664_0_unique_F2_attempt", "unique-F2 parent proof attempted", "FAILED_UNSIGNED_COUNTERTERM_LIVE", "f_XF^2 remains legal under current parent grammar"),
        ("CG3664_1_solar_HHe_row", "solar H/He B_source_EM row filled", "PASSED_PARTIAL_FILL_NONCLAIM", "bulk H/He mass fractions plus SEMF Coulomb proxy used"),
        ("CG3664_2_metals_retained", "solar metals retained", "ACTIVE_GUARD", "metal mixture not expanded, so solar source is not score-ready"),
        ("CG3664_3_no_gamma_claim", "no Cassini/gamma/local-GR pass claimed", "ACTIVE_GUARD", "f_EM/Z_X/profile inputs and metals missing"),
        ("CG3664_4_next", "next step expands solar metals or reopens unique-F2 proof", "SOLAR_METALS_OR_UNIQUE_F2_NEXT", "turns partial solar row into a complete source row"),
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
            "status": "UNIQUE_F2_UNSIGNED_SOLAR_HHE_BSOURCEEM_PARTIAL_ROW_READY_NONCLAIM",
            "summary": "3664 fails to close unique-F2/no-f_XF2 from the current parent grammar, then fills a nonclaim bulk-solar H/He B_source_EM partial row while retaining metals and f_EM/profile inputs as blockers.",
            "claim_ceiling": "no f_EM zero, solar B_source_EM score, gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The Cassini/gamma EM source branch now has a first sourced solar row; the next honest step is metals expansion or a real unique-F2 theorem.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3664_0",
            "target_doc": "3665-Y5-R2FR-solar-metal-mixture-expansion-or-unique-F2-closure.md",
            "target_script": "scripts/Y5_R2FR_3665_solar_metal_mixture_expansion_or_unique_F2_closure.py",
            "objective": "expand the solar metal mixture into a complete nonclaim B_source_EM row, or derive a parent unique-F2/no-f_XF2 closure that makes f_EM=0",
            "success_gate": "solar B_source_EM is complete with H/He/metals provenance or f_EM is parent-zero; all rows remain nonclaim unless every profile/input gate is also closed",
        }
    ]


def write_doc(sources, proof, solar, gamma_status, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3664 - Unique-F2 parent proof or solar BsourceEM first row",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The unique-`F^2` route still does not close: the current parent grammar has not excluded an independent scalar gauge-kinetic term `f_X(X_N)F_Q^2`, so `f_EM=0` is not claimed.",
        "",
        "Fallback progress: a bulk-solar H/He partial row is now filled for the Cassini/gamma source branch. Using bulk solar `X=0.7154`, `Y=0.2703`, `Z=0.0142` and SEMF `a_C=0.711 MeV`, hydrogen contributes zero Coulomb term and helium gives the first partial value:",
        "",
        "`B_Sun_EM,HHe_partial = 6.4929539e-05`.",
        "",
        "This is still nonclaim: solar metals, `f_EM`, `Z_X`, `lambda_X`, `k_H`, `k_G`, and the gamma kernel remain missing.",
        "",
        "## Unique-F2 proof attempt",
    ]
    for row in proof:
        lines.append(f"- `{row['proof_id']}`: {row['proof_status']} - `{row['formula']}`")
    lines.extend(["", "## Solar BsourceEM rows"])
    for row in solar:
        lines.append(f"- `{row['row_id']}`: `{row['component']}` B=`{row['B_A_EM']}` - {row['current_status']}")
    lines.extend(["", "## Solar gamma status"])
    for row in gamma_status:
        lines.append(f"- `{row['status_id']}`: {row['current_status']} - missing: {row['missing_for_score']}")
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


def validate(ts, output_paths, sources, proof, solar, gamma_status, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3664_0_sources_exist", all(row["exists"] for row in sources), "every cited local/external source marker exists")
    add("VAL3664_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found or externally declared")
    add("VAL3664_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3664 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3664_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3664_4_uniqueF2_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in proof), "unique-F2/fEM zero not accepted")
    add("VAL3664_5_counterterm_live", any(row["proof_status"] == "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR" for row in proof), "counterterm obstruction recorded")
    add("VAL3664_6_solar_hhe_row", any(row["row_id"] == "SOL3664_3_BsourceEM_HHe_partial" and row["B_A_EM"] == round(0.2703 * em_fraction(2, 4.002602)[2], 12) for row in solar), "solar H/He partial row filled")
    add("VAL3664_7_metals_retained", any(row["row_id"] == "SOL3664_2_metals_retained" and row["current_status"] == "METAL_MIXTURE_RETAINED_NONCLAIM" for row in solar), "solar metals retained as missing")
    add("VAL3664_8_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in solar), "solar rows are not score-ready")
    add("VAL3664_9_gamma_status", any("METALS" not in row["current_status"] and "fEM" not in row["status_id"] for row in gamma_status) or len(gamma_status) >= 2, "gamma/fEM branch status rows present")
    add("VAL3664_10_claim_gates_present", {"CG3664_0_unique_F2_attempt", "CG3664_1_solar_HHe_row", "CG3664_2_metals_retained", "CG3664_3_no_gamma_claim", "CG3664_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + proof + solar + gamma_status + gates + status_rows_ + next_target
    add("VAL3664_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3664_12_doc_written", "f_X(X_N)F_Q^2" in doc_text and "B_Sun_EM,HHe_partial" in doc_text and "nonclaim" in doc_text, "doc records unique-F2 failure and solar partial row")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3664*", "3664-Y5-R2FR-*", "Y5_R2FR_3664_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3664_13_no_formalization_leak", not leaks, "no 3664 checkpoint files in formalization-workbench")
    add("VAL3664_14_next_target", next_target[0]["target_doc"].startswith("3665-") and "solar-metal" in next_target[0]["target_doc"], "3665 solar metals/unique-F2 target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    proof = unique_f2_proof_rows(ts)
    solar = solar_component_rows(ts)
    gamma_status = solar_gamma_status_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3664_SOURCE_REGISTER.csv",
        "proof": RESIDUALS / "P8_Y5_R2FR_3664_UNIQUE_F2_PROOF_ATTEMPT.csv",
        "solar": RESIDUALS / "P8_Y5_R2FR_3664_SOLAR_BSOURCEEM_ROWS.csv",
        "gamma_status": RESIDUALS / "P8_Y5_R2FR_3664_SOLAR_GAMMA_STATUS_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3664_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3664_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3664_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3664_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["proof"], proof)
    write_csv(outputs["solar"], solar)
    write_csv(outputs["gamma_status"], gamma_status)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, proof, solar, gamma_status, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, proof, solar, gamma_status, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3664 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3664 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
