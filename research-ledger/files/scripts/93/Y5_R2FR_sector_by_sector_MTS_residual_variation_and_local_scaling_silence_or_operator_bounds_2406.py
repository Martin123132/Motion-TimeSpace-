from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SECTOR_BY_SECTOR_MTS_RESIDUAL_VARIATION_AND_LOCAL_SCALING_SILENCE_OR_OPERATOR_BOUNDS_2406"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md"


def post(path_text: str) -> Path:
    return POST_ROOT / path_text


SOURCES = [
    {
        "source_id": "SRC2406_2405_doc",
        "path": str(post("2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md")),
        "needles": "RSS2405_0_higher_derivative|RSS2405_6_verdict|NEXT2405_0_selected|VAL2405_OVERALL",
        "role": "immediate parent checkpoint reducing EH dominance to named residual sectors",
    },
    {
        "source_id": "SRC2406_2405_sector_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2405_RESIDUAL_SECTOR_SILENCE_AUDIT.csv")),
        "needles": "RSS2405_0_higher_derivative|RSS2405_6_verdict",
        "role": "2405 sector silence source table",
    },
    {
        "source_id": "SRC2406_2405_operator_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2405_OPERATOR_BOUND_PACK.csv")),
        "needles": "OPB2405_0_total_DeltaE_MTS|OPB2405_6_c_q_source",
        "role": "2405 operator coefficient pack",
    },
    {
        "source_id": "SRC2406_1771_doc",
        "path": str(post("1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md")),
        "needles": "SAV1771_0_higher_derivative|SCL1771_0_higher_derivative|DEC1771_3_best_next|VAL1771_OVERALL",
        "role": "earlier sector-variation audit selecting Pi_M commutator as the concrete obstruction",
    },
    {
        "source_id": "SRC2406_1771_variation_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv")),
        "needles": "SAV1771_0_higher_derivative|SAV1771_6_verdict",
        "role": "1771 variation ledger",
    },
    {
        "source_id": "SRC2406_1771_scaling_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1771_LOCAL_SCALING_LEDGER.csv")),
        "needles": "SCL1771_0_higher_derivative|SCL1771_5_source_normalization",
        "role": "1771 local scaling ledger",
    },
    {
        "source_id": "SRC2406_1841_doc",
        "path": str(post("1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md")),
        "needles": "SAV1841_0_higher_derivative|SCL1841_0_higher_derivative|DEC1841_3_best_next|VAL1841_OVERALL",
        "role": "later sector-variation audit selecting sector Lagrangian/boundary ownership",
    },
    {
        "source_id": "SRC2406_1841_variation_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1841_SECTOR_ACTION_VARIATION_LEDGER.csv")),
        "needles": "SAV1841_0_higher_derivative|SAV1841_6_verdict",
        "role": "1841 variation ledger",
    },
    {
        "source_id": "SRC2406_1841_scaling_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1841_LOCAL_SCALING_LEDGER.csv")),
        "needles": "SCL1841_0_higher_derivative|SCL1841_5_source_normalization",
        "role": "1841 local scaling ledger",
    },
    {
        "source_id": "SRC2406_2236_doc",
        "path": str(post("2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md")),
        "needles": "GRAM2236_0_no_DRAB|ELIM2236_4_current|VAL2236_OVERALL",
        "role": "auxiliary/no-derivative grammar warning for zero-stress claims",
    },
    {
        "source_id": "SRC2406_2301_q_firstclass_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv")),
        "needles": "QFC2301_0_parent_Omega|QFC2301_6_verdict",
        "role": "q first-class removal obstruction",
    },
    {
        "source_id": "SRC2406_2301_q_ricci_weyl_csv",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_RICCI_WEYL_SPLIT_ATTEMPT.csv")),
        "needles": "QRWS2301_2_Weyl_not_silent|QRWS2301_4_verdict",
        "role": "q curvature split and Weyl-tail warning",
    },
]


