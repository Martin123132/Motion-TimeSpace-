from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1030_0_1029_next", "source-intake/mts_residuals/P8_Y5_R10_1029_NEXT_TARGET.csv", "1030-Y5-R10-single-public-metric", "1029 handoff to single-public-metric parent action derivation."),
        ("SRC1030_1_1029_theorem", "source-intake/mts_residuals/P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv", "NST1029_2_no_extra_frame_slot", "1029 no-extra-frame missing parent clause."),
        ("SRC1030_2_1029_intake", "source-intake/mts_residuals/P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv", "CGI1029_1_finite_cg_R10", "1029 c_g finite/zero intake template."),
        ("SRC1030_3_1029_tau", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_1_PPN_gamma_beta", "1029 tau projection requirements."),
        ("SRC1030_4_943_contract", "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv", "CFC943_6_no_shadow_frame_rule", "943 coframe/no-shadow contract."),
        ("SRC1030_5_953_source_functor", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "953 source functor theorem attempt."),
        ("SRC1030_6_954_label_forgetting", "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv", "PLF954_5_verdict", "954 label-forgetting parent contract."),
        ("SRC1030_7_955_minimal_action", "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", "MMA955_6_verdict", "955 minimal matter action lemma."),
        ("SRC1030_8_956_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_3_minimal_matter_action", "956 source-side GR/Newton spine."),
        ("SRC1030_9_949_parent_clause", "source-intake/mts_residuals/P8_Y5_R10_949_PARENT_CLAUSE_ATTEMPT.csv", "PCA949_1_matter_factorization", "949 parent clause attempt."),
        ("SRC1030_10_950_source_norm", "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv", "SNL950_4_countermodel", "950 source-normalization countermodel."),
        ("SRC1030_11_951_ward", "source-intake/mts_residuals/P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv", "SWA951_3_species_weight_countermodel", "951 Ward action countermodel."),
        ("SRC1030_12_951_provenance", "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv", "PGS951_2_derivation_status", "951 provenance gate schema."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def derivation_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SPD1030_0_target",
            "attempt": "derive one public metric/coframe for ordinary matter from the parent action",
            "mathematical_form": "Allowed[S_m] ?= Sbar[Psi,e_pub(q(Phi)),omega[e_pub],theta(q)] with no A_g(Xhat)e_pub argument",
            "result": "TARGET_SHARP",
            "what_it_proves": "would set c_g=0 and align matter/source/readout with the GR/Newton spine",
            "why_not_enough": "target statement is not itself a derivation",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_1_covariance_test",
            "attempt": "derive no shadow frame from diffeomorphism covariance",
            "mathematical_form": "S_m[Psi,A_g(Xhat)^2 g_obs] is still diffeomorphism covariant",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "what_it_proves": "covariance constrains tensor form and Ward identities",
            "why_not_enough": "covariance does not forbid a scalar conformal factor or common Jordan frame",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_2_WEP_test",
            "attempt": "derive c_g=0 from WEP/universality",
            "mathematical_form": "A_g is common to all species so eta_AB can vanish while c_g is nonzero",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "what_it_proves": "composition dependence is absent for the common frame piece",
            "why_not_enough": "common coupling still sources fifth-force, PPN, clock/common-mode, or source-normalization effects",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_3_Ward_test",
            "attempt": "derive single source/matter frame from Ward conservation",
            "mathematical_form": "nabla_mu T^{mu nu}=0 also holds for many covariant actions with A_g(Xhat)",
            "result": "FAILS_UNCONDITIONAL_DERIVATION",
            "what_it_proves": "on-shell conservation in whatever matter geometry is chosen",
            "why_not_enough": "Ward identities are homogeneous under hidden common-frame or source-weight choices",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_4_minimal_action_test",
            "attempt": "derive no shadow frame from minimal matter action",
            "mathematical_form": "S_m=sum_A S_A[Psi_A,e_pub,theta_A] excludes A_g only if this is the full allowed action domain",
            "result": "CONDITIONAL_PARENT_SCHEMA",
            "what_it_proves": "if parent minimality is signed, c_g and source-only frame coefficients are absent by construction",
            "why_not_enough": "minimality cannot be smuggled in as taste; it must be derived from quotient/domain rules",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_5_quotient_naturality_route",
            "attempt": "derive no shadow frame from quotient naturality and a terminal public metric object",
            "mathematical_form": "Matter functor domain is Q_obs with terminal e_pub; any observable frame map factors uniquely through e_pub",
            "result": "BEST_DERIVATION_ROUTE_CONDITIONAL",
            "what_it_proves": "A_g(Xhat) is either quotient-owned, hence vertical-constant, or not an allowed ordinary matter argument",
            "why_not_enough": "the parent corpus has not proved terminal e_pub/ordinary-matter-domain uniqueness",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SPD1030_6_verdict",
            "attempt": "single-public-metric parent action theorem",
            "mathematical_form": "quotient naturality + terminal e_pub + no extra matter-frame slots => c_g=0 and source/readout same-frame",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "what_it_proves": "exact theorem target is now isolated",
            "why_not_enough": "terminal public metric and no-extra-slot are not yet parent-derived",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM1030_0_common_Jordan_frame",
            "allowed_by": "diffeomorphism covariance; universal matter coupling; WEP quiet",
            "construction": "S_m[Psi,A_g(Xhat)^2 g_obs,theta]",
            "blocks": "covariance/WEP proof of c_g=0",
            "repair": "derive terminal public metric/no-extra-frame action domain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1030_1_species_weighted_source",
            "allowed_by": "Ward conservation and additivity",
            "construction": "S_source=sum_A kappa_A int e_obs T_A with constant or marker-dependent kappa_A",
            "blocks": "Ward-to-single-source proof",
            "repair": "derive label-forgetting/source-domain uniqueness",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1030_2_frame_renamed_constants",
            "allowed_by": "field redefinition without full ledger",
            "construction": "remove A_g from metric and put it into m_A(Xhat), alpha_EM(Xhat), or G_eff(Xhat)",
            "blocks": "notation-only matter frame proof",
            "repair": "same ledger for metric, constants, clocks, source normalization, and support",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1030_3_disformal_shadow",
            "allowed_by": "single conformal metric check only",
            "construction": "g_m=A_g^2 g_obs+B_g(Xhat)U_mu U_nu",
            "blocks": "c_g-only closure of local frame leak",
            "repair": "include b_dis in no-shadow theorem or retain b_dis bound row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_action_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "SPM1030_0_public_metric_object",
            "required_clause": "parent defines one public observed coframe/metric object",
            "mathematical_form": "e_pub=e_obs(q(Phi)); all ordinary rods, clocks, photons, free fall, and source readout use e_pub",
            "would_close": "observed-frame uniqueness through tested local order",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "test_or_gate": "q-kernel and Obs_e uniqueness certificate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_1_matter_functor_domain",
            "required_clause": "ordinary matter functor has no representative-field argument",
            "mathematical_form": "S_matter: Q_obs x MatterFields x Theta_Q -> R, not S_matter[Phi_rep]",
            "would_close": "vertical representative variables cannot enter matter action",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "test_or_gate": "terminal public metric / quotient naturality proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_2_no_shadow_frame_slot",
            "required_clause": "no A_g(Xhat)e_pub or B_g(Xhat) disformal shadow frame slot",
            "mathematical_form": "Allowed[S_matter] excludes independent A_g(Xhat), B_g(Xhat), U_mu shadow-frame coefficients",
            "would_close": "c_g=0 and b_dis=0 by action-domain exclusion",
            "current_status": "EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
            "test_or_gate": "no-shadow-frame theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_3_total_Hilbert_source",
            "required_clause": "active source is total Hilbert/coframe variation of the same matter action",
            "mathematical_form": "T_total := delta S_matter / delta e_pub; E_geom = kappa_univ T_total + retained residuals",
            "would_close": "source-side GR/Newton structure after common G calibration",
            "current_status": "CONDITIONAL_FROM_954_955_956",
            "test_or_gate": "no source-only species weights, no hidden source current",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_4_constants_quotient_owned",
            "required_clause": "masses, charges, and clock constants are quotient-owned or retained",
            "mathematical_form": "theta_A=theta_A(q) or finite b_A/b_alpha rows; no hidden marker constants",
            "would_close": "no field-rename hiding of A_g into constants",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "test_or_gate": "constant superselection/no-marker theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_5_hidden_current_silence",
            "required_clause": "non-Hilbert, boundary, and support-shift source tails are zero or retained",
            "mathematical_form": "DeltaJ_hidden=q_nonH+Delta_W_support+domain/boundary terms = 0 or bounded",
            "would_close": "prevents local-GR source claim from riding only on c_g=0",
            "current_status": "OPEN_RETAINED_RESIDUAL",
            "test_or_gate": "source-support/local projection theorem or numeric row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "SPM1030_6_contract_verdict",
            "required_clause": "single-public-metric parent action contract",
            "mathematical_form": "SPM1030_0 through SPM1030_5 all parent-signed",
            "would_close": "right-hand matter/source side of local GR/Newton spine up to left-hand EH/Newton gates",
            "current_status": "CONTRACT_READY_NOT_CURRENT_THEOREM",
            "test_or_gate": "do not claim local GR until signed and left-hand field equation limit closes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def cg_provenance_binding_rows() -> list[dict[str, str]]:
    return [
        {
            "binding_id": "CPG1030_0_zero_branch",
            "coefficient_symbol": "c_g",
            "branch": "zero theorem",
            "required_before_score": "SPM1030_0 through SPM1030_3 parent-signed plus q-kernel ownership",
            "current_status": "MISSING_PARENT_THEOREM",
            "provenance_gate_result": "REJECTED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "binding_id": "CPG1030_1_finite_cg_value",
            "coefficient_symbol": "c_g",
            "branch": "finite value",
            "required_before_score": "numeric c_g, units, source path, source row id, derivation status, and claim policy",
            "current_status": "MISSING_PARENT_INPUT_AND_SOURCE",
            "provenance_gate_result": "REJECTED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "binding_id": "CPG1030_2_tau_R10",
            "coefficient_symbol": "tau_R10",
            "branch": "R10 projection",
            "required_before_score": "K_X(lambda), Qbar_XH, source/test profile convention, tau_R10, and R10 bound curve link",
            "current_status": "MISSING_ARENA_PROJECTION",
            "provenance_gate_result": "REJECTED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "binding_id": "CPG1030_3_tau_PPN",
            "coefficient_symbol": "tau_PPN",
            "branch": "PPN projection",
            "required_before_score": "M_gamma, M_beta, gauge, profile, disformal separation, and weak-field response matrix",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "provenance_gate_result": "REJECTED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "binding_id": "CPG1030_4_no_cancellation",
            "coefficient_symbol": "c_g;b_A;b_alpha;b_dis;q_nonH;Delta_W_support",
            "branch": "aggregate local envelope",
            "required_before_score": "each retained component theorem-zero or numeric/source-backed; no cancellation between unknowns",
            "current_status": "ABSOLUTE_ENVELOPE_REQUIRED",
            "provenance_gate_result": "REJECTED_FOR_CLAIM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1030_0_sources",
            "claim": "all 1030 cited sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1030_1_single_public_metric_theorem",
            "claim": "single-public-metric parent action theorem is derived",
            "gate_pass": "false",
            "reason": "SPD1030_6 is not derived in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1030_2_cg_zero",
            "claim": "c_g=0 follows for current MTS",
            "gate_pass": "false",
            "reason": "no-extra-frame slot and q-kernel ownership are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1030_3_cg_provenance",
            "claim": "finite c_g/tau rows can be scored",
            "gate_pass": "false",
            "reason": "provenance bindings reject missing parent input, source path, and arena projections",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1030_4_GR_Newton",
            "claim": "local GR/Newton reduction is established",
            "gate_pass": "false",
            "reason": "right-hand matter/source side is only a contract; left-hand EH/Newton and hidden residual gates remain separate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1030_0_failed_shortcuts",
            "decision": "Covariance, WEP, and Ward identities do not derive the single public metric.",
            "because": "common conformal frames and weighted source currents remain legal countermodels.",
            "next_action": "stop using those as proof of c_g=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1030_1_best_derivation_route",
            "decision": "The best derivation route is quotient naturality plus terminal public metric.",
            "because": "if ordinary matter functors only see the terminal public metric object of Q_obs, an A_g(Xhat) shadow frame is not an allowed argument.",
            "next_action": "attempt terminal public metric proof directly",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1030_2_contract_status",
            "decision": "The single-public-metric action contract is written but not current theorem.",
            "because": "it states exactly what would close c_g, source-side matter coupling, and frame/readout alignment, but it is still parent-signature work.",
            "next_action": "do not claim c_g zero or local GR from the contract alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1030_3_next_target",
            "decision": "Next target is terminal public metric proof or explicit SPM closure.",
            "because": "terminal e_pub is the last clean chance to derive the no-extra-frame slot rather than declaring it.",
            "next_action": "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
            "objective": "try to prove that the ordinary-observable quotient category has a terminal public metric/coframe object, forcing all ordinary matter/readout functors to factor through it; if this cannot be derived, demote the single-public-metric route to explicit closure and continue finite c_g/tau provenance",
            "include": "Q_obs category, terminal e_pub object, matter functor domain, naturality, no A_g shadow-frame argument, no field-rename hiding, closure/demotion rule, c_g provenance fallback",
            "exclude": "covariance-only proof, WEP-only proof, Ward-only proof, notation-only frame choice, placeholder numeric values, R10/PPN/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    derivation: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    contract: list[dict[str, str]],
    provenance: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    derivation_required = {f"SPD1030_{idx}_{name}" for idx, name in [
        (0, "target"),
        (1, "covariance_test"),
        (2, "WEP_test"),
        (3, "Ward_test"),
        (4, "minimal_action_test"),
        (5, "quotient_naturality_route"),
        (6, "verdict"),
    ]}
    contract_required = {f"SPM1030_{idx}_{name}" for idx, name in [
        (0, "public_metric_object"),
        (1, "matter_functor_domain"),
        (2, "no_shadow_frame_slot"),
        (3, "total_Hilbert_source"),
        (4, "constants_quotient_owned"),
        (5, "hidden_current_silence"),
        (6, "contract_verdict"),
    ]}
    provenance_required = {f"CPG1030_{idx}_{name}" for idx, name in [
        (0, "zero_branch"),
        (1, "finite_cg_value"),
        (2, "tau_R10"),
        (3, "tau_PPN"),
        (4, "no_cancellation"),
    ]}
    checks = [
        ("V1030_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1030_1_derivation_rows_complete", derivation_required.issubset({row["audit_id"] for row in derivation}), "derivation audit covers target, covariance, WEP, Ward, minimality, quotient naturality, and verdict"),
        ("V1030_2_shortcuts_rejected", all(row["result"] == "FAILS_UNCONDITIONAL_DERIVATION" for row in derivation if row["audit_id"] in {"SPD1030_1_covariance_test", "SPD1030_2_WEP_test", "SPD1030_3_Ward_test"}), "covariance/WEP/Ward shortcuts are explicitly rejected"),
        ("V1030_3_theorem_not_claimed", any(row["audit_id"] == "SPD1030_6_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in derivation), "single-public-metric theorem remains nonclaim"),
        ("V1030_4_countermodels_present", len(countermodels) >= 4 and all(row["valid_for_claim"] == "false" for row in countermodels), "countermodels block shortcut derivations"),
        ("V1030_5_contract_complete", contract_required.issubset({row["contract_id"] for row in contract}), "single-public-metric contract covers public metric, functor domain, no shadow slot, Hilbert source, constants, hidden currents, and verdict"),
        ("V1030_6_contract_nonclaim", all(row["valid_for_claim"] == "false" for row in contract), "contract is not promoted to theorem"),
        ("V1030_7_provenance_bindings_complete", provenance_required.issubset({row["binding_id"] for row in provenance}), "c_g provenance bindings cover zero branch, finite value, tau_R10, tau_PPN, and no-cancellation"),
        ("V1030_8_provenance_rejects", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in provenance), "provenance rows reject placeholder scoring"),
        ("V1030_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1030_10_decision_next", any(row["decision_id"] == "DEC1030_3_next_target" for row in decisions), "decision ledger selects the 1031 target"),
        ("V1030_11_next_target_written", len(next_target) == 1 and "1031-Y5-R10-quotient-naturality" in next_target[0]["next_target"], "1031 next target row is present"),
        ("V1030_12_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, derivation, countermodels, contract, provenance, gates, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1030_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1030_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1030 single-public-metric parent action validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    derivation: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    contract: list[dict[str, str]],
    provenance: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1030 Y5 R10 single-public-metric parent action derivation or c_g provenance gate",
            "",
            "**Status:** The shortcut routes fail cleanly: covariance, WEP, and Ward identities do not derive the absence of a shadow matter frame. The strongest route is now isolated: prove quotient naturality plus a terminal public metric/coframe object for ordinary observables. If that terminal object is parent-signed, the no-extra-frame slot follows and `c_g=0`; if not, `c_g` remains a finite coefficient under the 1029/951 provenance gates.",
            "",
            "**Claim ceiling:** no single-public-metric theorem, `c_g=0`, finite-`c_g` score, R10, PPN, WEP, clock, orbital, local-GR/Newton, or source-side GR pass is allowed from 1030.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Derivation audit",
            md_table(derivation, ["audit_id", "attempt", "mathematical_form", "result", "what_it_proves", "why_not_enough", "parent_signed", "valid_for_claim"]),
            "## Countermodel ledger",
            md_table(countermodels, ["countermodel_id", "allowed_by", "construction", "blocks", "repair", "valid_for_claim"]),
            "## Single-public-metric parent action contract",
            md_table(contract, ["contract_id", "required_clause", "mathematical_form", "would_close", "current_status", "test_or_gate", "valid_for_claim"]),
            "## c_g provenance gate binding",
            md_table(provenance, ["binding_id", "coefficient_symbol", "branch", "required_before_score", "current_status", "provenance_gate_result", "claim_allowed", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    derivation = derivation_audit_rows()
    countermodels = countermodel_rows()
    contract = parent_action_contract_rows()
    provenance = cg_provenance_binding_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, derivation, countermodels, contract, provenance, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1030_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1030_SINGLE_PUBLIC_METRIC_DERIVATION_AUDIT.csv", derivation)
    write_csv(OUT / "P8_Y5_R10_1030_COUNTERMODEL_LEDGER.csv", countermodels)
    write_csv(OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv", provenance)
    write_csv(OUT / "P8_Y5_R10_1030_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1030_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1030_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1030_VALIDATION.csv", validations)
    write_doc(sources, derivation, countermodels, contract, provenance, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
