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

CHECKPOINT = "4520"
CLAIM_ID = "L-362"
MARKER = "PPC4161_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520"
PACKET_MARKER = "PPC4161_PACKET_RANK_ZERO_SOURCE_CURRENT_SILENCE_OR_ALPHA_INPUT_ACQUISITION_4520"
DECISION = "RANK_ZERO_HILBERT_SOURCE_CURRENT_SILENCE_DERIVED_CONDITIONALLY_BOUNDARY_CDB_READOUT_STILL_LIVE"
NEXT_TARGET = "4521-Y5-R2FR-boundary-CDB-readout-silence-or-alpha-input-fill.md"

FORMAL_PATH = FORMAL / "536-PPC4161-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
DOC_PATH = POST / "4520-Y5-R2FR-rank-zero-source-current-silence-or-alpha-input-acquisition.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4520_SOURCE_REGISTER.csv"
THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_SOURCE_CURRENT_SILENCE_THEOREM.csv"
CLAUSE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4520_SOURCE_CURRENT_CLAUSE_AUDIT.csv"
POYNTING_GATE = SOURCE_DIR / "P8_Y5_R2FR_4520_POYNTING_HILBERT_FLOW_GATE.csv"
RHS_MAP = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_RHS_CLOSURE_MAP.csv"
ALPHA_FALLBACK = SOURCE_DIR / "P8_Y5_R2FR_4520_ALPHA_INPUT_FALLBACK_ACQUISITION.csv"
BRANCH_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4520_BRANCH_DECISION.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4520_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4520_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4520_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4520_VALIDATION.csv"

FORMAL_4519 = FORMAL / "535-PPC4161-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md"
DOC_4519 = POST / "4519-Y5-R2FR-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md"
RANK_RESIDUAL_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv"
BRANCH_STATUS_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_BRANCH_STATUS.csv"
ALPHA_INPUT_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_ALPHA_LAMBDA_INPUT_CONTRACT.csv"
FORMAL_4515 = FORMAL / "531-PPC4161-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
FORMAL_4516 = FORMAL / "532-PPC4161-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
FORMAL_4517 = FORMAL / "533-PPC4161-domain-bulk-species-source-tail-or-coefficient-fill.md"
SOURCE_FUNCTOR_4515 = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
COUPLING_4515 = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
WARD_CONTRACT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
HILBERT_DIV = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
HILBERT_VERDICT = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv"
RZ_THEOREM_2213 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv"
CONSTRAINT_2264 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2264_CONDITIONAL_CONSTRAINT_THEOREM.csv"
CONSTRAINT_GATES_2263 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv"


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


