from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3665"
BRANCH_ID = "MTS_R2FR_Y5_SOLAR_METAL_MIXTURE_EXPANSION_OR_UNIQUE_F2_CLOSURE_3665"
DOC = ROOT / "3665-Y5-R2FR-solar-metal-mixture-expansion-or-unique-F2-closure.md"

A_C_MEV = 0.711
U_MEV = 931.49410242
BULK_X = 0.7154
BULK_Y = 0.2703
BULK_Z = 0.0142
SOLAR_SOURCE = "Asplund, Grevesse, Sauval, Scott 2009 solar composition; bulk X=0.7154,Y=0.2703,Z=0.0142; Table 1 log-epsilon metal basis; https://arxiv.org/abs/0909.0948"
SEMF_SOURCE = "semi_empirical_mass_formula_convention; Coulomb term E_C=a_C Z(Z-1) A^(-1/3), a_C=0.711 MeV; https://en.wikipedia.org/wiki/Semi-empirical_mass_formula"
ATOMIC_WEIGHT_SOURCE = "CIAAW/IUPAC standard atomic weights used as A_effective proxies; https://www.ciaaw.org/atomic-weights.htm"
METAL_METHOD = "AGSS09_LISTED_METAL_PROXY_NORMALIZED_TO_BULK_Z_NONCLAIM"

METALS = [
    ("Li", 1.05, 6.94, 3),
    ("Be", 1.38, 9.0122, 4),
    ("B", 2.70, 10.81, 5),
    ("C", 8.43, 12.011, 6),
    ("N", 7.83, 14.007, 7),
    ("O", 8.69, 15.999, 8),
    ("F", 4.56, 18.998, 9),
    ("Ne", 7.93, 20.180, 10),
    ("Na", 6.24, 22.990, 11),
    ("Mg", 7.60, 24.305, 12),
    ("Al", 6.45, 26.982, 13),
    ("Si", 7.51, 28.085, 14),
    ("P", 5.41, 30.974, 15),
    ("S", 7.12, 32.06, 16),
    ("Cl", 5.50, 35.45, 17),
    ("Ar", 6.40, 39.948, 18),
    ("K", 5.03, 39.098, 19),
    ("Ca", 6.34, 40.078, 20),
    ("Sc", 3.15, 44.956, 21),
    ("Ti", 4.95, 47.867, 22),
    ("V", 3.93, 50.942, 23),
    ("Cr", 5.64, 51.996, 24),
    ("Mn", 5.43, 54.938, 25),
    ("Fe", 7.50, 55.845, 26),
    ("Co", 4.99, 58.933, 27),
    ("Ni", 6.22, 58.693, 28),
    ("Cu", 4.19, 63.546, 29),
    ("Zn", 4.56, 65.38, 30),
]


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


