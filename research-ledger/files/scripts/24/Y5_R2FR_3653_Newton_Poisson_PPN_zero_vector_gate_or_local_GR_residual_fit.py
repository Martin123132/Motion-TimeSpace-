from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3653"
BRANCH_ID = "MTS_R2FR_Y5_NEWTON_POISSON_PPN_ZERO_VECTOR_GATE_OR_LOCAL_GR_RESIDUAL_FIT_3653"
DOC = ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md"


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


def source_register(ts: str) -> list[dict[str, object]]:
    bounds = LOCAL_BOUNDS / "local_bound_claims.csv"
    specs = [
        ("next_3652", RESIDUALS / "P8_Y5_R2FR_3652_NEXT_TARGET.csv", "Newton-Poisson-PPN-zero-vector", "3652 selected local-GR zero-vector gate"),
        ("doc_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "Delta_PPN_MTS", "3652 fitted-GM/source Hamiltonian result"),
        ("theorem_3652", RESIDUALS / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv", "LOCAL_GR_CONTRACT_DERIVED", "3652 local-GR contract"),
        ("calibration_3652", RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "q_GM_source_abs", "3652 GM/source residual row"),
        ("residual_3652", RESIDUALS / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv", "PVR3652_0_gamma", "3652 PPN/orbital residual vector"),
        ("projection_3652", RESIDUALS / "P8_Y5_R2FR_3652_PROJECTION_ROWS.csv", "Newtonian_Poisson", "3652 local projection rows"),
        ("doc_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "EH_plus_Lambda_baseline", "EH retained ledger and baseline policy"),
        ("doc_02", ROOT / "02-motion-load-local-GR-reduction.md", "motion_load_local_GR_reduction_conditional_not_promoted", "early local-GR reduction caveat"),
        ("matrix_1048", RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "BM1048_4_PPN_source", "PPN source bound matrix"),
        ("bounds_R3", bounds, "R3_gamma", "Cassini gamma anchor"),
        ("bounds_R4", bounds, "R4_beta", "PPN beta anchor"),
        ("bounds_R5", bounds, "R5_alpha1", "alpha1 bound anchor"),
        ("bounds_R6", bounds, "R6_alpha2", "alpha2 bound anchor"),
        ("bounds_R7", bounds, "R7_alpha3", "alpha3 bound anchor"),
        ("bounds_R8", bounds, "R8_xi", "xi bound anchor"),
        ("bounds_R9", bounds, "R9_Gdot", "Gdot bound anchor"),
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


def theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "theorem_id": "NPG3653_0_parent_EH_weak_field",
            "claim": "EH weak-field GR coefficients follow if the parent action reduces to the same-frame Einstein-Hilbert action with owned source.",
            "mathematical_form": "S_loc=(16*pi*G_N)^-1 int sqrt(-g)(R-2Lambda) + S_matter[g_obs,Psi,theta_rep]; g00=-1+2U/c^2-2U^2/c^4+O(c^-6), gij=(1+2U/c^2)delta_ij+O(c^-4), g0i=O(c^-3).",
            "derivation_step": "The EH variation plus conserved same-frame stress gives G_{mu nu}=8*pi*G_N*T_{mu nu}; the standard weak-field expansion then yields gamma=1, beta=1, alpha_i=xi=0, and Gdot=0 when all retained residual channels vanish.",
            "result": "The metric side of local GR is conditionally derivable, but only with source/readout/boundary/non-EH silence.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent-signed EH dominance, source identity, readout, boundary, and non-EH silence",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_1_Poisson_zero_gate",
            "claim": "Newton-Poisson is the c^-2 part of the same local-GR branch.",
            "mathematical_form": "nabla^2 Phi_N = 4*pi*G_N*rho_inertial iff q_Poisson = q_metric_Poisson + q_source + q_readout + q_boundary + q_nonEH = 0.",
            "derivation_step": "The 00 field equation gives Poisson only after the active source equals the inertial source and no boundary/operator/readout term contributes at Newtonian order.",
            "result": "Newton's law is not just fitted GM; it is a zero condition on the Poisson source channel.",
            "status": "NEWTON_POISSON_ZERO_CONDITION_DERIVED",
            "missing_for_claim": "active/inertial source identity plus Newtonian-order residual silence",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_2_PPN_coefficient_gate",
            "claim": "The full PPN vector is the correct local-GR observable gate.",
            "mathematical_form": "Delta_PPN_MTS=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G)=P_EH[h00,hij,h0i]+P_source+P_readout+P_boundary+P_nonEH+P_frame+P_time.",
            "derivation_step": "Second-order metric coefficients control gamma/beta; vector and frame terms control alpha_i; background/location terms control xi; time drift in G_N/source/readout controls Gdot.",
            "result": "A local-GR claim requires the whole vector to be zero or below bounds with a common source/readout convention.",
            "status": "PPN_ZERO_VECTOR_CONDITION_DERIVED",
            "missing_for_claim": "all PPN components and common convention map",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_3_nonEH_operator_gate",
            "claim": "Non-EH operators must be absent, topological/boundary-only, or numerically bounded.",
            "mathematical_form": "Delta L_nonEH = sum_i c_i O_i[g,q,X,boundary]; local GR requires P_PPN[delta O_i]=0 or |P_PPN[delta O_i]| <= bound_i with no cancellation assumption.",
            "derivation_step": "Higher-curvature, disformal, boundary, preferred-frame, and memory terms can re-enter PPN even when the EH core exists.",
            "result": "EH presence is not EH dominance; the retained non-EH vector remains a gate.",
            "status": "NON_EH_RESIDUAL_GATE_DERIVED",
            "missing_for_claim": "operator classification/dominance theorem or coefficient bounds",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_4_common_frame_source_readout_gate",
            "claim": "Metric, matter, clocks, EM, and source calibration must share one observed frame.",
            "mathematical_form": "g_obs=e_obs(q)^T eta e_obs(q); T_matter=T_matter[g_obs,Psi,theta_rep]; clocks=nu_bar(q,theta_rep); sources=M_bar(q,theta_rep); no g_shadow, no e_shadow, no source-only frame.",
            "derivation_step": "PPN comparisons use light propagation, clock readout, source mass, and orbit fits together. A frame mismatch can fake agreement in one component while failing another.",
            "result": "The local-GR gate includes no-shadow/no-source-only-frame conditions.",
            "status": "COMMON_FRAME_GATE_DERIVED",
            "missing_for_claim": "parent-signed common observed frame across matter/EM/clock/source sectors",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_5_residual_bound_rule",
            "claim": "If zero is not signed, the replacement is a bounded residual vector, not a claim.",
            "mathematical_form": "Delta_local_GR_abs = |q_Poisson| + |delta_gamma| + |delta_beta| + |alpha1| + |alpha2| + |alpha3| + |xi| + |Gdot/G|_norm + |q_source| + |q_readout| + |q_boundary| + |q_nonEH|.",
            "derivation_step": "The no-cancellation policy turns every missing theorem into an absolute-envelope row linked to the relevant local bound.",
            "result": "This gives a scoreable future path without smuggling closure.",
            "status": "NO_CANCELLATION_RESIDUAL_RULE_DERIVED",
            "missing_for_claim": "numeric/source-backed residual components",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_6_baseline_comparator_policy",
            "claim": "MTS local tests must compare against the GR/null baseline in the same pipeline.",
            "mathematical_form": "score(MTS)=Compare[Delta_local_GR_MTS, bounds, baseline=(GR/null vector)] with identical source/readout/bound conventions.",
            "derivation_step": "A failed jackknife or bound-runner check is only meaningful if the GR/null baseline is run through the same data pipeline.",
            "result": "The gate now encodes the user's correct criticism: test MTS and the comparator together.",
            "status": "BASELINE_COMPARATOR_POLICY_DERIVED",
            "missing_for_claim": "executable comparator run with real residual values",
        },
        {
            **base(ts),
            "theorem_id": "NPG3653_7_verdict",
            "claim": "Current MTS proves Newton-Poisson and the PPN-GR zero vector.",
            "mathematical_form": "NPG3653_0 through NPG3653_6 parent-signed => local GR/Newton pass; otherwise retain Delta_local_GR_abs and component rows.",
            "derivation_step": "The exact contract is now explicit, but current corpus does not sign EH dominance, source identity, readout, boundary, non-EH, and PPN coefficients as one branch.",
            "result": "Current MTS has a serious local-GR gate, not yet a local-GR pass.",
            "status": "FAIL_CURRENT_CLAIM_LOCAL_GR_ZERO_VECTOR_UNSIGNED",
            "missing_for_claim": "parent-signed zero certificate or numeric residual fit",
        },
    ]


def zero_contract_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("ZC3653_0_EH_action", "q_EH_action", "local action is EH+Lambda in the observed frame", "dimensionless pass/fail or coefficient", "EH dominance theorem or non-EH coefficient ledger", "PARENT_EH_DOMINANCE_UNSIGNED", "Newton;PPN"),
        ("ZC3653_1_EH_prefactor", "q_GN_prefactor", "G_N prefactor is fixed and same as source/orbital calibration", "dimensionless", "source-calibrated EH prefactor theorem", "GN_PREFACTOR_OWNER_UNSIGNED", "Newton;PPN;Gdot"),
        ("ZC3653_2_Poisson_source", "q_Poisson_source", "active source equals inertial source in Poisson equation", "dimensionless", "weak-field source Hamiltonian theorem", "ACTIVE_INERTIAL_SOURCE_UNSIGNED", "Newton;WEP;orbital"),
        ("ZC3653_3_metric_second_order", "q_metric_PPN", "metric h00/hij/h0i coefficients match GR through PPN order", "dimensionless vector", "weak-field metric coefficient derivation", "PPN_METRIC_COEFFICIENTS_UNSIGNED", "PPN"),
        ("ZC3653_4_readout", "q_readout_PPN", "clock/light/ruler readout uses same observed frame", "dimensionless vector", "no-shadow readout theorem", "READOUT_FRAME_UNSIGNED", "clock;PPN;EM"),
        ("ZC3653_5_boundary", "q_boundary_PPN", "boundary/domain terms do not contribute to local PPN", "dimensionless vector", "boundary silence/exactness theorem", "BOUNDARY_DOMAIN_UNSIGNED", "PPN;Gdot;orbital"),
        ("ZC3653_6_nonEH", "q_nonEH_PPN", "all non-EH operators are absent/topological/bounded below local limits", "dimensionless vector", "non-EH operator classification/dominance theorem", "NON_EH_OPERATOR_VECTOR_UNSIGNED", "PPN;Newton;R10"),
        ("ZC3653_7_source_coupling", "q_source_coupling_PPN", "EM/mass/source coupling rows from 3650-3652 are zero or bounded", "dimensionless vector", "Q_A_X;f_EM;b_alpha;q_GM_source_abs", "SOURCE_COUPLING_VECTOR_UNSIGNED", "WEP;R10;PPN;orbital"),
        ("ZC3653_8_time_drift", "q_time_drift", "G_N/source/readout drift vanishes or is below Gdot bound", "yr^-1 normalized", "Gdot source/readout theorem", "TIME_DRIFT_UNSIGNED", "Gdot;clock;orbital"),
        ("ZC3653_9_total", "Delta_local_GR_abs", "absolute local-GR residual envelope across all Newton/PPN/source/readout/boundary/non-EH rows", "mixed normalized vector", "all components theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **row,
            "contract_id": contract_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_evidence": required,
            "current_status": status,
            "observable_links": links,
        }
        for contract_id, symbol, definition, units, required, status, links in specs
    ]


def residual_component_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("LGR3653_0_Poisson", "q_Poisson", "Newtonian Poisson residual from metric/source/boundary/non-EH terms", "dimensionless", "q_metric_Poisson+q_source+q_boundary+q_nonEH", "NEWTON_COMPONENTS_REQUIRED", "Newtonian_Poisson"),
        ("LGR3653_1_gamma", "delta_gamma_MTS", "gamma-1 residual", "dimensionless", "P_metric_gamma+P_source_gamma+P_readout_gamma+P_boundary_gamma+P_nonEH_gamma", "GAMMA_COMPONENTS_REQUIRED", "R3_gamma"),
        ("LGR3653_2_beta", "delta_beta_MTS", "beta-1 residual", "dimensionless", "P_metric_beta+P_source_beta+P_readout_beta+P_boundary_beta+P_nonEH_beta", "BETA_COMPONENTS_REQUIRED", "R4_beta"),
        ("LGR3653_3_alpha1", "alpha1_MTS", "preferred-frame alpha1 residual", "dimensionless", "frame/source-current/boundary vector terms", "ALPHA1_COMPONENTS_REQUIRED", "R5_alpha1"),
        ("LGR3653_4_alpha2", "alpha2_MTS", "preferred-frame alpha2 residual", "dimensionless", "frame/spin/source/boundary terms", "ALPHA2_COMPONENTS_REQUIRED", "R6_alpha2"),
        ("LGR3653_5_alpha3", "alpha3_MTS", "momentum/flux alpha3 residual", "dimensionless", "source flux/boundary/nonconservation terms", "ALPHA3_COMPONENTS_REQUIRED", "R7_alpha3"),
        ("LGR3653_6_xi", "xi_MTS", "preferred-location xi residual", "dimensionless", "background/source/boundary/domain terms", "XI_COMPONENTS_REQUIRED", "R8_xi"),
        ("LGR3653_7_Gdot", "Gdot_over_G_MTS", "time drift in G/source/readout", "yr^-1", "d_t ln G_N + d_t ln M_source + readout drift", "GDOT_COMPONENTS_REQUIRED", "R9_Gdot"),
        ("LGR3653_8_source", "q_source_PPN_abs", "absolute source-calibration contribution to PPN vector", "dimensionless", "q_GM_source_abs;Q_source_X;rho_active_minus_inertial", "SOURCE_VECTOR_REQUIRED", "PPN;WEP;R10;orbital"),
        ("LGR3653_9_readout", "q_readout_PPN_abs", "absolute clock/light/ruler readout contribution", "dimensionless", "b_clock;b_alpha;b_Hodge;common frame", "READOUT_VECTOR_REQUIRED", "clock;PPN;EM"),
        ("LGR3653_10_boundary", "q_boundary_PPN_abs", "absolute boundary/domain contribution", "dimensionless", "boundary flux/exactness/domain certificate", "BOUNDARY_VECTOR_REQUIRED", "PPN;orbital;Gdot"),
        ("LGR3653_11_nonEH", "q_nonEH_PPN_abs", "absolute non-EH operator contribution", "dimensionless", "non-EH operator coefficient vector", "NON_EH_VECTOR_REQUIRED", "PPN;Newton"),
        ("LGR3653_12_total", "Delta_local_GR_abs", "sum of absolute local-GR residual components", "mixed normalized vector", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **row,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "formula_or_required_inputs": formula,
            "current_status": status,
            "observable_links": links,
        }
        for row_id, symbol, definition, units, formula, status, links in specs
    ]


def bound_interface_rows(ts: str) -> list[dict[str, object]]:
    row = {**base(ts), "score_ready": False}
    specs = [
        ("BI3653_0_gamma", "gamma_minus_1", "delta_gamma_MTS", "R3_gamma", "2.3e-05", "dimensionless"),
        ("BI3653_1_beta", "beta_minus_1", "delta_beta_MTS", "R4_beta", "7.8e-05", "dimensionless"),
        ("BI3653_2_alpha1", "alpha1", "alpha1_MTS", "R5_alpha1", "1e-04", "dimensionless"),
        ("BI3653_3_alpha2", "alpha2", "alpha2_MTS", "R6_alpha2", "2e-09", "dimensionless"),
        ("BI3653_4_alpha3", "alpha3", "alpha3_MTS", "R7_alpha3", "4e-20", "dimensionless"),
        ("BI3653_5_xi", "xi", "xi_MTS", "R8_xi", "4e-09", "dimensionless"),
        ("BI3653_6_Gdot", "Gdot_over_G", "Gdot_over_G_MTS", "R9_Gdot", "9.6e-15", "yr^-1"),
        ("BI3653_7_Poisson", "Poisson_source_identity", "q_Poisson", "R11_EH_operator_ledger", "symbolic", "dimensionless"),
        ("BI3653_8_total", "local_GR_residual_envelope", "Delta_local_GR_abs", "R3-R9 plus R11", "vector", "mixed normalized vector"),
    ]
    return [
        {
            **row,
            "interface_id": interface_id,
            "observable": observable,
            "mts_symbol": symbol,
            "bound_row": bound_row,
            "upper_bound_or_status": bound,
            "units": units,
            "current_status": "BOUND_ANCHOR_READY_MTS_VALUE_MISSING" if "R3" in bound_row or "R4" in bound_row or "R5" in bound_row or "R6" in bound_row or "R7" in bound_row or "R8" in bound_row or "R9" in bound_row else "SYMBOLIC_GATE_REQUIRED",
        }
        for interface_id, observable, symbol, bound_row, bound, units in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "decision_id": "DEC3653_0_gate",
            "decision": "Newton-Poisson and PPN are now one local-GR zero-vector gate, not separate claim fragments.",
            "status": "NEWTON_PPN_ZERO_VECTOR_GATE_DERIVED",
        },
        {
            **base(ts),
            "decision_id": "DEC3653_1_verdict",
            "decision": "Current MTS does not sign EH dominance, source identity, readout, boundary, non-EH, and PPN coefficient zeros together.",
            "status": "PARENT_LOCAL_GR_ZERO_VECTOR_UNSIGNED",
        },
        {
            **base(ts),
            "decision_id": "DEC3653_2_residuals",
            "decision": "Local-GR residual rows are staged with units, bound anchors, source/readout/boundary/non-EH components, and no-cancellation guards.",
            "status": "LOCAL_GR_RESIDUAL_VECTOR_CREATED_NOT_SCORE_READY",
        },
        {
            **base(ts),
            "decision_id": "DEC3653_3_next",
            "decision": "Next target is an executable local-GR residual comparator/dry-run that runs the GR/null baseline and MTS residual vector through the same interface.",
            "status": "LOCAL_GR_COMPARATOR_DRYRUN_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "NEWTON_PPN_ZERO_VECTOR_GATE_DERIVED_LOCAL_GR_RESIDUALS_NONCLAIM",
            "summary": "3653 derives the Newton-Poisson/PPN zero-vector gate and creates a nonclaim local-GR residual component interface with bound anchors.",
            "claim_ceiling": "no Newtonian, PPN, local-GR, source-calibration, WEP, R10, clock, orbital, or EH-dominance pass is claimed",
            "useful_result": "The local-GR target is now a precise contract: sign every zero condition in one parent branch, or run a bounded residual vector against a GR/null baseline.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3653_0",
            "target_doc": "3654-Y5-R2FR-local-GR-residual-comparator-dryrun-or-parent-zero-certificate.md",
            "target_script": "scripts/Y5_R2FR_3654_local_GR_residual_comparator_dryrun_or_parent_zero_certificate.py",
            "objective": "build a dry-run comparator that evaluates the GR/null baseline and MTS local-GR residual vector through the same Newton/PPN bound interface, or accepts a parent zero certificate if every component is signed",
            "success_gate": "baseline rows, MTS residual rows, bound anchors, source paths, units, no-cancellation policy, and claim gates all validate without treating placeholders as evidence",
        }
    ]


