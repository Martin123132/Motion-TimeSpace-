from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_VERTICAL_SECTOR_VARIATION_LEDGER_OR_QV_PIECE_LEAK_ROWS_2394"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


SOURCES = [
    {
        "source_id": "SRC2394_2393_doc",
        "path": str(POST_ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"),
        "needed_for": "selected 2394 target and vertical Noether contract",
        "needles": "NEXT2393_0_selected|VQC2393_4_Qv|epsilon_theta_piece_missing|epsilon_Qv_piece_missing",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_2393_certificate",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_QV_CERTIFICATE.csv"),
        "needed_for": "missing Qv and Theta certificate rows",
        "needles": "VQC2393_1_Theta_parent|VQC2393_4_Qv|MISSING_VERTICAL_QV",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_2393_leaks",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv"),
        "needed_for": "theta/Qv/Bv/integrability leak names",
        "needles": "epsilon_theta_piece_missing|epsilon_Qv_piece_missing|epsilon_Bv_ambiguity|epsilon_Hv_integrability",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_1008_piece_ledger",
        "path": str(RESIDUALS / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv"),
        "needed_for": "prior tau charge sector split",
        "needles": "QTA1008_0_L_parent|QTA1008_1_theta_total|QTA1008_5_Q_extra|QTA1008_6_Q_projector",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_1008_parent_audit",
        "path": str(RESIDUALS / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv"),
        "needed_for": "parent variation blockers",
        "needles": "PVA1008_0_parent_action|PVA1008_1_theta_MTS|PVA1008_6_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_1771_sector_variation",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv"),
        "needed_for": "retained local sectors and silence tests",
        "needles": "SAV1771_0_higher_derivative|SAV1771_1_projector|SAV1771_2_boundary|SAV1771_6_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_771_owner_audit",
        "path": str(RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"),
        "needed_for": "Noether current owner requirements",
        "needles": "TQ771_0_parent_variation|TQ771_1_Noether_current|TQ771_5_matter_coupling|TQ771_6_owner_verdict",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_2389_matter_owner",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv"),
        "needed_for": "matter/source current descent blockers",
        "needles": "OCC2389_2_Lm_density|OCC2389_4_matter_lift|OCC2389_7_MHref",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_2390_same_frame",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv"),
        "needed_for": "same-frame and support/projector descent blockers",
        "needles": "SFC2390_1_Obs_e|SFC2390_2_same_readout|SFC2390_5_projector_support",
        "valid_for_claim": no_claim(),
    },
    {
        "source_id": "SRC2394_2391_q_obse",
        "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv"),
        "needed_for": "quotient, basic coframe, and presymplectic-null blockers",
        "needles": "QOC2391_2_presymplectic_null|QOC2391_3_basic_coframe|QOC2391_6_matter_readout_descent",
        "valid_for_claim": no_claim(),
    },
]


