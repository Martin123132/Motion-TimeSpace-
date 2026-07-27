from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4521"
CLAIM_ID = "L-363"
MARKER = "PPC4161_BOUNDARY_CDB_READOUT_SILENCE_OR_ALPHA_INPUT_FILL_4521"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_CDB_READOUT_SILENCE_OR_ALPHA_INPUT_FILL_4521"
DECISION = "BOUNDARY_CDB_READOUT_RHS_ZERO_THEOREM_DERIVED_CONDITIONALLY_FINITE_FALLBACKS_RETAINED"
NEXT_TARGET = "4522-Y5-R2FR-rank-M-lock-and-retained-current-firewall-or-alpha-runner.md"

FORMAL_PATH = FORMAL / "537-PPC4161-boundary-CDB-readout-silence-or-alpha-input-fill.md"
DOC_PATH = POST / "4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4521_SOURCE_REGISTER.csv"
THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4521_BOUNDARY_CDB_READOUT_THEOREM.csv"
RHS_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4521_RANK_ZERO_RHS_UPDATE.csv"
CLAUSE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4521_COMPONENT_CLAUSE_AUDIT.csv"
CDB_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4521_CDB_ZERO_OR_BOUND_MATRIX.csv"
READOUT_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4521_READOUT_FIREWALL.csv"
ALPHA_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4521_ALPHA_INPUT_FILL_DECISION.csv"
BRANCH_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4521_BRANCH_DECISION.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4521_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4521_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4521_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4521_VALIDATION.csv"

FORMAL_4520 = FORMAL / "536-PPC4161-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
DOC_4520 = POST / "4520-Y5-R2FR-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
RHS_4520 = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_RHS_CLOSURE_MAP.csv"
CLAUSES_4520 = SOURCE_DIR / "P8_Y5_R2FR_4520_SOURCE_CURRENT_CLAUSE_AUDIT.csv"
ALPHA_4520 = SOURCE_DIR / "P8_Y5_R2FR_4520_ALPHA_INPUT_FALLBACK_ACQUISITION.csv"

FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_529 = FORMAL / "529-PPC4161-boundary-domain-readout-tail-or-final-BWeyl-vector.md"

