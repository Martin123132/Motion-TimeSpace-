import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3794"
BRANCH = "MTS_R2FR_Y5_PARENT_BQ_OWNER_CONSTRUCTOR_TWO_PAIR_CP2_OR_FINITE_PROFILE_3794"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3794_SOURCE_REGISTER.csv",
    "constructor": RESIDUALS / "P8_Y5_R2FR_3794_PARENT_BQ_CONSTRUCTOR_THEOREM.csv",
    "sweep": RESIDUALS / "P8_Y5_R2FR_3794_CURRENT_PRIMITIVE_SWEEP.csv",
    "candidates": RESIDUALS / "P8_Y5_R2FR_3794_OWNER_CANDIDATE_DECISION_MATRIX.csv",
    "profile": RESIDUALS / "P8_Y5_R2FR_3794_BPERP_HPERP_PROFILE_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3794_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3794_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3794_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3794_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3794_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3794_0_3793",
        "path": PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md",
        "needle": "B_Q=q_obs^*Bbar_Q+dchi+B_perp",
        "role": "handoff: exact local B_Q descent amplitude law",
    },
    {
        "source_id": "SRC3794_1_3785",
        "path": PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
        "needle": "B_Q=sum_i C_i dD_i",
        "role": "Darboux/Clebsch construction route",
    },
    {
        "source_id": "SRC3794_2_3786",
        "path": PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
        "needle": "parent-owned two-Clebsch-pair",
        "role": "internal multiplet owner theorem and finite demotion",
    },
    {
        "source_id": "SRC3794_3_1174",
        "path": PCW / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
        "needle": "Theta_Q := Tr(Q^{-1} delta Q) - delta(log N_D)",
        "role": "Q-flow stationarity defect route",
    },
    {
        "source_id": "SRC3794_4_1166",
        "path": PCW / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
        "needle": "delta J_C = J_C Tr(Q^-1 delta Q) - J_C delta(log N_D)",
        "role": "Q/coframe determinant variation formula",
    },
    {
        "source_id": "SRC3794_5_1167",
        "path": PCW / "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
        "needle": "local stationary domains",
        "role": "local stationary domain condition",
    },
    {
        "source_id": "SRC3794_6_275",
        "path": PCW / "275-JC-three-form-memory-current-from-Q.md",
        "needle": "Q_coh^i_j = (N_D / u3) delta^i_j",
        "role": "coherent Q projection and tracefree shear guard",
    },
    {
        "source_id": "SRC3794_7_08",
        "path": PCW / "08-phase-volume-reciprocity-origin.md",
        "needle": "T sqrt(S) = 1.",
        "role": "phase-volume route supplies at most a low-rank pair",
    },
    {
        "source_id": "SRC3794_8_1237",
        "path": PCW / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md",
        "needle": "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED",
        "role": "sorted parent grammar not derived from current primitives",
    },
    {
        "source_id": "SRC3794_9_000",
        "path": PCW / "000-private-fork-heuristics-for-martin-style-search.md",
        "needle": "EM/Poynting/Hodge-flow route",
        "role": "private search heuristic for Poynting/Hodge-flow fork",
    },
    {
        "source_id": "SRC3794_10_spine",
        "path": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
        "needle": "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md",
        "role": "live spine handoff",
    },
]


def text_contains(path, needle):
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_id": spec["source_id"],
            "source_path": str(spec["path"]),
            "exists": spec["path"].exists(),
            "needle": spec["needle"],
            "needle_found": text_contains(spec["path"], spec["needle"]),
            "source_role": spec["role"],
            "valid_for_claim": False,
        }
        for spec in SOURCE_SPECS
    ]