def sector_variation_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_0_EH_local_geometry",
            "sector": "Einstein-Hilbert / observed local geometry",
            "vertical_variation_piece": "Theta_EH(e_obs; Lie_v e_obs) and mu_EH[v]",
            "conditional_derivation": "If e_obs=Obs_e(q(Phi)) and Dq(v)=0, then Lie_v e_obs=0; the EH vertical contribution to J_v and Q_v is zero in the quotient kernel. If v includes a true observed diffeomorphism, the usual EH charge is only a reference piece, not an MTS kernel proof.",
            "needed_parent_input": "parent q, Obs_e, basic coframe proof, and clear split between pure kernel v and observed spacetime diffeomorphism",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "theta_piece_status": "MISSING_BASIC_COFRAME_TO_KILL_THETA_EH",
            "Qv_piece_status": "MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT",
            "source_rows": "QOC2391_2_presymplectic_null;QOC2391_3_basic_coframe;SFC2390_1_Obs_e",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_1_matter_source",
            "sector": "ordinary matter / Hilbert source / worldtube",
            "vertical_variation_piece": "Theta_matter(v_m) - mu_m[v] plus possible source current constraints C_v^matter",
            "conditional_derivation": "If S_matter=Sbar_matter[q(Phi),psi,theta] and the matter lift fixes representation data along ker(Dq), then delta_v S_matter=0 and the matter/source piece is constraint-only with no independent vertical charge.",
            "needed_parent_input": "explicit L_m density, matter lift, no direct source slots, support theorem, and same-frame positive M_H_ref",
            "current_status": "CONDITIONAL_DESCENT_NOT_PARENT_SIGNED",
            "theta_piece_status": "MISSING_MATTER_THETA_DESCENT",
            "Qv_piece_status": "MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT",
            "source_rows": "OCC2389_2_Lm_density;OCC2389_4_matter_lift;OCC2389_7_MHref;TQ771_5_matter_coupling",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_2_extra_residual",
            "sector": "motion/time/domain/memory/range residual sector",
            "vertical_variation_piece": "Theta_extra(v_X) - mu_extra[v] = dQ_v^extra + C_v^extra + leak_extra",
            "conditional_derivation": "Any retained MTS residual field must either be quotient-basic, algebraic/constraint-only, or have its own Noether charge extracted. Otherwise the kernel can carry physical charge and local-GR reduction is not derived.",
            "needed_parent_input": "explicit retained extra-sector action and v action on motion/time/domain/memory variables",
            "current_status": "RETAINED_SECTOR_NOT_VARIED",
            "theta_piece_status": "MISSING_THETA_EXTRA",
            "Qv_piece_status": "MISSING_QV_EXTRA",
            "source_rows": "QTA1008_5_Q_extra;SAV1771_4_memory_coframe;TQ771_1_Noether_current",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_3_projector_readout",
            "sector": "projector / Pi_M / source-measure / readout support",
            "vertical_variation_piece": "Theta_projector(v_Pi,v_J,v_W)-mu_projector[v] plus [d,Pi_M] and delta Pi_M source terms",
            "conditional_derivation": "A projector/readout sector is silent only if Pi_M, support W, and readout surfaces descend through q/e_obs before scoring and commute with the relevant exterior derivative/current operation.",
            "needed_parent_input": "Pi_M chain map, [d,Pi_M] control, support descent, no readout retuning, and source worldtube equality",
            "current_status": "EXACT_OBSTRUCTION_KNOWN_NOT_SILENCED",
            "theta_piece_status": "MISSING_THETA_PROJECTOR",
            "Qv_piece_status": "MISSING_QV_PROJECTOR_OR_COMMUTATOR_BOUND",
            "source_rows": "QTA1008_6_Q_projector;SAV1771_1_projector;SFC2390_5_projector_support",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_4_boundary_reference",
            "sector": "boundary / reference / improvement",
            "vertical_variation_piece": "delta_v B_ref, Q_v^boundary, and improvement ambiguity in delta H_v[S]",
            "conditional_derivation": "Boundary/reference data are harmless only if fixed before readout, derivative-silent under v, and unable to absorb the residual normalization. Otherwise Q_v can be shifted by an improvement.",
            "needed_parent_input": "boundary class, reference subtraction, B_v convention, compact surface class, and zero-flux theorem",
            "current_status": "REFERENCE_SHAPE_KNOWN_NOT_PARENT_FIXED",
            "theta_piece_status": "MISSING_BOUNDARY_THETA_AND_BV",
            "Qv_piece_status": "MISSING_QV_BOUNDARY_AND_ZERO_FLUX",
            "source_rows": "QTA1008_4_Q_boundary;SAV1771_2_boundary;VQC2393_5_Bv_boundary",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_5_coupling_coframe",
            "sector": "nonminimal coupling / coframe / preferred-frame",
            "vertical_variation_piece": "Theta_coupling(v)-mu_coupling[v] and any Weyl/disformal/species/source-prefactor charge",
            "conditional_derivation": "The coupling sector is zero only if all constants, charge normalizations, coframes, connections, and species frames descend from the same q/Obs_e data with no direct residual slot.",
            "needed_parent_input": "coupling grammar, no shadow frame theorem, charge normalization descent, and WEP/common-geometry signature",
            "current_status": "COUPLING_ZERO_NOT_SIGNED",
            "theta_piece_status": "MISSING_THETA_COUPLING",
            "Qv_piece_status": "MISSING_QV_COUPLING_OR_NO_SLOT_PROOF",
            "source_rows": "SAV1771_3_nonminimal;SAV1771_4_memory_coframe;SFC2390_4_no_shadow_frame;QOC2391_6_matter_readout_descent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "SVL2394_6_total",
            "sector": "total parent vertical charge",
            "vertical_variation_piece": "J_v=sum_s(Theta_s(v)-mu_s[v]) = d(sum_s Q_v^s)+sum_s C_v^s+leak_v",
            "conditional_derivation": "Q_v is extracted only if every sector piece is derived, zeroed by descent, or bounded with a sourced coefficient. One unowned sector keeps epsilon_kernel_charge alive.",
            "needed_parent_input": "complete sector-by-sector parent variation ledger",
            "current_status": "TOTAL_QV_NOT_EXTRACTED",
            "theta_piece_status": "epsilon_theta_piece_missing_nonzero",
            "Qv_piece_status": "epsilon_Qv_piece_missing_nonzero",
            "source_rows": "VNC2393_5_verdict;VQC2393_4_Qv;QTA1008_8_Q_total",
            "valid_for_claim": no_claim(),
        },
    ]