def markdown_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


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
        ("SRC4520_00_formal4519", "4519 formal branch split", FORMAL_4519, "PPC4161_BULK_RANGE_ALPHA_CURVE_INPUT_FILL_OR_RANK_ZERO_CONSTRAINT_4519", "finite/rank-zero classifier handoff"),
        ("SRC4520_01_post4519", "4519 post next target", DOC_4519, "NT4519_0", "declares rank-zero source-current target"),
        ("SRC4520_02_rzr4519", "4519 rank-zero RHS map", RANK_RESIDUAL_4519, "RZR4519_1_J", "source current component in RHS"),
        ("SRC4520_03_branch4519", "4519 branch status", BRANCH_STATUS_4519, "BST4519_1_rank_zero", "rank-zero theorem ready but unsigned"),
        ("SRC4520_04_alpha4519", "4519 alpha fallback", ALPHA_INPUT_4519, "AIC4519_2_Qsource", "finite-range input fallback"),
        ("SRC4520_05_formal4515", "4515 source functor prose", FORMAL_4515, "PPC4161_Y5Y6_SOURCE_TRACE_TAIL_OR_CMEM_JMEM_SOURCE_COUPLING_VECTOR_4515", "source functor descent theorem"),
        ("SRC4520_06_sft4515", "4515 source functor theorem", SOURCE_FUNCTOR_4515, "SFT4515_4_EM_Poynting_guard", "Poynting/Hilbert guard"),
        ("SRC4520_07_scv4515", "4515 coupling vector", COUPLING_4515, "SCV4515_2_Jmem_EM_Poynting", "EM/Poynting flux channel"),
        ("SRC4520_08_ward", "source-current Ward contract", WARD_CONTRACT, "SC4_no_nonHilbert_source_current", "non-Hilbert current gate"),
        ("SRC4520_09_owner", "source-owner action contract", OWNER_CONTRACT, "A2_no_retained_source_constraint", "retained source exclusion"),
        ("SRC4520_10_hilbert_div", "Hilbert divergence identity", HILBERT_DIV, "DIV2467_4_Killing_clock", "stationary Hilbert current route"),
        ("SRC4520_11_hilbert_verdict", "Hilbert promotion verdict", HILBERT_VERDICT, "PV2467_2_worldtube", "worldtube surface independence"),
        ("SRC4520_12_formal4516", "4516 stationary source subset", FORMAL_4516, "PPC4161_SOURCE_FUNCTOR_PARENT_SIGNATURE_OR_FIRST_Y5_COEFFICIENT_FILL_4516", "stationary no-flux source closures"),
        ("SRC4520_13_formal4517", "4517 domain source theorem", FORMAL_4517, "PPC4161_DOMAIN_BULK_SPECIES_SOURCE_TAIL_OR_COEFFICIENT_FILL_4517", "domain/source split"),
        ("SRC4520_14_rz2213", "2213 rank-zero theorem attempt", RZ_THEOREM_2213, "RZS2213_2_rank_zero_silence_theorem", "older rank-zero silence theorem"),
        ("SRC4520_15_constraint2264", "2264 conditional constraint theorem", CONSTRAINT_2264, "THM2264_0_constraint_statement", "constraint route"),
        ("SRC4520_16_gates2263", "2263 constraint algebra gates", CONSTRAINT_GATES_2263, "CAG2263_5_matter", "matter compatibility gate"),
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
            "theorem_id": "RZSC4520_0_definition",
            "piece": "rank-zero source current",
            "statement": "For an eliminated/rank-zero direction v_A, define J_A^src := D_{v_A} S_src, the vertical derivative of the source sector before readout.",
            "derivation_status": "DERIVED_DEFINITION",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_1_chain_rule",
            "piece": "quotient descent zero",
            "statement": "If S_src = Sbar_src[q(Phi),Psi,theta] and Dq[v_A]=0 with no vertical action on Psi or theta, then D_{v_A} Sbar_src = <delta Sbar_src/delta q,Dq[v_A]>=0.",
            "derivation_status": "DERIVED_CONDITIONAL",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_2_hilbert_matter",
            "piece": "ordinary Hilbert matter silence",
            "statement": "For q-basic Hilbert matter with a universal coframe/current owner, ordinary matter contributes no independent vertical source current: J_A^Hilbert=0.",
            "derivation_status": "DERIVED_CONDITIONAL",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_3_poynting",
            "piece": "EM/Poynting flow",
            "statement": "Poynting flow is a Hilbert stress flux, S^i=-T_EM^i{}_nu tau^nu. In a stationary no-flux worldtube it contributes boundary flux, not a bulk J_A; if the wall flux vanishes and the EM action is q-basic, J_A^EM/Poynting=0.",
            "derivation_status": "DERIVED_CONDITIONAL",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_4_retained",
            "piece": "retained/non-Hilbert exception",
            "statement": "Any explicit vertical dependence in constitutive maps, non-Hilbert source standards, memory kernels, material markers, or readout selectors survives as J_A^retained.",
            "derivation_status": "DERIVED_SPLIT",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_5_rhs_reduction",
            "piece": "rank-zero RHS after Hilbert silence",
            "statement": "The rank-zero equation reduces to M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A^src/readout/projector once the Hilbert/ordinary/Poynting subcurrent is silent.",
            "derivation_status": "DERIVED_CONDITIONAL_REDUCTION",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZSC4520_6_verdict",
            "piece": "4520 theorem verdict",
            "statement": "4520 proves the useful conditional source-current part, not the whole local-GR branch. The remaining live gates are retained current, boundary/corner B_A, CDB tails, readout/projector R_A, and the rank/M lock.",
            "derivation_status": "PARTIAL_ADVANCE_NOT_FULL_CLOSURE",
            "claim_status": "NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def clause_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "SCA4520_0_vertical",
            "clause": "v_A in ker(Dq)",
            "needed_for": "Dq[v_A]=0 chain-rule zero",
            "current_status": "CONDITIONAL_FROM_RANK_ZERO_ROUTE_NOT_PARENT_CERTIFIED",
            "closes": "quotient-visible source variation",
            "still_open": "rank certificate on physical quotient",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_1_matter_descent",
            "clause": "S_matter descends through q(Phi) and observed coframe",
            "needed_for": "ordinary matter source silence",
            "current_status": "CONTRACT_EXISTS_PARENT_SIGNATURE_INCOMPLETE",
            "closes": "J_A^Hilbert conditionally",
            "still_open": "full parent action signature",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_2_no_vertical_standards",
            "clause": "masses, clocks, rods, material labels and source standards have no explicit v_A dependence",
            "needed_for": "no retained source current",
            "current_status": "NOT_FULLY_SIGNED",
            "closes": "none globally",
            "still_open": "species/material/readout charges",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_3_hilbert_ward",
            "clause": "Hilbert current conserved in stationary collar",
            "needed_for": "closed source monopole and no bulk source leak",
            "current_status": "DERIVED_CONDITIONAL_FROM_2467_4516",
            "closes": "radial/time Hilbert drift subset",
            "still_open": "parent ell_J and Newton calibration",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_4_poynting_no_flux",
            "clause": "EM/Poynting is Hilbert-owned and no wall flux crosses the local worldtube",
            "needed_for": "J_A^EM/Poynting=0",
            "current_status": "DERIVED_CONDITIONAL_GUARD",
            "closes": "Poynting bulk-current worry under no-flux",
            "still_open": "radiative/constitutive/non-Hilbert EM branch",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_5_boundary",
            "clause": "boundary/corner/reference source charge vanishes",
            "needed_for": "B_A=0",
            "current_status": "LIVE",
            "closes": "nothing in 4520",
            "still_open": "proper boundary/topological class proof",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_6_cdb",
            "clause": "connection/domain/boundary derivative tails are zero or constraint-owned",
            "needed_for": "C_A^CDB=0",
            "current_status": "LIVE",
            "closes": "nothing in 4520",
            "still_open": "CDB operator inventory and sign",
            "valid_for_claim": False,
        },
        {
            "clause_id": "SCA4520_7_readout",
            "clause": "source-normalization/readout/projector does not reinsert v_A",
            "needed_for": "R_A=0",
            "current_status": "LIVE",
            "closes": "nothing in 4520",
            "still_open": "observed-descent/fixed-readout protocol",
            "valid_for_claim": False,
        },
    ]