SECTORS = [
    {
        "sector_id": "SVC2406_0_higher_derivative",
        "coefficient": "c_HD",
        "sector": "higher-curvature / higher-derivative geometry",
        "action_owner": "S_HD=int sqrt(-g)(c_R2 R^2+c_Ricci2 R_munu R^munu+c_boxR R box R+...)",
        "variation_target": "E_HD_munu with fourth-order/local higher-derivative metric response",
        "variation_status": "FORM_TEMPLATE_KNOWN_PARENT_ADOPTION_UNSIGNED",
        "silence_test": "parent normal form excludes the sector, makes it topological, or supplies bounds below every local tolerance",
        "local_scaling": "epsilon_HD ~ |c_HD|/L_local^2 plus operator-basis factors",
        "zero_status": "NOT_ZEROED",
        "bound_status": "MISSING_COEFFICIENT_SCALE_AND_TOLERANCE",
        "next_action": "derive no-higher-derivative parent grammar or source local bounds for c_HD",
        "priority": "SECONDARY_BUT_STANDARD_LOCAL_GR_FILTER",
    },
    {
        "sector_id": "SVC2406_1_constraint_auxiliary",
        "coefficient": "c_aux",
        "sector": "constraint/auxiliary metric stress",
        "action_owner": "S_aux=int sqrt(-g)(lambda_C C_MTS+lambda_R R_AB+q auxiliary blocks)",
        "variation_target": "lambda delta_g C plus metric-volume terms plus auxiliary-elimination tails",
        "variation_status": "ZERO_STRESS_SHORTCUT_REJECTED",
        "silence_test": "first-class zero-boundary generator or algebraic second-class elimination with zero metric stress",
        "local_scaling": "epsilon_aux ~ |lambda delta_g C + eliminated-tail|/|G_munu|",
        "zero_status": "UNSIGNED_ZERO_STRESS",
        "bound_status": "MISSING_AUXILIARY_ELIMINATION_STRESS_BOUND",
        "next_action": "prove auxiliary elimination is stress-silent or retain c_aux as a local operator bound",
        "priority": "ROOT_GUARDRAIL_AGAINST_FAKE_GR_LIMIT",
    },
    {
        "sector_id": "SVC2406_2_projector_domain",
        "coefficient": "c_projector_operator",
        "sector": "projector/domain/readout operator",
        "action_owner": "S_PiM or variation-before-readout Hamiltonian/worldtube projector block",
        "variation_target": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H and d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
        "variation_status": "EXACT_OBSTRUCTION_WRITTEN_NOT_SILENCED",
        "silence_test": "Pi_M is a fixed chain map on the same Hilbert worldtube, delta_g Pi_M=0, and [d,Pi_M]J_H=0",
        "local_scaling": "epsilon_PiM ~ |I_commutator|/M_H_ref + |projector_stress_beta_equiv|",
        "zero_status": "NOT_ZEROED_EXACT_OBSTRUCTION",
        "bound_status": "MISSING_I_COMMUTATOR_MHREF_AND_PROJECTOR_STRESS",
        "next_action": "prove Pi_M commutator/projector variation zero or source a coefficient bound",
        "priority": "BEST_NEXT_CONCRETE_TARGET",
    },
    {
        "sector_id": "SVC2406_3_boundary_reference",
        "coefficient": "c_boundary_operator",
        "sector": "boundary/reference/improvement",
        "action_owner": "S_GHY+B_ref+exact/topological improvements+symplectic boundary terms",
        "variation_target": "theta_boundary, Q_boundary, DeltaE_boundary, H_ref_shift, Delta_symp",
        "variation_status": "REFERENCE_LOCK_UNSIGNED",
        "silence_test": "fixed-before-readout reference plus zero compact linked-boundary flux and a shared falloff class",
        "local_scaling": "epsilon_boundary ~ |B_zero_flux + Delta_symp + H_ref_shift|/M_H_ref",
        "zero_status": "BOUNDARY_GATE_OPEN",
        "bound_status": "MISSING_BOUNDARY_REFERENCE_LOCK",
        "next_action": "own B_ref/tau/boundary conditions before using orbital or local readout",
        "priority": "PARALLEL_OWNER_FOR_NEWTON_BRIDGE",
    },
    {
        "sector_id": "SVC2406_4_memory_coframe",
        "coefficient": "c_memory_frame",
        "sector": "memory/coframe/current-chain residual",
        "action_owner": "S_memory/coframe with theta_X, Q_X, C_tau, tau-lock terms, and frame response",
        "variation_target": "E_memory_munu, E_coframe_munu, PPN alpha_i, clock-drift residuals",
        "variation_status": "LOCAL_FRAME_AND_TAU_LOCK_UNSIGNED",
        "silence_test": "terminal public coframe and tau_source=tau_charge=tau_clock=tau_readout kill preferred-frame stress",
        "local_scaling": "epsilon_frame ~ preferred-frame alpha_i + clock drift + tau-lock mismatch",
        "zero_status": "NOT_ZEROED",
        "bound_status": "MISSING_LOCAL_FRAME_TAU_LOCK_OR_PPN_BOUND",
        "next_action": "prove public coframe descent/tau lock or carry preferred-frame and clock bounds",
        "priority": "IMPORTANT_FOR_CLOCKS_AND_PPN",
    },
    {
        "sector_id": "SVC2406_5_q_source_vector",
        "coefficient": "c_q_source",
        "sector": "q / reciprocal source vector tails",
        "action_owner": "S_q residual vector with B_qW C_Weyl + B_qRic R_Ricci + C_qT T_H + Q_q[body] + Pi_q + tail_q",
        "variation_target": "q Euler/source vector and its local exterior projection",
        "variation_status": "FIRSTCLASS_AND_WEYL_ZERO_UNSIGNED",
        "silence_test": "q first-class removal closes, q has no Weyl spurion, and boundary/source q charges vanish",
        "local_scaling": "epsilon_q ~ |B_qW C_Weyl + B_qRic R_Ricci + C_qT T_H + Q_q + Pi_q + tail_q|/|G_munu|",
        "zero_status": "NOT_ZEROED_WEYL_TAIL_DANGER",
        "bound_status": "MISSING_Q_FIRSTCLASS_OR_BQWEYL_BOUND",
        "next_action": "prove q representation/no-spurion zero or retain B_qW and source-vector coefficient bounds",
        "priority": "DANGEROUS_LOCAL_VACUUM_TAIL",
    },
]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCES:
        source_path = Path(source["path"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_path": source["path"],
                "exists": str(source_path.exists()).lower(),
                "needles": source["needles"],
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def sector_variation_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": sector["sector_id"],
            "coefficient": sector["coefficient"],
            "sector": sector["sector"],
            "action_owner": sector["action_owner"],
            "variation_target": sector["variation_target"],
            "variation_status": sector["variation_status"],
            "silence_test": sector["silence_test"],
            "zero_status": sector["zero_status"],
            "bound_status": sector["bound_status"],
            "next_action": sector["next_action"],
            "valid_for_claim": "false",
        }
        for sector in SECTORS
    ] + [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVC2406_6_verdict",
            "coefficient": "DeltaE_MTS",
            "sector": "total MTS residual operator",
            "action_owner": "sum of all retained non-EH MTS residual sectors",
            "variation_target": "DeltaE_MTS=sum_i c_i O_i^{mu nu}",
            "variation_status": "NO_SECTOR_FULLY_SILENCED",
            "silence_test": "all six sector rows must prove zero/silence or source-backed sub-threshold bounds",
            "zero_status": "EH_DOMINANCE_NOT_PROVED",
            "bound_status": "OPERATOR_BOUND_PACK_RETAINED_NONCLAIM",
            "next_action": "attack the smallest exact obstruction first: Pi_M commutator/projector variation",
            "valid_for_claim": "false",
        }
    ]