def closure_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCC2394_0_additive_variation",
            "contract": "parent action sector sum",
            "required_clause": "L_parent=sum_s L_s + dB_ref with every retained L_s named before variation",
            "current_result": "sector labels exist, but no single adopted L_parent sums them",
            "claim_effect": "blocks total Theta_parent ownership",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCC2394_1_vertical_action",
            "contract": "v action on every sector",
            "required_clause": "v_epsilon acts on e_obs, matter, residual fields, projector/support, coupling constants/frames, and boundary/reference data",
            "current_result": "v action is formal and not sector-signed",
            "claim_effect": "blocks mu_v and sector current extraction",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCC2394_2_sector_current",
            "contract": "sector Noether current",
            "required_clause": "J_v^s=Theta_s(v)-mu_s[v]=dQ_v^s+C_v^s+leak_s for each sector",
            "current_result": "only the formal equation is available",
            "claim_effect": "Q_v remains a symbol, not a derived charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCC2394_3_zero_or_bound",
            "contract": "zero/bound every leak",
            "required_clause": "each leak_s is zero by descent/basicness/constraint, or becomes a sourced numeric bound row",
            "current_result": "no sector has a full zero certificate",
            "claim_effect": "local GR/Newton and PPN pass remain blocked",
            "valid_for_claim": no_claim(),
        },
    ]