NO_FLUX_4176 = SOURCE_DIR / "P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv"
BD_4176 = SOURCE_DIR / "P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION.csv"
QN_4177 = SOURCE_DIR / "P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT.csv"
BDR_4513 = SOURCE_DIR / "P8_Y5_R2FR_4513_BOUNDARY_DOMAIN_READOUT_TAIL_THEOREM.csv"
PA_4513 = SOURCE_DIR / "P8_Y5_R2FR_4513_PARENT_SIGNATURE_AUDIT.csv"
CDB_2413 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2413_CDB_TO_ALGEBRAIC_RESIDUAL_MAP.csv"
CDB_SUB_2413 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2413_CDB_IMPORTABLE_SUBLEMMAS.csv"
CDB_ZERO_2112 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_ZERO_GATES.csv"
CDB_BOUND_2112 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_BOUND_ROWS.csv"
READOUT_EXCL_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_EXCLUSION_CERTIFICATE.csv"
READOUT_POLICY_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_CLOSURE_POLICY.csv"
VBR_1816 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv"
RNE_2353 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2353_READOUT_NO_REENTRY_ZERO_AUDIT.csv"
RNG_2418 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv"
CBP_2419 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_READOUT_BOUND_PACK.csv"
BP_2354 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2354_READOUT_REENTRY_BOUND_PACK.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC4521_00_formal4520", "4520 formal handoff", FORMAL_4520, "PPC4161_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520", "rank-zero source current handoff"),
        ("SRC4521_01_post4520", "4520 post handoff", DOC_4520, "4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md", "declared next target"),
        ("SRC4521_02_rhs4520", "4520 RHS closure map", RHS_4520, "RHS4520_6_Z", "remaining RHS after source-current silence"),
        ("SRC4521_03_clause4520", "4520 clause audit", CLAUSES_4520, "SCA4520_5_boundary", "boundary/CDB/readout live gates"),
        ("SRC4521_04_alpha4520", "4520 alpha fallback", ALPHA_4520, "AFA4520_0_Z", "finite-range fallback inputs"),
        ("SRC4521_05_boundary192", "PPC4161 boundary theorem", FORMAL_192, "PPC4161_LOCAL_BOUNDARY_NO_FLUX_SECTOR_INTERFACE_THEOREM", "no-flux selector theorem"),
        ("SRC4521_06_qnat193", "PPC4161 quotient naturality theorem", FORMAL_193, "PPC4161_QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM", "vertical/readout silence"),
        ("SRC4521_07_bweyl4513", "4513 boundary/domain/readout tail theorem", FORMAL_529, "PPC4161_BOUNDARY_DOMAIN_READOUT_TAIL_OR_FINAL_BWEYL_VECTOR_4513", "tail theorem lineage"),
        ("SRC4521_08_no_flux4176", "4176 no-flux theorem", NO_FLUX_4176, "NFT4176_5_no_flux_conclusion", "boundary no-flux conclusion"),
        ("SRC4521_09_bd4176", "4176 boundary/domain decomposition", BD_4176, "BD4176_5_projection", "local projection/readout boundary"),
        ("SRC4521_10_qn4177", "4177 quotient naturality", QN_4177, "QNC4177_6_naturality", "readout naturality"),
        ("SRC4521_11_bdr4513", "4513 BDR theorem", BDR_4513, "BDR4513_4_combined_tail_zero", "combined boundary/domain/readout zero"),
        ("SRC4521_12_pa4513", "4513 parent audit", PA_4513, "PA4513_1_same_branch", "same-branch not proved"),
        ("SRC4521_13_cdb2413", "CDB residual map", CDB_2413, "CRM2413_0_total_Qcdb", "CDB residual bound"),
        ("SRC4521_14_cdbsub2413", "CDB importable sublemmas", CDB_SUB_2413, "SUB2413_0_metric_only_LC", "CDB sublemma imports"),
        ("SRC4521_15_cdbzero2112", "CDB zero gates", CDB_ZERO_2112, "CZG2112_9_verdict", "component-zero verdict"),
        ("SRC4521_16_cdbbound2112", "CDB bound rows", CDB_BOUND_2112, "CDB2112_0_total", "absolute CDB fallback"),
        ("SRC4521_17_readout2625", "readout exclusion certificate", READOUT_EXCL_2625, "REC2625_1_solution_space_readout", "pure readout clause"),
        ("SRC4521_18_readoutpolicy2625", "readout closure policy", READOUT_POLICY_2625, "POL2625_1_reduced_action_retention", "reduced-action firewall"),
        ("SRC4521_19_vbr1816", "variation before readout", VBR_1816, "VBR1816_6_verdict", "post-readout theorem limit"),
        ("SRC4521_20_rne2353", "readout no-reentry audit", RNE_2353, "RNE2353_7_verdict", "general readout not closed"),
        ("SRC4521_21_rng2418", "readout no-reentry gate", RNG_2418, "RNG2418_7_verdict", "readout live countermodels"),
        ("SRC4521_22_cbp2419", "chainmap readout bound pack", CBP_2419, "CBP2419_0_total", "readout bound envelope"),
        ("SRC4521_23_bp2354", "readout reentry bound pack", BP_2354, "BP2354_0_total", "readout reentry envelope"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": needle in body,
            "line": line_of(path, needle),
            "note": note,
            "valid_for_claim": False,
        })
    return rows


def theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "BCR4521_0_rhs_start",
            "piece": "4520 rank-zero RHS",
            "statement": "After 4520, M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A.",
            "formula": "MZ = J_retained + B + CDB + R",
            "status": "INPUT_FROM_4520",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_1_boundary_zero",
            "piece": "boundary/corner/reference term",
            "statement": "B_A=0 if the local worldtube is compact/support-separated, boundary data are fixed or q-owned before variation, Hamiltonian flux is zero or routed as an explicit boundary charge, and no corner/reference/source class depends on v_A.",
            "formula": "D_v S_boundary = D_v Bbar[q(Phi)] + F_rad^routed + C_corner; if Dq[v]=0 and F_rad=C_corner=0 then B_A=0",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_2_cdb_zero",
            "piece": "connection/domain/boundary derivative tails",
            "statement": "C_A^CDB=0 if K_conn, K_domain, K_boundary and K_comm are each zero in the same branch: LC/Palatini-silent connection, q-basic fixed domain/support/projector, proper no-flux boundary, and pure postprocess readout commuting with variation/divergence.",
            "formula": "C_A^CDB <= N_div(K_conn+K_domain+K_boundary+K_comm+DeltaK_live); all components zero => C_A^CDB=0",
            "status": "DERIVED_CONDITIONAL_WITH_BOUND",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_3_readout_zero",
            "piece": "readout/projector reentry",
            "statement": "R_A=0 for post-solution readout maps R_post:Sol(S_parent)/G -> Data with variation-before-readout and no reduced action, field-dependent source-worldtube projector, calibration feedback, hidden marker, or apparatus source inserted before variation.",
            "formula": "D_v(R_post o q)=D R_post[Dq[v]]=0; pre-variation readout gives R_A^retained",
            "status": "DERIVED_CONDITIONAL_WITH_FIREWALL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_4_combined_rhs_zero",
            "piece": "conditional RHS silence",
            "statement": "If the 4520 Hilbert/Poynting source-current silence and BCR4521_1-3 hold in one same parent branch and J_A^retained=0, then the rank-zero RHS vanishes termwise.",
            "formula": "J_retained=B=CDB=R=0 => M_AB Z^B=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_5_finite_fallback",
            "piece": "no-cancellation residual bound",
            "statement": "If any clause fails, the failed component is retained as an absolute finite residual; no cancellation between B_A, CDB, R_A and J_A^retained is credited.",
            "formula": "||MZ|| <= ||J_retained||+||B||+||CDB||+||R||",
            "status": "DERIVED_BOUND_INTERFACE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "BCR4521_6_verdict",
            "piece": "4521 verdict",
            "statement": "4521 gives a clean conditional route through the remaining RHS terms but still does not prove local GR: same-branch signing, rank/M lock and J_retained exclusion remain open.",
            "formula": "conditional RHS zero; claim remains blocked",
            "status": "PARTIAL_ADVANCE_NOT_FULL_CLOSURE",
            "valid_for_claim": False,
        },
    ]


def rhs_rows() -> list[dict[str, object]]:
    return [
        {
            "rhs_id": "RHU4521_0_input",
            "component": "post-4520 rank-zero RHS",
            "before_4521": "M_AB Z^B = J_retained + B_A + CDB + R_A",
            "after_4521": "same expression, but B_A/CDB/R_A now have exact conditional zero laws and finite fallback rows",
            "status": "STRUCTURE_DERIVED",
            "next_gate": "same-branch signing plus rank/M lock",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHU4521_1_boundary",
            "component": "B_A",
            "before_4521": "live boundary/corner/reference source charge",
            "after_4521": "zero under fixed/q-owned no-flux Hamiltonian boundary; otherwise retained as B_rad+B_corner+B_ref",
            "status": "CONDITIONAL_ZERO_OR_FINITE",
            "next_gate": "proper boundary/topological class proof in the active branch",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHU4521_2_cdb",
            "component": "C_A^CDB",
            "before_4521": "live derivative/commutator tails",
            "after_4521": "zero if K_conn,K_domain,K_boundary,K_comm all zero; otherwise bounded by CDB component envelope",
            "status": "CONDITIONAL_ZERO_OR_BOUND",
            "next_gate": "component-by-component CDB signature",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHU4521_3_readout",
            "component": "R_A",
            "before_4521": "live source/readout/projector reentry",
            "after_4521": "zero for pure postprocess/variation-before-readout; retained for reduced-action, projector, calibration, marker, apparatus branches",
            "status": "CONDITIONAL_ZERO_OR_RETAINED",
            "next_gate": "readout firewall and source-worldtube fixedness",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHU4521_4_combined",
            "component": "full RHS",
            "before_4521": "J_retained+B+CDB+R",
            "after_4521": "J_retained remains the main live source channel; B/CDB/R can be silenced only under same-branch selector clauses",
            "status": "PARTIAL_REDUCTION_NOT_CLAIM",
            "next_gate": NEXT_TARGET,
            "valid_for_claim": False,
        },
    ]