def local_scaling_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "scale_id": sector["sector_id"].replace("SVC", "SCL"),
            "coefficient": sector["coefficient"],
            "sector": sector["sector"],
            "dimensionless_ratio": sector["local_scaling"],
            "local_silence_condition": sector["silence_test"],
            "status": sector["bound_status"],
            "valid_for_claim": "false",
        }
        for sector in SECTORS
    ]


def silence_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": sector["sector_id"].replace("SVC", "SD"),
            "coefficient": sector["coefficient"],
            "zero_claim": "false",
            "bound_claim": "false",
            "current_verdict": sector["zero_status"],
            "reason": sector["bound_status"],
            "next_action": sector["next_action"],
            "valid_for_claim": "false",
        }
        for sector in SECTORS
    ] + [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "SD2406_6_total_DeltaE_MTS",
            "coefficient": "DeltaE_MTS",
            "zero_claim": "false",
            "bound_claim": "false",
            "current_verdict": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "reason": "one or more live sector coefficients can still alter local GR/Newton/PPN readout",
            "next_action": "do not claim local GR; prove or bound projector and boundary/source-owner residuals",
            "valid_for_claim": "false",
        }
    ]


def operator_bound_input_rows() -> list[dict[str, str]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBI2406_0_total_DeltaE_MTS",
            "coefficient": "DeltaE_MTS",
            "operator_basis": "sum_i c_i O_i^{mu nu}",
            "required_inputs": "all sector coefficients zero/silent or numeric source-backed below local thresholds",
            "arena_links": "PPN, Newton/Poisson, R10, clocks, orbital, cosmology",
            "status": "NONCLAIM_ROOT_RESIDUAL",
            "valid_for_claim": "false",
        }
    ]
    for sector in SECTORS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": sector["sector_id"].replace("SVC", "OBI"),
                "coefficient": sector["coefficient"],
                "operator_basis": sector["variation_target"],
                "required_inputs": sector["bound_status"],
                "arena_links": arena_links_for(sector["coefficient"]),
                "status": "BOUND_OR_ZERO_NEEDED",
                "valid_for_claim": "false",
            }
        )
    return rows