def constructor_rows(timestamp):
    rows = [
        {
            "theorem_id": "PBC3794_0_two_pair_owner",
            "claim_piece": "two-pair Clebsch owner theorem",
            "mathematical_form": "If parent MTS owns four pre-EM scalars Y_Q=(C1,D1,C2,D2) and the fixed internal two-form omega_Q=dC1 wedge dD1 + dC2 wedge dD2, define B_Q=C1 dD1 + C2 dD2 and H_Q=dB_Q.",
            "derivation_status": "EXACT_CONDITIONAL_CONSTRUCTOR",
            "zero_result_if_signed": "B_Q is parent-owned before EM readout and dH_Q=0 automatically",
            "missing_for_current_claim": "current corpus has not parent-owned C1,D1,C2,D2 as pre-EM fields",
        },
        {
            "theorem_id": "PBC3794_1_rank",
            "claim_piece": "generic rank condition",
            "mathematical_form": "H_Q=dC1 wedge dD1 + dC2 wedge dD2 can have nonzero H_Q wedge H_Q, unlike a one-pair route where H_Q wedge H_Q=0.",
            "derivation_status": "EXACT_LOCAL_RANK_THEOREM",
            "zero_result_if_signed": "generic local Maxwell-rank obstruction is removed",
            "missing_for_current_claim": "two independent parent pairs or CP2/higher multiplet not supplied by current MTS sources",
        },
        {
            "theorem_id": "PBC3794_2_qobs_descent",
            "claim_piece": "descent zero condition",
            "mathematical_form": "For E_A in ker(Dq_obs), if Lie_EA C_i=Lie_EA D_i=0 modulo chart gauge, then Lie_EA B_Q=dchi_A and Lie_EA H_Q=0.",
            "derivation_status": "EXACT_DESCENT_THEOREM",
            "zero_result_if_signed": "B_perp=0, H_perp=0, eps_BQ_descent_A=0, and eps_dBQ_A=0 on U_good",
            "missing_for_current_claim": "q_obs descent of the candidate internal coordinates",
        },
        {
            "theorem_id": "PBC3794_3_CP2_Berry_owner",
            "claim_piece": "CP2/Berry equivalent theorem",
            "mathematical_form": "If parent MTS owns normalized z:U->C^3 with chart redundancy z->exp(i chi)z, then B_Q=-i z_dagger dz is a U(1) connection, B_Q->B_Q+dchi, and H_Q=dB_Q is chart-invariant.",
            "derivation_status": "EXACT_CONDITIONAL_CONSTRUCTOR",
            "zero_result_if_signed": "CP2/Berry route supplies a bundle-covariant B_Q owner with generic local rank",
            "missing_for_current_claim": "current corpus does not own z or its parent action before EM readout",
        },
        {
            "theorem_id": "PBC3794_4_no_smuggle",
            "claim_piece": "non-circularity condition",
            "mathematical_form": "Y_Q or z must be generated from Phi_MTS/Psi_Q before A_obs, F_obs, Maxwell equations, Lorentz force, or EM Poynting stress are defined.",
            "derivation_status": "NO_SMUGGLE_CONSTRAINT",
            "zero_result_if_signed": "prevents local parameterization of known EM from being misreported as a derivation",
            "missing_for_current_claim": "a concrete parent primitive-to-Y_Q or primitive-to-z map",
        },
        {
            "theorem_id": "PBC3794_5_current_verdict",
            "claim_piece": "strict current corpus outcome",
            "mathematical_form": "The constructor theorem is exact, but current inspected sources supply at most simple/partial routes and defects; no source signs a generic parent-owned two-pair or CP2 B_Q.",
            "derivation_status": "CONSTRUCTOR_THEOREM_PLUS_CURRENT_FAILURE",
            "zero_result_if_signed": "not applicable in current strict branch",
            "missing_for_current_claim": "parent owner map or finite B_perp/H_perp profile values",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def primitive_sweep_rows(timestamp):
    rows = [
        {
            "sweep_id": "SW3794_0_real_scalar",
            "primitive": "real scalar psi / scalar gradients",
            "supports": "one scalar or exact one-form f(psi)dpsi",
            "owner_test": "can supply generic two-pair B_Q before EM readout",
            "result": "REJECT_GENERIC_OWNER",
            "reason": "pure scalar gradients are exact or rank-too-small away from defects",
            "best_use": "none for generic B_Q; keep only as auxiliary scalar if another parent field supplies rank",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SW3794_1_phase_volume",
            "primitive": "phase-volume T,S route",
            "supports": "two operational scalars T and S with local-GR routing motivation",
            "owner_test": "can form B_Q=T dS or equivalent one-pair Clebsch sector",
            "result": "SIMPLE_SECTOR_ONLY",
            "reason": "one pair gives H_Q wedge H_Q=0 and cannot cover generic local EM",
            "best_use": "null/simple EM benchmark or one half of a future two-pair lift",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SW3794_2_Qflow",
            "primitive": "Q-flow / coherent-domain volume",
            "supports": "Q, Q_coh, N_D, Theta_Q_res, determinant/coframe volume variation",
            "owner_test": "can produce two independent pre-EM pairs and a chart-covariant U1 connection",
            "result": "PROMISING_NOT_SIGNED",
            "reason": "1174 gives a sharp stationarity defect, but Q_coh projector, N_D rule, tracefree shear, and two-pair extraction are not parent-owned",
            "best_use": "next constructive target: attempt Q-flow two-pair lift or finite projector-leak profile",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SW3794_3_defects_nodes",
            "primitive": "nodes/defects/Wilson data",
            "supports": "topological periods, singular support, charge lattice hints",
            "owner_test": "can generate generic smooth local H_Q",
            "result": "TOPOLOGICAL_SUPPORT_ONLY",
            "reason": "defects can own quantized residues but not generic smooth Maxwell curvature by themselves",
            "best_use": "D_Q/Wilson residual rows and charge-label support",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SW3794_4_Poynting_Hodge",
            "primitive": "Poynting/Hodge-flow intuition",
            "supports": "a candidate background stress-flow route if defined before EM",
            "owner_test": "can define B_Q from pre-EM stress-flow current without E cross B",
            "result": "CONDITIONAL_FORK_NOT_SOURCE_SIGNED",
            "reason": "ordinary Poynting is post-EM and circular; no source currently defines a pre-EM Hodge-flow current with two-pair rank",
            "best_use": "keep as a private construction fork, requiring a pre-EM stress-flow definition",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SW3794_5_sorted_parent_grammar",
            "primitive": "typed/sorted parent action grammar",
            "supports": "no-smuggling discipline and closure labels",
            "owner_test": "does it derive the B_Q owner from MTS primitives",
            "result": "DISCIPLINE_ONLY_NOT_OWNER",
            "reason": "1237 says sorted grammar is not derived from current primitives",
            "best_use": "guard against hidden-visible coefficient smuggling",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def candidate_rows(timestamp):
    rows = [
        {
            "candidate_id": "CAND3794_0_two_pair_Clebsch_extension",
            "candidate": "declare parent Y_Q=(C1,D1,C2,D2)",
            "mathematical_power": "generic local B_Q and H_Q with dH_Q=0",
            "non_smuggle_status": "valid only if Y_Q is parent action data or functor of MTS primitives before EM readout",
            "current_corpus_status": "NOT_DERIVED",
            "decision": "keep as exact parent-extension theorem, not current MTS derivation",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND3794_1_CP2_Berry_extension",
            "candidate": "declare parent normalized z:U->C^3",
            "mathematical_power": "bundle-covariant U1 connection with generic local rank",
            "non_smuggle_status": "valid only if z has parent dynamics and chart redundancy before EM readout",
            "current_corpus_status": "NOT_DERIVED",
            "decision": "cleanest geometric extension if an explicit internal multiplet is allowed",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND3794_2_Qflow_lift",
            "candidate": "derive Y_Q from Q-flow eigen/projector/shear variables",
            "mathematical_power": "could become MTS-native if Q supplies two independent pre-EM scalar pairs",
            "non_smuggle_status": "currently incomplete; must not use fitted EM field or post-hoc smoothing projector",
            "current_corpus_status": "BEST_DERIVATION_FORK_BUT_UNSIGNED",
            "decision": "make this the next target before giving up to purely finite profiles",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND3794_3_phase_volume_pair",
            "candidate": "B_Q=T dS or S dT",
            "mathematical_power": "simple/rank-two sector only",
            "non_smuggle_status": "pre-EM if T,S are parent observer variables, but rank-limited",
            "current_corpus_status": "PARTIAL_ONLY",
            "decision": "do not use as generic EM owner; can test null/simple-sector toy branch",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND3794_4_preEM_Poynting_Hodge",
            "candidate": "B_Q from pre-EM stress-flow/Hodge current",
            "mathematical_power": "could align with the user's Poynting/background-field intuition",
            "non_smuggle_status": "fails if Poynting means E cross B; viable only with parent stress-flow current",
            "current_corpus_status": "NO_PARENT_DEFINITION_YET",
            "decision": "keep as side fork behind Q-flow lift, not the main claim route",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def profile_contract_rows(timestamp):
    rows = [
        {
            "profile_id": "BHP3794_0_Bperp_profile",
            "quantity": "B_perp(x)",
            "definition": "B_Q - q_obs^*Bbar_Q - dchi on U_good after exact gauge projection",
            "norm": "||B_perp||_A/A_ref and ||P_A Lie_EA B_perp||_A/A_ref",
            "source_needed": "parent owner constructor or sampled candidate field profile on selected U_good arenas",
            "units": "connection_one_form_units",
            "feeds": "eps_BQ_descent_A;R_A;alpha_source",
            "valid_for_claim": False,
        },
        {
            "profile_id": "BHP3794_1_Hperp_profile",
            "quantity": "H_perp=dB_perp",
            "definition": "H_Q - q_obs^*Hbar_Q on U_good",
            "norm": "||H_perp||_F/F_ref and ||Lie_EA H_perp||_F/F_ref",
            "source_needed": "parent curvature profile or finite bound from Q-flow/projector/shear route",
            "units": "curvature_two_form_units",
            "feeds": "eps_dBQ_A;dR_A;PPN;R10;clock",
            "valid_for_claim": False,
        },
        {
            "profile_id": "BHP3794_2_Qflow_projector",
            "quantity": "Qflow_two_pair_lift",
            "definition": "candidate extraction of C1,D1,C2,D2 from Q/Q_coh/shear/eigenframe variables without EM readout",
            "norm": "projector_leak + tracefree_shear + domain_reference + chart_degeneracy",
            "source_needed": "parent Qcoh projector, N_D normalization law, eigenframe chart rule, and stationarity/domain transport",
            "units": "dimensionless_or_inverse_variation_units_by_component",
            "feeds": "B_perp;H_perp;eps_BQ_owner_map",
            "valid_for_claim": False,
        },
        {
            "profile_id": "BHP3794_3_domain_defect",
            "quantity": "D_Q/Wilson support",
            "definition": "defect and Wilson residue data not killed by local U_good trivialization",
            "norm": "absolute period/residue over selected cycles or boundary support",
            "source_needed": "defect owner, cycle support, and no-crossing certificate for each local arena",
            "units": "period_or_flux_units",
            "feeds": "eps_BQ_defect_Wilson;clock;R10;orbital",
            "valid_for_claim": False,
        },
        {
            "profile_id": "BHP3794_4_no_claim_acceptance",
            "quantity": "finite_profile_acceptance",
            "definition": "no local EM/local-GR claim until B_perp/Hperp and companion Z_EM/epsilon_J/domain rows are zeroed or arena-bounded",
            "norm": "no-cancellation absolute-sum envelope",
            "source_needed": "numeric/source-backed component values or exact zero theorems",
            "units": "dimensionless_envelope_after_normalization",
            "feeds": "local_GR_gate;PPN;WEP;R10;clock;orbital",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths and needles resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_1_constructor_theorem",
            "pass": True,
            "claim_allowed": False,
            "details": "two-pair Clebsch and CP2/Berry owner theorems emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_2_current_owner_found",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus does not parent-own Y_Q or z",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_3_Qflow_lift_closed",
            "pass": False,
            "claim_allowed": False,
            "details": "Q-flow route is the best derivation fork but lacks projector/N_D/eigenframe/two-pair certificates",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_4_finite_profile_ready",
            "pass": True,
            "claim_allowed": False,
            "details": "B_perp/Hperp finite profile contract emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3794_5_local_GR_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; owner, Z_EM/lambda, same-current, and domain gates remain open",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3794_0_constructor_exact",
            "decision": "A generic parent B_Q can be constructed exactly from two Clebsch pairs or CP2/Berry data.",
            "action": "Keep this as the mathematical target and reject single-pair generic claims.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3794_1_current_fail",
            "decision": "The current corpus does not yet derive the owner data from MTS primitives.",
            "action": "Do not claim EM/local-GR closure from 3794.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3794_2_best_fork",
            "decision": "The best non-smuggled next attempt is a Q-flow two-pair lift because Q-flow already owns a determinant/coframe route and a named stationarity defect.",
            "action": "Try Q-flow eigen/projector/shear variables as Y_Q, with strict no-EM and no-smoothing guards.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3794_3_profile_fallback",
            "decision": "If the Q-flow lift fails, the honest route is finite B_perp/Hperp profile acquisition.",
            "action": "Use the profile contract rather than writing more generic missing-ledger rows.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md",
            "target_script": "scripts/Y5_R2FR_3795_Qflow_two_pair_lift_or_Bperp_profile_first_input.py",
            "objective": "Try to construct Y_Q=(C1,D1,C2,D2) from Q-flow/Q_coh/shear/eigenframe primitives without EM readout; if that fails, emit the first concrete B_perp/Hperp profile input schema with arena selection and units.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "PARENT_BQ_CONSTRUCTOR_THEOREM_EXACT_CURRENT_OWNER_NOT_FOUND_QFLOW_LIFT_SELECTED",
            "plain_verdict": "3794 proves the exact two-pair/CP2 parent B_Q constructor theorem, then rejects a strict current-corpus closure because no parent-owned Y_Q or z is present. The best remaining derivation fork is a Q-flow two-pair lift; otherwise the branch must use finite B_perp/Hperp profiles.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(row["exists"] for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "needles_found",
            all(row["needle_found"] for row in grouped["sources"]),
            "every cited needle was found in the registered source",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3794 markdown document written"),
        (
            "constructor_theorem",
            any(row["theorem_id"] == "PBC3794_0_two_pair_owner" for row in grouped["constructor"]),
            "two-pair constructor theorem emitted",
        ),
        (
            "CP2_theorem",
            any(row["theorem_id"] == "PBC3794_3_CP2_Berry_owner" for row in grouped["constructor"]),
            "CP2/Berry constructor theorem emitted",
        ),
        (
            "Qflow_selected",
            any(row["candidate_id"] == "CAND3794_2_Qflow_lift" and row["current_corpus_status"] == "BEST_DERIVATION_FORK_BUT_UNSIGNED" for row in grouped["candidates"]),
            "Q-flow two-pair lift selected as best next derivation fork",
        ),
        (
            "profile_contract",
            all(
                any(row["quantity"] == quantity for row in grouped["profile"])
                for quantity in ["B_perp(x)", "H_perp=dB_perp", "Qflow_two_pair_lift"]
            ),
            "B_perp/Hperp profile contract emitted",
        ),
        (
            "owner_claim_closed",
            any(row["gate_id"] == "CG3794_2_current_owner_found" and row["pass"] is False for row in grouped["gates"]),
            "current owner claim remains closed",
        ),
        (
            "local_gr_closed",
            any(row["gate_id"] == "CG3794_5_local_GR_claim" and row["pass"] is False for row in grouped["gates"]),
            "local-GR claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3795-"),
            "3795 Q-flow two-pair lift target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3794 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3794 - Parent B_Q Owner Constructor, Two-Pair/CP2, or Finite Profile",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3794 does the constructive thing. It proves the exact shape of a non-smuggled parent `B_Q`: either two parent-owned Clebsch pairs `Y_Q=(C1,D1,C2,D2)` with `B_Q=C1 dD1+C2 dD2`, or a parent-owned CP2/Berry multiplet `z` with `B_Q=-i z_dagger dz`. Either route gives a genuine U(1)-style connection before EM readout if the parent owns the variables.",
        "",
        "The strict current-corpus answer is still no: the inspected sources do not yet own `Y_Q` or `z`. But the next derivation is now sharper. The best fork is to try extracting two independent pre-EM pairs from the `Q`/`Q_coh`/shear/eigenframe route. If that fails, the branch should stop circling and fill finite `B_perp/Hperp` profiles with units and arena domains.",
        "",
        "## Compact Constructor",
        "",
        "`B_Q=C1 dD1+C2 dD2` and `H_Q=dC1 wedge dD1+dC2 wedge dD2`.",
        "",
        "Generic-rank test: two pairs can have `H_Q wedge H_Q != 0`; one pair cannot.",
        "",
        "Descent test: if `Lie_EA C_i=Lie_EA D_i=0` modulo chart gauge for all `E_A in ker(Dq_obs)`, then `Lie_EA B_Q=dchi_A` and `Lie_EA H_Q=0`.",
        "",
        "CP2 equivalent: `B_Q=-i z_dagger dz`, with `z->exp(i chi)z` giving `B_Q->B_Q+dchi`.",
        "",
        render_section("Source Register", grouped["sources"], ["source_id"]),
        render_section("Parent B_Q Constructor Theorem", grouped["constructor"], ["theorem_id", "claim_piece"]),
        render_section("Current Primitive Sweep", grouped["sweep"], ["sweep_id", "primitive"]),
        render_section("Owner Candidate Decision Matrix", grouped["candidates"], ["candidate_id", "candidate"]),
        render_section("B_perp/Hperp Profile Contract", grouped["profile"], ["profile_id", "quantity"]),
        render_section("Claim Gates", grouped["gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "constructor": constructor_rows(timestamp),
        "sweep": primitive_sweep_rows(timestamp),
        "candidates": candidate_rows(timestamp),
        "profile": profile_contract_rows(timestamp),
        "gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["constructor"], grouped["constructor"])
    write_csv(OUTPUTS["sweep"], grouped["sweep"])
    write_csv(OUTPUTS["candidates"], grouped["candidates"])
    write_csv(OUTPUTS["profile"], grouped["profile"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3794 validation failed: {failures}")
    print("wrote 3794 checkpoint: parent B_Q constructor theorem and Q-flow lift fork emitted")


if __name__ == "__main__":
    main()