def clause_rows() -> list[dict[str, object]]:
    return [
        {"clause_id": "CCA4521_0_same_branch", "component": "all", "required_clause": "4520 source-current, 4521 boundary, CDB and readout clauses hold in the same parent branch", "status": "NOT_SIGNED", "failure_mode": "separate private closures cannot be multiplied into a public local-GR theorem", "valid_for_claim": False},
        {"clause_id": "CCA4521_1_boundary_fixed", "component": "B_A", "required_clause": "fixed/q-owned boundary data before variation", "status": "CONDITIONAL", "failure_mode": "source-dependent reference/corner charge", "valid_for_claim": False},
        {"clause_id": "CCA4521_2_boundary_flux", "component": "B_A", "required_clause": "no side flux; radiative flux is zero or explicitly routed to Hamiltonian boundary charge", "status": "CONDITIONAL", "failure_mode": "nonzero radiative or transition flux becomes finite B_A", "valid_for_claim": False},
        {"clause_id": "CCA4521_3_cdb_connection", "component": "CDB", "required_clause": "connection is LC[g_obs] or Palatini-silent with zero hypermomentum/projective source", "status": "CONDITIONAL", "failure_mode": "connection mismatch K_conn", "valid_for_claim": False},
        {"clause_id": "CCA4521_4_cdb_domain", "component": "CDB", "required_clause": "domain/support/projector q-basic and fixed before readout", "status": "CONDITIONAL", "failure_mode": "moving support/domain K_domain", "valid_for_claim": False},
        {"clause_id": "CCA4521_5_cdb_boundary", "component": "CDB", "required_clause": "proper compact boundary/collar with vanishing finite jets or exact routed charge", "status": "CONDITIONAL", "failure_mode": "edge/corner/boundary K_boundary", "valid_for_claim": False},
        {"clause_id": "CCA4521_6_cdb_comm", "component": "CDB", "required_clause": "P_loc/readout/source projection commutes with variation and divergence", "status": "CONDITIONAL", "failure_mode": "projector/readout commutator K_comm", "valid_for_claim": False},
        {"clause_id": "CCA4521_7_readout_post", "component": "R_A", "required_clause": "readout is pure postprocessing on solution space after variation", "status": "CONDITIONAL", "failure_mode": "pre-variation readout reentry", "valid_for_claim": False},
        {"clause_id": "CCA4521_8_readout_firewall", "component": "R_A", "required_clause": "no reduced action, calibration feedback, hidden material marker, source-worldtube projector or apparatus stress disguised as readout", "status": "LIVE_FIREWALL", "failure_mode": "R_A retained", "valid_for_claim": False},
        {"clause_id": "CCA4521_9_rank_M", "component": "Z", "required_clause": "M_AB invertible/first-class lock on the same rank-zero quotient", "status": "NEXT_TARGET", "failure_mode": "even zero RHS does not imply physical Z=0 until rank/M branch is signed", "valid_for_claim": False},
    ]


def cdb_rows() -> list[dict[str, object]]:
    return [
        {"cdb_id": "CDB4521_0_total", "component": "C_A^CDB", "zero_route": "all component norms vanish in same branch", "bound_if_not_zero": "||CDB|| <= A_ref^-1 N_div(K_conn+K_domain+K_boundary+K_comm+DeltaK_live)", "status": "CONDITIONAL_ZERO_OR_BOUND", "valid_for_claim": False},
        {"cdb_id": "CDB4521_1_Kconn", "component": "K_conn", "zero_route": "LC[g_obs] or Palatini EH-only connection with zero hypermomentum/projective source", "bound_if_not_zero": "K_LC_mismatch + torsion/nonmetricity/source trace terms", "status": "CONDITIONAL", "valid_for_claim": False},
        {"cdb_id": "CDB4521_2_Kdomain", "component": "K_domain", "zero_route": "domain/window/support/projector descends from q or is fixed/topological", "bound_if_not_zero": "C_chi||delta_g chi_D|| + C_sup||delta_g support|| + C_read||delta_g R_readout||", "status": "CONDITIONAL", "valid_for_claim": False},
        {"cdb_id": "CDB4521_3_Kboundary", "component": "K_boundary", "zero_route": "proper compact collar, fixed reference and routed/no flux", "bound_if_not_zero": "|b_C|+|outer_flux|+|corner|+|h_edge|+|Pi_R_tot|", "status": "CONDITIONAL", "valid_for_claim": False},
        {"cdb_id": "CDB4521_4_Kcomm", "component": "K_comm", "zero_route": "pure postprocess readout and commuting local projector/source measure", "bound_if_not_zero": "||(delta P_loc)J|| + ||[P_loc,nabla]K_res|| + ||[delta_parent,R_pre]T_H||", "status": "CONDITIONAL", "valid_for_claim": False},
        {"cdb_id": "CDB4521_5_policy", "component": "no cancellation", "zero_route": "each component zero independently", "bound_if_not_zero": "absolute sum; no inter-component cancellation credit", "status": "GUARD", "valid_for_claim": False},
    ]