def poynting_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PHF4520_0_identify",
            "object": "Poynting vector",
            "mathematical_role": "S^i=-T_EM^i{}_nu tau^nu is an energy flux component of the Hilbert stress tensor",
            "if_hilbert_owned": "belongs to T_EM in the ordinary source current",
            "if_not_hilbert_owned": "becomes retained current J_A^retained",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PHF4520_1_worldtube",
            "object": "local no-flux collar",
            "mathematical_role": "int_{partial W} T_EM^{mu nu} tau_nu n_mu dSigma = 0",
            "if_hilbert_owned": "no independent bulk J_A^EM/Poynting",
            "if_not_hilbert_owned": "finite flux/current bound required",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PHF4520_2_stationarity",
            "object": "stationary EM field branch",
            "mathematical_role": "partial_t source monopole = 0 and no radiative escape in local collar",
            "if_hilbert_owned": "supports J_A^EM/Poynting=0 under quotient descent",
            "if_not_hilbert_owned": "route to alpha/source-current acquisition",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PHF4520_3_verdict",
            "object": "Poynting concern",
            "mathematical_role": "not ignored; it is either Hilbert-owned no-flux or explicitly retained",
            "if_hilbert_owned": "conditionally silent",
            "if_not_hilbert_owned": "live finite residual",
            "valid_for_claim": False,
        },
    ]


