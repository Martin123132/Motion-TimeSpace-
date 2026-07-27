from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3661"
BRANCH_ID = "MTS_R2FR_Y5_QX_COMPONENT_BASIS_DECOMPOSITION_OR_SHARED_BOUND_RUNNER_3661"
DOC = ROOT / "3661-Y5-R2FR-QX-component-basis-decomposition-or-shared-bound-runner.md"


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


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3660", RESIDUALS / "P8_Y5_R2FR_3660_NEXT_TARGET.csv", "component-basis", "3660 selected QX component basis target"),
        ("proof_3660", RESIDUALS / "P8_Y5_R2FR_3660_QX_ZERO_PROOF_ATTEMPT.csv", "Q_A^X", "3660 QX zero proof"),
        ("input_pack_3660", RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_INPUT_PACK.csv", "GBI3660_0_QX", "3660 gamma input pack"),
        ("formulas_3660", RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv", "Q_X/(4*pi*Z_X)", "3660 gamma bound formula"),
        ("composition_schema_3651", RESIDUALS / "P8_Y5_R2FR_3651_COMPOSITION_MATRIX_SCHEMA_ROWS.csv", "composition_no_cancellation_guard", "3651 no-cancellation schema"),
        ("material_theorem_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv", "beta_source_alpha,A*b_alpha", "3651 material/source basis"),
        ("source_current_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv", "COUNTERMODEL_LIVE", "3650 source-current countermodel"),
        ("gm_rows_3652", RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "alpha_ST", "3652 shared R10/source rows"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "WEP/R10/gamma bound anchors"),
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


def local_bound_lookup() -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}


def qx_component_basis_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("QXB3661_0_beta_source_alpha", "beta_source_alpha_bar*b_alpha", "source-current/charge-normalization drift", "sum_A w_A beta_source_alpha,A*b_alpha", "3650 source-current owner", "MISSING_PARENT_SOURCE_CURRENT_THEOREM", "WEP;R10;gamma;PPN;orbital"),
        ("QXB3661_1_EM_binding", "B_source_EM*f_EM", "EM Coulomb binding sensitivity", "sum_A w_A B_A^EM*f_EM, B_A^EM ~= E_C/(M_A c^2)", "3651 EM binding law", "FORMULA_DERIVED_NUMERIC_COMPOSITION_MISSING", "WEP;R10;gamma;EM"),
        ("QXB3661_2_mass_scale", "B_source_m*b_m", "ordinary mass-scale sensitivity", "sum_A w_A B_A^m*b_m", "3651 source matrix slot", "MISSING_MASS_SENSITIVITY_OWNER", "WEP;R10;gamma;PPN"),
        ("QXB3661_3_nuclear_binding", "B_source_nuc*b_nuc", "nuclear binding/source sensitivity", "sum_A w_A B_A^nuc*b_nuc", "3651 source matrix slot", "MISSING_NUCLEAR_BINDING_SENSITIVITY", "WEP;R10;gamma"),
        ("QXB3661_4_source_measure", "b_J_source_bar", "source measure/current normalization sensitivity", "sum_A w_A b_J_source,A", "3650 current/source-measure clauses", "MISSING_SOURCE_MEASURE_DESCENT", "WEP;R10;gamma;PPN;orbital"),
        ("QXB3661_5_material_marker", "b_material_marker_bar", "explicit material marker leakage", "sum_A w_A b_material_marker,A", "3651 countermodel", "COUNTERMODEL_LIVE_PARENT_BAN_MISSING", "WEP;R10;gamma"),
        ("QXB3661_6_boundary", "b_boundary_bar+B_X", "boundary/domain/hair sensitivity", "sum_A w_A b_boundary,A + B_X", "3659 boundary hair row", "MISSING_BOUNDARY_SILENCE_SIGNATURE", "gamma;PPN;orbital"),
    ]
    return [
        {
            **base(ts),
            "basis_id": basis_id,
            "component_symbol": symbol,
            "definition": definition,
            "source_average_formula": formula,
            "source_anchor": source_anchor,
            "current_status": status,
            "shared_arenas": arenas,
            "parent_zero_status": "UNSIGNED",
            "numeric_status": "MISSING",
            "score_ready": False,
            "claim_allowed": False,
        }
        for basis_id, symbol, definition, formula, source_anchor, status, arenas in specs
    ]


def qx_envelope_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "envelope_id": "QXE3661_0_source_basis_sum",
            "object": "Q_X",
            "formula": "Q_X = beta_source_alpha_bar*b_alpha + B_source_EM*f_EM + B_source_m*b_m + B_source_nuc*b_nuc + b_J_source_bar + b_material_marker_bar + b_boundary_bar + B_X",
            "policy": "component sum only becomes signed if every term has a sign/zero theorem",
            "current_status": "BASIS_DECOMPOSITION_DERIVED_VALUES_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "envelope_id": "QXE3661_1_no_cancellation_bound",
            "object": "|Q_X|",
            "formula": "|Q_X| <= |beta_source_alpha_bar*b_alpha| + |B_source_EM*f_EM| + |B_source_m*b_m| + |B_source_nuc*b_nuc| + |b_J_source_bar| + |b_material_marker_bar| + |b_boundary_bar| + |B_X|",
            "policy": "use absolute envelope until parent signs cancellations",
            "current_status": "NO_CANCELLATION_ENVELOPE_ACTIVE",
            "claim_allowed": False,
        },
    ]


