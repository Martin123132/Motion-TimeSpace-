from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3649"
BRANCH_ID = "MTS_R2FR_Y5_EM_MAXWELL_SAME_FRAME_STRESS_OR_FEM_COEFFICIENT_ROW_3649"
DOC = ROOT / "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3649_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3649_EM_MAXWELL_THEOREM_ATTEMPT.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv",
        "projections": RESIDUALS / "P8_Y5_R2FR_3649_EM_OBSERVABLE_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3649_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3649_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3649_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3649_VALIDATION.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3648", RESIDUALS / "P8_Y5_R2FR_3648_NEXT_TARGET.csv", "EM-Maxwell-same-frame", "3648 handoff to EM/Maxwell same-frame stress"),
        ("doc_3648", ROOT / "3648-Y5-R2FR-no-marker-constant-superselection-or-alphaEM-mass-clock-coefficient-row.md", "EM_THEOREM_OR_B_ALPHA_ROW_REQUIRED", "3648 EM bridge and b_alpha caveat"),
        ("em_lock_989", RESIDUALS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_1_unique_F2", "989 EM-lock signature audit"),
        ("alpha_audit_1047", RESIDUALS / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_4_verdict", "1047 alpha/gauge normalization audit"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_1_no_extra_F2", "1048 no-extra-F2/no-mass-vertex audit"),
        ("matrix_1048", RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "BM1048_0_alpha_clock", "1048 alpha/mass/clock projection matrix"),
        ("doc_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "F2T1048_1_no_scalar_counterterm", "1048 theorem details for no f_X F2"),
        ("doc_1054", ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md", "ZC1054_2_alpha_owner", "1054 alpha owner and beta_source_alpha route"),
        ("doc_1055", ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", "PAC1055_1_EM_owner", "1055 alpha owner parent-action contract"),
        ("clock_646", RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", "delta_K_alpha_used", "source-backed clock alpha sensitivity rows"),
        ("bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R2_clock_redshift", "local clock/WEP/PPN bounds"),
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
            "theorem_id": "EMT3649_0_same_frame_action",
            "claim": "Maxwell/EM same-frame stress theorem.",
            "mathematical_form": "S_EM = -(C_P/4) int mu_obs(q) <F_Q T_Q,F_Q T_Q>_P, with mu_obs and Hodge star built from e_obs(q).",
            "derivation_step": "If T_Q, C_P<T_Q,T_Q>_P, mu_obs, Hodge star, and source current all descend through q or are fixed representation data, then Lie_vX S_EM=0 apart from owned Maxwell equations.",
            "result": "EM stress is same-frame and has no independent X_N source only under the full parent EM-lock signature.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent T_Q owner, unique F^2 normalization, no f_XF^2 counterterm, Hodge/readout descent, and current normalization owner",
        },
        {
            **base,
            "theorem_id": "EMT3649_1_unique_F2",
            "claim": "Unique Maxwell kinetic normalization fixes alpha_EM.",
            "mathematical_form": "g_EM^-2 = C_P <T_Q,T_Q>_P; b_alpha = -Lie_vX ln(g_EM^-2) plus readout terms.",
            "derivation_step": "A fixed compact charge generator and unique parent curvature norm make Lie_vX g_EM^-2=0.",
            "result": "b_alpha=0 follows only if no independent lambda_A F_Q^2 or f_X(X_N)F_Q^2 term is allowed.",
            "status": "FAIL_CURRENT_CLAIM_COUNTERTERM_LEGAL",
            "missing_for_claim": "operator-classification theorem forbidding scalar gauge-kinetic counterterms",
        },
        {
            **base,
            "theorem_id": "EMT3649_2_no_fEM_counterterm",
            "claim": "A scalar gauge-kinetic function is the exact EM leak.",
            "mathematical_form": "Delta S_EM = -1/4 int mu_obs f_EM(X_N)F_Q^2; b_alpha ~= Lie_vX ln f_EM after normalization.",
            "derivation_step": "Varying X_N gives J_X^EM = +(1/4) sqrt(-g_obs) partial_X f_EM F_Q^2 plus Hodge/readout terms.",
            "result": "If f_EM is not forbidden or quotient-owned, Maxwell stress and alpha/clock/WEP rows remain live.",
            "status": "FEM_SOURCE_FORMULA_DERIVED_CONDITIONALLY",
            "missing_for_claim": "f_EM theorem-zero or numeric/source-backed coefficient row",
        },
        {
            **base,
            "theorem_id": "EMT3649_3_Maxwell_stress",
            "claim": "Same-frame Maxwell stress is conserved only with owned EM action and source current.",
            "mathematical_form": "T_EM^{mu nu}=Z_EM(F^{mu rho}F^nu_rho - 1/4 g_obs^{mu nu}F^2); nabla_mu T_EM^{mu nu}=-F^{nu rho}J_rho plus coefficient-gradient exchange terms.",
            "derivation_step": "Metric variation gives the usual stress if Z_EM and the Hodge star are fixed by the same observed frame; gradients of Z_EM or f_EM are retained exchange currents.",
            "result": "Maxwell stress cannot be imported as GR-clean unless the EM coefficient and frame are parent-locked.",
            "status": "STRESS_IDENTITY_CONDITIONAL",
            "missing_for_claim": "same-frame Hodge, current owner, and coefficient-gradient silence",
        },
        {
            **base,
            "theorem_id": "EMT3649_4_photon_optical_frame",
            "claim": "Photon/optical frame can reintroduce the same leak even if F^2 is fixed.",
            "mathematical_form": "g_opt = g_obs + B_gamma(X_N)U_muU_nu or Hodge_opt=Hodge[e_obs,X_N].",
            "derivation_step": "A photon/readout frame changes spectra, clocks, Poynting flux, and EM stress through the Hodge/readout map.",
            "result": "Optical/Hodge leakage needs a zero theorem or coefficient row separate from b_alpha.",
            "status": "OPTICAL_FRAME_COUNTERMODEL_LIVE",
            "missing_for_claim": "photon frame/Hodge descent or b_optical/b_Hodge rows",
        },
        {
            **base,
            "theorem_id": "EMT3649_5_charge_current_owner",
            "claim": "Charge-current/source normalization must share the same T_Q owner.",
            "mathematical_form": "S_int = sum_A n_A int A_Q J_A; Lie_vX n_A=0 and J_A descends through the matter functor.",
            "derivation_step": "The same compact charge generator must own charge labels, current normalization, alpha_EM, and source/test charge rows.",
            "result": "Without this, beta_source_alpha can float independently of clock alpha drift.",
            "status": "SOURCE_NORMALIZATION_OWNER_UNSIGNED",
            "missing_for_claim": "charge lattice/current owner and source/test material normalization",
        },
        {
            **base,
            "theorem_id": "EMT3649_6_verdict",
            "claim": "Current MTS proves Maxwell/EM same-frame stress and alpha owner.",
            "mathematical_form": "EMT3649_0 through EMT3649_5 parent-signed => b_alpha=f_EM=b_Hodge=b_optical=beta_source_alpha=0 for EM channel.",
            "derivation_step": "All EM-lock clauses must close in one parent branch.",
            "result": "The route is precise but unsigned; f_EM/b_alpha/source-current rows remain live.",
            "status": "FAIL_CURRENT_CLAIM_EM_LOCK_NOT_SIGNED",
            "missing_for_claim": "parent EM owner, no-extra-F2 theorem, readout/radiative closure, and charge-current normalization",
        },
    ]


def audit_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}
    specs = [
        ("EMA3649_0_TQ_owner", "T_Q compact charge generator owner", "fixed parent charge lattice/norm and varied EM connection", "MISSING_PARENT_TQ_OWNER", "charge units and alpha normalization can float", "b_alpha;beta_source_alpha"),
        ("EMA3649_1_unique_F2", "unique Maxwell F^2 normalization", "no independent lambda_A F_Q^2 or branch-specific kinetic coefficient", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "alpha_EM remains a retained coefficient", "b_alpha;f_EM"),
        ("EMA3649_2_no_fEM", "no f_EM(X_N)F_Q^2 scalar counterterm", "operator/symmetry rule excluding scalar gauge-kinetic functions", "MISSING_NO_FEM_THEOREM", "EM stress has coefficient-gradient exchange", "f_EM;b_alpha"),
        ("EMA3649_3_Hodge_frame", "same observed Hodge/coframe for Maxwell stress", "Hodge star and volume form descend through e_obs(q)", "MISSING_HODGE_READOUT_DESCENT", "photon/optical frame can source clocks and Poynting flux", "b_Hodge;b_optical"),
        ("EMA3649_4_current_owner", "charge current and source normalization owner", "S_int charge labels/currents descend from same T_Q owner", "MISSING_CHARGE_CURRENT_OWNER", "source/test alpha charge can float", "beta_source_alpha;q_EM_source"),
        ("EMA3649_5_radiative_readout", "no radiative/readout re-entry", "renormalized alpha_eff and spectral readout remain quotient/fixed", "MISSING_RADIATIVE_READOUT_CLOSURE", "tree-level zero can be re-opened by effective readout", "b_alpha_eff;b_clock"),
        ("EMA3649_6_total", "EM same-frame lock", "all EM-lock clauses close in one parent branch", "EM_LOCK_UNSIGNED", "no Maxwell/EM stress or local-GR claim", "q_EM_stress_abs"),
    ]
    return [
        {
            **base,
            "audit_id": audit_id,
            "clause": clause,
            "required_parent_signature": required,
            "current_status": status,
            "blocks_if_missing": blocks,
            "fallback_symbol": fallback,
        }
        for audit_id, clause, required, status, blocks, fallback in specs
    ]


def coefficient_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "score_ready": False}
    specs = [
        ("FEM3649_0_balpha_zero", "b_alpha_zero_candidate", "b_alpha=0 if parent EM-lock/no-extra-F2/readout theorem is signed", "dimensionless per normalized Xhat", "parent theorem certificate path", "MISSING_PARENT_THEOREM_CERTIFICATE", "clock;EM;WEP;R10"),
        ("FEM3649_1_fEM", "f_EM", "scalar gauge-kinetic coefficient in Delta S=-1/4 int f_EM(X_N)F_Q^2", "coefficient of F^2; derivative per Xhat", "f_EM value/bound or theorem-zero; source_path; EM field convention", "MISSING_FEM_OR_ZERO_THEOREM", "EM stress;clock;R10;WEP"),
        ("FEM3649_2_balpha", "b_alpha", "vertical derivative d ln alpha_EM/dXhat from gauge kinetic/readout normalization", "Xhat^-1 or dimensionless per normalized Xhat", "unique-F2 theorem or numeric/source-backed b_alpha", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM", "clock;EM spectra;WEP;R10"),
        ("FEM3649_3_bHodge", "b_Hodge", "vertical derivative of EM Hodge/volume/readout map", "Xhat^-1", "same-frame Hodge theorem or coefficient bound", "MISSING_HODGE_DESCENT_OR_BOUND", "EM stress;Poynting;clock"),
        ("FEM3649_4_boptical", "b_optical", "photon/optical metric or spectral readout frame derivative", "Xhat^-1", "photon frame lock or optical coefficient bound", "MISSING_OPTICAL_FRAME_LOCK", "clock;EM propagation;PPN"),
        ("FEM3649_5_beta_source_alpha", "beta_source_alpha", "source/test charge response to alpha_EM or EM binding channel", "dimensionless source charge", "charge-current owner; material sensitivity; source path", "MISSING_CHARGE_SOURCE_NORMALIZATION", "WEP;R10;source_calibration"),
        ("FEM3649_6_total_guard", "q_EM_stress_abs", "|q_EM_stress| <= |f_EM|+|b_alpha|+|b_Hodge|+|b_optical|+|beta_source_alpha|+|radiative_tail|", "dimensionless/source-normalized envelope", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **base,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
        }
        for row_id, symbol, definition, units, required, status, links in specs
    ]


def projection_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "score_ready": False}
    specs = [
        ("EP3649_0_EM_stress", "EM_Maxwell_stress", "T_EM and Poynting flux are same-frame only if Z_EM/Hodge/current are parent-owned; otherwise q_EM_stress_abs is retained", "Z_EM;Hodge;e_obs;J_Q;f_EM;b_Hodge;b_optical", "NOT_SCORE_READY"),
        ("EP3649_1_clock_alpha", "clock_alpha_sensitivity", "d ln R_clock = DeltaK_alpha b_alpha dXhat plus Hodge/readout terms", "clock sensitivity rows;b_alpha;b_Hodge;b_optical;tau_clock", "SENSITIVITY_SOURCE_AVAILABLE_MTS_PROJECTION_MISSING"),
        ("EP3649_2_WEP_alpha", "WEP_EM_binding", "eta_AB_EM receives beta_source_alpha*b_alpha*tau_WEP and EM binding sensitivity terms", "composition matrix;beta_source_alpha;b_alpha;tau_WEP;WEP bound", "COMPOSITION_AND_TAU_MISSING"),
        ("EP3649_3_R10_alpha", "R10_short_range", "alpha_X(lambda) receives K_X Qbar_XH q_EM_source/test contributions from EM coefficient/source rows", "lambda_X;K_X;Qbar_XH;q_EM_stress_abs;R10 curve", "BOUND_AND_MTS_COMPONENTS_NOT_CLAIM_READY"),
        ("EP3649_4_PPN_source", "PPN_source_calibration", "EM stress/source normalization can feed PPN vector and measured-GM calibration if not locked", "weak-field map;source Hamiltonian;EM stress residual;PPN bounds", "NOT_SCORE_READY"),
        ("EP3649_5_charge_conservation", "charge_current_Ward", "nabla_mu J_Q^mu=0 and EM stress exchange require same charge-current owner, not just Maxwell notation", "T_Q owner;J_Q;matter functor;boundary terms", "SOURCE_CURRENT_OWNER_MISSING"),
        ("EP3649_6_radiative_closure", "radiative_readout", "loop/readout alpha_eff must remain quotient-owned or becomes b_alpha_eff", "renormalization/readout owner;clock/spectra convention", "RADIATIVE_CLOSURE_MISSING"),
        ("EP3649_7_total_guard", "all_local_arenas", "no cancellation between EM, frame, marker, non-Hilbert, boundary, or source calibration terms", "all component rows;source paths;units", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        {
            **base,
            "projection_id": projection_id,
            "arena": arena,
            "projection_law": law,
            "required_inputs": required,
            "current_status": status,
        }
        for projection_id, arena, law, required, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}
    return [
        {
            **base,
            "decision_id": "DEC3649_0_theorem_shape",
            "decision": "Maxwell same-frame stress is derivable if EM action, Hodge, gauge kinetic normalization, and charge current all descend through the quotient or fixed representation data.",
            "status": "EM_MAXWELL_THEOREM_SHAPE_EXACT",
        },
        {
            **base,
            "decision_id": "DEC3649_1_current_verdict",
            "decision": "Current MTS cannot claim EM-lock because f_XF^2, optical/Hodge readout, radiative/readout, and charge-current normalization remain unsigned.",
            "status": "PARENT_EM_LOCK_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3649_2_coefficients",
            "decision": "f_EM, b_alpha, b_Hodge, b_optical, beta_source_alpha, and q_EM_stress_abs rows are retained as nonclaim rows.",
            "status": "FEM_BALPHA_ROWS_CREATED_NOT_SCORE_READY",
        },
        {
            **base,
            "decision_id": "DEC3649_3_next",
            "decision": "Next target is calibrated EM/source-current normalization: charge lattice/current owner or beta_source_alpha remains live.",
            "status": "EM_SOURCE_CURRENT_NORMALIZATION_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "EM_MAXWELL_THEOREM_CONDITIONAL_FEM_BALPHA_ROWS_CREATED",
            "summary": "3649 derives the conditional Maxwell/EM same-frame stress theorem, rejects current EM-lock claim status, and creates explicit f_EM, b_alpha, b_Hodge, b_optical, beta_source_alpha, and q_EM_stress rows.",
            "claim_ceiling": "no Maxwell/EM same-frame stress, b_alpha=0, f_EM=0, local-GR/Newton, R10, PPN, WEP, clock, orbital, or source-calibration pass is claimed",
            "useful_result": "EM is now tied to a parent-action owner route or explicit source/stress coefficients; the next bottleneck is calibrated charge-current/source normalization",
            "valid_for_claim": False,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3649_0",
            "target_doc": "3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md",
            "target_script": "scripts/Y5_R2FR_3650_EM_source_current_normalization_or_beta_source_alpha_row.py",
            "objective": "prove charge/current labels and EM source normalization descend from the same compact T_Q owner as alpha_EM; if unsigned, create beta_source_alpha and charge-current source/test rows with WEP/R10/clock/source-calibration links",
            "success_gate": "either charge-current/source normalization is parent-signed, or beta_source_alpha rows have units, source paths, material/source sensitivities, and no-cancellation guards",
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
        "# 3649 Y5 R2FR EM Maxwell same-frame stress or fEM coefficient row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "**Claim ceiling:** no Maxwell/EM same-frame stress, EM-lock, local-GR/Newton, R10, PPN, WEP, clock, orbital, or source-calibration pass is claimed.",
        "",
        "## Main result",
        "",
        "The clean theorem is exact but conditional: if `S_EM=-(C_P/4) int mu_obs(q)<F_QT_Q,F_QT_Q>_P`, the Hodge star uses `e_obs(q)`, the charge generator/norm is fixed, no `f_X(X_N)F_Q^2` term exists, and the charge current descends from the same owner, then Maxwell stress is same-frame and `b_alpha=f_EM=0`.",
        "",
        "Current MTS does not yet sign those parent clauses. Therefore `f_EM`, `b_alpha`, Hodge/optical leakage, and EM source-current normalization remain live nonclaim rows.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} — {row['result']}")
    lines.extend(["", "## EM-lock audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: `{row['fallback_symbol']}` — {row['current_status']}")
    lines.extend(["", "## f_EM/b_alpha coefficient rows"])
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

    add("VAL3649_0_sources_exist", all(bool(row["source_exists"]) for row in src), "all source paths exist")
    add("VAL3649_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3649_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all outputs and doc written")

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
    add("VAL3649_3_csv_parse", parse_ok, "; ".join(counts))

    theorem = parsed["theorem"]
    audit = parsed["audit"]
    coeffs = parsed["coefficients"]
    projections = parsed["projections"]
    decisions = parsed["decisions"]
    status = parsed["status"]
    nxt = parsed["next_target"]
    groups = [theorem, audit, coeffs, projections, decisions, status, nxt]

    add("VAL3649_4_same_frame_theorem_shape", any("EM stress is same-frame" in row["result"] for row in theorem), "same-frame Maxwell theorem shape present")
    add("VAL3649_5_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_EM_LOCK_NOT_SIGNED" for row in theorem), "EM-lock not claimed")
    required_audit = {"b_alpha;f_EM", "f_EM;b_alpha", "b_Hodge;b_optical", "beta_source_alpha;q_EM_source", "b_alpha_eff;b_clock", "q_EM_stress_abs"}
    add("VAL3649_6_audit_complete", required_audit.issubset({row["fallback_symbol"] for row in audit}), "EM owner, fEM, Hodge, source, radiative, and total audit rows present")
    required_coeffs = {"b_alpha_zero_candidate", "f_EM", "b_alpha", "b_Hodge", "b_optical", "beta_source_alpha", "q_EM_stress_abs"}
    add("VAL3649_7_coeff_rows_complete", required_coeffs.issubset({row["symbol"] for row in coeffs}), "f_EM/b_alpha coefficient rows complete")
    required_proj = {"EM_Maxwell_stress", "clock_alpha_sensitivity", "WEP_EM_binding", "R10_short_range", "PPN_source_calibration", "charge_current_Ward"}
    add("VAL3649_8_projection_rows_complete", required_proj.issubset({row["arena"] for row in projections}), "EM stress, clock, WEP, R10, PPN/source, and current projections present")
    add("VAL3649_9_no_score_ready", all(row.get("score_ready", "False").lower() == "false" for table in [coeffs, projections] for row in table), "coefficient/projection rows refuse scoring")
    add("VAL3649_10_nonclaim_all_outputs", all(row.get("valid_for_claim", "False").lower() == "false" for table in groups for row in table), "all generated rows remain nonclaim")
    add("VAL3649_11_decision_next", any(row["status"] == "EM_SOURCE_CURRENT_NORMALIZATION_NEXT" for row in decisions), "EM source-current normalization selected next")
    add("VAL3649_12_next_target_written", bool(nxt) and "3650" in nxt[0]["target_doc"], "3650 target written")
    add("VAL3649_13_status_honest", status[0]["status"] == "EM_MAXWELL_THEOREM_CONDITIONAL_FEM_BALPHA_ROWS_CREATED", "status keeps EM theorem conditional")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3649_14_doc_written", "f_EM" in doc_text and "Maxwell stress is same-frame" in doc_text and "Current MTS does not yet sign" in doc_text, "doc records EM theorem and caveat")
    leak_patterns = ["*Y5_R2FR_3649*", "3649-Y5-R2FR-*", "Y5_R2FR_3649_*"]
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3649_15_no_formalization_leak", not leaks, "no 3649 checkpoint files in formalization-workbench")
    add("VAL3649_16_no_extra_F2_guard", any("f_EM(X_N)F_Q^2" in row["mathematical_form"] for row in theorem), "no-extra-F2/fEM leak explicitly represented")
    add("VAL3649_17_source_calibration_bridge", any(row["symbol"] == "beta_source_alpha" for row in coeffs), "source calibration bridge retained")
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
        raise SystemExit(f"3649 validation failed: {failures}")
    print(f"wrote 3649 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