def rhs_rows() -> list[dict[str, object]]:
    return [
        {
            "rhs_id": "RHS4520_0_J_Hilbert",
            "component": "ordinary Hilbert source current",
            "before_4520": "part of J_A",
            "after_4520": "J_A^Hilbert=0 under q-basic matter, vertical silence, stationary/no-flux collar",
            "status": "CONDITIONALLY_DERIVED_ZERO",
            "next_gate": "parent action signature and rank certificate",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_1_J_EM_Poynting",
            "component": "EM/Poynting source flow",
            "before_4520": "possible J_A concern",
            "after_4520": "zero if Hilbert-owned and no worldtube flux; retained otherwise",
            "status": "CONDITIONALLY_DERIVED_ZERO_OR_RETAINED",
            "next_gate": "EM owner/constitutive branch",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_2_J_retained",
            "component": "retained non-Hilbert current",
            "before_4520": "live",
            "after_4520": "still live unless parent excludes explicit vertical source dependence",
            "status": "LIVE",
            "next_gate": "source-owner no-retained-current theorem",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_3_B",
            "component": "B_A boundary/corner/reference",
            "before_4520": "live",
            "after_4520": "unchanged",
            "status": "LIVE",
            "next_gate": "boundary/corner no source charge",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_4_CDB",
            "component": "C_A^CDB derivative tails",
            "before_4520": "live",
            "after_4520": "unchanged",
            "status": "LIVE",
            "next_gate": "CDB topological/constraint-owned inventory",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_5_R",
            "component": "R_A source/readout/projector",
            "before_4520": "live",
            "after_4520": "unchanged",
            "status": "LIVE",
            "next_gate": "observed-descent fixed readout",
            "valid_for_claim": False,
        },
        {
            "rhs_id": "RHS4520_6_Z",
            "component": "rank-zero solution",
            "before_4520": "M_AB Z^B = J+B+CDB+R",
            "after_4520": "M_AB Z^B = J_retained+B+CDB+R after Hilbert/Poynting silence",
            "status": "PARTIAL_REDUCTION_NOT_CLOSURE",
            "next_gate": NEXT_TARGET,
            "valid_for_claim": False,
        },
    ]


