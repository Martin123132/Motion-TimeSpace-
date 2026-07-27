from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3644"
BRANCH_ID = "MTS_R2FR_Y5_PROFILE_SOURCE_OWNER_OR_FIRST_AMPLITUDE_PRIOR_3644"
DOC = ROOT / "3644-Y5-R2FR-profile-source-owner-or-first-amplitude-prior.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3644_SOURCE_REGISTER.csv",
        "source_owner_audit": RESIDUALS / "P8_Y5_R2FR_3644_PROFILE_SOURCE_OWNER_AUDIT.csv",
        "operator_prior_rows": RESIDUALS / "P8_Y5_R2FR_3644_OPERATOR_RANGE_PRIOR_ROWS.csv",
        "amplitude_prior_rows": RESIDUALS / "P8_Y5_R2FR_3644_AMPLITUDE_PRIOR_ROWS.csv",
        "runner_schema": RESIDUALS / "P8_Y5_R2FR_3644_PROFILE_RUNNER_SCHEMA.csv",
        "decision": RESIDUALS / "P8_Y5_R2FR_3644_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3644_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3644_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3644_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    specs = [
        ("next_3643", RESIDUALS / "P8_Y5_R2FR_3643_NEXT_TARGET.csv", "A_X components are parent-zero/owned", "3643 handoff to profile source owner or amplitude prior"),
        ("amp_3643", RESIDUALS / "P8_Y5_R2FR_3643_XN_AMPLITUDE_RANGE_PROFILE_ROWS.csv", "A_X=A_src+A_bdy+A_top+A_proj+A_shell", "3643 amplitude decomposition"),
        ("premise_3643", RESIDUALS / "P8_Y5_R2FR_3643_NOHAIR_PREMISE_AUDIT.csv", "MISSING_PARENT_OPERATOR_OWNERSHIP", "3643 missing premise audit"),
        ("bounds_3643", RESIDUALS / "P8_Y5_R2FR_3643_PROFILE_BOUND_UPDATE_ROWS.csv", "BOUND_UPDATED_WITH_AMPLITUDE_ROW", "3643 bound updates"),
        ("hessian_1025", RESIDUALS / "P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv", "PHA1025_1_ZX_positive", "1025 Hessian sign/ownership audit"),
        ("second_variation_1025", RESIDUALS / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv", "SV1025_3_range_relation", "1025 local X block and range relation"),
        ("alpha_template_1025", RESIDUALS / "P8_Y5_R10_1025_ALPHA_SOURCE_ROW_TEMPLATE.csv", "ASR1025_0_bulk_Hessian", "1025 source row template for Z_X/M_X2/lambda"),
        ("parent_x_1036", RESIDUALS / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv", "PX1036_3_source_current", "1036 parent X action/source current audit"),
        ("beta_split_1036", RESIDUALS / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv", "BETA1036_1_two_body_exchange", "1036 source/test exchange law"),
        ("beta_template_1037", RESIDUALS / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv", "BB1037_7_beta_product_guard", "1037 bounded beta source/test fallback"),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
            "valid_for_claim": False,
        }
        for source_id, path, needle, role in specs
    ]


def owner_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    specs = [
        ("OWN3644_0_operator_DX", "D_X", "coefficient of exterior gradient term in parent second variation", "parent Hessian in same X_N normalization", "MISSING_PARENT_KINETIC_RESIDUE"),
        ("OWN3644_1_operator_MX2", "M_X^2", "coefficient of local potential/curvature term in parent second variation", "parent Hessian mass gap in same X_N normalization", "MISSING_PARENT_MASS_GAP"),
        ("OWN3644_2_range_ellX", "ell_X", "sqrt(D_X/M_X^2) when D_X>0,M_X^2>0", "same-branch D_X and M_X^2 with SI length conversion", "RELATION_DERIVED_VALUES_MISSING"),
        ("OWN3644_3_source_Asrc", "A_src", "Green-kernel integral of J_X^eff over compact source", "parent source current J_X^eff including matter/hidden/domain terms", "MISSING_SOURCE_CURRENT_OWNER"),
        ("OWN3644_4_boundary_Abdy", "A_bdy", "exterior boundary flux contribution to profile amplitude", "boundary flux/no-flux theorem or source-backed flux value", "MISSING_BOUNDARY_FLUX_OWNER"),
        ("OWN3644_5_topology_Atop", "A_top;Q_X", "harmonic/topological exterior mode amplitude", "topology/cohomology certificate or finite topological charge row", "MISSING_TOPOLOGY_OWNER"),
        ("OWN3644_6_projector_Aproj", "A_proj", "projector/readout/calibration profile source", "projector variation and calibration-source silence or value", "MISSING_PROJECTOR_SOURCE_OWNER"),
        ("OWN3644_7_shell_Ashell", "A_shell", "transition-shell/domain mismatch contribution", "domain support, shell projector, or finite shell bound", "MISSING_SHELL_SOURCE_OWNER"),
    ]
    return [
        {
            **base,
            "owner_id": owner_id,
            "symbol": symbol,
            "definition": definition,
            "required_parent_owner": owner,
            "current_status": status,
            "claim_allowed": False,
        }
        for owner_id, symbol, definition, owner, status in specs
    ]


def operator_prior_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    return [
        {
            **base,
            "prior_id": "OP3644_0_DX",
            "symbol": "D_X",
            "definition": "positive kinetic/gradient residue for X_N exterior operator",
            "units": "operator-dependent; must make D_X Delta X_N match J_X^eff",
            "prior_family": "unsigned_placeholder_not_sampleable",
            "lower": "",
            "upper": "",
            "required_before_sampling": "parent Hessian normalization and sign",
            "status": "PRIOR_ROW_CREATED_VALUES_MISSING",
        },
        {
            **base,
            "prior_id": "OP3644_1_MX2",
            "symbol": "M_X^2",
            "definition": "positive mass-gap/curvature residue for X_N exterior operator",
            "units": "D_X / m^2 in SI profile normalization",
            "prior_family": "unsigned_placeholder_not_sampleable",
            "lower": "",
            "upper": "",
            "required_before_sampling": "same-branch parent Hessian and field normalization",
            "status": "PRIOR_ROW_CREATED_VALUES_MISSING",
        },
        {
            **base,
            "prior_id": "OP3644_2_ellX",
            "symbol": "ell_X",
            "definition": "local profile range, ell_X=sqrt(D_X/M_X^2)",
            "units": "m",
            "prior_family": "log_range_placeholder_not_claim",
            "lower": "",
            "upper": "",
            "required_before_sampling": "D_X and M_X^2 or explicit parent range; R10 alpha(lambda) curve before scoring",
            "status": "RANGE_PRIOR_ROW_CREATED_VALUES_MISSING",
        },
    ]


def amplitude_prior_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    return [
        {
            **base,
            "prior_id": "AP3644_0_AX_total",
            "symbol": "A_X_abs",
            "definition": "|A_X| <= |A_src|+|A_bdy|+|A_top|+|A_proj|+|A_shell|",
            "units": "X_N*length",
            "prior_family": "absolute_sum_envelope_placeholder",
            "lower": "0",
            "upper": "",
            "source_owner_needed": "all component owners or one theorem-zero certificate",
            "bound_channels": "Gdot;radial_orbital;PPN;R10",
            "status": "FIRST_AMPLITUDE_PRIOR_ROW_CREATED_VALUES_MISSING",
        },
        {
            **base,
            "prior_id": "AP3644_1_QX_massless",
            "symbol": "Q_X_abs",
            "definition": "massless/Gauss exterior charge amplitude",
            "units": "X_N*length",
            "prior_family": "absolute_nonnegative_placeholder",
            "lower": "0",
            "upper": "",
            "source_owner_needed": "topological/Gauss charge owner or no-pole theorem",
            "bound_channels": "radial_orbital;PPN;Gdot",
            "status": "MASSLESS_PRIOR_ROW_CREATED_VALUES_MISSING",
        },
        {
            **base,
            "prior_id": "AP3644_2_time_coefficients",
            "symbol": "dot_A_X;dot_ell_X;dot_X_inf",
            "definition": "time-profile coefficients entering Xdot_N",
            "units": "X_N*length/time; length/time; X_N/time",
            "prior_family": "time_drift_placeholder",
            "lower": "",
            "upper": "",
            "source_owner_needed": "stationarity theorem or source-backed time evolution",
            "bound_channels": "Gdot;clock",
            "status": "TIME_PRIOR_ROW_CREATED_VALUES_MISSING",
        },
        {
            **base,
            "prior_id": "AP3644_3_component_vector",
            "symbol": "A_src;A_bdy;A_top;A_proj;A_shell",
            "definition": "profile-amplitude component vector with no-cancellation policy",
            "units": "X_N*length per component",
            "prior_family": "componentwise_absolute_placeholder",
            "lower": "0 per absolute component",
            "upper": "",
            "source_owner_needed": "J_X, boundary flux, topology, projector, shell/domain rows",
            "bound_channels": "all local beta_common profile channels",
            "status": "COMPONENT_PRIOR_ROWS_CREATED_VALUES_MISSING",
        },
    ]


def runner_schema_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "field": "profile_id",
            "required": True,
            "units": "label",
            "description": "unique source/local environment identifier",
            "status": "SCHEMA_READY",
        },
        {
            **base,
            "field": "D_X;M_X2;ell_X",
            "required": True,
            "units": "operator;operator;m",
            "description": "same-branch operator and range values or explicit theorem-zero",
            "status": "REQUIRED_MISSING_VALUES",
        },
        {
            **base,
            "field": "A_src;A_bdy;A_top;A_proj;A_shell;Q_X",
            "required": True,
            "units": "X_N*length",
            "description": "absolute component amplitudes; no cancellation between components",
            "status": "REQUIRED_MISSING_VALUES",
        },
        {
            **base,
            "field": "dot_A_X;dot_ell_X;dot_X_inf",
            "required": True,
            "units": "time derivatives",
            "description": "time-profile coefficients for Gdot/clock projection",
            "status": "REQUIRED_MISSING_VALUES",
        },
        {
            **base,
            "field": "source_paths",
            "required": True,
            "units": "paths/URLs",
            "description": "source path for every nonzero amplitude/operator value",
            "status": "REQUIRED_FOR_ANY_NUMERIC_RUN",
        },
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": t,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }
    return [
        {
            **base,
            "decision_id": "DEC3644_0_owner_not_found",
            "decision": "Current corpus does not parent-own D_X, M_X^2, or the A_X component sources.",
            "status": "SOURCE_OWNER_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3644_1_prior_rows_created",
            "decision": "Create nonclaim prior rows for A_X, ell_X, Q_X, and time coefficients without numeric sampling.",
            "status": "PRIOR_ROWS_CREATED_NOT_SAMPLEABLE",
        },
        {
            **base,
            "decision_id": "DEC3644_2_next",
            "decision": "Next target is the effective source current J_X^eff and component owner split.",
            "status": "JX_SOURCE_OWNER_NEXT",
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SOURCE_OWNER_UNSIGNED_AMPLITUDE_RANGE_PRIOR_ROWS_CREATED",
            "summary": "3644 audits ownership of D_X, M_X^2, ell_X, A_src, A_bdy, A_top, A_proj, and A_shell. No parent owner is found, so it creates nonclaim prior/schema rows for A_X, ell_X, Q_X, and time-profile coefficients without numeric sampling or pass claims.",
            "claim_ceiling": "no local-GR/Newton, no-hair, finite-range, PPN, R10, Gdot, or profile-amplitude pass is allowed from 3644",
            "useful_result": "a future runner now knows the exact required fields and source-owner requirements before any numeric profile smoke test",
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3644_0",
            "target_doc": "3645-Y5-R2FR-effective-JX-source-current-owner-or-profile-smoke-schema.md",
            "target_script": "scripts/Y5_R2FR_3645_effective_JX_source_current_owner_or_profile_smoke_schema.py",
            "objective": "derive the effective source current J_X^eff and split it into matter, hidden/domain, boundary, projector, and shell components; if unsigned, emit a smoke-runner input table that refuses numeric runs until each component has a source path",
            "success_gate": "either J_X^eff is theorem-zero/owned, or every A_X source component has an explicit row with units, source paths, and refusal gates",
            "valid_for_claim": False,
        }
    ]


def write_doc(src, owners, op_priors, amp_priors, schema, decisions, status, nxt) -> None:
    text = "\n\n".join(
        [
            "# 3644 Y5 R2FR profile source owner or first amplitude prior",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Owner audit",
            (
                "The exact range relation `ell_X=sqrt(D_X/M_X^2)` already exists, but `D_X`, `M_X^2`, and the profile source components "
                "`A_src`, `A_bdy`, `A_top`, `A_proj`, `A_shell` are still not parent-owned. Therefore no numeric profile sample is allowed."
            ),
            "## Prior rows",
            (
                "The created prior rows are placeholders for future private smoke runners. They are intentionally non-sampleable until "
                "the parent action or a source-backed bound supplies units and values. The key anti-cheat rule is componentwise absolute "
                "addition: `|A_X| <= |A_src|+|A_bdy|+|A_top|+|A_proj|+|A_shell|`."
            ),
            "## Owner rows",
            "\n".join(f"- `{row['owner_id']}`: `{row['symbol']}` — {row['current_status']}" for row in owners),
            "## Operator/range prior rows",
            "\n".join(f"- `{row['prior_id']}`: `{row['symbol']}` — {row['status']}" for row in op_priors),
            "## Amplitude prior rows",
            "\n".join(f"- `{row['prior_id']}`: `{row['symbol']}` — {row['status']}" for row in amp_priors),
            "## Runner schema",
            "\n".join(f"- `{row['field']}`: {row['status']} — {row['description']}" for row in schema),
            "## Decisions",
            "\n".join(f"- `{row['decision_id']}`: {row['status']} — {row['decision']}" for row in decisions),
            "## Next target",
            f"`{nxt[0]['target_doc']}` via `{nxt[0]['target_script']}`.",
            "## Sources",
            "\n".join(f"- `{row['source_id']}`: `{row['local_path']}` exists={row['exists']} needle_found={row['needle_found']}" for row in src),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(out: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3644_0_sources_exist", all(bool(row["exists"]) for row in src), "all source paths exist")
    add("VAL3644_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3644_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")
    parse_ok = True
    details = []
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3644_3_csv_parse", parse_ok, "; ".join(details))

    owners = read_csv(out["source_owner_audit"])
    op_priors = read_csv(out["operator_prior_rows"])
    amp_priors = read_csv(out["amplitude_prior_rows"])
    schema = read_csv(out["runner_schema"])
    decisions = read_csv(out["decision"])
    status = read_csv(out["status"])
    nxt = read_csv(out["next_target"])

    add("VAL3644_4_owner_symbols", {"D_X", "M_X^2", "ell_X", "A_src", "A_bdy", "A_top;Q_X", "A_proj", "A_shell"}.issubset({row["symbol"] for row in owners}), "operator and amplitude owners audited")
    add("VAL3644_5_operator_prior_rows", {"D_X", "M_X^2", "ell_X"}.issubset({row["symbol"] for row in op_priors}), "D_X/M_X2/ell_X prior rows present")
    add("VAL3644_6_amplitude_prior_rows", any(row["symbol"] == "A_X_abs" and "|A_src|+|A_bdy|+|A_top|+|A_proj|+|A_shell|" in row["definition"] for row in amp_priors), "absolute A_X prior envelope present")
    add("VAL3644_7_no_fake_numeric_sampling", all(row["score_ready"].lower() == "false" for row in op_priors + amp_priors), "prior rows explicitly not sample-ready")
    add("VAL3644_8_runner_schema_fields", {"D_X;M_X2;ell_X", "A_src;A_bdy;A_top;A_proj;A_shell;Q_X", "dot_A_X;dot_ell_X;dot_X_inf", "source_paths"}.issubset({row["field"] for row in schema}), "runner schema includes operator, amplitude, time, and source fields")
    add("VAL3644_9_decision_next", any(row["status"] == "JX_SOURCE_OWNER_NEXT" for row in decisions), "J_X source owner selected next")
    add("VAL3644_10_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in owners + op_priors + amp_priors + schema + decisions + status + nxt), "all generated rows remain nonclaim")
    leak_patterns = ["*Y5_R2FR_3644*", "3644-Y5-R2FR-*", "Y5_R2FR_3644_*"]
    leaks = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3644_11_no_formalization_leak", not leaks, "no 3644 checkpoint files in formalization-workbench")
    add("VAL3644_12_next_target_written", bool(nxt) and "3645" in nxt[0]["target_doc"], "3645 J_X source-current target written")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3644_13_doc_written", "|A_X| <=" in doc_text, "checkpoint doc written with absolute amplitude rule")
    add("VAL3644_14_status_honest", status[0]["status"] == "SOURCE_OWNER_UNSIGNED_AMPLITUDE_RANGE_PRIOR_ROWS_CREATED", "status keeps source owner unsigned")
    return rows


def main() -> None:
    t = now()
    out = outputs()
    src = source_rows(t)
    owners = owner_rows(t)
    op_priors = operator_prior_rows(t)
    amp_priors = amplitude_prior_rows(t)
    schema = runner_schema_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)

    write_csv(out["source_register"], src)
    write_csv(out["source_owner_audit"], owners)
    write_csv(out["operator_prior_rows"], op_priors)
    write_csv(out["amplitude_prior_rows"], amp_priors)
    write_csv(out["runner_schema"], schema)
    write_csv(out["decision"], decisions)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, owners, op_priors, amp_priors, schema, decisions, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3644 validation failed: {failures}")
    print(f"wrote 3644 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