def write_doc(sources, theorem, contracts, residuals, bounds, decisions, status, next_target) -> None:
    lines = [
        "# 3653 - Newton-Poisson PPN zero-vector gate or local-GR residual fit",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The local-GR target is now a vector gate, not a mood. Newton-Poisson requires `nabla^2 Phi_N = 4*pi*G_N*rho_inertial` with active/inertial source identity and no Newtonian-order residuals. PPN requires `Delta_PPN_MTS=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G)=0` with the same source, readout, boundary, and non-EH conventions.",
        "",
        "Current MTS does not yet sign those clauses as one parent branch. Therefore the correct fallback is `Delta_local_GR_abs`, an absolute-envelope residual vector with bound anchors and a future GR/null baseline comparator.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: `{row['status']}` — {row['result']}")
    lines.extend(["", "## Zero-contract rows"])
    for row in contracts:
        lines.append(f"- `{row['contract_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Local-GR residual rows"])
    for row in residuals:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Bound interface rows"])
    for row in bounds:
        lines.append(f"- `{row['interface_id']}`: `{row['mts_symbol']}` -> `{row['bound_row']}` — {row['current_status']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` — {row['decision']}")
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


def validate(ts, output_paths, sources, theorem, contracts, residuals, bounds, decisions, status, next_target):
    rows = []

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

    add("VAL3653_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3653_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3653_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3653 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3653_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3653_4_EH_weak_field", any("g00=-1+2U/c^2" in row["mathematical_form"] for row in theorem), "EH weak-field metric expansion present")
    add("VAL3653_5_Poisson_zero", any("nabla^2 Phi_N" in row["mathematical_form"] and "q_Poisson" in row["mathematical_form"] for row in theorem), "Newton-Poisson zero condition present")
    add("VAL3653_6_PPN_vector", any("Delta_PPN_MTS" in row["mathematical_form"] for row in theorem), "PPN zero-vector condition present")
    add("VAL3653_7_nonEH_gate", any(row["status"] == "NON_EH_RESIDUAL_GATE_DERIVED" for row in theorem), "non-EH residual gate present")
    add("VAL3653_8_baseline_policy", any(row["status"] == "BASELINE_COMPARATOR_POLICY_DERIVED" for row in theorem), "GR/null baseline comparator policy present")
    add("VAL3653_9_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_LOCAL_GR_ZERO_VECTOR_UNSIGNED" for row in theorem), "local-GR pass not claimed")
    required_contracts = {"q_EH_action", "q_GN_prefactor", "q_Poisson_source", "q_metric_PPN", "q_readout_PPN", "q_boundary_PPN", "q_nonEH_PPN", "q_source_coupling_PPN", "q_time_drift", "Delta_local_GR_abs"}
    add("VAL3653_10_contract_rows_complete", required_contracts.issubset({row["symbol"] for row in contracts}), "zero-contract rows complete")
    required_residuals = {"q_Poisson", "delta_gamma_MTS", "delta_beta_MTS", "alpha1_MTS", "alpha2_MTS", "alpha3_MTS", "xi_MTS", "Gdot_over_G_MTS", "q_source_PPN_abs", "q_readout_PPN_abs", "q_boundary_PPN_abs", "q_nonEH_PPN_abs", "Delta_local_GR_abs"}
    add("VAL3653_11_residual_rows_complete", required_residuals.issubset({row["symbol"] for row in residuals}), "local-GR residual rows complete")
    required_bounds = {"R3_gamma", "R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi", "R9_Gdot", "R11_EH_operator_ledger", "R3-R9 plus R11"}
    add("VAL3653_12_bound_interface_complete", required_bounds.issubset({row["bound_row"] for row in bounds}), "PPN/local bound interface complete")
    add("VAL3653_13_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in contracts + residuals + bounds), "no generated rows score-ready")
    generated = sources + theorem + contracts + residuals + bounds + decisions + status + next_target
    add("VAL3653_14_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3653_15_no_cancellation", any(row["symbol"] == "Delta_local_GR_abs" and "sum of absolute" in row["definition"] for row in residuals), "local-GR no-cancellation envelope present")
    add("VAL3653_16_status_honest", status[0]["status"] == "NEWTON_PPN_ZERO_VECTOR_GATE_DERIVED_LOCAL_GR_RESIDUALS_NONCLAIM", "status keeps local-GR branch nonclaim")
    doc_text = read_text(DOC)
    add("VAL3653_17_doc_written", "Delta_PPN_MTS" in doc_text and "Current MTS does not yet sign" in doc_text and "GR/null baseline comparator" in doc_text, "doc records vector gate and caveat")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3653*", "3653-Y5-R2FR-*", "Y5_R2FR_3653_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3653_18_no_formalization_leak", not leaks, "no 3653 checkpoint files in formalization-workbench")
    add("VAL3653_19_next_target", next_target[0]["target_doc"].startswith("3654-") and "comparator" in next_target[0]["target_doc"], "3654 comparator target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = theorem_rows(ts)
    contracts = zero_contract_rows(ts)
    residuals = residual_component_rows(ts)
    bounds = bound_interface_rows(ts)
    decisions_list = decision_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3653_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3653_NEWTON_PPN_ZERO_VECTOR_THEOREM_ATTEMPT.csv",
        "contracts": RESIDUALS / "P8_Y5_R2FR_3653_ZERO_CONTRACT_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3653_LOCAL_GR_RESIDUAL_COMPONENT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3653_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3653_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3653_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3653_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["decisions"], decisions_list)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, contracts, residuals, bounds, decisions_list, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, contracts, residuals, bounds, decisions_list, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3653 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3653 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