def readout_rows() -> list[dict[str, object]]:
    return [
        {"firewall_id": "RFW4521_0_pure_postprocess", "readout_case": "R_post:Sol(S_parent)/G -> Data", "verdict": "ZERO_CONDITIONAL", "reason": "absent from parent/effective action before variation", "residual_if_fails": "none if pure", "valid_for_claim": False},
        {"firewall_id": "RFW4521_1_variation_before_readout", "readout_case": "source current formed before readout/selector", "verdict": "ZERO_CONDITIONAL", "reason": "post-current transfer coefficients are not source couplings", "residual_if_fails": "pre-action weights become retained branch", "valid_for_claim": False},
        {"firewall_id": "RFW4521_2_reduced_action", "readout_case": "varied S_red[g,P_read] or S_eff with readout/cutoff", "verdict": "RETAINED", "reason": "reduced action can produce real Euler/source terms", "residual_if_fails": "R_A^red", "valid_for_claim": False},
        {"firewall_id": "RFW4521_3_worldtube_projector", "readout_case": "field-dependent source worldtube/projector/support", "verdict": "RETAINED_OR_BOUND", "reason": "delta(Pi J)=Pi delta J+(delta Pi)J", "residual_if_fails": "epsilon_chainmap_readout_abs", "valid_for_claim": False},
        {"firewall_id": "RFW4521_4_calibration", "readout_case": "GM/PPN/calibration feedback or material/clock sensitivity", "verdict": "RETAINED", "reason": "calibration masks can be physical source standards", "residual_if_fails": "R_A^cal", "valid_for_claim": False},
        {"firewall_id": "RFW4521_5_marker", "readout_case": "material/species/source labels renamed as readout", "verdict": "RETAINED", "reason": "hidden markers are not killed by postprocessing theorem", "residual_if_fails": "R_A^marker", "valid_for_claim": False},
    ]


def alpha_rows() -> list[dict[str, object]]:
    rows = []
    for row in read_csv(ALPHA_4520):
        rows.append({
            "alpha_decision_id": row["fallback_id"].replace("AFA4520", "AFD4521"),
            "source_quantity": row["source_quantity"],
            "4521_decision": "DEFERRED_NOT_FILLED",
            "reason": "4521 produced a conditional RHS-zero route; alpha input filling is reserved for explicit branch failure or finite-rank selection",
            "current_status": row["current_status"],
            "required_evidence": row["required_evidence"],
            "valid_for_claim": False,
        })
    return rows


def branch_rows() -> list[dict[str, object]]:
    return [
        {"decision_id": "BD4521_0_boundary", "branch": "boundary B_A", "result": "CONDITIONAL_ZERO_OR_FINITE", "reason": "fixed/q-owned no-flux Hamiltonian boundary kills B_A; radiative/corner/reference charges remain finite residuals", "next_action": "same-branch parent signing", "valid_for_claim": False},
        {"decision_id": "BD4521_1_cdb", "branch": "CDB derivative tails", "result": "CONDITIONAL_ZERO_OR_BOUND", "reason": "CDB decomposed into K_conn,K_domain,K_boundary,K_comm with zero routes and absolute bounds", "next_action": "component signature or numeric bound rows", "valid_for_claim": False},
        {"decision_id": "BD4521_2_readout", "branch": "readout/projector R_A", "result": "CONDITIONAL_ZERO_OR_RETAINED", "reason": "pure postprocessing is silent; reduced-action/projector/calibration/marker branches retained", "next_action": "readout firewall adoption", "valid_for_claim": False},
        {"decision_id": "BD4521_3_rank_zero", "branch": "full rank-zero silence", "result": "NOT_CLOSED", "reason": "J_retained, same-branch signing, and rank/M lock remain open", "next_action": NEXT_TARGET, "valid_for_claim": False},
        {"decision_id": "BD4521_4_alpha", "branch": "finite alpha fallback", "result": "DEFERRED", "reason": "do not fill alpha rows until rank-zero route fails or finite rank is selected", "next_action": "keep alpha contract staged", "valid_for_claim": False},
    ]


