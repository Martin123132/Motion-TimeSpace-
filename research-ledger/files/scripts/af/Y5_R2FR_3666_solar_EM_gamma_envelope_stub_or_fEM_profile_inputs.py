from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3666"
BRANCH_ID = "MTS_R2FR_Y5_SOLAR_EM_GAMMA_ENVELOPE_STUB_OR_FEM_PROFILE_INPUTS_3666"
DOC = ROOT / "3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md"

G_NEWTON = 6.67430e-11
M_SUN_KG = 1.9885e30
R_SUN_M = 6.957e8
C_LIGHT = 299_792_458.0
SOLAR_CONSTANT_SOURCE = "NASA/NSSDC Sun fact sheet proxy constants M_sun=1.9885e30 kg, R_sun=695700 km; https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html"
G_SOURCE = "CODATA/NIST Newtonian constant G=6.67430e-11 SI; https://physics.nist.gov/cgi-bin/cuu/Value?bg"
C_SOURCE = "SI exact speed of light c=299792458 m/s"


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


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3665", RESIDUALS / "P8_Y5_R2FR_3665_NEXT_TARGET.csv", "3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md", "3665 selected this target"),
        ("doc_3665", ROOT / "3665-Y5-R2FR-solar-metal-mixture-expansion-or-unique-F2-closure.md", "solar_B_source_EM_total = 8.256508261034e-05", "3665 completed solar source scalar"),
        ("solar_total_3665", RESIDUALS / "P8_Y5_R2FR_3665_SOLAR_BSOURCEEM_TOTAL_ROWS.csv", "SOL3665_3_solar_B_source_EM_total", "numeric solar B_source_EM input"),
        ("gamma_3656", RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_WEAK_FIELD_DERIVATION_ROWS.csv", "delta_gamma_MTS", "weak-field gamma residual definition"),
        ("profile_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "Yukawa_like_profile", "radial profile gamma coefficient"),
        ("bound_formula_3660", RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv", "GBF3660_1_gamma_profile_envelope", "Cassini gamma envelope formula"),
        ("input_pack_3660", RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_INPUT_PACK.csv", "GBI3660_7_gamma_kernel", "gamma profile input pack"),
        ("component_basis_3661", ROOT / "3661-Y5-R2FR-QX-component-basis-decomposition-or-shared-bound-runner.md", "Q_X = beta_source_alpha_bar", "non-EM source components retained"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "Cassini_Shapiro_gamma_2003", "Cassini gamma external comparator row"),
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
    external = [
        ("external_solar_constants", SOLAR_CONSTANT_SOURCE, "M_sun=1.9885e30 kg; R_sun=695700 km", "solar-limb nonclaim geometry proxy"),
        ("external_G_constant", G_SOURCE, "G=6.67430e-11", "Newtonian-potential nonclaim proxy"),
        ("external_c_exact", C_SOURCE, "c=299792458", "Newtonian-potential nonclaim proxy"),
    ]
    for source_id, path, needle, role in external:
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": path,
                "exists": True,
                "needle": needle,
                "needle_found": True,
                "role": role,
            }
        )
    return rows


def solar_b_source_value() -> float:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3665_SOLAR_BSOURCEEM_TOTAL_ROWS.csv")
    matches = [row for row in rows if row.get("row_id") == "SOL3665_3_solar_B_source_EM_total"]
    if not matches:
        raise RuntimeError("missing SOL3665_3_solar_B_source_EM_total")
    return float(matches[0]["B_A_EM"])


def cassini_bound_row() -> dict[str, str]:
    rows = load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    matches = [row for row in rows if row.get("row_id") == "R3_gamma"]
    if not matches:
        raise RuntimeError("missing local Cassini R3_gamma row")
    return matches[0]


def solar_limb_geometry_rows(ts: str) -> list[dict[str, object]]:
    phi_n_abs = G_NEWTON * M_SUN_KG / (C_LIGHT**2 * R_SUN_M)
    schwarzschild_radius = 2.0 * G_NEWTON * M_SUN_KG / C_LIGHT**2
    return [
        {
            **base(ts),
            "geometry_id": "SLG3666_0_solar_limb_proxy",
            "r_proxy_m": f"{R_SUN_M:.12e}",
            "M_sun_kg": f"{M_SUN_KG:.12e}",
            "G_SI": f"{G_NEWTON:.12e}",
            "c_m_per_s": f"{C_LIGHT:.12e}",
            "Phi_N_abs_dimensionless": f"{phi_n_abs:.12e}",
            "schwarzschild_radius_m": f"{schwarzschild_radius:.12e}",
            "formula": "|Phi_N(R_sun)|=G*M_sun/(c^2*R_sun)",
            "source_reference": f"{SOLAR_CONSTANT_SOURCE}; {G_SOURCE}; {C_SOURCE}",
            "current_status": "SOLAR_LIMB_SCALE_PROXY_NONCLAIM_NOT_CASSINI_TRANSFER_KERNEL",
            "score_ready": False,
            "claim_allowed": False,
        }
    ]


def envelope_rows(ts: str, b_sun_em: float, cassini: dict[str, str], geometry: list[dict[str, object]]) -> list[dict[str, object]]:
    bound = float(cassini["upper_bound"])
    phi_proxy = geometry[0]["Phi_N_abs_dimensionless"]
    r_proxy = geometry[0]["r_proxy_m"]
    return [
        {
            **base(ts),
            "envelope_id": "ENV3666_0_source_insert",
            "object": "solar_EM_source_charge_component",
            "inserted_numeric": f"{b_sun_em:.12e}",
            "formula": f"Q_X^EM_solar = ({b_sun_em:.12e}) * f_EM",
            "cassini_upper_bound": bound,
            "status": "SOURCE_SCALAR_INSERTED_COUPLING_OPEN",
            "required_inputs": "f_EM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "envelope_id": "ENV3666_1_amplitude_insert",
            "object": "Yukawa_profile_amplitude_EM_component",
            "inserted_numeric": f"{b_sun_em:.12e}",
            "formula": f"A_X^EM = ({b_sun_em:.12e} * f_EM)/(4*pi*Z_X)",
            "cassini_upper_bound": bound,
            "status": "AMPLITUDE_FORMULA_READY_ZX_FEM_OPEN",
            "required_inputs": "f_EM;Z_X",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "envelope_id": "ENV3666_2_gamma_EM_profile_bound",
            "object": "Cassini_delta_gamma_EM_profile_envelope",
            "inserted_numeric": f"{b_sun_em:.12e}",
            "formula": f"|delta_gamma_EM| <= |k_H|*|{b_sun_em:.12e}*f_EM|/(4*pi*|Z_X|)*exp(-r/lambda_X)*(3/r^3+3/(lambda_X*r^2)+1/(lambda_X^2*r))/|Phi_N(r)| + |k_G|*({b_sun_em:.12e}*f_EM/(4*pi*Z_X))^2*exp(-2*r/lambda_X)*(1/r^2+1/(lambda_X*r))^2/|Phi_N(r)| + |C_other_gamma|",
            "cassini_upper_bound": bound,
            "status": "SYMBOLIC_ENVELOPE_READY_NUMERIC_PROFILE_INPUTS_OPEN",
            "required_inputs": "f_EM;Z_X;lambda_X;k_H;k_G;r;Phi_N(r);C_other_gamma;K_gamma_profile",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "envelope_id": "ENV3666_3_limb_proxy_substitution",
            "object": "solar_limb_scale_substitution",
            "inserted_numeric": f"{b_sun_em:.12e}",
            "formula": f"use r_proxy={r_proxy} m and |Phi_N|_proxy={phi_proxy} only as a scale check; do not replace Cassini path-transfer kernel",
            "cassini_upper_bound": bound,
            "status": "GEOMETRY_SCALE_PROXY_FILLED_TRANSFER_KERNEL_STILL_OPEN",
            "required_inputs": "lambda_X;k_H;k_G;K_gamma_profile;impact_parameter/path_kernel",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "envelope_id": "ENV3666_4_full_QX_guard",
            "object": "full_source_charge_not_only_EM",
            "inserted_numeric": f"{b_sun_em:.12e}",
            "formula": f"Q_X^solar = ({b_sun_em:.12e})*f_EM + Q_X^nonEM + B_X",
            "cassini_upper_bound": bound,
            "status": "EM_BRANCH_INSERTED_NONEM_COMPONENTS_RETAINED",
            "required_inputs": "Q_X_nonEM;b_alpha;b_m;b_nuc;b_J_source;b_material_marker;b_boundary",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def input_requirement_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("REQ3666_0_fEM", "f_EM", "EM coupling of X/source residual into Maxwell/binding sector", "Q_X^EM_solar=B_source_EM*f_EM", "MISSING_PARENT_ZERO_OR_NUMERIC_COUPLING", "try f_EM=0 theorem from unique-F2/no-f_XF2; otherwise source a finite coefficient"),
        ("REQ3666_1_ZX", "Z_X", "quadratic kinetic normalization for X", "A_X=Q_X/(4*pi*Z_X)", "MISSING_PARENT_QUADRATIC_ACTION", "derive from parent Hessian/action normalization"),
        ("REQ3666_2_lambdaX", "lambda_X", "range/mass scale of local X profile", "lambda_X=sqrt(Z_X/M_X^2) or declared equivalent", "MISSING_PARENT_HESSIAN_OR_RANGE", "derive mass gap/range from parent local operator"),
        ("REQ3666_3_kH", "k_H", "linear Hessian-STF gamma projection coefficient", "C_H=|k_H|*|A_X|*H_kernel/|Phi_N|", "MISSING_WEAK_FIELD_PROJECTION", "derive weak-field projection from same-frame metric response"),
        ("REQ3666_4_kG", "k_G", "gradient-square-STF gamma projection coefficient", "C_G=|k_G|*A_X^2*G_kernel/|Phi_N|", "MISSING_WEAK_FIELD_PROJECTION", "derive whether gradient-square operator is absent or coefficient-bounded"),
        ("REQ3666_5_Kgamma", "K_gamma_profile", "Cassini/Shapiro transfer kernel from local profile to observed gamma residual", "path/impact transfer maps local profile coefficient into gamma readout", "MISSING_GAMMA_GEOMETRY_KERNEL", "derive transfer kernel or declare conservative bounding geometry"),
        ("REQ3666_6_Cother", "C_other_gamma", "non-profile gamma floors: boundary, readout, source, non-EH residuals", "|C_boundary|+|C_readout|+|C_source|+|C_nonEH_other|", "MISSING_COMPONENT_BOUNDS", "prove zero or source bounded rows"),
        ("REQ3666_7_QnonEM", "Q_X_nonEM", "non-EM source charge components retained by 3661", "Q_X_nonEM=beta_source_alpha*b_alpha+B_m*b_m+B_nuc*b_nuc+b_J+b_marker+b_boundary", "MISSING_NONEM_COMPONENTS", "derive zeros or source rows for mass/nuclear/boundary/source-marker components"),
    ]
    return [
        {
            **base(ts),
            "requirement_id": req_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "current_status": status,
            "next_action": next_action,
            "score_ready": False,
            "claim_allowed": False,
        }
        for req_id, symbol, definition, formula, status, next_action in specs
    ]


def symbolic_fem_bound_rows(ts: str, b_sun_em: float, cassini: dict[str, str]) -> list[dict[str, object]]:
    bound = float(cassini["upper_bound"])
    return [
        {
            **base(ts),
            "bound_id": "SFB3666_0_coefficients",
            "object": "define_fEM_bound_coefficients",
            "formula": f"a_gamma=|k_H|*({b_sun_em:.12e})*H(r,lambda_X)/(4*pi*|Z_X|*|Phi_N|); b_gamma=|k_G|*({b_sun_em:.12e}/(4*pi*|Z_X|))^2*G(r,lambda_X)/|Phi_N|",
            "cassini_upper_bound": bound,
            "interpretation": "The EM profile contribution has the form a_gamma*|f_EM| + b_gamma*f_EM^2 + |C_other_gamma|.",
            "current_status": "SYMBOLIC_ONLY_WAITING_PROFILE_COEFFICIENTS",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "bound_id": "SFB3666_1_linear_quadratic_bound",
            "object": "symbolic_fEM_max_if_inputs_real",
            "formula": "if b_gamma>0 and B>|C_other|: |f_EM| <= (-a_gamma + sqrt(a_gamma^2 + 4*b_gamma*(B_gamma-|C_other_gamma|)))/(2*b_gamma); if b_gamma=0: |f_EM| <= (B_gamma-|C_other_gamma|)/a_gamma",
            "cassini_upper_bound": bound,
            "interpretation": "This becomes a real coupling bound only after Z_X, lambda_X, k_H, k_G, Phi_N/kernel, and C_other are sourced.",
            "current_status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "bound_id": "SFB3666_2_zero_shortcut",
            "object": "fEM_zero_or_source_charge_zero",
            "formula": "f_EM=0 or B_source_EM_solar=0 or K_gamma_profile=0 or k_H=k_G=0 kills this EM branch, but none is currently parent-signed",
            "cassini_upper_bound": bound,
            "interpretation": "Do not infer local GR from source-composition completion; coupling/profile silence must be derived.",
            "current_status": "ZERO_SHORTCUTS_LISTED_UNSIGNED",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3666_0_source_scalar_inserted", "solar B_source_EM total inserted into gamma envelope", "PASSED_NONCLAIM_INSERTION", "3665 total appears explicitly in Q_X^EM and A_X formulas"),
        ("CG3666_1_limb_proxy", "solar-limb Phi_N scale proxy filled", "PASSED_SCALE_PROXY_ONLY", "useful for scale checks but not a Cassini transfer kernel"),
        ("CG3666_2_fEM_zero", "f_EM zero theorem", "FAILED_UNSIGNED_COUNTERTERM_LIVE", "unique-F2/no-f_XF2 remains unsigned"),
        ("CG3666_3_numeric_gamma_score", "numeric Cassini gamma score", "BLOCKED_BY_PROFILE_AND_COUPLING_INPUTS", "f_EM, Z_X, lambda_X, k_H, k_G, K_gamma_profile, C_other, and non-EM source pieces remain open"),
        ("CG3666_4_local_GR_claim", "local-GR/PPN pass claim", "ACTIVE_GUARD", "source scalar insertion is not a local-GR derivation"),
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


def status_rows(ts: str, b_sun_em: float, cassini: dict[str, str], geometry: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "SOLAR_EM_SOURCE_INSERTED_IN_GAMMA_ENVELOPE_NONCLAIM",
            "summary": "3666 imports the completed solar B_source_EM scalar, inserts it into the EM part of the Cassini gamma profile envelope, and fills a solar-limb Phi_N scale proxy while retaining all MTS coupling/profile blockers.",
            "solar_B_source_EM_total": f"{b_sun_em:.12e}",
            "cassini_gamma_upper_bound": cassini["upper_bound"],
            "solar_limb_Phi_N_abs_proxy": geometry[0]["Phi_N_abs_dimensionless"],
            "claim_ceiling": "no f_EM zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The EM source scalar is now inside an explicit gamma inequality; next progress must derive or source f_EM/Z_X/lambda_X/k_H/k_G/K_gamma rather than circling source composition.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3666_0",
            "target_doc": "3667-Y5-R2FR-fEM-ZX-profile-normalization-proof-or-first-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3667_fEM_ZX_profile_normalization_proof_or_first_bound_row.py",
            "objective": "try to close f_EM=0 or derive the parent normalization chain for Z_X, lambda_X, k_H, and k_G; if that fails, stage the first nonclaim finite-coupling bound row using the 3666 envelope",
            "success_gate": "either the EM branch is parent-zero, or the first finite gamma-bound row has explicit symbolic/numeric placeholders only for identified parent/profile coefficients and remains nonclaim",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    geometry: list[dict[str, object]],
    envelope: list[dict[str, object]],
    requirements: list[dict[str, object]],
    symbolic_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3666 - Solar EM gamma envelope stub or fEM profile inputs",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        f"The completed 3665 solar source scalar is now inserted into the EM part of the gamma envelope: `B_source_EM_solar = {status[0]['solar_B_source_EM_total']}`.",
        "",
        "`Q_X^EM_solar = B_source_EM_solar * f_EM`.",
        "",
        "`A_X^EM = B_source_EM_solar * f_EM / (4*pi*Z_X)`.",
        "",
        "The Cassini-facing inequality is now explicit, but nonclaim: the live blockers are `f_EM`, `Z_X`, `lambda_X`, `k_H`, `k_G`, `K_gamma_profile`, `C_other_gamma`, and non-EM source-charge pieces.",
        "",
        "## Solar-limb scale proxy",
    ]
    for row in geometry:
        lines.append(f"- `{row['geometry_id']}`: `|Phi_N(R_sun)|={row['Phi_N_abs_dimensionless']}`, `r={row['r_proxy_m']} m` - {row['current_status']}")
    lines.extend(["", "## Inserted envelope rows"])
    for row in envelope:
        lines.append(f"- `{row['envelope_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Required inputs still open"])
    for row in requirements:
        lines.append(f"- `{row['symbol']}`: {row['current_status']} - {row['next_action']}")
    lines.extend(["", "## Symbolic fEM bound helper"])
    for row in symbolic_bounds:
        lines.append(f"- `{row['bound_id']}`: {row['current_status']} - `{row['formula']}`")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    geometry: list[dict[str, object]],
    envelope: list[dict[str, object]],
    requirements: list[dict[str, object]],
    symbolic_bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    b_sun_em: float,
    cassini: dict[str, str],
) -> list[dict[str, object]]:
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

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    phi = float(geometry[0]["Phi_N_abs_dimensionless"])
    required_symbols = {"f_EM", "Z_X", "lambda_X", "k_H", "k_G", "K_gamma_profile", "C_other_gamma", "Q_X_nonEM"}
    generated = sources + geometry + envelope + requirements + symbolic_bounds + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3666*", "3666-Y5-R2FR-*", "P8_Y5*3666*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    add("VAL3666_0_sources_exist", all(row["exists"] for row in sources), "every cited local path/external source marker exists")
    add("VAL3666_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found or externally declared")
    add("VAL3666_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3666 outputs written")
    add("VAL3666_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3666_4_solar_scalar_imported", math.isclose(b_sun_em, 8.256508261034e-05, rel_tol=1e-10, abs_tol=1e-15), f"B_source_EM_solar={b_sun_em:.12e}")
    add("VAL3666_5_cassini_bound_imported", cassini.get("row_id") == "R3_gamma" and float(cassini["upper_bound"]) > 0, f"Cassini bound row={cassini.get('row_id')} upper_bound={cassini.get('upper_bound')}")
    add("VAL3666_6_geometry_proxy_numeric", 1.0e-6 < phi < 3.0e-6, f"solar-limb Phi_N proxy={phi:.12e}")
    scalar_formula_ids = {"ENV3666_0_source_insert", "ENV3666_1_amplitude_insert", "ENV3666_2_gamma_EM_profile_bound", "ENV3666_4_full_QX_guard"}
    scalar_formula_rows = [row for row in envelope if row["envelope_id"] in scalar_formula_ids]
    add("VAL3666_7_envelope_inserts_scalar", all(f"{b_sun_em:.12e}" in row["formula"] for row in scalar_formula_rows), "inserted scalar appears in source/amplitude/profile/full-Q formulas")
    add("VAL3666_8_requirements_complete", required_symbols.issubset({str(row["symbol"]) for row in requirements}), "all profile/coupling requirements listed")
    add("VAL3666_9_symbolic_bound_present", any("sqrt" in row["formula"] and "f_EM" in row["formula"] for row in symbolic_bounds), "symbolic fEM bound helper present")
    add("VAL3666_10_nonclaim_rows", not any(str(row.get("score_ready", "")).lower() == "true" for row in geometry + envelope + requirements + symbolic_bounds), "all formula rows remain not score-ready")
    add("VAL3666_11_all_generated_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3666_12_gamma_blockers_preserved", "K_gamma_profile" in envelope[2]["required_inputs"] and "Q_X_nonEM" in requirements[-1]["symbol"], "gamma kernel and non-EM source blockers retained")
    add("VAL3666_13_doc_written", "Q_X^EM_solar" in doc_text and "A_X^EM" in doc_text and "nonclaim" in doc_text, "doc records inserted gamma envelope and nonclaim status")
    add("VAL3666_14_no_formalization_leak", not leaks, "no 3666 checkpoint files in formalization-workbench")
    add("VAL3666_15_next_target", next_target[0]["target_doc"].startswith("3667-") and "fEM-ZX-profile" in next_target[0]["target_doc"], "3667 fEM/ZX/profile target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    b_sun_em = solar_b_source_value()
    cassini = cassini_bound_row()
    geometry = solar_limb_geometry_rows(ts)
    envelope = envelope_rows(ts, b_sun_em, cassini, geometry)
    requirements = input_requirement_rows(ts)
    symbolic_bounds = symbolic_fem_bound_rows(ts, b_sun_em, cassini)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, b_sun_em, cassini, geometry)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3666_SOURCE_REGISTER.csv",
        "geometry": RESIDUALS / "P8_Y5_R2FR_3666_SOLAR_LIMB_GEOMETRY_PROXY.csv",
        "envelope": RESIDUALS / "P8_Y5_R2FR_3666_INSERTED_SOLAR_GAMMA_ENVELOPE.csv",
        "requirements": RESIDUALS / "P8_Y5_R2FR_3666_FEM_PROFILE_INPUT_REQUIREMENTS.csv",
        "symbolic_bounds": RESIDUALS / "P8_Y5_R2FR_3666_SYMBOLIC_FEM_BOUND_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3666_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3666_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3666_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3666_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["geometry"], geometry)
    write_csv(outputs["envelope"], envelope)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["symbolic_bounds"], symbolic_bounds)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, geometry, envelope, requirements, symbolic_bounds, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, geometry, envelope, requirements, symbolic_bounds, gates, status, next_target, b_sun_em, cassini)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3666 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3666 checkpoint with {len(validation)} validation checks; solar_EM_gamma_scalar={b_sun_em:.12e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