def arena_links_for(coefficient: str) -> str:
    arenas = {
        "c_HD": "PPN, R10/Yukawa, gravitational waves",
        "c_aux": "Newton exterior, PPN, q/RAB local branch",
        "c_projector_operator": "source normalization, PPN gamma/beta, local response",
        "c_boundary_operator": "orbital systems, source charge, boundary leakage",
        "c_memory_frame": "PPN preferred-frame, clocks, orbital secular drift",
        "c_q_source": "local vacuum, PPN, R10, source-profile tests",
    }
    return arenas[coefficient]


def priority_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "rank": str(priority_rank),
            "coefficient": sector["coefficient"],
            "priority": sector["priority"],
            "reason": priority_reason_for(sector["coefficient"]),
            "next_action": sector["next_action"],
            "valid_for_claim": "false",
        }
        for priority_rank, sector in enumerate(
            sorted(SECTORS, key=lambda sector: priority_sort_value(sector["coefficient"])), start=1
        )
    ]


def priority_sort_value(coefficient: str) -> int:
    order = {
        "c_projector_operator": 0,
        "c_boundary_operator": 1,
        "c_aux": 2,
        "c_q_source": 3,
        "c_HD": 4,
        "c_memory_frame": 5,
    }
    return order[coefficient]


def priority_reason_for(coefficient: str) -> str:
    reasons = {
        "c_projector_operator": "exact product-rule/commutator obstruction from 1771 and direct source-normalization relevance",
        "c_boundary_operator": "1841 shows boundary/source-owner lock is the broad structure behind Newton bridge terms",
        "c_aux": "prevents smuggling GR through C=0 constraints with nonzero metric stress",
        "c_q_source": "Weyl tail can survive exterior vacuum unless q type/no-spurion clauses are signed",
        "c_HD": "standard local-GR filter, but less MTS-specific than projector/source ownership",
        "c_memory_frame": "important for clocks/preferred-frame tests after the local geometry/source bridge is owned",
    }
    return reasons[coefficient]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2406_0_EH_dominance",
            "gate": "DeltaE_MTS=0",
            "status": "BLOCKED",
            "why": "no sector-by-sector zero certificate closes all retained MTS residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2406_1_local_GR_Newton",
            "gate": "GR/Newton reduction",
            "status": "BLOCKED",
            "why": "projector/source, boundary, auxiliary, q, higher-derivative, and memory residuals remain live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2406_2_operator_bounds",
            "gate": "finite residual below local thresholds",
            "status": "BLOCKED",
            "why": "coefficient units, arena projections, and tolerances are still missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2406_3_cancellation",
            "gate": "sector cancellations",
            "status": "BLOCKED",
            "why": "no cancellation is allowed without parent identity and no-arena-fine-tuning proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2406_4_public_claim",
            "gate": "public/GitHub claim update",
            "status": "BLOCKED",
            "why": "this checkpoint is private scaffolding for derivability, not a claim of success",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2406_0_constraint_shortcut",
            "claim": "constraint equation C=0 proves zero stress",
            "allowed": "false",
            "reason": "lambda delta_g C and auxiliary-elimination tails can survive",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2406_1_commutator_ignore",
            "claim": "projector/readout can be applied after variation with no cost",
            "allowed": "false",
            "reason": "delta_g Pi_M and [d,Pi_M]J_H are exact obstruction terms until zeroed or bounded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2406_2_small_without_units",
            "claim": "residuals are small by intuition",
            "allowed": "false",
            "reason": "smallness requires dimensionless local ratios and source-backed thresholds",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2406_3_q_vacuum_silence",
            "claim": "q source vector vanishes in exterior vacuum automatically",
            "allowed": "false",
            "reason": "Weyl/tidal curvature survives in Schwarzschild-like vacuum unless the q coupling is forbidden",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2406_4_github",
            "claim": "2406 is ready for GitHub/public promotion",
            "allowed": "false",
            "reason": "it is a private gate that tells us what remains to prove or bound",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2406_0_gain",
            "decision": "accept finite residual-sector decomposition",
            "reason": "2405 made DeltaE_MTS a finite owner problem and 2406 maps each owner to a variation/scaling test",
            "consequence": "future local-GR work has a scoreboard instead of fog",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2406_1_no_sector_zero",
            "decision": "do not claim any sector silence",
            "reason": "all six sectors retain an unsigned theorem, coefficient, or arena projection",
            "consequence": "EH dominance and Newton reduction remain blocked but sharply localized",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2406_2_best_next",
            "decision": "select Pi_M commutator/projector variation as the next target",
            "reason": "it is the smallest exact obstruction, already rank-one in 1771, and touches source normalization directly",
            "consequence": "2407 should either prove [d,Pi_M]J_H and delta_g Pi_M vanish or produce a coefficient-bound row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2406_3_parallel_route",
            "decision": "keep sector Lagrangian/boundary ownership as the broad parallel route",
            "reason": "1841 shows L_X, Theta_X, Q_X, B_ref, tau ownership are needed for the full Newton bridge",
            "consequence": "if 2407 cannot zero the projector, move to the broader source-owner action contract",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2406_0_selected",
            "next_doc": "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md",
            "why": "Pi_M commutator/projector variation is the most concrete exact obstruction to source normalization and local GR reduction",
            "expected_output": "prove fixed-chain-map/projector-stress zero, or emit c_projector_operator/I_commutator bound rows with arena projections",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2406_1_fallback",
            "next_doc": "2407B-Y5-R2FR-sector-Lagrangian-boundary-owner-normal-form-or-source-owner-bound-pack.md",
            "why": "if the projector zero proof needs parent action ownership first, route to L_X/Theta_X/Q_X/B_ref/tau owner construction",
            "expected_output": "source-owner normal form that tells the projector and boundary terms what they are allowed to be",
            "valid_for_claim": "false",
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2406_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2406_SECTOR_VARIATION_CERTIFICATE.csv": sector_variation_rows,
    "P8_Y5_PARENT_QLOC_2406_LOCAL_SCALING_LEDGER.csv": local_scaling_rows,
    "P8_Y5_PARENT_QLOC_2406_SILENCE_DECISION_LEDGER.csv": silence_decision_rows,
    "P8_Y5_PARENT_QLOC_2406_OPERATOR_BOUND_INPUT_PACK.csv": operator_bound_input_rows,
    "P8_Y5_PARENT_QLOC_2406_PRIORITY_LEDGER.csv": priority_rows,
    "P8_Y5_PARENT_QLOC_2406_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2406_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2406_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2406_NEXT_TARGET.csv": next_target_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sources_exist() -> bool:
    return all(Path(source["path"]).exists() for source in SOURCES)