def claim_rows() -> list[dict[str, object]]:
    return [
        {"gate_id": "CG4521_0_boundary", "claim": "B_A=0", "passed": False, "blocker": "only conditional; same-branch boundary/no-flux/source-reference clauses not parent-signed", "valid_for_claim": False},
        {"gate_id": "CG4521_1_cdb", "claim": "C_A^CDB=0", "passed": False, "blocker": "component zero routes exist but active-branch K_conn/K_domain/K_boundary/K_comm signatures are unsigned", "valid_for_claim": False},
        {"gate_id": "CG4521_2_readout", "claim": "R_A=0", "passed": False, "blocker": "pure postprocess theorem does not cover reduced action/projector/calibration/marker counterbranches", "valid_for_claim": False},
        {"gate_id": "CG4521_3_rhs", "claim": "full rank-zero RHS=0", "passed": False, "blocker": "J_retained, same-branch signing and rank/M lock remain open", "valid_for_claim": False},
        {"gate_id": "CG4521_4_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "conditional RHS theorem is not parent-signed and no empirical local gate is claim-ready", "valid_for_claim": False},
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "conditional zero laws for B_A, CDB and R_A plus absolute no-cancellation fallback bounds",
            "not_derived": "same-branch parent signing,J_retained=0,rank(Z)=0 certificate,M_AB lock,global adoption,alpha numeric inputs",
            "claim_status": "NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": now(),
        }
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NT4521_0",
            "target_file": NEXT_TARGET,
            "task": "try to lock rank(Z_AB)=0 and M_AB on the physical quotient while excluding J_retained in the same branch; if that fails, run the finite alpha fallback input contract",
        }
    ]