def alpha_fallback_rows() -> list[dict[str, object]]:
    rows = []
    for row in read_csv(ALPHA_INPUT_4519):
        rows.append({
            "fallback_id": row["input_id"].replace("AIC4519", "AFA4520"),
            "source_quantity": row["quantity"],
            "required_if": "rank-zero source/current/boundary/CDB/readout silence fails or rank(Z_AB)>0",
            "formula_role": row["formula_role"],
            "required_evidence": row["required_evidence"],
            "current_status": row["current_status"],
            "valid_for_claim": False,
        })
    return rows


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD4520_0_source_current",
            "branch": "rank-zero source-current silence",
            "result": "PARTIAL_ADVANCE",
            "reason": "Hilbert ordinary matter and Hilbert-owned Poynting are silent under quotient descent and stationary no-flux; retained current remains live.",
            "next_action": "try boundary/CDB/readout silence before alpha scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "BD4520_1_rank_zero",
            "branch": "full rank-zero local silence",
            "result": "NOT_CLOSED",
            "reason": "rank certificate, M_AB lock, retained source, boundary, CDB and readout gates remain unsigned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        },
        {
            "decision_id": "BD4520_2_alpha",
            "branch": "finite-range alpha(lambda)",
            "result": "FALLBACK_STAGED",
            "reason": "use only if rank-zero route fails or finite rank is parent-selected; no alpha rows are claim-valid",
            "next_action": "fill Z/M/source/test/bound curve inputs only after branch selection",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CG4520_0_Hilbert_source",
            "claim": "ordinary Hilbert source current is silent",
            "passed": False,
            "blocker": "conditional proof lacks full parent signature and rank certificate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4520_1_Poynting",
            "claim": "Poynting is harmless",
            "passed": False,
            "blocker": "true only for Hilbert-owned stationary no-flux branch; radiative/constitutive branch retained",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4520_2_rank_zero",
            "claim": "rank-zero RHS vanishes",
            "passed": False,
            "blocker": "J_retained, B_A, CDB, R_A and rank/M lock remain live",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4520_3_local_GR",
            "claim": "local GR/Newton/PPN pass",
            "passed": False,
            "blocker": "rank-zero closure and finite-range alpha branch are nonclaim",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "J_A^Hilbert=0 and J_A^EM/Poynting=0 under q-basic Hilbert ownership and stationary no-flux",
            "not_derived": "rank certificate,M_AB lock,J_retained,B_A,CDB,R_A,finite alpha inputs",
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
            "next_id": "NT4520_0",
            "target_file": NEXT_TARGET,
            "task": "try to silence boundary/corner, CDB derivative tails and readout/projector reentry in the rank-zero RHS; if any cannot be derived, route to finite alpha input acquisition",
        }
    ]