def needles_found() -> bool:
    for source in SOURCES:
        source_path = Path(source["path"])
        if not source_path.exists():
            return False
        source_text = source_path.read_text(encoding="utf-8", errors="ignore")
        for needle in source["needles"].split("|"):
            if needle not in source_text:
                return False
    return True


def csvs_parse() -> bool:
    csv_paths = list(CSV_BUILDERS.keys()) + ["P8_Y5_BRR545_2406_VALIDATION.csv"]
    for csv_name in csv_paths:
        csv_path = RESIDUALS / csv_name
        if not csv_path.exists():
            return False
        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            parsed_rows = list(csv.DictReader(csv_file))
        if not parsed_rows:
            return False
    return True


def no_claim_flags() -> bool:
    rows = [
        *source_register_rows(),
        *sector_variation_rows(),
        *local_scaling_rows(),
        *silence_decision_rows(),
        *operator_bound_input_rows(),
        *priority_rows(),
        *claim_gate_rows(),
        *refusal_rows(),
        *decision_rows(),
        *next_target_rows(),
    ]
    return all(str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows)


def all_sector_coefficients_present() -> bool:
    coefficients = {row["coefficient"] for row in sector_variation_rows()}
    expected = {"c_HD", "c_aux", "c_projector_operator", "c_boundary_operator", "c_memory_frame", "c_q_source", "DeltaE_MTS"}
    return coefficients == expected