def validate(sources: list[dict[str, object]], theorem: list[dict[str, object]], rhs: list[dict[str, object]], clauses: list[dict[str, object]], cdb: list[dict[str, object]], readout: list[dict[str, object]], claims: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append({"validation_id": validation_id, "status": "PASS" if ok else "FAIL", "detail": detail})

    add("VAL4521_00_sources", all(row["exists"] and row["needle_found"] for row in sources), "all source paths exist and source needles are found")
    add("VAL4521_01_theorem", any(row["theorem_id"] == "BCR4521_4_combined_rhs_zero" for row in theorem), "combined RHS theorem row exists")
    add("VAL4521_02_rhs", any(row["rhs_id"] == "RHU4521_4_combined" and row["status"] == "PARTIAL_REDUCTION_NOT_CLAIM" for row in rhs), "combined RHS remains nonclaim")
    add("VAL4521_03_clauses", len(clauses) == 10 and any(row["clause_id"] == "CCA4521_9_rank_M" for row in clauses), "ten clause audit rows including rank/M next gate")
    add("VAL4521_04_cdb", any(row["cdb_id"] == "CDB4521_0_total" for row in cdb) and any(row["cdb_id"] == "CDB4521_5_policy" for row in cdb), "CDB total and no-cancellation policy exist")
    add("VAL4521_05_readout", any(row["firewall_id"] == "RFW4521_2_reduced_action" and row["verdict"] == "RETAINED" for row in readout), "readout reduced-action firewall is retained")
    add("VAL4521_06_claims_blocked", all(str(row["passed"]).lower() == "false" and str(row["valid_for_claim"]).lower() == "false" for row in claims), "all claim gates remain blocked")
    csv_paths = [SOURCE_REGISTER, THEOREM, RHS_UPDATE, CLAUSE_AUDIT, CDB_MATRIX, READOUT_FIREWALL, ALPHA_DECISION, BRANCH_DECISION, CLAIM_GATES, STATUS_CSV, NEXT_CSV]
    parsed_ok = True
    detail = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # noqa: BLE001
            parsed_ok = False
            detail.append(f"{path.name}:{exc}")
    add("VAL4521_07_csv_parse", parsed_ok, ";".join(detail))
    add("VAL4521_08_next_target", NEXT_TARGET in text(NEXT_CSV), NEXT_TARGET)
    add("VAL4521_09_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")
    add("VAL4521_OVERALL", all(row["status"] == "PASS" for row in rows), "4521 boundary/CDB/readout silence or alpha input fill")
    return rows


def build_doc(sources: list[dict[str, object]], theorem: list[dict[str, object]], rhs: list[dict[str, object]], clauses: list[dict[str, object]], cdb: list[dict[str, object]], readout: list[dict[str, object]], alpha: list[dict[str, object]], branch: list[dict[str, object]], claims: list[dict[str, object]], status: list[dict[str, object]], next_target: list[dict[str, object]], validation: list[dict[str, object]]) -> str:
    return f"""# 4521 - Boundary/CDB/Readout Silence Or Alpha Input Fill

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4520 reduced the rank-zero equation to:

`M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A`.

4521 attacks the three non-source pieces instead of writing another open ledger:

- `B_A` is boundary/corner/reference leakage.
- `C_A^CDB` is connection/domain/boundary/projector derivative leakage.
- `R_A` is source-readout/projector reentry.

The conditional theorem is exact:

`B_A=C_A^CDB=R_A=0`

if the active parent branch has fixed/q-owned no-flux boundary data, zero CDB component tails, and pure post-solution readout with variation before readout. If any clause fails, the failed term is retained as a finite residual and no cancellation is credited.

So the project moved forward, but it is still not a local-GR claim: `J_A^retained`, the same-branch signature, `rank(Z_AB)=0`, and the `M_AB` lock remain open.

## Source Register

{table(sources)}

## Boundary/CDB/Readout Theorem

{table(theorem)}

## Rank-Zero RHS Update

{table(rhs)}

## Component Clause Audit

{table(clauses)}

## CDB Zero Or Bound Matrix

{table(cdb)}

## Readout Firewall

{table(readout)}

## Alpha Input Fill Decision

{table(alpha)}

## Branch Decision

{table(branch)}

## Claim Gates

{table(claims)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def append_claim_once() -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_rank_zero_rhs",
        "claim": "4521 conditionally derives boundary, CDB and readout/projector silence laws for the rank-zero RHS, with finite no-cancellation fallback lanes.",
        "current_evidence": "Generated theorem BCR4521_1-6, RHS update RHU4521_0-4, CDB/readout firewall matrices, and validation P8_Y5_BRR545_4521_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Same-branch signing, J_retained exclusion, rank(Z_AB)=0 certificate and M_AB lock remain unproved.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Conditional closure could be mistaken for a parent-signed local-GR theorem; alpha fallback still needed if any gate fails.",
    }
    if not CLAIMS_PATH.exists():
        write_csv(CLAIMS_PATH, [row])
        return
    existing = read_csv(CLAIMS_PATH)
    if any(existing_row.get("claim_id") == CLAIM_ID for existing_row in existing):
        return
    headers = list(existing[0].keys()) if existing else list(row.keys())
    with CLAIMS_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writerow({header: row.get(header, "") for header in headers})


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    rhs = rhs_rows()
    clauses = clause_rows()
    cdb = cdb_rows()
    readout = readout_rows()
    alpha = alpha_rows()
    branch = branch_rows()
    claims = claim_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM, theorem)
    write_csv(RHS_UPDATE, rhs)
    write_csv(CLAUSE_AUDIT, clauses)
    write_csv(CDB_MATRIX, cdb)
    write_csv(READOUT_FIREWALL, readout)
    write_csv(ALPHA_DECISION, alpha)
    write_csv(BRANCH_DECISION, branch)
    write_csv(CLAIM_GATES, claims)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, rhs, clauses, cdb, readout, claims)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, rhs, clauses, cdb, readout, alpha, branch, claims, status, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4521 Boundary/CDB/Readout Silence Or Alpha Input Fill

Marker: `{MARKER}`  
4521 derives the conditional zero theorem for the remaining non-source pieces in the rank-zero RHS: `B_A`, `C_A^CDB` and `R_A`. The RHS can vanish termwise only if the boundary/no-flux, CDB component, readout firewall, source-current, retained-current and rank/M clauses all hold in the same branch. Otherwise the failed terms remain finite residuals; no cancellation is credited.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4521 Packet Integration

Marker: `{PACKET_MARKER}`  
The private local packet now has a single rank-zero RHS discipline: prove termwise silence for `J_retained`, `B_A`, `CDB` and `R_A`, then lock `rank(Z_AB)=0` and `M_AB`; otherwise route to finite alpha/residual inputs. Next target: `{NEXT_TARGET}`.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
