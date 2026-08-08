from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3647"
BRANCH_ID = "MTS_R2FR_Y5_OBSERVED_FRAME_NO_SHADOW_OR_CG_BDIS_ROWS_3647"
DOC = ROOT / "3647-Y5-R2FR-observed-frame-no-shadow-theorem-or-cg-bdis-coefficient-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3647_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3647_NO_SHADOW_THEOREM_ATTEMPT.csv",
        "countermodels": RESIDUALS / "P8_Y5_R2FR_3647_SHADOW_FRAME_COUNTERMODEL_AUDIT.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3647_CG_BDIS_COEFFICIENT_ROWS.csv",
        "arena_projection": RESIDUALS / "P8_Y5_R2FR_3647_ARENA_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3647_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3647_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3647_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3647_VALIDATION.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3646", RESIDUALS / "P8_Y5_R2FR_3646_NEXT_TARGET.csv", "observed-frame-no-shadow", "3646 handoff to observed-frame no-shadow/c_g-b_dis rows"),
        ("doc_3646", ROOT / "3646-Y5-R2FR-matter-coupling-descent-or-first-beta-source-row.md", "MISSING_NO_SHADOW_FRAME_THEOREM_OR_COEFFICIENTS", "3646 clause audit and beta_geom_shadow gap"),
        ("beta_3646", RESIDUALS / "P8_Y5_R2FR_3646_FIRST_BETA_SOURCE_ROWS.csv", "beta_geom_shadow", "3646 first beta source rows"),
        ("obs_637", RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv", "OF637_2_counterexample_filter", "637 observed functor and hidden frame filter"),
        ("blindness_594", RESIDUALS / "P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv", "MBG594_0_metric_blindness", "594 matter blindness gate"),
        ("shadow_gate_636", RESIDUALS / "P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv", "NS636_2_honesty_test", "636 no-shadow-frame classification gate"),
        ("nomarker_736", RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv", "NMC736_3_shadow_frame_forbidden", "736 no-marker/no-shadow contract"),
        ("matter_functor_1045", RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_4_no_shadow_frame", "1045 parent matter functor signature audit"),
        ("no_shadow_1046", ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md", "NSF1046_5_verdict", "1046 no-shadow theorem attempt"),
        ("shadow_audit_1029", RESIDUALS / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv", "NST1029_6_verdict", "1029 c_g theorem audit"),
        ("qbar_1027", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "BQT1027_0_visible_geometry", "1027 qbarXT visible geometry frame-leak row"),
        ("finite_pack_1028", ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md", "FMB1028_0_cg", "1028 finite coupling input pack"),
        ("spm_1032", ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md", "ACQ1032_1_finite_cg_value", "1032 closure warning and finite c_g/tau runner"),
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
                "needle_found": needle in text,
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
            "theorem_id": "NSF3647_0_public_frame_domain",
            "claim": "Ordinary matter has one public observed frame.",
            "mathematical_form": "S_matter = sum_A S_A[Psi_A, e_obs(q(Phi)), omega[e_obs], theta_A] before variation and before calibration.",
            "derivation_step": "If this is the parent action domain, there is no independent A_g(X_N), B_dis(X_N), source-only metric, or post-readout frame slot to vary.",
            "result": "No shadow-frame current exists from the action domain itself.",
            "status": "EXACT_ACTION_DOMAIN_ROUTE_NOT_PARENT_SIGNED",
            "missing_for_claim": "single-public-frame parent action clause and matter bundle functor",
        },
        {
            **base,
            "theorem_id": "NSF3647_1_shadow_frame_definition",
            "claim": "A shadow frame is any matter/readout frame not uniquely equal to the quotient-owned observed frame.",
            "mathematical_form": "e_m=A_g(X_N)e_obs or g_m=A_g(X_N)^2 g_obs + B_dis(X_N) U_mu U_nu + ...",
            "derivation_step": "Define c_g := partial_Xhat ln A_g and b_dis := partial_Xhat B_dis after the Xhat/X_N normalization is fixed.",
            "result": "Finite c_g or b_dis is a source coupling, not a harmless notation choice.",
            "status": "DEFINITION_SHARP",
            "missing_for_claim": "Xhat normalization and frame/source scope for finite branch",
        },
        {
            **base,
            "theorem_id": "NSF3647_2_chain_rule_zero",
            "claim": "If frame functions factor through the quotient, vertical X cannot change them.",
            "mathematical_form": "A_g(Phi)=Abar_g(q(Phi)), B_dis(Phi)=Bbar_dis(q(Phi)), Dq[v_X]=0 => Lie_vX ln A_g=0 and Lie_vX B_dis=0.",
            "derivation_step": "Apply the chain rule: D ln Abar_g[Dq(v_X)] and DBbar_dis[Dq(v_X)] both vanish.",
            "result": "c_g=0 and b_dis=0 follow exactly under quotient-owned frame functions.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent q-kernel, observed-frame factorization, and no independent frame slot",
        },
        {
            **base,
            "theorem_id": "NSF3647_3_trace_source",
            "claim": "Finite c_g gives the leading conformal matter source.",
            "mathematical_form": "delta_X S_matter = 1/2 int sqrt(-g_m) T_m^{mu nu} delta_X g^m_{mu nu}; delta_X g^m_{mu nu}=2 c_g g^m_{mu nu} delta Xhat + ...",
            "derivation_step": "Contract with the stress tensor to get a trace/source term proportional to c_g T_m.",
            "result": "A universal c_g can be WEP-quiet while still sourcing R10/PPN/clock/orbital channels.",
            "status": "SOURCE_FORMULA_SHAPE_DERIVED_CONDITIONALLY",
            "missing_for_claim": "sign convention, Xhat units, stress normalization, and arena projection matrices",
        },
        {
            **base,
            "theorem_id": "NSF3647_4_disformal_source",
            "claim": "Finite b_dis is a preferred-frame/readout source unless excluded.",
            "mathematical_form": "delta_X g^m_{mu nu} includes b_dis U_mu U_nu delta Xhat plus derivative/profile terms.",
            "derivation_step": "The source projects through T_m^{mu nu} U_mu U_nu and through clock/orbital/PPN frame response matrices.",
            "result": "b_dis must be theorem-zero or bounded separately from c_g.",
            "status": "SOURCE_FORMULA_SHAPE_DERIVED_CONDITIONALLY",
            "missing_for_claim": "choice of U_mu, weak-field gauge, projection tau_dis, and source path",
        },
        {
            **base,
            "theorem_id": "NSF3647_5_calibration_guard",
            "claim": "A constant common frame factor may be calibration; an X-dependent derivative is not.",
            "mathematical_form": "A_g=A_0 is removable by units, but partial_Xhat ln A_g=c_g is physical unless theorem-zero.",
            "derivation_step": "Separate constant normalization from vertical derivative before fitting G, masses, clocks, or source measure.",
            "result": "WEP silence or unit freedom cannot set c_g=0.",
            "status": "PHYSICS_GUARD",
            "missing_for_claim": "fixed-before-readout calibration and measured-G/source normalization",
        },
        {
            **base,
            "theorem_id": "NSF3647_6_verdict",
            "claim": "Current MTS proves no shadow frame for ordinary matter.",
            "mathematical_form": "NSF3647_0 + NSF3647_2 + observable completeness parent signatures => c_g=b_dis=0.",
            "derivation_step": "All required clauses must close in the same parent branch.",
            "result": "The theorem route is exact, but current claim status fails; finite c_g/b_dis rows stay live.",
            "status": "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED",
            "missing_for_claim": "parent-signed single-public-frame/no-extra-frame clause and observable-completeness theorem",
        },
    ]


def countermodel_rows(ts: str) -> list[dict[str, object]]:
    base = {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}
    specs = [
        ("CM3647_0_universal_weyl", "g_m=A_g(X_N)^2 g_obs for all ordinary matter", "composition spread can vanish while trace/source coupling remains", "c_g", "R10;PPN;clock;orbital", "LIVE_UNLESS_NO_SHADOW_THEOREM"),
        ("CM3647_1_disformal", "g_m=g_obs+B_dis(X_N) U_mu U_nu", "preferred-frame, clock, and orbital effects can survive same-coframe notation", "b_dis", "PPN;clock;orbital;R10", "LIVE_UNLESS_NO_DISFORMAL_SLOT"),
        ("CM3647_2_source_only_frame", "source preparation or source measure uses A_s(X_N) even if test readout uses e_obs", "source leg beta survives while WEP-looking test leg is quiet", "c_g_source", "R10;orbital;GM calibration", "LIVE_UNLESS_SOURCE_FRAME_LOCK"),
        ("CM3647_3_post_readout_calibration", "frame factor inserted after variation through fitted G, masses, or clock calibration", "can hide finite coupling as a fitted normalization", "delta_frame_cal", "PPN;clock;GM calibration", "LIVE_UNLESS_FIXED_BEFORE_READOUT"),
        ("CM3647_4_species_shadow", "A_A(X_N) or B_A(X_N) differs by matter species", "composition/WEP rows activate and beta differs by material", "Delta_c_g;Delta_b_dis", "WEP;composition;R10", "LIVE_UNLESS_SPECIES_FRAME_UNIQUENESS"),
        ("CM3647_5_photon_em_frame", "photon/gauge sector uses f_EM(X_N) or a different optical metric", "Maxwell stress/clock/spectral links can re-enter even if massive matter frame is public", "b_EM_frame", "EM stress;clock;fine_structure", "LIVE_UNLESS_EM_FRAME_LOCK"),
        ("CM3647_6_field_rename", "A_g is moved into masses, alpha_EM, G_eff, or source normalization", "same physics can hide outside the metric variable", "renamed_coupling_vector", "all_local_arenas", "LIVE_UNLESS_OBSERVABLE_COMPLETENESS"),
    ]
    return [
        {
            **base,
            "countermodel_id": cid,
            "countermodel": countermodel,
            "why_dangerous": why,
            "fallback_symbol": symbol,
            "observable_links": links,
            "current_status": status,
        }
        for cid, countermodel, why, symbol, links, status in specs
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
        ("CGBD3647_0_cg_zero", "c_g_zero_candidate", "theorem_zero", "c_g=0 if no-shadow public-frame theorem is parent-signed", "dimensionless in Xhat units; zero invariant", "parent theorem certificate path", "MISSING_PARENT_THEOREM_CERTIFICATE", "R10;PPN;clock;orbital"),
        ("CGBD3647_1_cg_common", "c_g", "finite_common_weyl", "c_g := partial_Xhat ln A_g for universal ordinary matter/source frame", "dimensionless per Xhat; 1/X_N if X_N dimensional", "Xhat normalization; frame scope; value or bound; source_path", "MISSING_PARENT_ZERO_OR_NUMERIC_CG", "R10;PPN;clock;orbital"),
        ("CGBD3647_2_cg_source", "c_g_source", "finite_source_leg", "source-body/source-measure conformal derivative", "dimensionless per Xhat", "source preparation map; material/source scope; source_path", "MISSING_SOURCE_FRAME_LOCK_OR_BOUND", "R10;GM calibration;orbital"),
        ("CGBD3647_3_bdis", "b_dis", "finite_disformal", "b_dis := partial_Xhat B_dis or profile-normalized disformal derivative", "metric coefficient per Xhat", "U_mu convention; weak-field gauge; value or bound; source_path", "MISSING_NO_DISFORMAL_THEOREM_OR_NUMERIC_BDIS", "PPN;clock;orbital;R10"),
        ("CGBD3647_4_bdis_projected", "tau_dis*b_dis", "arena_projected_disformal", "arena-projected disformal response after gauge/profile projection", "dimensionless response", "tau_dis;projection matrix;profile convention;source_path", "MISSING_ARENA_PROJECTION", "PPN;clock;orbital"),
        ("CGBD3647_5_frame_calibration", "delta_frame_cal", "post_readout_frame_leak", "post-variation calibration/readout frame derivative", "dimensionless per Xhat", "fixed-before-readout certificate or calibration derivative bound", "MISSING_FIXED_BEFORE_READOUT_FRAME_LOCK", "GM calibration;clock;PPN"),
        ("CGBD3647_6_total_guard", "beta_geom_shadow_abs", "absolute_envelope", "|beta_geom_shadow| <= |tau_R10 c_g|+|tau_dis b_dis|+|c_g_source|+|delta_frame_cal|+|b_EM_frame|", "dimensionless", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **base,
            "row_id": rid,
            "symbol": symbol,
            "row_type": row_type,
            "definition": definition,
            "units": units,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
        }
        for rid, symbol, row_type, definition, units, required, status, links in specs
    ]


def arena_projection_rows(ts: str) -> list[dict[str, object]]:
    base = {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "score_ready": False,
    }
    specs = [
        ("AP3647_0_R10", "R10_short_range", "alpha_R10_frame(lambda) <= |K_X Qbar_XH| [|tau_R10 c_g|+|tau_dis_R10 b_dis|+tails]_source_test_abs", "c_g;b_dis;tau_R10;tau_dis_R10;K_X;Qbar_XH;lambda_X;bound_curve", "NOT_SCORE_READY"),
        ("AP3647_1_PPN_gamma_beta", "PPN_gamma_beta", "[gamma-1,beta-1]_frame = M_PPN(profile,gauge) [c_g,b_dis,delta_frame_cal]^T", "M_PPN;tau_PPN_gamma;tau_PPN_beta;c_g;b_dis;gauge;profile", "NOT_SCORE_READY"),
        ("AP3647_2_PPN_preferred", "PPN_preferred_frame", "[alpha1,alpha2,alpha3]_frame = M_pref [b_dis,delta_frame_cal,source_frame]^T", "M_pref;U_mu convention;b_dis;source_frame;boundary silence", "NOT_SCORE_READY"),
        ("AP3647_3_WEP", "WEP_composition", "eta_frame depends on differential species/source spread Delta c_g, Delta b_dis; universal c_g alone is not killed by WEP", "species rows;Delta_c_g;Delta_b_dis;material sensitivities", "ANCHOR_ONLY_COMPONENTS_MISSING"),
        ("AP3647_4_clock", "clock_redshift_spectra", "delta ln nu_clock = tau_clock^g c_g + tau_clock^dis b_dis + marker/EM terms", "tau_clock;c_g;b_dis;b_EM_frame;b_alpha", "NOT_SCORE_READY"),
        ("AP3647_5_orbital_Gdot", "orbital_Gdot", "dot G_eff/G or source GM drift receives dot(c_g Xhat) and disformal/source-frame drift terms", "time profile;dot_Xhat;c_g;b_dis;source_frame;LLR/orbital bound", "NOT_SCORE_READY"),
        ("AP3647_6_EM_Maxwell", "EM_Maxwell_stress", "Maxwell stress is same-frame only if photon/gauge sector uses e_obs and f_EM is X-blind; otherwise b_EM_frame/b_alpha rows feed EM stress", "photon frame;f_EM(X);b_EM_frame;b_alpha;stress convention", "THEOREM_OR_EM_COEFFICIENTS_MISSING"),
        ("AP3647_7_total_guard", "all_local_arenas", "no arena may use cancellation between c_g, b_dis, marker, non-Hilbert, boundary, or calibration tails", "absolute component rows and source paths", "NO_CANCELLATION_POLICY_ACTIVE"),
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
            "decision_id": "DEC3647_0_theorem_shape",
            "decision": "The no-shadow observed-frame theorem is exact if ordinary matter has only the quotient public frame and all frame functions factor through q.",
            "status": "NO_SHADOW_THEOREM_SHAPE_EXACT",
        },
        {
            **base,
            "decision_id": "DEC3647_1_current_verdict",
            "decision": "Current MTS cannot claim c_g=b_dis=0 because the parent single-public-frame/no-extra-frame action clause is unsigned.",
            "status": "PARENT_NO_SHADOW_SIGNATURE_UNSIGNED",
        },
        {
            **base,
            "decision_id": "DEC3647_2_coefficients",
            "decision": "c_g and b_dis are retained as explicit nonclaim coefficient rows with arena projection requirements.",
            "status": "CG_BDIS_ROWS_CREATED_NOT_SCORE_READY",
        },
        {
            **base,
            "decision_id": "DEC3647_3_closure_warning",
            "decision": "Single Public Metric may be used only as a labelled closure branch, not as derived MTS evidence.",
            "status": "SPM_CLOSURE_NOT_DERIVED_THEOREM",
        },
        {
            **base,
            "decision_id": "DEC3647_4_next",
            "decision": "Next target is no-marker/constant superselection: alpha_EM, masses, clock ratios, and material markers can reintroduce beta even after frame locking.",
            "status": "NO_MARKER_CONSTANT_SUPERSELECTION_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "NO_SHADOW_THEOREM_CONDITIONAL_CG_BDIS_ROWS_CREATED",
            "summary": "3647 consolidates the observed-frame no-shadow theorem, rejects current c_g=b_dis=0 claim status, and creates explicit c_g/b_dis coefficient plus arena-projection rows for R10, PPN, WEP, clocks, orbital, and EM/Maxwell stress checks.",
            "claim_ceiling": "no c_g=0, b_dis=0, beta_geom_shadow=0, local-GR/Newton, R10, PPN, clock, orbital, WEP, or EM stress pass is claimed",
            "useful_result": "the frame-coupling fork is now exact: parent-sign single-public-frame/no-extra-frame, or source c_g/b_dis and projections before scoring",
            "valid_for_claim": False,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": ts,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3647_0",
            "target_doc": "3648-Y5-R2FR-no-marker-constant-superselection-or-alphaEM-mass-clock-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_3648_no_marker_constant_superselection_or_alphaEM_mass_clock_coefficient_row.py",
            "objective": "prove alpha_EM, particle masses/mass ratios, clock constants, and material markers are fixed representation data or quotient-owned; if unsigned, create b_alpha, b_mass, b_clock, and material-sensitivity rows with observable links",
            "success_gate": "either no-marker constant superselection is parent-signed, or constants/material coefficient rows have units, source paths, sensitivity vectors, and no-cancellation guards",
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


def write_doc(
    src: list[dict[str, object]],
    theorem: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    projections: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    lines = [
        "# 3647 Y5 R2FR observed frame no-shadow theorem or cg bdis coefficient row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "**Claim ceiling:** no frame-zero, local-GR/Newton, R10, PPN, clock, orbital, WEP, or EM stress pass is claimed.",
        "",
        "## Main result",
        "",
        "The clean theorem is sharp: if ordinary matter is restricted at parent-action level to `S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]`, and any frame function factors through `q`, then `Dq[v_X]=0` gives `c_g=0` and `b_dis=0` by chain rule.",
        "",
        "Current MTS does not yet own that parent action-domain clause, so `c_g` and `b_dis` remain explicit nonclaim coefficient rows. Single Public Metric is allowed only as a labelled closure branch, not as derived evidence.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} — {row['result']}")
    lines.extend(["", "## Countermodel audit"])
    for row in countermodels:
        lines.append(f"- `{row['countermodel_id']}`: `{row['fallback_symbol']}` — {row['current_status']} ({row['observable_links']})")
    lines.extend(["", "## c_g/b_dis coefficient rows"])
    for row in coefficients:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Arena projections"])
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

    add("VAL3647_0_sources_exist", all(bool(row["source_exists"]) for row in src), "all source paths exist")
    add("VAL3647_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in out.items() if name != "validation"}
    add("VAL3647_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all outputs and doc written")

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
    add("VAL3647_3_csv_parse", parse_ok, "; ".join(counts))

    theorem = parsed["theorem"]
    countermodels = parsed["countermodels"]
    coefficients = parsed["coefficients"]
    projections = parsed["arena_projection"]
    decisions = parsed["decisions"]
    status = parsed["status"]
    nxt = parsed["next_target"]
    generated_groups = [theorem, countermodels, coefficients, projections, decisions, status, nxt]

    add("VAL3647_4_theorem_zero_shape", any("c_g=0 and b_dis=0" in row["result"] for row in theorem), "c_g/b_dis zero theorem shape present")
    add("VAL3647_5_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED" for row in theorem), "no-shadow zero not claimed")
    required_counter = {"c_g", "b_dis", "c_g_source", "delta_frame_cal", "Delta_c_g;Delta_b_dis", "b_EM_frame"}
    add("VAL3647_6_countermodels_complete", required_counter.issubset({row["fallback_symbol"] for row in countermodels}), "countermodels include Weyl, disformal, source, calibration, species, and EM frame routes")
    required_coeffs = {"c_g_zero_candidate", "c_g", "c_g_source", "b_dis", "tau_dis*b_dis", "delta_frame_cal", "beta_geom_shadow_abs"}
    add("VAL3647_7_coeff_rows_complete", required_coeffs.issubset({row["symbol"] for row in coefficients}), "c_g/b_dis coefficient rows complete")
    required_arenas = {"R10_short_range", "PPN_gamma_beta", "PPN_preferred_frame", "WEP_composition", "clock_redshift_spectra", "orbital_Gdot", "EM_Maxwell_stress"}
    add("VAL3647_8_arena_projection_complete", required_arenas.issubset({row["arena"] for row in projections}), "R10, PPN, WEP, clock, orbital, and EM projections present")
    add("VAL3647_9_no_score_ready", all(row.get("score_ready", "False").lower() == "false" for table in [coefficients, projections] for row in table), "coefficient/projection rows refuse scoring")
    add("VAL3647_10_nonclaim_all_outputs", all(row.get("valid_for_claim", "False").lower() == "false" for table in generated_groups for row in table), "all generated rows remain nonclaim")
    add("VAL3647_11_decision_next", any(row["status"] == "NO_MARKER_CONSTANT_SUPERSELECTION_NEXT" for row in decisions), "no-marker/constant target selected next")
    add("VAL3647_12_next_target_written", bool(nxt) and "3648" in nxt[0]["target_doc"], "3648 target written")
    add("VAL3647_13_status_honest", status[0]["status"] == "NO_SHADOW_THEOREM_CONDITIONAL_CG_BDIS_ROWS_CREATED", "status keeps no-shadow theorem conditional")
    doc_text = DOC.read_text(encoding="utf-8", errors="replace") if DOC.exists() else ""
    add("VAL3647_14_doc_written", "c_g=0" in doc_text and "b_dis=0" in doc_text and "closure branch" in doc_text, "doc records zero theorem and closure warning")
    leak_patterns = ["*Y5_R2FR_3647*", "3647-Y5-R2FR-*", "Y5_R2FR_3647_*"]
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in leak_patterns:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3647_15_no_formalization_leak", not leaks, "no 3647 checkpoint files in formalization-workbench")
    add("VAL3647_16_spm_not_claim", any(row["status"] == "SPM_CLOSURE_NOT_DERIVED_THEOREM" for row in decisions), "SPM closure warning retained")
    add("VAL3647_17_no_cancellation_guard", any(row["symbol"] == "beta_geom_shadow_abs" and "tau_R10 c_g" in row["definition"] for row in coefficients), "absolute frame-coupling guard present")
    return rows


def main() -> None:
    ts = now()
    out = outputs()
    src = source_register(ts)
    theorem = theorem_rows(ts)
    countermodels = countermodel_rows(ts)
    coefficients = coefficient_rows(ts)
    projections = arena_projection_rows(ts)
    decisions = decision_rows(ts)
    status = status_rows(ts)
    nxt = next_target_rows(ts)

    write_csv(out["source_register"], src)
    write_csv(out["theorem"], theorem)
    write_csv(out["countermodels"], countermodels)
    write_csv(out["coefficients"], coefficients)
    write_csv(out["arena_projection"], projections)
    write_csv(out["decisions"], decisions)
    write_csv(out["status"], status)
    write_csv(out["next_target"], nxt)
    write_doc(src, theorem, countermodels, coefficients, projections, decisions, status, nxt)

    validation = validate(out, src)
    write_csv(out["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3647 validation failed: {failures}")
    print(f"wrote 3647 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