def no_sector_zero_claimed() -> bool:
    return all(row["zero_status"] != "PROVED_ZERO" for row in sector_variation_rows())


def claims_blocked() -> bool:
    return all(row["status"] == "BLOCKED" for row in claim_gate_rows())


def formalization_untouched_by_outputs() -> bool:
    output_paths = [DOC_PATH, *(RESIDUALS / csv_name for csv_name in CSV_BUILDERS), RESIDUALS / "P8_Y5_BRR545_2406_VALIDATION.csv"]
    try:
        formalization_resolved = FORMALIZATION_ROOT.resolve()
    except FileNotFoundError:
        return True
    for output_path in output_paths:
        try:
            output_resolved = output_path.resolve()
        except FileNotFoundError:
            output_resolved = output_path.parent.resolve() / output_path.name
        if formalization_resolved in output_resolved.parents or output_resolved == formalization_resolved:
            return False
    return True


def generated_text() -> str:
    row_groups = [
        source_register_rows(),
        sector_variation_rows(),
        local_scaling_rows(),
        silence_decision_rows(),
        operator_bound_input_rows(),
        priority_rows(),
        claim_gate_rows(),
        refusal_rows(),
        decision_rows(),
        next_target_rows(),
    ]
    return "\n".join(str(row) for rows in row_groups for row in rows)