def em_fraction(charge_z: int, atomic_weight: float) -> tuple[float, float, float]:
    e_c = A_C_MEV * charge_z * (charge_z - 1) * atomic_weight ** (-1.0 / 3.0)
    mass_e = atomic_weight * U_MEV
    return e_c, mass_e, e_c / mass_e


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3664", RESIDUALS / "P8_Y5_R2FR_3664_NEXT_TARGET.csv", "3665-Y5-R2FR-solar-metal-mixture-expansion-or-unique-F2-closure.md", "3664 selected this target"),
        ("doc_3664", ROOT / "3664-Y5-R2FR-unique-F2-parent-proof-or-solar-BsourceEM-first-row.md", "B_Sun_EM,HHe_partial = 6.4929539e-05", "3664 partial solar H/He source row"),
        ("uniqueF2_3664", RESIDUALS / "P8_Y5_R2FR_3664_UNIQUE_F2_PROOF_ATTEMPT.csv", "COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR", "3664 unique-F2 obstruction"),
        ("solar_3664", RESIDUALS / "P8_Y5_R2FR_3664_SOLAR_BSOURCEEM_ROWS.csv", "SOL3664_3_BsourceEM_HHe_partial", "3664 H/He numeric row reused"),
        ("doc_3649", ROOT / "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md", "FAIL_CURRENT_CLAIM_COUNTERTERM_LEGAL", "3649 EM-lock obstruction"),
        ("audit_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "3649 EM-lock clause audit"),
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
    external_specs = [
        ("external_AGSS09_bulk_and_metals", SOLAR_SOURCE, "X=0.7154,Y=0.2703,Z=0.0142; log epsilon metal values hardcoded from AGSS09 Table 1", "solar bulk composition and listed metal abundance basis"),
        ("external_SEMF_coulomb_term", SEMF_SOURCE, "E_C=a_C Z(Z-1) A^(-1/3)", "Coulomb binding proxy used only as nonclaim source-composition scalar"),
        ("external_CIAAW_atomic_weights", ATOMIC_WEIGHT_SOURCE, "standard atomic weights", "atomic-weight proxies for A_effective in the metal basis"),
    ]
    for source_id, path, needle, role in external_specs:
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


def unique_f2_closure_audit(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "audit_id": "UF23665_0_target_theorem",
            "object": "unique same-frame Maxwell block",
            "statement": "To make f_EM=0, the parent action must own one Maxwell kinetic block and forbid independent scalar gauge-kinetic dressing.",
            "formula": "S_EM=-(C_P/4) int mu_obs <F_QT_Q,F_QT_Q>_P ; forbid DeltaS=-(1/4)int mu_obs f_X(X_N)F_Q^2",
            "test": "Does existing parent grammar exclude f_X(X_N)F_Q^2?",
            "result": "NO",
            "accepted_as_zero": False,
            "claim_allowed": False,
            "missing_parent_clause": "no independent visible gauge-kinetic scalar; no hidden-visible coefficient morphism in the EM block",
        },
        {
            **base(ts),
            "audit_id": "UF23665_1_counterexample",
            "object": "legal scalar gauge-kinetic counterterm",
            "statement": "The counterterm is gauge invariant and diffeomorphism invariant when f_X is a scalar built from the MTS residual sector.",
            "formula": "DeltaL = -(1/4) f_X(X_N) F_Q^2",
            "test": "Can ordinary covariance/gauge invariance alone ban it?",
            "result": "NO",
            "accepted_as_zero": False,
            "claim_allowed": False,
            "missing_parent_clause": "stronger quotient/superselection rule tying EM normalization to one observed coframe",
        },
        {
            **base(ts),
            "audit_id": "UF23665_2_possible_closure_contract",
            "object": "future parent closure",
            "statement": "A future parent could close this if X_N is vertical-null for the visible Maxwell functor and all visible gauge kinetic normalization is a quotient constant.",
            "formula": "Dq(v_X)=0 and delta_X C_P=0 and Hom(hidden residual scalars, visible F_Q^2)=0",
            "test": "Is this contract already signed by current files?",
            "result": "NO_PARENT_SIGNATURE_FOUND",
            "accepted_as_zero": False,
            "claim_allowed": False,
            "missing_parent_clause": "signed quotient-invariant EM normalization theorem",
        },
        {
            **base(ts),
            "audit_id": "UF23665_3_verdict",
            "object": "f_EM status",
            "statement": "3665 cannot honestly set f_EM=0, so it proceeds by source-composition completion instead of smuggling a zero.",
            "formula": "f_EM retained; Q_X^EM_solar = B_source_EM_solar * f_EM",
            "test": "Claim f_EM zero?",
            "result": "REJECT_ZERO_RETAIN_FINITE_COUPLING_INPUT",
            "accepted_as_zero": False,
            "claim_allowed": False,
            "missing_parent_clause": "f_EM numeric/source row or zero theorem",
        },
    ]


