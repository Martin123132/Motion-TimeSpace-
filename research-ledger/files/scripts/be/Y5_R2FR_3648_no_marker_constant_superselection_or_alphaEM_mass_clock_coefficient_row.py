from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3648"
BRANCH_ID = "MTS_R2FR_Y5_NO_MARKER_CONSTANT_SUPERSELECTION_OR_ALPHA_MASS_CLOCK_ROWS_3648"
DOC = ROOT / "3648-Y5-R2FR-no-marker-constant-superselection-or-alphaEM-mass-clock-coefficient-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3648_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3648_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3648_CONSTANT_MARKER_AUDIT.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3648_ALPHA_MASS_CLOCK_COEFFICIENT_ROWS.csv",
        "projections": RESIDUALS / "P8_Y5_R2FR_3648_OBSERVABLE_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3648_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3648_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3648_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3648_VALIDATION.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3647", RESIDUALS / "P8_Y5_R2FR_3647_NEXT_TARGET.csv", "alpha_EM, particle masses/mass ratios", "3647 handoff to constant/no-marker fork"),
        ("doc_3647", ROOT / "3647-Y5-R2FR-observed-frame-no-shadow-theorem-or-cg-bdis-coefficient-row.md", "NO_MARKER_CONSTANT_SUPERSELECTION_NEXT", "3647 decision selecting constants/material markers"),
        ("nomarker_736", RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv", "NMC736_2_no_direct_species_marker", "736 no direct species/marker contract"),
        ("blindness_594", RESIDUALS / "P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv", "MBG594_1_clock_and_unit_blindness", "594 clock/unit/material blindness gate"),
        ("no_shadow_1046", ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md", "CMA1046_0_alpha_EM", "1046 constant marker split audit"),
        ("pack_1028", ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md", "FMB1028_7_b_alpha", "1028 b_alpha/b_A input pack"),
        ("const_1047", ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md", "CST1047_5_verdict", "1047 constant superselection and coefficient provenance"),
        ("no_extra_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "PVS1048_1_no_extra_F2", "1048 no-extra-F2/no-mass-vertex route"),
        ("constant_contract", RESIDUALS / "P8_constant_sector_universality_CONTRACT.csv", "constant", "constant-sector universality contract"),
        ("constant_ownership_637", RESIDUALS / "P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv", "constant", "constant ownership theorem attempt"),
        ("constant_zero_638", RESIDUALS / "P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv", "constant", "constant zero route attempt"),
        ("clock_sensitivity_646", RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", "delta_K_alpha_used", "source-backed clock alpha sensitivity rows"),
        ("clock_projection_646", RESIDUALS / "P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv", "clock", "clock projection ledger"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R2_clock_redshift", "local WEP/clock bound anchors"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle.lower() in text.lower(),
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "theorem_id": "CST3648_0_statement",
            "claim": "No-marker constant superselection theorem.",
            "mathematical_form": "theta_I(Phi)=theta_I^rep fixed, or theta_I(Phi)=theta_bar_I(q(Phi)); Dq[v_X]=0 => Lie_vX theta_I=0.",
            "derivation_step": "Apply the quotient chain rule or fixed-representation condition to every dimensionless ordinary-matter constant and material marker before variation.",
            "result": "If all theta_I close in one parent branch, b_alpha=b_mass=b_clock=b_material=0 and qbar_constants_abs=0.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent constant owner, matter spectrum owner, no-extra-vertex rule, and readout/renormalization lock",
        },
        {
            **base,
            "theorem_id": "CST3648_1_alpha_EM",
            "claim": "alpha_EM is not removable by units.",
            "mathematical_form": "b_alpha := Lie_vX ln alpha_EM, with alpha_EM=e_eff^2/(4*pi*hbar*c) after gauge and readout normalization.",
            "derivation_step": "A unique Maxwell/gauge kinetic normalization and no f_X(X)F^2 counterterm would imply b_alpha=0.",
            "result": "Current corpus does not parent-sign unique-F2/no-extra-F2/readout closure; b_alpha remains live.",
            "status": "FAIL_CURRENT_CLAIM_RETAIN_B_ALPHA",
            "missing_for_claim": "gauge generator owner, unique F^2 norm, no scalar gauge-kinetic counterterm, and quotient-owned hbar*c/readout",
        },
        {
            **base,
            "theorem_id": "CST3648_2_mass_ratios",
            "claim": "Mass ratios and binding fractions are observable constants.",
            "mathematical_form": "b_mu := Lie_vX ln(m_e/m_p); b_mA := Lie_vX ln m_A^obs; b_nuc := Lie_vX ln E_binding^obs.",
            "derivation_step": "A common mass scale may be convention, but dimensionless ratios and composition-dependent binding fractions are not.",
            "result": "Mass/material channels stay live without a parent matter-spectrum theorem.",
            "status": "FAIL_CURRENT_CLAIM_RETAIN_B_MASS",
            "missing_for_claim": "Yukawa/Higgs/QCD/nuclear binding ownership or numeric coefficient provenance",
        },
        {
            **base,
            "theorem_id": "CST3648_3_clock_transitions",
            "claim": "Clock rows inherit alpha, mass, nuclear, and readout debts.",
            "mathematical_form": "b_clock_i = K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + b_readout_i.",
            "derivation_step": "Clock transition silence follows only after upstream constants and readout frame are theorem-zero or sourced.",
            "result": "Clock sensitivities are useful anchors, not a zero proof.",
            "status": "CLOCK_THEOREM_INHERITS_CONSTANT_DEBT",
            "missing_for_claim": "full sensitivity matrix, upstream coefficient rows, local dXhat projection, and clock readout lock",
        },
        {
            **base,
            "theorem_id": "CST3648_4_material_markers",
            "claim": "Material/species labels cannot carry hidden X_N dependence.",
            "mathematical_form": "Lie_vX material_label_A=0 and Lie_vX S_A=0, or material sensitivity rows must be retained.",
            "derivation_step": "Species/material markers are either fixed representation data or explicit residual source charges.",
            "result": "Composition/WEP and R10 material-response rows remain live.",
            "status": "MATERIAL_MARKER_ZERO_UNSIGNED",
            "missing_for_claim": "species/source marker exclusion theorem or material sensitivity matrix",
        },
        {
            **base,
            "theorem_id": "CST3648_5_verdict",
            "claim": "Current MTS proves constant/marker superselection.",
            "mathematical_form": "CST3648_0 through CST3648_4 parent-signed in one branch => qbar_constants_abs=0.",
            "derivation_step": "All hidden alpha, mass, clock, marker, and readout vertices must be excluded together.",
            "result": "The theorem is clean but unsigned; coefficient rows are required.",
            "status": "FAIL_CURRENT_CLAIM_COEFFICIENT_ROWS_REQUIRED",
            "missing_for_claim": "parent no-extra-F2, no-mass-vertex, no-clock-readout-vertex, and no-marker signatures",
        },
    ]


def audit_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}
    specs = [
        ("CMA3648_0_alpha_EM", "alpha_EM/gauge kinetic normalization", "dimensionless fine-structure/gauge coupling can vary through f_X F^2 or readout normalization", "b_alpha", "clock;EM spectra;WEP;R10;EM_Maxwell_stress", "MISSING_ALPHA_OWNER_OR_B_ALPHA"),
        ("CMA3648_1_mass_ratio", "particle masses and mass ratios", "dimensionless ratios and binding fractions cannot be removed by unit choice", "b_mu;b_mA", "clock;WEP;composition;R10", "MISSING_MATTER_SPECTRUM_OWNER_OR_B_MASS"),
        ("CMA3648_2_nuclear_binding", "nuclear/EM binding fractions", "material-dependent binding creates composition-dependent source charge", "b_nuc;b_binding", "WEP;composition;R10", "MISSING_BINDING_SENSITIVITY_ROWS"),
        ("CMA3648_3_clock", "clock transitions and clock ratios", "clock sensitivity rows project upstream constants into observed frequency ratios", "b_clock_i", "clock;redshift;alpha drift", "MISSING_CLOCK_PROJECTION"),
        ("CMA3648_4_material_marker", "material/species/source markers", "species or preparation labels can source X_N even with public metric", "b_material;S_A", "WEP;composition;source_test_R10", "MISSING_NO_MARKER_THEOREM_OR_SENSITIVITIES"),
        ("CMA3648_5_source_weight", "source-only weights and abundance maps", "source leg can carry marker dependence independent of test readout", "q_source_weight", "R10;GM calibration;orbital", "MISSING_SOURCE_WEIGHT_LOCK"),
        ("CMA3648_6_total", "qbar_constants_abs", "absolute envelope over all constant/material leakage", "qbar_constants_abs", "all_local_arenas", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            **base,
            "audit_id": aid,
            "object": obj,
            "why_dangerous": why,
            "fallback_symbol": symbol,
            "observable_links": links,
            "current_status": status,
        }
        for aid, obj, why, symbol, links, status in specs
    ]


def coefficient_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    specs = [
        ("CP3648_0_b_alpha", "b_alpha", "vertical derivative d ln alpha_EM/dXhat or equivalent gauge kinetic/readout derivative", "Xhat^-1 or dimensionless per normalized Xhat", "no-extra-F2 theorem or numeric/source-backed b_alpha", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM", "clock;EM spectra;WEP;R10;EM_Maxwell_stress"),
        ("CP3648_1_b_mu", "b_mu", "vertical derivative of dimensionless mass ratios such as m_e/m_p", "Xhat^-1", "matter spectrum theorem or numeric/source-backed b_mu", "MISSING_B_MU_OR_PARENT_ZERO_THEOREM", "clock;WEP;composition"),
        ("CP3648_2_b_mA", "b_mA", "vertical derivative of material/species mass or binding constants", "Xhat^-1", "species/material row, sensitivity, source path", "MISSING_B_MA_OR_MATERIAL_SENSITIVITY", "WEP;composition;R10"),
        ("CP3648_3_b_nuc", "b_nuc;b_binding", "vertical derivative of nuclear/EM binding fractions", "Xhat^-1", "binding model, material fractions, source path", "MISSING_BINDING_COEFFICIENTS", "WEP;clock;composition"),
        ("CP3648_4_b_clock", "b_clock_i", "vertical derivative of a clock transition or clock ratio after sensitivity projection", "Xhat^-1", "K_alpha,K_mu,K_nuc matrix; upstream b rows; clock source", "MISSING_CLOCK_CONSTANT_PROJECTION", "clock;redshift;alpha drift"),
        ("CP3648_5_sensitivities", "S_A;S_alpha;S_clock;f_binding", "material/clock sensitivity vector multiplying constant coefficients", "dimensionless", "material pair, clock pair, source/test body, source path", "MISSING_SENSITIVITY_VECTOR", "WEP;clock;R10;composition"),
        ("CP3648_6_qbar_constants", "qbar_constants_abs", "|qbar_constants| <= |S_alpha b_alpha|+|S_mu b_mu|+|S_A b_mA|+|S_nuc b_nuc|+|b_clock_i|+|q_source_weight|", "dimensionless source/readout charge", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **base,
            "row_id": rid,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
        }
        for rid, symbol, definition, units, required, status, links in specs
    ]


def projection_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "score_ready": False}
    specs = [
        ("OP3648_0_clock_alpha", "clock_alpha_sensitivity", "d ln R_clock = DeltaK_alpha b_alpha dXhat + DeltaK_mu b_mu dXhat + DeltaK_nuc b_nuc dXhat + ...", "clock sensitivity rows; b_alpha;b_mu;b_nuc;local dXhat", "SENSITIVITIES_AVAILABLE_MTS_PROJECTION_MISSING"),
        ("OP3648_1_clock_redshift", "clock_redshift_LPI", "alpha_clock_redshift constrains full clock/readout residual, not b_alpha alone", "clock residual map; local profile/time projection; redshift bound", "ANCHOR_AVAILABLE_CLOCK_MAP_MISSING"),
        ("OP3648_2_WEP", "WEP_composition", "eta_AB receives differential material response from S_alpha b_alpha + S_mu b_mu + S_A b_mA + binding terms", "composition matrix; source/test body; WEP bound; no-cancellation envelope", "ANCHOR_AVAILABLE_COMPOSITION_MATRIX_MISSING"),
        ("OP3648_3_R10", "R10_short_range", "alpha_X(lambda) receives K_X Qbar_XH qbar_constants_abs plus frame/source tails", "lambda_X;K_X;Qbar_XH;qbar_constants_abs;R10 curve", "BOUND_AND_MTS_COMPONENTS_NOT_CLAIM_READY"),
        ("OP3648_4_EM_stress", "EM_Maxwell_stress", "Maxwell stress is same-frame only if alpha_EM/gauge kinetic normalization is theorem-owned; finite b_alpha feeds EM stress and clocks", "unique F^2 norm; no f_XF^2; b_alpha;Hodge/readout", "EM_THEOREM_OR_B_ALPHA_ROW_REQUIRED"),
        ("OP3648_5_PPN_source", "PPN_source_calibration", "constant/source marker drift can enter measured GM, source normalization, and PPN residual vector", "source measure;GM calibration;PPN projection matrix", "NOT_SCORE_READY"),
        ("OP3648_6_total_guard", "all_local_arenas", "no cancellation between alpha, mass, clock, material, frame, non-Hilbert, or boundary components", "all component rows;source paths;units", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        {
            **base,
            "projection_id": pid,
            "arena": arena,
            "projection_law": law,
            "required_inputs": required,
            "current_status": status,
        }
        for pid, arena, law, required, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "decision_id": "DEC3648_0_theorem_shape",
            "decision": "No-marker constant superselection is a clean chain-rule theorem if constants are fixed representation data or quotient-owned.",
            "status": "CONSTANT_SUPERSELECTION_THEOREM_SHAPE_EXACT",
        },
        {
            **base,
            "decision_id": "DEC3648_1_current_verdict",
            "decision": "Current MTS cannot claim b_alpha, b_mass, or b_clock vanish because no-extra-F2, no-mass-vertex, and no-clock-readout signatures are unsigned.",
            "status": "PARENT_CONSTANT_SIGNATURE_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3648_2_coefficients",
            "decision": "b_alpha, b_mu, b_mA, b_nuc, b_clock_i, and sensitivity rows are retained as nonclaim rows.",
            "status": "CONSTANT_COEFFICIENT_ROWS_CREATED_NOT_SCORE_READY",
        },
        {
            **base,
            "decision_id": "DEC3648_3_next",
            "decision": "Next target should attack EM/Maxwell specifically: unique F^2 normalization and no f_X(X)F^2 counterterm, or b_alpha remains live.",
            "status": "EM_MAXWELL_STRESS_OR_FEM_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "CONSTANT_SUPERSELECTION_CONDITIONAL_COEFFICIENT_ROWS_CREATED",
            "summary": "3648 consolidates the no-marker constant-superselection theorem, rejects current zero-claim status for alpha_EM/mass/clock/material channels, and creates explicit b_alpha, b_mu, b_mA, b_nuc, b_clock, sensitivity, and qbar_constants rows.",
            "claim_ceiling": "no b_alpha=0, b_mass=0, b_clock=0, qbar_constants=0, local-GR/Newton, R10, PPN, clock, WEP, orbital, or EM stress pass is claimed",
            "useful_result": "the next concrete bridge is EM/Maxwell: prove unique F^2/no f_XF^2 or keep b_alpha as a live stress/source coefficient",
            "valid_for_claim": False,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3648_0",
            "target_doc": "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_3649_EM_Maxwell_same_frame_stress_or_fEM_coefficient_row.py",
            "objective": "prove the EM/gauge sector uses the quotient observed frame with unique Maxwell F^2 normalization and no f_X(X_N)F^2 or optical-frame counterterm; if unsigned, create f_EM/b_alpha EM-stress coefficient rows",
            "success_gate": "either Maxwell/EM same-frame stress is parent-signed, or f_EM/b_alpha rows have units, source paths, clock/EM/WEP projections, and no-cancellation guards",
            "valid_for_claim": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_doc(src, theorem, audit, coefficients, projections, decisions, status, nxt) -> None:
    lines = [
        "# 3648 Y5 R2FR no-marker constant superselection or alphaEM mass clock coefficient row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "**Claim ceiling:** no constant-zero, local-GR/Newton, R10, PPN, clock, WEP, orbital, or EM stress pass is claimed.",
        "",
        "## Main result",
        "",
        "The clean route is exact: if every ordinary-matter constant or marker `theta_I` is fixed representation data or factors through `q`, then `Dq[v_X]=0` gives `Lie_vX theta_I=0`. That would set `b_alpha`, mass-ratio coefficients, clock coefficients, and material-marker charge to zero.",
        "",
        "Current MTS does not yet parent-sign the no-extra-F2, no-mass-vertex, no-clock-readout, and no-marker clauses. The coefficient rows therefore stay live and nonclaim.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} — {row['result']}")
    lines.extend(["", "## Constant/marker audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: `{row['fallback_symbol']}` — {row['current_status']} ({row['observable_links']})")
    lines.extend(["", "## Coefficient rows"])
    for row in coefficients:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Observable projections"])
    for row in projections:
        lines.append(f"- `{row['projection_id']}`: `{row['arena']}` — {row['current_status']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} — {row['decision']}")
    lines.extend(["", "## Next target", "", f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.", "", "## Sources"])
    for row in src:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['source_exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(out: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    ts = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append({"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "validation_id": validation_id, "result": "PASS" if ok else "FAIL", "detail": detail})

    add("VAL3648_0_sources_exist", all(bool(row["source_exists"]) for row in src), "all source paths exist")
    add("VAL3648_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3648_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all outputs and doc written")

    parsed: dict[str, list[dict[str, str]]] = {}
    parse_ok = True
    counts = []
    for name, path in pre.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            parsed[name] = read_csv(path)
            counts.append(f"{name}:{len(parsed[name])}")
        except Exception as exc:  # pragma: no cover
            parse_ok = False
            counts.append(f"{name}:ERR:{exc}")
    add("VAL3648_3_csv_parse", parse_ok, "; ".join(counts))

    theorem = parsed["theorem"]
    audit = parsed["audit"]
    coeffs = parsed["coefficients"]
    projections = parsed["projections"]
    decisions = parsed["decisions"]
    status = parsed["status"]
    nxt = parsed["next_target"]
    groups = [theorem, audit, coeffs, projections, decisions, status, nxt]

    add("VAL3648_4_theorem_zero_shape", any("b_alpha=b_mass=b_clock=b_material=0" in row["result"] for row in theorem), "constant zero theorem shape present")
    add("VAL3648_5_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_COEFFICIENT_ROWS_REQUIRED" for row in theorem), "constant zero not claimed")
    required_audit = {"b_alpha", "b_mu;b_mA", "b_nuc;b_binding", "b_clock_i", "b_material;S_A", "qbar_constants_abs"}
    add("VAL3648_6_audit_complete", required_audit.issubset({row["fallback_symbol"] for row in audit}), "alpha, mass, binding, clock, material, and total audit rows present")
    required_coeffs = {"b_alpha", "b_mu", "b_mA", "b_nuc;b_binding", "b_clock_i", "S_A;S_alpha;S_clock;f_binding", "qbar_constants_abs"}
    add("VAL3648_7_coeff_rows_complete", required_coeffs.issubset({row["symbol"] for row in coeffs}), "constant coefficient rows complete")
    required_proj = {"clock_alpha_sensitivity", "clock_redshift_LPI", "WEP_composition", "R10_short_range", "EM_Maxwell_stress", "PPN_source_calibration"}
    add("VAL3648_8_projection_rows_complete", required_proj.issubset({row["arena"] for row in projections}), "clock, WEP, R10, EM, and PPN/source projections present")
    add("VAL3648_9_no_score_ready", all(row.get("score_ready", "False").lower() == "false" for table in [coeffs, projections] for row in table), "coefficient/projection rows refuse scoring")
    add("VAL3648_10_nonclaim_all_outputs", all(row.get("valid_for_claim", "False").lower() == "false" for table in groups for row in table), "all generated rows remain nonclaim")
    add("VAL3648_11_decision_next", any(row["status"] == "EM_MAXWELL_STRESS_OR_FEM_NEXT" for row in decisions), "EM/Maxwell target selected next")
    add("VAL3648_12_next_target_written", bool(nxt) and "3649" in nxt[0]["target_doc"], "3649 target written")
    add("VAL3648_13_status_honest", status[0]["status"] == "CONSTANT_SUPERSELECTION_CONDITIONAL_COEFFICIENT_ROWS_CREATED", "status keeps constant theorem conditional")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3648_14_doc_written", "b_alpha" in doc_text and "no-extra-F2" in doc_text and "coefficient rows therefore stay live" in doc_text, "doc records b_alpha/no-extra-F2 caveat")
    leak_patterns = ["*Y5_R2FR_3648*", "3648-Y5-R2FR-*", "Y5_R2FR_3648_*"]
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3648_15_no_formalization_leak", not leaks, "no 3648 checkpoint files in formalization-workbench")
    add("VAL3648_16_em_bridge", any(row["arena"] == "EM_Maxwell_stress" for row in projections), "EM/Maxwell bridge included")
    add("VAL3648_17_no_cancellation_guard", any(row["symbol"] == "qbar_constants_abs" and "S_alpha b_alpha" in row["definition"] for row in coeffs), "absolute constants envelope present")
    return rows


def main() -> None:
    ts = now()
    out = outputs()
    src = source_register(ts)
    theorem = theorem_rows(ts)
    audit = audit_rows(ts)
    coeffs = coefficient_rows(ts)
    projections = projection_rows(ts)
    decisions = decision_rows(ts)
    status = status_rows(ts)
    nxt = next_target_rows(ts)

    write_csv(out["source_register"], src)
    write_csv(out["theorem"], theorem)
    write_csv(out["audit"], audit)
    write_csv(out["coefficients"], coeffs)
    write_csv(out["projections"], projections)
    write_csv(out["decisions"], decisions)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, theorem, audit, coeffs, projections, decisions, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3648 validation failed: {failures}")
    print(f"wrote 3648 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