def validation_rows() -> list[dict[str, str]]:
    text = generated_text()
    checks = [
        {
            "row_id": "VAL2406_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2406_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2406_02_sector_coefficients_present",
            "status": "PASS" if all_sector_coefficients_present() else "FAIL",
            "detail": "six residual sectors plus total DeltaE_MTS are present",
        },
        {
            "row_id": "VAL2406_03_no_sector_zero_claimed",
            "status": "PASS" if no_sector_zero_claimed() else "FAIL",
            "detail": "no residual sector is promoted to proved zero",
        },
        {
            "row_id": "VAL2406_04_local_scaling_complete",
            "status": "PASS" if len(local_scaling_rows()) == 6 and "epsilon_PiM" in text else "FAIL",
            "detail": "all six sectors have dimensionless local scaling placeholders",
        },
        {
            "row_id": "VAL2406_05_operator_pack_nonclaim",
            "status": "PASS" if "OBI2406_0_total_DeltaE_MTS" in text and "NONCLAIM_ROOT_RESIDUAL" in text else "FAIL",
            "detail": "operator bound input pack is retained as nonclaim",
        },
        {
            "row_id": "VAL2406_06_priority_selected",
            "status": "PASS" if "NEXT2406_0_selected" in text and "Pi_M commutator" in text else "FAIL",
            "detail": "projector/Pi_M commutator route selected as next concrete target",
        },
        {
            "row_id": "VAL2406_07_claims_blocked",
            "status": "PASS" if claims_blocked() else "FAIL",
            "detail": "EH dominance, local GR/Newton, finite bounds, cancellation, and public claim gates are blocked",
        },
        {
            "row_id": "VAL2406_08_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2406_09_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2406_10_formalization_untouched_by_outputs",
            "status": "PASS" if formalization_untouched_by_outputs() else "FAIL",
            "detail": "script outputs stay inside post-checkpoint-work",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2406_OVERALL",
            "status": overall,
            "detail": "2406 consolidates sector variation/local scaling gates, keeps every residual nonclaim, and selects Pi_M commutator variation as the next concrete target",
        }
    )
    return [{"branch_id": BRANCH_ID, **row} for row in checks]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    body = f"""# 2406 - Sector-By-Sector MTS Residual Variation And Local Scaling Silence Or Operator Bounds

## Result

This checkpoint consolidates the old `1771` and `1841` sector audits into the current `2405` EH-dominance branch.

The exact local-GR problem remains:

`DeltaE_MTS^{{mu nu}} = sum_i c_i O_i^{{mu nu}}`

and every retained non-EH sector must either be parent-proved silent/zero or carried into a source-backed local bound.

Current verdict: no residual sector is fully silenced.  Local GR/Newton reduction is still blocked, but the blocker is
now finite and named rather than vague.  The best next target is the `Pi_M` commutator/projector variation obstruction,
because it is exact, concrete, and directly contaminates source normalization.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## Sector Variation Certificate

{markdown_table(sector_variation_rows(), ["sector_id", "coefficient", "sector", "action_owner", "variation_target", "variation_status", "silence_test", "zero_status", "bound_status", "next_action", "valid_for_claim"])}

## Local Scaling Ledger

{markdown_table(local_scaling_rows(), ["scale_id", "coefficient", "sector", "dimensionless_ratio", "local_silence_condition", "status", "valid_for_claim"])}

## Silence Decision Ledger

{markdown_table(silence_decision_rows(), ["decision_id", "coefficient", "zero_claim", "bound_claim", "current_verdict", "reason", "next_action", "valid_for_claim"])}

## Operator Bound Input Pack

{markdown_table(operator_bound_input_rows(), ["row_id", "coefficient", "operator_basis", "required_inputs", "arena_links", "status", "valid_for_claim"])}

## Priority Ledger

{markdown_table(priority_rows(), ["rank", "coefficient", "priority", "reason", "next_action", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["row_id", "gate", "status", "why", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows(), ["row_id", "decision", "reason", "consequence", "valid_for_claim"])}

## Next Target

{markdown_table(next_target_rows(), ["row_id", "next_doc", "why", "expected_output", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

This is not grim; it is annoyingly precise.  We have not derived local GR yet, but we have stopped chasing smoke.
The immediate fight is no longer "make MTS reduce to GR somehow"; it is:

`delta_g Pi_M = 0`, `[d,Pi_M]J_H = 0`, or a real coefficient bound.

If that route closes, the Newton/GR bridge gets much cleaner.  If it fails, the honest fallback is the broader
sector-Lagrangian/boundary-owner action contract.  Either way, no GitHub/public claim is being made from 2406.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for csv_name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / csv_name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2406_VALIDATION.csv", validation_rows())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2406_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2406_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