def metal_basis_rows(ts: str) -> list[dict[str, object]]:
    raw_weights = []
    for symbol, log_epsilon, atomic_weight, charge_z in METALS:
        number_ratio_to_h = 10.0 ** (log_epsilon - 12.0)
        raw_mass_weight = number_ratio_to_h * atomic_weight
        raw_weights.append((symbol, log_epsilon, atomic_weight, charge_z, number_ratio_to_h, raw_mass_weight))
    raw_sum = sum(row[5] for row in raw_weights)
    rows = []
    for index, (symbol, log_epsilon, atomic_weight, charge_z, number_ratio_to_h, raw_mass_weight) in enumerate(raw_weights):
        normalized_within_metals = raw_mass_weight / raw_sum
        solar_mass_fraction = BULK_Z * normalized_within_metals
        e_c, mass_e, b_em = em_fraction(charge_z, atomic_weight)
        contribution = solar_mass_fraction * b_em
        rows.append(
            {
                **base(ts),
                "row_id": f"SOL3665_METAL_{index:02d}_{symbol}",
                "source_body": "Sun_bulk",
                "component": symbol,
                "log_epsilon_AGSS09": log_epsilon,
                "number_ratio_to_H": f"{number_ratio_to_h:.12e}",
                "raw_mass_weight": f"{raw_mass_weight:.12e}",
                "normalized_within_listed_metals": f"{normalized_within_metals:.12e}",
                "solar_mass_fraction": f"{solar_mass_fraction:.12e}",
                "bulk_Z_target": BULK_Z,
                "charge_Z": charge_z,
                "A_effective": atomic_weight,
                "E_C_MeV": f"{e_c:.12e}",
                "mass_energy_MeV": f"{mass_e:.12e}",
                "B_A_EM": f"{b_em:.12e}",
                "contribution_to_B_source_EM": f"{contribution:.12e}",
                "source_reference": f"{SOLAR_SOURCE}; {SEMF_SOURCE}; {ATOMIC_WEIGHT_SOURCE}",
                "method": METAL_METHOD,
                "current_status": "SOLAR_METAL_PROXY_NUMERIC_NONCLAIM",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def solar_total_rows(ts: str, metal_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    h_b = 0.0
    he_e_c, he_mass_e, he_b = em_fraction(2, 4.002602)
    h_contribution = BULK_X * h_b
    he_contribution = BULK_Y * he_b
    metal_contribution = sum(float(row["contribution_to_B_source_EM"]) for row in metal_rows)
    metal_weighted_b = metal_contribution / BULK_Z
    total_b = h_contribution + he_contribution + metal_contribution
    return [
        {
            **base(ts),
            "row_id": "SOL3665_0_H",
            "source_body": "Sun_bulk",
            "component": "H",
            "mass_fraction": BULK_X,
            "B_A_EM": f"{h_b:.12e}",
            "contribution_to_B_source_EM": f"{h_contribution:.12e}",
            "method": "SEMF Coulomb term vanishes for charge_Z=1",
            "source_reference": SOLAR_SOURCE,
            "current_status": "SOURCE_BACKED_NUMERIC_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3665_1_He",
            "source_body": "Sun_bulk",
            "component": "He",
            "mass_fraction": BULK_Y,
            "B_A_EM": f"{he_b:.12e}",
            "E_C_MeV": f"{he_e_c:.12e}",
            "mass_energy_MeV": f"{he_mass_e:.12e}",
            "contribution_to_B_source_EM": f"{he_contribution:.12e}",
            "method": "SEMF Coulomb fraction from a_C=0.711 MeV and CIAAW He atomic weight proxy",
            "source_reference": f"{SOLAR_SOURCE}; {SEMF_SOURCE}; {ATOMIC_WEIGHT_SOURCE}",
            "current_status": "SOURCE_BACKED_NUMERIC_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3665_2_metals_listed_proxy",
            "source_body": "Sun_bulk",
            "component": "listed_metals_normalized_to_Z",
            "mass_fraction": BULK_Z,
            "B_A_EM": f"{metal_weighted_b:.12e}",
            "contribution_to_B_source_EM": f"{metal_contribution:.12e}",
            "method": METAL_METHOD,
            "source_reference": f"{SOLAR_SOURCE}; {SEMF_SOURCE}; {ATOMIC_WEIGHT_SOURCE}",
            "current_status": "COMPLETE_LISTED_METAL_PROXY_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "row_id": "SOL3665_3_solar_B_source_EM_total",
            "source_body": "Sun_bulk",
            "component": "H_plus_He_plus_listed_metals_proxy",
            "mass_fraction": BULK_X + BULK_Y + BULK_Z,
            "B_A_EM": f"{total_b:.12e}",
            "contribution_to_B_source_EM": f"{total_b:.12e}",
            "method": f"H/He plus {METAL_METHOD}; rounded bulk mass fractions sum to {BULK_X + BULK_Y + BULK_Z:.4f}",
            "source_reference": f"{SOLAR_SOURCE}; {SEMF_SOURCE}; {ATOMIC_WEIGHT_SOURCE}",
            "current_status": "SOLAR_B_SOURCE_EM_TOTAL_PROXY_COMPLETE_NONCLAIM_NOT_SCORE_READY",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def gamma_status_rows(ts: str, total_b: float) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "GEM3665_0_inserted_solar_source_scalar",
            "object": "solar_B_source_EM_total",
            "formula": "B_source_EM_solar = sum_i w_i B_i_EM",
            "numeric_value": f"{total_b:.12e}",
            "current_status": "SOURCE_COMPOSITION_SCALAR_FILLED_AS_PROXY_NONCLAIM",
            "missing_for_score": "f_EM; Z_X; lambda_X; k_H; k_G; gamma kernel; parent profile normalization",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "status_id": "GEM3665_1_gamma_envelope",
            "object": "Cassini_gamma_EM_branch",
            "formula": "Q_X^EM_solar = B_source_EM_solar * f_EM ; A_X ~= Q_X/(4*pi*Z_X)",
            "numeric_value": "symbolic_until_f_EM_Z_X_profile",
            "current_status": "EXECUTABLE_SOURCE_INSERTION_READY_BUT_COUPLING_PROFILE_BLOCKED",
            "missing_for_score": "f_EM; Z_X; lambda_X; k_H; k_G; gamma kernel",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "status_id": "GEM3665_2_fEM_zero_route",
            "object": "f_EM_zero",
            "formula": "unique_F2_owner plus no f_XF2 => f_EM=0",
            "numeric_value": "not_applicable",
            "current_status": "REJECTED_FOR_NOW_COUNTERTERM_LIVE",
            "missing_for_score": "signed parent unique-F2/no-f_XF2 theorem",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3665_0_unique_F2_zero", "f_EM zero from unique-F2 closure", "FAILED_UNSIGNED_COUNTERTERM_LIVE", "do not claim f_EM=0"),
        ("CG3665_1_metal_basis", "AGSS09 listed metal basis expanded", "PASSED_PROXY_FILL_NONCLAIM", "metals are numeric but normalized listed-proxy not a claim-ready solar model"),
        ("CG3665_2_solar_total", "solar B_source_EM total filled", "PASSED_PROXY_TOTAL_NONCLAIM", "H/He/metals source scalar can feed symbolic gamma envelope"),
        ("CG3665_3_gamma_score", "Cassini/gamma score readiness", "BLOCKED_BY_COUPLING_PROFILE_INPUTS", "f_EM, Z_X, lambda_X, k_H, k_G and gamma kernel still absent"),
        ("CG3665_4_no_public_claim", "no local-GR or PPN/local-source claim", "ACTIVE_GUARD", "complete source scalar is not a completed field-theory reduction"),
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


def status_rows(ts: str, total_b: float, metal_b: float) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "SOLAR_METAL_MIXTURE_EXPANDED_PROXY_UNIQUE_F2_UNSIGNED_NONCLAIM",
            "summary": "3665 keeps f_EM live, expands the AGSS09 listed metal mixture, and produces a complete nonclaim solar B_source_EM proxy row for the EM/gamma branch.",
            "solar_B_source_EM_total": f"{total_b:.12e}",
            "solar_metal_contribution": f"{metal_b:.12e}",
            "claim_ceiling": "no f_EM zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The solar source-composition scalar is no longer blocked by missing metals; the remaining live obstruction is now the coupling/profile side rather than source composition.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3665_0",
            "target_doc": "3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md",
            "target_script": "scripts/Y5_R2FR_3666_solar_EM_gamma_envelope_stub_or_fEM_profile_inputs.py",
            "objective": "insert completed solar B_source_EM into the gamma envelope and expose remaining f_EM, Z_X, lambda_X, k_H, k_G, and gamma-kernel inputs; or derive f_EM=0",
            "success_gate": "gamma EM branch has a nonclaim executable formula with known source rows inserted and only explicit parent/profile inputs blocking score",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    metal_rows: list[dict[str, object]],
    total_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    total_row = next(row for row in total_rows if row["row_id"] == "SOL3665_3_solar_B_source_EM_total")
    metal_row = next(row for row in total_rows if row["row_id"] == "SOL3665_2_metals_listed_proxy")
    top_metals = sorted(metal_rows, key=lambda row: float(row["contribution_to_B_source_EM"]), reverse=True)[:8]
    lines = [
        "# 3665 - Solar metal mixture expansion or unique-F2 closure",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The unique-`F^2` route still does not close: an independent scalar gauge-kinetic term `f_X(X_N)F_Q^2` remains legal unless a future parent theorem explicitly bans it.",
        "",
        "The concrete advance is source-side: the solar metal term that blocked 3664 is now expanded into a numeric AGSS09 listed-metal proxy, normalized to bulk `Z=0.0142`, then combined with the existing H/He row.",
        "",
        f"`solar_B_source_EM_total = {total_row['B_A_EM']}`.",
        "",
        f"`solar_B_source_EM_metals_proxy = {metal_row['contribution_to_B_source_EM']}`.",
        "",
        "This is deliberately nonclaim: it is a source-composition scalar, not a completed gamma/local-GR/PPN pass.",
        "",
        "## Unique-F2 closure audit",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['result']} - `{row['formula']}`")
    lines.extend(["", "## Solar metal basis"])
    lines.append(f"- Method: `{METAL_METHOD}`.")
    lines.append(f"- Listed metal rows: `{len(metal_rows)}`; normalized metal mass-fraction sum: `{sum(float(row['solar_mass_fraction']) for row in metal_rows):.12e}`.")
    lines.append("- Largest EM-source contributors in the proxy:")
    for row in top_metals:
        lines.append(f"  - `{row['component']}`: mass_fraction=`{row['solar_mass_fraction']}`, B_A_EM=`{row['B_A_EM']}`, contribution=`{row['contribution_to_B_source_EM']}`")
    lines.extend(["", "## Solar BsourceEM total rows"])
    for row in total_rows:
        lines.append(f"- `{row['row_id']}`: `{row['component']}` B=`{row['B_A_EM']}` contribution=`{row['contribution_to_B_source_EM']}` - {row['current_status']}")
    lines.extend(["", "## Gamma/EM status"])
    for row in gamma_rows:
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


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    metal_rows: list[dict[str, object]],
    total_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
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
    total_row = next(row for row in total_rows if row["row_id"] == "SOL3665_3_solar_B_source_EM_total")
    metal_total_row = next(row for row in total_rows if row["row_id"] == "SOL3665_2_metals_listed_proxy")
    total_b = float(total_row["B_A_EM"])
    component_sum = sum(float(row["contribution_to_B_source_EM"]) for row in total_rows if row["row_id"] != "SOL3665_3_solar_B_source_EM_total")
    metal_mass_sum = sum(float(row["solar_mass_fraction"]) for row in metal_rows)
    required_metals = {"C", "N", "O", "Ne", "Mg", "Si", "S", "Fe"}
    generated = sources + audit + metal_rows + total_rows + gamma_rows + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3665*", "3665-Y5-R2FR-*", "P8_Y5*3665*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    add("VAL3665_0_sources_exist", all(row["exists"] for row in sources), "every cited local path/external source marker exists")
    add("VAL3665_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found or externally declared")
    add("VAL3665_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3665 outputs written")
    add("VAL3665_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3665_4_uniqueF2_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in audit), "unique-F2/fEM zero not accepted")
    add("VAL3665_5_counterterm_live", any(row["result"] == "REJECT_ZERO_RETAIN_FINITE_COUPLING_INPUT" for row in audit), "finite f_EM route retained")
    add("VAL3665_6_required_metals_present", required_metals.issubset({str(row["component"]) for row in metal_rows}), "major AGSS09 metal basis entries present")
    add("VAL3665_7_metal_mass_sum", math.isclose(metal_mass_sum, BULK_Z, rel_tol=0.0, abs_tol=5e-15), f"normalized listed metal mass fraction sum={metal_mass_sum:.12e}")
    add("VAL3665_8_total_numeric", total_b > 0.0 and math.isfinite(total_b), f"solar_B_source_EM_total={total_b:.12e}")
    add("VAL3665_9_total_component_sum", math.isclose(total_b, component_sum, rel_tol=1e-10, abs_tol=5e-15), f"total equals H+He+metals within tolerance; sum={component_sum:.12e}")
    add("VAL3665_10_all_proxy_nonclaim", not any(str(row.get("score_ready", "")).lower() == "true" for row in metal_rows + total_rows), "source rows remain not score-ready")
    add("VAL3665_11_all_generated_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3665_12_gamma_missing_inputs", all(token in gamma_rows[0]["missing_for_score"] for token in ["f_EM", "Z_X", "lambda_X", "k_H", "k_G", "gamma kernel"]), "gamma status preserves coupling/profile blockers")
    add("VAL3665_13_metal_method_recorded", all(METAL_METHOD in row["method"] for row in metal_rows) and METAL_METHOD in metal_total_row["method"], "metal proxy method recorded")
    add("VAL3665_14_doc_written", "solar_B_source_EM_total" in doc_text and "AGSS09" in doc_text and "nonclaim" in doc_text, "doc records total, AGSS09 method, and nonclaim status")
    add("VAL3665_15_no_formalization_leak", not leaks, "no 3665 checkpoint files in formalization-workbench")
    add("VAL3665_16_next_target", next_target[0]["target_doc"].startswith("3666-") and "gamma-envelope" in next_target[0]["target_doc"], "3666 gamma envelope/input target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = unique_f2_closure_audit(ts)
    metal_rows = metal_basis_rows(ts)
    total_rows = solar_total_rows(ts, metal_rows)
    total_b = float(next(row for row in total_rows if row["row_id"] == "SOL3665_3_solar_B_source_EM_total")["B_A_EM"])
    metal_b = float(next(row for row in total_rows if row["row_id"] == "SOL3665_2_metals_listed_proxy")["contribution_to_B_source_EM"])
    gamma_rows = gamma_status_rows(ts, total_b)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, total_b, metal_b)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3665_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3665_UNIQUE_F2_CLOSURE_AUDIT.csv",
        "metals": RESIDUALS / "P8_Y5_R2FR_3665_SOLAR_METAL_BASIS_ROWS.csv",
        "solar_total": RESIDUALS / "P8_Y5_R2FR_3665_SOLAR_BSOURCEEM_TOTAL_ROWS.csv",
        "gamma_status": RESIDUALS / "P8_Y5_R2FR_3665_GAMMA_EM_STATUS_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3665_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3665_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3665_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3665_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["metals"], metal_rows)
    write_csv(outputs["solar_total"], total_rows)
    write_csv(outputs["gamma_status"], gamma_rows)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, metal_rows, total_rows, gamma_rows, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, metal_rows, total_rows, gamma_rows, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3665 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3665 checkpoint with {len(validation)} validation checks; solar_B_source_EM_total={total_b:.12e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