def component_zero_audit_rows(ts: str, basis_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in basis_rows:
        rows.append(
            {
                **base(ts),
                "audit_id": row["basis_id"].replace("QXB", "QZA"),
                "component_symbol": row["component_symbol"],
                "zero_route": f"parent signs zero/absence of {row['definition']}",
                "source_anchor": row["source_anchor"],
                "current_status": "ZERO_NOT_SIGNED_" + str(row["current_status"]),
                "accepted_as_zero": False,
                "claim_allowed": False,
            }
        )
    return rows


def shared_arena_rows(ts: str) -> list[dict[str, object]]:
    bounds = local_bound_lookup()
    r1 = bounds["R1_WEP_source_charge"]
    r3 = bounds["R3_gamma"]
    r10 = bounds["R10_fifth_force"]
    return [
        {
            **base(ts),
            "arena_id": "SBA3661_0_WEP",
            "arena": "WEP/MICROSCOPE",
            "observable": "eta_AB",
            "formula": "eta_AB ~= DeltaQ_AB^X * Q_source_X * tau_WEP",
            "bound_row": "R1_WEP_source_charge",
            "upper_bound": parse_float(r1["upper_bound"]),
            "units": r1["units"],
            "needed_inputs": "test body compositions; source composition; tau_WEP; QX component basis values",
            "current_status": "BOUND_ANCHOR_READY_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "arena_id": "SBA3661_1_R10",
            "arena": "short-range fifth force",
            "observable": "alpha_X(lambda_X)",
            "formula": "alpha_X(lambda_X)=K_X*Q_source_X*Q_test_X/(4*pi*Z_X*G_obs)",
            "bound_row": "R10_fifth_force",
            "upper_bound": r10["upper_bound"],
            "units": r10["units"],
            "needed_inputs": "alpha_bound(lambda) curve; lambda_X; K_X; Z_X; source/test QX basis values",
            "current_status": "SYMBOLIC_CURVE_REQUIRED_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "arena_id": "SBA3661_2_gamma",
            "arena": "Cassini/PPN gamma",
            "observable": "delta_gamma_MTS",
            "formula": "profile envelope from 3660 with Q_X component basis inserted, bounded by C_gamma_TF_total",
            "bound_row": "R3_gamma",
            "upper_bound": parse_float(r3["upper_bound"]),
            "units": r3["units"],
            "needed_inputs": "Q_X basis values; Z_X; lambda_X; k_H; k_G; gamma geometry kernel; C_other_gamma",
            "current_status": "BOUND_ANCHOR_READY_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "arena_id": "SBA3661_3_PPN_orbital_source",
            "arena": "PPN/orbital source calibration",
            "observable": "q_GM_source_abs;Delta_PPN_MTS",
            "formula": "source-calibration vector receives the same Q_X component basis through active/inertial source and fitted-GM separation",
            "bound_row": "R3-R9 plus orbital source map",
            "upper_bound": "mixed",
            "units": "mixed",
            "needed_inputs": "source Hamiltonian; orbital source map; PPN vector projection; QX component basis",
            "current_status": "MIXED_BOUND_INTERFACE_READY_VALUES_MISSING",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3661_0_basis", "Q_X component basis decomposed", "PASSED_DERIVATION", "source charge is now a component envelope, not a mystery scalar"),
        ("CG3661_1_no_cancellation", "absolute no-cancellation envelope active", "PASSED_POLICY_GATE", "no cancellation used without parent sign theorem"),
        ("CG3661_2_zero_audit", "each component zero route audited", "PASSED_AUDIT", "no component accepted as zero"),
        ("CG3661_3_shared_arenas", "WEP/R10/gamma/PPN arenas mapped to same basis", "PASSED_MAPPING_GATE", "shared empirical branch prevents separate knobs"),
        ("CG3661_4_no_claim", "no local-GR/gamma/WEP/R10 pass claimed", "ACTIVE_GUARD", "component values remain missing or unsigned"),
        ("CG3661_5_next", "next step should fill easiest component", "EM_BINDING_COMPONENT_NEXT", "EM binding has a symbolic formula and plausible source data route"),
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
            "status": "QX_COMPONENT_BASIS_AND_SHARED_BOUND_ARENAS_READY_NONCLAIM",
            "summary": "3661 decomposes Q_X into source-current, EM-binding, mass/nuclear, source-measure, material-marker, and boundary components; no component is zero-claimed, and the shared WEP/R10/gamma/PPN arenas now point to the same basis.",
            "claim_ceiling": "no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed",
            "useful_result": "The coupling branch is now componentized; the next concrete fill should target the EM binding component because it already has a symbolic SEMF formula.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3661_0",
            "target_doc": "3662-Y5-R2FR-EM-binding-component-first-fill-or-zero-theorem.md",
            "target_script": "scripts/Y5_R2FR_3662_EM_binding_component_first_fill_or_zero_theorem.py",
            "objective": "try to parent-zero the EM-binding Q_X component; if not, source the SEMF Coulomb coefficient and Ti/Pt/source composition rows needed for a first nonclaim B_source_EM fill",
            "success_gate": "EM-binding component is either parent-zero or has source-backed nonclaim numeric/provenance rows ready for shared WEP/R10/gamma use",
        }
    ]


def write_doc(sources, basis, envelopes, audit, arenas, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3661 - QX component basis decomposition or shared bound runner",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "`Q_X` is now decomposed into a component basis:",
        "",
        "`Q_X = beta_source_alpha_bar*b_alpha + B_source_EM*f_EM + B_source_m*b_m + B_source_nuc*b_nuc + b_J_source_bar + b_material_marker_bar + b_boundary_bar + B_X`.",
        "",
        "Until a parent theorem signs cancellations, the active policy is the absolute no-cancellation envelope. This matters because the same component basis feeds WEP, R10, Cassini gamma, and source-calibration/PPN; it is not allowed to tune a separate coupling for each arena.",
        "",
        "## Component basis rows",
    ]
    for row in basis:
        lines.append(f"- `{row['basis_id']}`: `{row['component_symbol']}` - {row['current_status']} -> {row['shared_arenas']}")
    lines.extend(["", "## No-cancellation envelopes"])
    for row in envelopes:
        lines.append(f"- `{row['envelope_id']}`: {row['current_status']} - `{row['formula']}`")
    lines.extend(["", "## Component zero audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['current_status']} - {row['zero_route']}")
    lines.extend(["", "## Shared bound arenas"])
    for row in arenas:
        lines.append(f"- `{row['arena_id']}`: `{row['arena']}` / `{row['observable']}` - {row['current_status']}")
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


def validate(ts, output_paths, sources, basis, envelopes, audit, arenas, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3661_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3661_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3661_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3661 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3661_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3661_4_basis_complete", len(basis) >= 7 and {"beta_source_alpha_bar*b_alpha", "B_source_EM*f_EM", "b_boundary_bar+B_X"}.issubset({row["component_symbol"] for row in basis}), "QX component basis includes required slots")
    add("VAL3661_5_no_cancellation_envelope", any(row["envelope_id"] == "QXE3661_1_no_cancellation_bound" and "|Q_X| <=" in row["formula"] for row in envelopes), "absolute envelope recorded")
    add("VAL3661_6_no_component_zero_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in audit), "no component zero accepted")
    add("VAL3661_7_arena_mapping", {"WEP/MICROSCOPE", "short-range fifth force", "Cassini/PPN gamma"}.issubset({row["arena"] for row in arenas}), "shared WEP/R10/gamma arenas present")
    add("VAL3661_8_wep_bound_numeric", any(row["arena_id"] == "SBA3661_0_WEP" and parse_float(row["upper_bound"]) == 2.8e-15 for row in arenas), "WEP bound carried")
    add("VAL3661_9_gamma_bound_numeric", any(row["arena_id"] == "SBA3661_2_gamma" and parse_float(row["upper_bound"]) == 2.3e-05 for row in arenas), "gamma bound carried")
    add("VAL3661_10_claim_gates_present", {"CG3661_0_basis", "CG3661_1_no_cancellation", "CG3661_2_zero_audit", "CG3661_3_shared_arenas", "CG3661_4_no_claim", "CG3661_5_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + basis + envelopes + audit + arenas + gates + status_rows_ + next_target
    add("VAL3661_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3661_12_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in basis), "basis rows are not score-ready")
    doc_text = read_text(DOC)
    add("VAL3661_13_doc_written", "Q_X =" in doc_text and "absolute no-cancellation envelope" in doc_text and "WEP, R10, Cassini gamma" in doc_text, "doc records shared component-basis result")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3661*", "3661-Y5-R2FR-*", "Y5_R2FR_3661_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3661_14_no_formalization_leak", not leaks, "no 3661 checkpoint files in formalization-workbench")
    add("VAL3661_15_next_target", next_target[0]["target_doc"].startswith("3662-") and "EM-binding" in next_target[0]["target_doc"], "3662 EM binding first-fill target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    basis = qx_component_basis_rows(ts)
    envelopes = qx_envelope_rows(ts)
    audit = component_zero_audit_rows(ts, basis)
    arenas = shared_arena_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3661_SOURCE_REGISTER.csv",
        "basis": RESIDUALS / "P8_Y5_R2FR_3661_QX_COMPONENT_BASIS_ROWS.csv",
        "envelopes": RESIDUALS / "P8_Y5_R2FR_3661_QX_NO_CANCELLATION_ENVELOPE_ROWS.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3661_COMPONENT_ZERO_AUDIT.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3661_SHARED_BOUND_ARENA_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3661_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3661_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3661_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3661_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["basis"], basis)
    write_csv(outputs["envelopes"], envelopes)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["arenas"], arenas)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, basis, envelopes, audit, arenas, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, basis, envelopes, audit, arenas, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3661 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3661 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
