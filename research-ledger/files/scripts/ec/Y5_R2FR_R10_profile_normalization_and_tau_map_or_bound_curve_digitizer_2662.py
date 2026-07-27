from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2662"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2662-Y5-R2FR-R10-profile-normalization-and-tau-map-or-bound-curve-digitizer.md"

CHECKPOINT = "2662"
BRANCH_ID = "Y5_R2FR_R10_PROFILE_TAU_MAP_2662"
PARENT_BRANCH = "Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661"
PREFIX = "P8_Y5_R10_TAU_PROFILE_2662"
MISSING_TOKENS = ("MISSING", "UNSIGNED", "PLACEHOLDER", "NOT_DERIVED", "ANCHOR_ONLY")

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "tau_profile_derivation": RESIDUALS / f"{PREFIX}_TAU_PROFILE_DERIVATION.csv",
    "tau_identity_gate": RESIDUALS / f"{PREFIX}_TAU_IDENTITY_GATE.csv",
    "profile_template": RESIDUALS / f"{PREFIX}_PROFILE_NORMALIZATION_TEMPLATE_NONCLAIM.csv",
    "bound_curve_route": RESIDUALS / f"{PREFIX}_BOUND_CURVE_ROUTE_LEDGER.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_PROFILE_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2662_R10_PROFILE_TAU_INPUT_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "R10_tau_profile_map_2662_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "R10_PROFILE_TAU_MAP_2662_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2662_R10_PROFILE_TEMPLATE.csv",
    "quarantine": QUARANTINE / "P8_Y5_2662_PROFILE_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2661_doc": {
        "path": ROOT / "2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md",
        "needles": ["R10P2661_0_formula", "NEXT2661_0_selected", "VAL2661_OVERALL"],
        "role": "immediate handoff selecting R10 profile normalization and tau map",
    },
    "2660_doc": {
        "path": ROOT / "2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md",
        "needles": ["APM2660_0_R10", "ENV2660_0_R10", "VAL2660_OVERALL"],
        "role": "coupling vector R10 component and no-cancellation envelope",
    },
    "947_doc": {
        "path": ROOT / "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
        "needles": ["PFA947_0_R10_projection", "BI947_0_cg_R10", "V947_4_R10_projection_blocked"],
        "role": "prior projection attempt showing tau_R10 and parent coefficients missing",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["PHA1025_7_prefactor", "ASR1025_3_Hamiltonian_projection", "DEC1025_3_coupling"],
        "role": "alpha prefactor, Qbar_XH projection and coupling normalization gap",
    },
    "1048_doc": {
        "path": ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
        "needles": ["BM1048_3_R10_yukawa", "REF1048_1_bound_matrix", "CG1048"],
        "role": "R10 source/test charge projection through alpha/mass/clock matrix",
    },
    "563_doc": {
        "path": ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "needles": ["R10_RUNNER_563_ANCHOR_SMOKE_RECHECK", "B563_1_no_numeric_MTS_alpha", "V563_10_no_overclaim"],
        "role": "anchor-only noncurve data and symbolic MTS alpha blocker",
    },
    "437_doc": {
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needles": ["C10_2_bound_match", "R10_template_written", "claim_ceiling_enforced"],
        "role": "R10 alpha(lambda) executable curve contract",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(row: dict[str, Any]) -> bool:
    joined = " ".join(str(value) for value in row.values())
    return any(token in joined for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2662_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def tau_profile_derivation_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "derivation_id": "TAU2662_0_target",
            "object": "tau_R10(lambda)",
            "statement": "tau_R10 is the same-convention map from the parent X-channel force kernel and source/test charge profiles into the empirical Yukawa alpha(lambda) convention.",
            "derived_form": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10(lambda) c_g + alpha_tail_abs(lambda)",
            "status": "TARGET_SHARP",
            "missing_for_claim": "source/test charge profiles, readout kernel, geometry convention, K_X, Qbar_XH, c_g and tail envelope",
        },
        {
            "derivation_id": "TAU2662_1_point_kernel",
            "object": "point-source Yukawa normalization",
            "statement": "For a parent scalar kernel G_X(r)=exp(-r/lambda)/(4*pi*Z_X*r), the point-pair force has the same radial Yukawa shape as the standard alpha(lambda) comparator.",
            "derived_form": "alpha_point(lambda)=Q_source_X Q_test_X/(4*pi*Z_X*G_obs*M_source*M_test) under the same mass/charge normalization",
            "status": "EXACT_CONDITIONAL_KERNEL_FORM",
            "missing_for_claim": "source/test charges and Z_X/G_obs same-frame normalization",
        },
        {
            "derivation_id": "TAU2662_2_extended_profile",
            "object": "extended source/test profile functional",
            "statement": "For extended bodies, the point-pair kernel must be folded through the same source density, test density and readout weighting used by the experimental alpha(lambda) bound.",
            "derived_form": "tau_R10(lambda)=I_MTS_X(lambda;rho_s,rho_t,W_readout)/I_unit_Yukawa(lambda;rho_s,rho_t,W_readout)",
            "status": "DERIVED_SYMBOLIC_PROFILE_FUNCTIONAL",
            "missing_for_claim": "rho_s, rho_t, W_readout, geometry/separation modulation and unit-Yukawa denominator",
        },
        {
            "derivation_id": "TAU2662_3_bound_convention",
            "object": "external bound convention match",
            "statement": "The alpha(lambda) bound is claim-usable only when the MTS projection is expressed in the same Yukawa potential and finite-geometry convention as the published bound curve.",
            "derived_form": "alpha_MTS(lambda) is comparable iff force_law_form, lambda units, source/test normalization and geometry folding match the bound curve contract",
            "status": "CONVENTION_MATCH_REQUIRED",
            "missing_for_claim": "full claim-valid alpha(lambda) curve and experiment geometry convention",
        },
        {
            "derivation_id": "TAU2662_4_tau_identity_conditions",
            "object": "tau_R10=1 shortcut",
            "statement": "tau_R10=1 is allowed only in a signed point-pair/same-profile limit where MTS and the published unit-Yukawa kernel use identical source/test weighting and readout normalization.",
            "derived_form": "tau_R10=1 iff I_MTS_X/I_unit_Yukawa=1 after Qbar and K_X normalization are already fixed",
            "status": "CONDITIONAL_IDENTITY_NOT_ACTIVE",
            "missing_for_claim": "identity conditions are not parent-signed or experiment-sourced",
        },
        {
            "derivation_id": "TAU2662_5_verdict",
            "object": "R10 tau/profile map",
            "statement": "The tau/profile map is derived as a symbolic functional, but no numeric or theorem-zero R10 projection is produced.",
            "derived_form": "R10 projection remains nonclaim until the profile functional is evaluated or collapsed by signed identity conditions",
            "status": "TAU_R10_PROFILE_MAP_DERIVED_SYMBOLIC_NOT_NUMERIC",
            "missing_for_claim": "numeric geometry/source/test/readout inputs or parent-signed tau identity conditions",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def tau_identity_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("ID2662_0_same_kernel", "MTS finite-range kernel exactly matches standard Yukawa kernel", "CONDITIONAL_FORM_ONLY", False),
        ("ID2662_1_mass_proportional_charge", "source/test X charge densities are proportional to the mass densities used by the bound convention", "MISSING_SOURCE_TEST_CHARGE_NORMALIZATION", False),
        ("ID2662_2_same_geometry", "same extended-body geometry and readout weighting as alpha(lambda) bound", "MISSING_EXPERIMENT_GEOMETRY_TRANSFER", False),
        ("ID2662_3_same_normalization", "K_X, Qbar_XH, c_g and G_obs normalization already fixed in the same frame", "MISSING_PARENT_NORMALIZATION", False),
        ("ID2662_4_no_tail", "alpha_tail_abs(lambda)=0 by theorem or source-backed negligible bound", "MISSING_TAIL_ZERO_OR_BOUND", False),
        ("ID2662_5_tau_one_verdict", "tau_R10=1 may be used for claim scoring", "TAU_ONE_SHORTCUT_FORBIDDEN", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "condition": condition,
            "status": status,
            "gate_pass": gate_pass,
            "blocks_tau_one": not gate_pass,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, condition, status, gate_pass in rows
    ]


def profile_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "template_id": "PROF2662_0_R10_unit_yukawa",
            "system_id": "R10_source_test_profile",
            "lambda_value": "MISSING_LAMBDA_GRID",
            "lambda_units": "m",
            "source_profile": "MISSING_RHO_SOURCE_AND_GEOMETRY",
            "test_profile": "MISSING_RHO_TEST_AND_GEOMETRY",
            "readout_kernel": "MISSING_W_READOUT",
            "unit_yukawa_denominator": "I_unit_Yukawa(lambda;rho_s,rho_t,W_readout)",
            "mts_kernel_numerator": "I_MTS_X(lambda;rho_s,rho_t,W_readout)",
            "tau_R10_formula": "I_MTS_X/I_unit_Yukawa",
            "K_X_formula": "MISSING_K_X_OR_THEOREM_ZERO",
            "Qbar_XH_formula": "MISSING_QBAR_XH_OR_THEOREM_ZERO",
            "c_g_status": "MISSING_C_G_OR_VISIBLE_DOMAIN_ZERO",
            "tail_policy": "absolute_tail_required_no_cancellation",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "Template only; evaluates the same-convention profile functional once real geometry/profile inputs exist.",
        },
        {
            "template_id": "PROF2662_1_point_pair_limit",
            "system_id": "R10_point_pair_limit",
            "lambda_value": "MISSING_LAMBDA_GRID",
            "lambda_units": "m",
            "source_profile": "point_source_only_if_bound_convention_matches",
            "test_profile": "point_test_only_if_bound_convention_matches",
            "readout_kernel": "ideal_pair_separation_r",
            "unit_yukawa_denominator": "exp(-r/lambda)/r",
            "mts_kernel_numerator": "exp(-r/lambda)/(4*pi*Z_X*r)",
            "tau_R10_formula": "1 only after K_X/Qbar/c_g normalization absorbs 1/(4*pi*Z_X) and charge-to-mass ratios",
            "K_X_formula": "MISSING_NORMALIZATION",
            "Qbar_XH_formula": "MISSING_SOURCE_CHARGE",
            "c_g_status": "MISSING_C_G_OR_VISIBLE_DOMAIN_ZERO",
            "tail_policy": "absolute_tail_required_no_cancellation",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "Analytic limit for checking algebra, not a claim route for real R10 geometry.",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def bound_curve_route_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "route_id": "BCR2662_0_anchor_status",
            "route": "existing anchor rows",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "why": "useful for smoke/unit checks but not a full alpha(lambda) curve",
            "next_action": "keep nonclaim",
        },
        {
            "route_id": "BCR2662_1_full_curve",
            "route": "digitize/import full R10 alpha(lambda) curve",
            "status": "DEFER_UNTIL_PROFILE_MAP_HAS_INPUTS",
            "why": "a full curve still cannot score without tau_R10, K_X, Qbar_XH, c_g and tails",
            "next_action": "return after profile/source normalization rows exist",
        },
        {
            "route_id": "BCR2662_2_claim_condition",
            "route": "claim-valid R10 comparison",
            "status": "BLOCKED",
            "why": "requires both MTS alpha(lambda) rows and bound rows with valid_for_claim=true",
            "next_action": "no R10 pass claim",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def runner_results_rows(profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in profile_rows:
        missing = has_missing(row)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2662_{row['template_id'].split('_')[-1]}",
                "template_id": row["template_id"],
                "has_missing_markers": missing,
                "score_ready": False,
                "runner_status": "REJECTED_MISSING_PROFILE_OR_NORMALIZATION" if missing else "READY_NONCLAIM",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2662_0_tau_map", "tau_R10 profile functional is numeric or theorem-collapsed", "FAIL_SYMBOLIC_ONLY", "TAU2662_5_verdict"),
        ("CG2662_1_tau_one", "tau_R10=1 shortcut is legal", "FAIL_TAU_ONE_SHORTCUT_FORBIDDEN", "ID2662_5_tau_one_verdict"),
        ("CG2662_2_profile_inputs", "R10 source/test/readout profile inputs exist", "FAIL_PROFILE_INPUTS_MISSING", "PROF2662 rows"),
        ("CG2662_3_bound_curve", "claim-valid full alpha(lambda) bound curve exists", "FAIL_FULL_CURVE_DEFERRED", "BCR2662_1_full_curve"),
        ("CG2662_4_verdict", "R10 projection can be scored or claimed", "CLAIM_BLOCKED", "symbolic tau map; missing profile inputs; anchor-only bound rows"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2662_0_tau_status",
            "decision": "tau_R10 is derived as a profile functional, not a number",
            "reason": "the same-convention geometry/readout/source profiles are missing",
            "next_action": "source or derive Qbar/source-test profile normalization",
        },
        {
            "decision_id": "DEC2662_1_tau_one_policy",
            "decision": "tau_R10=1 remains forbidden for claims",
            "reason": "identity conditions are not parent-signed or experiment-sourced",
            "next_action": "use the profile functional or prove every identity condition",
        },
        {
            "decision_id": "DEC2662_2_bound_curve_policy",
            "decision": "full bound curve digitization is useful but not first priority",
            "reason": "MTS-side projection factors are still symbolic",
            "next_action": "fill source/test charge normalization and K_X/Qbar_XH before curve digitization",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2662_0_selected",
            "status": "selected",
            "next_doc": "2663-Y5-R2FR-R10-source-test-charge-normalization-or-QbarXH-source-row.md",
            "next_script": "scripts/Y5_R2FR_R10_source_test_charge_normalization_or_QbarXH_source_row_2663.py",
            "task": "derive/source the source-test charge normalization feeding K_X(lambda), Qbar_XH and the tau_R10 profile functional",
            "must_include": "source density, test density, charge-to-mass normalization, Qbar_XH, K_X, Z_X/G_obs frame, visible-domain zero switch, no-cancellation tail policy",
            "must_exclude": "tau=1 shortcut, point-pair limit as real experiment, alpha=1 anchor as full curve, invented c_g or Qbar values, R10 pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2662_0_progress", "R10 tau/profile", "SYMBOLIC_FUNCTIONAL_DERIVED", "tau_R10 is now an explicit same-convention profile functional, not a free knob"),
        ("STAT2662_1_claim", "R10 claim status", "BLOCKED_NONCLAIM", "no numeric tau/profile factors or full claim-valid bound curve exist"),
        ("STAT2662_2_best_next", "next route", "SOURCE_TEST_CHARGE_NORMALIZATION", "Qbar_XH/K_X/source-test normalization is the next useful MTS-side input"),
        ("STAT2662_3_project", "local GR route", "TEST_PIPELINE_TIGHTER_NOT_CLOSED", "the R10 lane is becoming executable while the GR reduction claim remains blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["profile_template"], BRANCH_COPIES["queue"], "R10 profile/tau input queue"),
        "local_bounds": (OUTPUTS["tau_profile_derivation"], BRANCH_COPIES["local_bounds"], "R10 tau profile derivation"),
        "source_weight": (OUTPUTS["tau_identity_gate"], BRANCH_COPIES["source_weight"], "tau identity gate"),
        "microscope": (OUTPUTS["profile_template"], BRANCH_COPIES["microscope"], "profile template copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "profile runner refusal results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2662_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2662-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2662*",
        "*Y5_R2FR_R10_profile_normalization_and_tau_map_or_bound_curve_digitizer_2662*",
        "*JR2662*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    tau_ok = any(row["derivation_id"] == "TAU2662_5_verdict" and row["status"] == "TAU_R10_PROFILE_MAP_DERIVED_SYMBOLIC_NOT_NUMERIC" for row in rows["tau_profile_derivation"])
    identity_ok = any(row["gate_id"] == "ID2662_5_tau_one_verdict" and row["status"] == "TAU_ONE_SHORTCUT_FORBIDDEN" for row in rows["tau_identity_gate"]) and all(not row["gate_pass"] for row in rows["tau_identity_gate"])
    template_ok = len(rows["profile_template"]) == 2 and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["profile_template"])
    runner_ok = len(rows["runner_results"]) == len(rows["profile_template"]) and all(row["runner_status"] == "REJECTED_MISSING_PROFILE_OR_NORMALIZATION" for row in rows["runner_results"])
    bound_ok = any(row["route_id"] == "BCR2662_1_full_curve" and row["status"] == "DEFER_UNTIL_PROFILE_MAP_HAS_INPUTS" for row in rows["bound_curve_route"])
    claim_ok = any(row["gate_id"] == "CG2662_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2663-Y5-R2FR-R10-source-test-charge-normalization" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2662_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2662_01_tau_functional", tau_ok, "tau_R10 profile map is derived symbolically but not numeric"),
        ("VAL2662_02_tau_one_guard", identity_ok, "tau=1 shortcut is forbidden unless all identity gates close"),
        ("VAL2662_03_template", template_ok, "profile templates are staged as nonclaim rows"),
        ("VAL2662_04_runner_refuses", runner_ok, "profile runner refuses missing inputs"),
        ("VAL2662_05_bound_route", bound_ok, "full bound curve is deferred until MTS-side profile factors exist"),
        ("VAL2662_06_claim_gates_blocked", claim_ok, "claim gates block R10 scoring"),
        ("VAL2662_07_next_target", next_ok, "2663 source/test charge normalization target selected"),
        ("VAL2662_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2662_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2662_10_formalization_untouched", formal_ok, "no 2662 outputs are written under formalization-workbench"),
        ("VAL2662_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2662_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2662 derives a symbolic same-convention R10 tau/profile functional, forbids tau=1 shortcut, defers full curve digitization, and selects source-test charge normalization next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2662 - R10 Profile Normalization And Tau Map Or Bound Curve Digitizer

## Purpose

This checkpoint derives the R10 profile/tau map far enough to stop treating `tau_R10` as a free knob. It also decides whether a full bound-curve digitizer should happen now or after the MTS-side projection factors are sourced.

## Result

- `tau_R10(lambda)` is now an explicit same-convention profile functional: `I_MTS_X/I_unit_Yukawa`.
- The point-pair Yukawa algebra is clean, but real R10 scoring needs the extended source/test geometry and readout convention.
- `tau_R10=1` is forbidden unless the same-kernel, same-charge, same-geometry, same-normalization and no-tail gates are all signed.
- Full external bound-curve digitization is deferred: without `K_X`, `Qbar_XH`, `c_g` and the tau/profile inputs, a full curve still cannot score MTS.

## Source Register

{markdown_table(rows["source_register"])}

## Tau/Profile Derivation

{markdown_table(rows["tau_profile_derivation"])}

## Tau Identity Gate

{markdown_table(rows["tau_identity_gate"])}

## Profile Normalization Template

{markdown_table(rows["profile_template"])}

## Bound Curve Route Ledger

{markdown_table(rows["bound_curve_route"])}

## Profile Runner Results

{markdown_table(rows["runner_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "tau_profile_derivation": tau_profile_derivation_rows(),
        "tau_identity_gate": tau_identity_gate_rows(),
        "profile_template": profile_template_rows(),
        "bound_curve_route": bound_curve_route_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["profile_template"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