def validate(sources: list[dict[str, object]], theorem: list[dict[str, object]], clauses: list[dict[str, object]], rhs: list[dict[str, object]], claims: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append({"validation_id": validation_id, "status": "PASS" if ok else "FAIL", "detail": detail})

    add(
        "VAL4520_00_sources",
        all(row["exists"] and row["needle_found"] for row in sources),
        "all source paths exist and source needles are found",
    )
    add(
        "VAL4520_01_theorem",
        any(row["theorem_id"] == "RZSC4520_3_poynting" for row in theorem)
        and any(row["theorem_id"] == "RZSC4520_5_rhs_reduction" for row in theorem),
        "Poynting theorem and RHS reduction rows exist",
    )
    add(
        "VAL4520_02_clauses",
        len(clauses) == 8 and any(row["clause_id"] == "SCA4520_4_poynting_no_flux" for row in clauses),
        "eight source-current clauses including Poynting no-flux",
    )
    add(
        "VAL4520_03_rhs",
        any(row["rhs_id"] == "RHS4520_2_J_retained" and row["status"] == "LIVE" for row in rhs),
        "retained source current remains live, not hidden",
    )
    add(
        "VAL4520_04_claims_blocked",
        all(str(row["passed"]).lower() == "false" and str(row["valid_for_claim"]).lower() == "false" for row in claims),
        "all claim gates remain blocked",
    )
    csv_paths = [
        SOURCE_REGISTER,
        THEOREM,
        CLAUSE_AUDIT,
        POYNTING_GATE,
        RHS_MAP,
        ALPHA_FALLBACK,
        BRANCH_DECISION,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_detail = []
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            parse_detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # noqa: BLE001
            parse_ok = False
            parse_detail.append(f"{path.name}:{exc}")
    add("VAL4520_05_csv_parse", parse_ok, ";".join(parse_detail))
    add("VAL4520_06_next_target", NEXT_TARGET in text(NEXT_CSV), NEXT_TARGET)
    add("VAL4520_07_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")
    add("VAL4520_OVERALL", all(row["status"] == "PASS" for row in rows), "4520 rank-zero source-current silence or alpha input acquisition")
    return rows


def build_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    poynting: list[dict[str, object]],
    rhs: list[dict[str, object]],
    alpha: list[dict[str, object]],
    decision: list[dict[str, object]],
    claims: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return f"""# 4520 - Rank-Zero Source Current Silence Or Alpha Input Acquisition

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4520 takes the actual derivation route first. 4519 left the rank-zero algebraic branch as

`M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector`.

The new move is to split `J_A` rather than treating it as a foggy missing coefficient:

`J_A = J_A^Hilbert + J_A^EM/Poynting + J_A^retained`.

The conditional theorem is:

`S_src = Sbar_src[q(Phi), Psi, theta]`, `v_A in ker(Dq)`, no explicit vertical action on matter standards, and a stationary no-flux worldtube imply

`J_A^Hilbert = 0`, and Hilbert-owned EM/Poynting flow is not a separate bulk vertical current.

So the rank-zero equation is reduced to

`M_AB Z^B = J_A^retained + B_A + C_A^CDB + R_A^src/readout/projector`.

That is forward motion: the ordinary Hilbert/Poynting worry is conditionally neutralized. It is not a local-GR claim because the retained current, boundary/corner, CDB and readout gates still need their own derivations.

## Source Register

{markdown_table(sources)}

## Rank-Zero Source Current Silence Theorem

{markdown_table(theorem)}

## Source Current Clause Audit

{markdown_table(clauses)}

## Poynting Hilbert Flow Gate

{markdown_table(poynting)}

## Rank-Zero RHS Closure Map

{markdown_table(rhs)}

## Alpha Input Fallback Acquisition

{markdown_table(alpha)}

## Branch Decision

{markdown_table(decision)}

## Claim Gates

{markdown_table(claims)}

## Status

{markdown_table(status)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""


def append_claim_once() -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_rank_zero_source_current",
        "claim": "4520 conditionally derives rank-zero source-current silence for q-basic Hilbert matter and Hilbert-owned no-flux EM/Poynting, reducing the rank-zero RHS but not closing local GR.",
        "current_evidence": "Generated theorem rows RZSC4520_1-5; RHS map RHS4520_0-6; validation P8_Y5_BRR545_4520_VALIDATION.csv",
        "status": "conditional_internal_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Retained non-Hilbert current, boundary/corner charge, CDB tails, readout/projector reentry and rank/M lock remain unsigned.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Could still fall to finite alpha input acquisition if any live RHS component cannot be silenced.",
    }
    if not CLAIMS_PATH.exists():
        write_csv(CLAIMS_PATH, [row])
        return
    existing = read_csv(CLAIMS_PATH)
    if any(existing_row.get("claim_id") == CLAIM_ID for existing_row in existing):
        return
    headers = existing[0].keys() if existing else row.keys()
    with CLAIMS_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(headers))
        writer.writerow({header: row.get(header, "") for header in headers})


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    clauses = clause_rows()
    poynting = poynting_rows()
    rhs = rhs_rows()
    alpha = alpha_fallback_rows()
    decision = decision_rows()
    claims = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM, theorem)
    write_csv(CLAUSE_AUDIT, clauses)
    write_csv(POYNTING_GATE, poynting)
    write_csv(RHS_MAP, rhs)
    write_csv(ALPHA_FALLBACK, alpha)
    write_csv(BRANCH_DECISION, decision)
    write_csv(CLAIM_GATES, claims)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, clauses, rhs, claims)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, clauses, poynting, rhs, alpha, decision, claims, status, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4520 Rank-Zero Source Current Silence Or Alpha Input Acquisition

Marker: `{MARKER}`  
4520 conditionally derives the source-current silence subtheorem for q-basic Hilbert matter and Hilbert-owned no-flux EM/Poynting flow. The rank-zero RHS is reduced from `J_A+B_A+C_A^CDB+R_A` to `J_A^retained+B_A+C_A^CDB+R_A`. This is real progress but not full local-GR closure.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4520 Packet Integration

Marker: `{PACKET_MARKER}`  
The local packet now treats Poynting flow cleanly: Hilbert-owned no-flux Poynting is silent; non-Hilbert/radiative/constitutive Poynting is retained as a finite source current. Next target: `{NEXT_TARGET}`.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