def qv_piece_leak_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_EH_kernel_split",
            "definition": "possible EH/reference charge contamination if vertical v is not separated from observed diffeomorphism",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_0_EH_local_geometry",
            "status": "MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_matter_source",
            "definition": "unowned matter/source constraint or charge contribution to vertical Hamiltonian",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_1_matter_source",
            "status": "MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_extra",
            "definition": "retained motion/time/domain/memory/range Noether charge contribution",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_2_extra_residual",
            "status": "MISSING_QV_EXTRA",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_projector",
            "definition": "Pi_M/support/readout commutator or projector charge contribution",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_3_projector_readout",
            "status": "MISSING_QV_PROJECTOR_OR_COMMUTATOR_BOUND",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_boundary",
            "definition": "boundary/reference/improvement shift in vertical charge",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_4_boundary_reference",
            "status": "MISSING_QV_BOUNDARY_AND_ZERO_FLUX",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_coupling",
            "definition": "nonminimal coupling/coframe/shadow-frame vertical charge contribution",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_5_coupling_coframe",
            "status": "MISSING_QV_COUPLING_OR_NO_SLOT_PROOF",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "quantity_id": "epsilon_Qv_total",
            "definition": "sum of all unclosed sector Q_v pieces",
            "units": "dimensionless after M_H_ref normalization",
            "source_sector": "SVL2394_6_total",
            "status": "TOTAL_QV_NOT_EXTRACTED",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2394_0_accept_additive_sector_contract",
            "decision": "accept sector-additive vertical current decomposition",
            "reason": "If the parent action is a sector sum, the Noether current and charge must split by the same sectors plus boundary improvements.",
            "consequence": "future derivations must close or bound each sector, not only the EH-looking piece",
            "status": "CONDITIONAL_CONTRACT_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2394_1_no_sector_zero_claim",
            "decision": "do not claim any sector zero yet",
            "reason": "each candidate zero depends on missing q/Obs_e, matter lift, projector, coupling, boundary, or v-action clauses",
            "consequence": "epsilon_theta_piece_missing and epsilon_Qv_piece_missing stay alive",
            "status": "ALL_SECTOR_ZEROS_UNSIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2394_2_next",
            "decision": "attack EH/local-geometry kernel split first",
            "reason": "it is the least exotic sector and can establish whether pure vertical v is truly different from observed diffeomorphism; if this fails, the whole local-GR route becomes much harder",
            "consequence": "2395 should derive the EH/reference contribution for vertical v, or produce the EH contamination source row",
            "status": "SELECT_2395_EH_KERNEL_SPLIT",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2394_0_Qv_extracted",
            "gate": "vertical Q_v extracted",
            "gate_status": "BLOCKED",
            "claim_effect": "not extracted until all sector pieces are derived or killed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2394_1_kernel_null",
            "gate": "vertical kernel presymplectic-null",
            "gate_status": "BLOCKED",
            "claim_effect": "not proven while any sector charge leak remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2394_2_matter_invisible",
            "gate": "matter/source invisibility under vertical v",
            "gate_status": "BLOCKED",
            "claim_effect": "not proven without L_m density, lift, and no-direct-slot grammar",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2394_3_projector_silent",
            "gate": "projector/readout silent",
            "gate_status": "BLOCKED",
            "claim_effect": "not proven without Pi_M/support descent and commutator control",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2394_4_GR_Newton",
            "gate": "local GR/Newton reduction",
            "gate_status": "BLOCKED",
            "claim_effect": "no local GR/Newton claim from 2394",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2394_0_claim_sector_zero",
            "claim": "all vertical sector contributions vanish",
            "allowed": "false",
            "reason": "zero clauses are conditional and parent inputs remain missing",
            "blocking_rows": "SVL2394_0_EH_local_geometry;SVL2394_1_matter_source;SVL2394_2_extra_residual;SVL2394_3_projector_readout;SVL2394_4_boundary_reference;SVL2394_5_coupling_coframe",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2394_1_claim_Qv_piece_sum",
            "claim": "Q_v=sum_s Q_v^s has been extracted",
            "allowed": "false",
            "reason": "sector Q_v pieces are named but not calculated from a parent action",
            "blocking_rows": "SCC2394_0_additive_variation;SCC2394_1_vertical_action;SCC2394_2_sector_current",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2394_2_claim_GR_Newton",
            "claim": "local GR/Newton follows from the sector ledger",
            "allowed": "false",
            "reason": "the ledger is a derivation map, not the completed derivation",
            "blocking_rows": "CG2394_0_Qv_extracted;CG2394_1_kernel_null;CG2394_4_GR_Newton",
            "valid_for_claim": no_claim(),
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2394_0_selected",
            "next_file": "2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md",
            "success_condition": "prove pure vertical v gives Lie_v e_obs=0 and no EH Q_v contamination, while observed diffeomorphism charge remains only the GR reference",
            "fallback_condition": "create epsilon_Qv_EH_kernel_split bound/source row and keep local-GR gate blocked",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2394_1_parallel",
            "next_file": "2395b-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md",
            "success_condition": "prove vertical v leaves matter/source representation data invisible through q/Obs_e",
            "fallback_condition": "retain epsilon_Qv_matter_source and epsilon_hidden_source_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2394_2_later",
            "next_file": "2395c-Y5-R2FR-projector-commutator-and-boundary-improvement-cleanup.md",
            "success_condition": "prove Pi_M/support descent and fixed boundary improvement",
            "fallback_condition": "retain projector and boundary Q_v leak rows",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2394_SOURCE_REGISTER.csv": lambda: SOURCES,
    "P8_Y5_PARENT_QLOC_2394_SECTOR_VARIATION_LEDGER.csv": sector_variation_rows,
    "P8_Y5_PARENT_QLOC_2394_SECTOR_CLOSURE_CONTRACT.csv": closure_contract_rows,
    "P8_Y5_PARENT_QLOC_2394_QV_PIECE_LEAK_ROWS.csv": qv_piece_leak_rows,
    "P8_Y5_PARENT_QLOC_2394_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2394_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2394_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2394_NEXT_TARGET.csv": next_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    missing_sources = [src["path"] for src in SOURCES if not Path(src["path"]).exists()]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_00_sources_exist",
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": "all required source paths exist" if not missing_sources else ";".join(missing_sources),
            "valid_for_claim": no_claim(),
        }
    )

    missing_needles: list[str] = []
    for src in SOURCES:
        path = Path(src["path"])
        for needle in src["needles"].split("|"):
            if not contains(path, needle):
                missing_needles.append(f"{src['source_id']}::{needle}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_01_needles_found",
            "status": "PASS" if not missing_needles else "FAIL",
            "detail": "all source needles found" if not missing_needles else ";".join(missing_needles),
            "valid_for_claim": no_claim(),
        }
    )

    sectors = sector_variation_rows()
    expected_sector_ids = {
        "SVL2394_0_EH_local_geometry",
        "SVL2394_1_matter_source",
        "SVL2394_2_extra_residual",
        "SVL2394_3_projector_readout",
        "SVL2394_4_boundary_reference",
        "SVL2394_5_coupling_coframe",
        "SVL2394_6_total",
    }
    present_sector_ids = {row["sector_id"] for row in sectors}
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_02_all_major_sectors_present",
            "status": "PASS" if expected_sector_ids <= present_sector_ids else "FAIL",
            "detail": "EH, matter, extra, projector, boundary, coupling, and total sector rows present",
            "valid_for_claim": no_claim(),
        }
    )

    contracts = closure_contract_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_03_contract_has_current_split",
            "status": "PASS" if any("J_v^s=Theta_s(v)-mu_s[v]=dQ_v^s+C_v^s+leak_s" in row["required_clause"] for row in contracts) else "FAIL",
            "detail": "sector current split contract present",
            "valid_for_claim": no_claim(),
        }
    )

    leak_rows = qv_piece_leak_rows()
    leak_status = all(row["valid_for_claim"] == "false" and row["status"].startswith("MISSING") or row["status"] == "TOTAL_QV_NOT_EXTRACTED" for row in leak_rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_04_leak_rows_nonready",
            "status": "PASS" if leak_status else "FAIL",
            "detail": "all Qv piece leak rows remain nonclaim/nonready",
            "valid_for_claim": no_claim(),
        }
    )

    gates = claim_gate_rows()
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_05_global_claims_blocked",
            "status": "PASS" if all(row["gate_status"] == "BLOCKED" for row in gates) else "FAIL",
            "detail": "Qv, kernel-null, matter invisibility, projector silence, and GR/Newton gates blocked",
            "valid_for_claim": no_claim(),
        }
    )

    csv_failures: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            csv_failures.append(f"{name}:missing")
            continue
        try:
            parsed = csv_rows(path)
        except Exception as exc:
            csv_failures.append(f"{name}:{exc}")
            continue
        if not parsed:
            csv_failures.append(f"{name}:empty")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_06_csv_parse",
            "status": "PASS" if not csv_failures else "FAIL",
            "detail": "generated CSVs parse and have rows" if not csv_failures else ";".join(csv_failures),
            "valid_for_claim": no_claim(),
        }
    )

    true_claims: list[str] = []
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            continue
        for row in csv_rows(path):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                true_claims.append(f"{name}:{row}")
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_07_no_claim_flags",
            "status": "PASS" if not true_claims else "FAIL",
            "detail": "no generated row has valid_for_claim=true" if not true_claims else ";".join(true_claims),
            "valid_for_claim": no_claim(),
        }
    )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_08_formalization_untouched_by_script",
            "status": "PASS",
            "detail": "script writes only post-checkpoint-work outputs",
            "valid_for_claim": no_claim(),
        }
    )

    next_selected = any(row["row_id"] == "NEXT2394_0_selected" for row in next_rows())
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_09_next_selected",
            "status": "PASS" if next_selected else "FAIL",
            "detail": "EH/local-geometry kernel split selected next",
            "valid_for_claim": no_claim(),
        }
    )

    overall_status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2394_OVERALL",
            "status": overall_status,
            "detail": "2394 splits the formal vertical Qv problem into EH, matter, extra, projector, boundary, and coupling sectors, keeps every unsigned sector nonclaim, and selects EH kernel split next",
            "valid_for_claim": no_claim(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    sectors = sector_variation_rows()
    contracts = closure_contract_rows()
    leaks = qv_piece_leak_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()
    validation = validation_rows()

    body = f"""# 2394 — Vertical Sector Variation Ledger Or Qv Piece Leak Rows

## Result

2394 takes the formal 2393 object

`J_v := Theta_parent(v_epsilon) - mu_v = dQ_v + C_v`

and splits it into the sector-level contract

`J_v = sum_s J_v^s = sum_s(Theta_s(v)-mu_s[v]) = d(sum_s Q_v^s) + sum_s C_v^s + leak_v`.

This is a derivation advance, not a claim advance.  The useful result is that the missing `Q_v` is no longer one
foggy object.  It has six named doors:

1. EH/local geometry kernel split.
2. Matter/source descent.
3. Extra residual field charge.
4. Projector/readout commutator charge.
5. Boundary/reference improvement charge.
6. Coupling/coframe/shadow-frame charge.

The only safe route to local GR/Newton is: every door must either close by quotient descent/basicness/constraint,
or become a sourced bound row.  One open door keeps `epsilon_kernel_charge` alive.

## Derived Sector Identity

Assume only a sector-summed parent action:

`L_parent = L_EH + L_matter + L_extra + L_projector + dB_ref + L_coupling`.

Then, by linearity of the variation and Noether current construction,

`Theta_parent(v) = Theta_EH(v) + Theta_matter(v) + Theta_extra(v) + Theta_projector(v) + delta_v B_ref + Theta_coupling(v)`,

`mu_v = mu_EH + mu_matter + mu_extra + mu_projector + mu_boundary + mu_coupling`,

and therefore

`Q_v = Q_v^EH + Q_v^matter + Q_v^extra + Q_v^projector + Q_v^boundary + Q_v^coupling`

only after each sector current has actually been derived as `J_v^s=dQ_v^s+C_v^s+leak_s`.

Current MTS has not yet done this.  So the ledger below refuses the total charge claim and turns each unclosed
piece into an explicit leak row.

## Source Register

{markdown_table(SOURCES, ["source_id", "path", "needed_for", "needles", "valid_for_claim"])}

## Sector Variation Ledger

{markdown_table(sectors, ["sector_id", "sector", "vertical_variation_piece", "conditional_derivation", "current_status", "theta_piece_status", "Qv_piece_status", "source_rows", "valid_for_claim"])}

## Sector Closure Contract

{markdown_table(contracts, ["row_id", "contract", "required_clause", "current_result", "claim_effect", "valid_for_claim"])}

## Qv Piece Leak Rows

{markdown_table(leaks, ["quantity_id", "definition", "units", "source_sector", "status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_targets, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is a better shape than before.  We are no longer saying "derive `Q_v`" as if that is one black box.  The problem
has split into named pieces.  The least-scrutiny next move is the EH/local-geometry kernel split, because if pure
vertical directions truly leave `e_obs` fixed, then the EH sector can plausibly be removed from the kernel problem
without importing a fitted GR charge.  If that fails, the local branch keeps a concrete EH contamination row instead
of smuggling a plateau or gauge axiom.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2394_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2394_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
