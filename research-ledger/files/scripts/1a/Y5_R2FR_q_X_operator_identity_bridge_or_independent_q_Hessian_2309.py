from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_Q_X_OPERATOR_BRIDGE_OR_Q_HESSIAN_2309"
DOC = ROOT / "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md"

PATHS = {
    "2308_doc": ROOT / "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
    "2308_validation": OUT / "P8_Y5_BRR545_2308_VALIDATION.csv",
    "2308_operator": OUT / "P8_Y5_PARENT_QLOC_2308_Q_OPERATOR_X_BRIDGE_AUDIT.csv",
    "2308_normal": OUT / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
    "2301_rep": OUT / "P8_Y5_PARENT_QLOC_2301_Q_REPRESENTATION_TYPE_GATE.csv",
    "2301_firstclass": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "2302_doc": ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
    "2303_doc": ROOT / "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1157_doc": ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
    "637_qmap": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "669_lx_candidates": OUT / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
    "669_residual": OUT / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
    "669_gates": OUT / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
    "1025_doc": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "1026_doc": ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "1027_doc": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
}

SOURCES = [
    ("SRC2309_00_2308_doc", "2308_doc", PATHS["2308_doc"], ["DEC2308_3_next", "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md"], "direct 2308 handoff"),
    ("SRC2309_01_2308_validation", "2308_validation", PATHS["2308_validation"], ["VAL2308_OVERALL", "PASS"], "2308 validation"),
    ("SRC2309_02_2308_operator", "2308_operator", PATHS["2308_operator"], ["QOP2308_0_bridge_target", "BRIDGE_NOT_SIGNED"], "q-X bridge audit handoff"),
    ("SRC2309_03_2308_normal", "2308_normal", PATHS["2308_normal"], ["NF2308_0_minimal_action", "CONTRACT_WRITTEN_NOT_DERIVED"], "minimal q normal form"),
    ("SRC2309_04_2301_rep", "2301_rep", PATHS["2301_rep"], ["QREP2301_5_verdict", "FAIL_CURRENT_CLAIM"], "q representation gate blocks promotion"),
    ("SRC2309_05_2301_firstclass", "2301_firstclass", PATHS["2301_firstclass"], ["QFC2301_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "q first-class removal not proven"),
    ("SRC2309_06_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_3_operator_norm", "MISSING_OPERATOR_NORM_BOUND"], "q operator norm missing"),
    ("SRC2309_07_2302_doc", "2302_doc", PATHS["2302_doc"], ["EVID2302_2_firstclass_package", "CLEANEST_ROUTE_BUT_UNSIGNED"], "q firstclass package conditional"),
    ("SRC2309_08_2303_doc", "2303_doc", PATHS["2303_doc"], ["QFCH2303_6_verdict", "FAIL_CURRENT_CLAIM_SOURCE_HUNT_NEGATIVE"], "q field content source hunt negative"),
    ("SRC2309_09_1023_doc", "1023_doc", PATHS["1023_doc"], ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "single q/vX/action descent certificate fails"),
    ("SRC2309_10_1157_doc", "1157_doc", PATHS["1157_doc"], ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "parent q-map/null-generator proof not derived"),
    ("SRC2309_11_637_qmap", "637_qmap", PATHS["637_qmap"], ["QM637_2_vertical_kernel", "Dq[v_X]=0"], "conditional vertical kernel"),
    ("SRC2309_12_669_lx_candidates", "669_lx_candidates", PATHS["669_lx_candidates"], ["LX669_2_positive_sourcefree_massive", "conditional_sourcefree_operator_route"], "X/L_X operator candidate"),
    ("SRC2309_13_669_residual", "669_residual", PATHS["669_residual"], ["RV669_0_Z_X", "MISSING_PARENT_INPUT"], "X operator values missing"),
    ("SRC2309_14_669_gates", "669_gates", PATHS["669_gates"], ["G669_1_positive_kinetic", "blocked_as_expected"], "X operator gates blocked"),
    ("SRC2309_15_1025_doc", "1025_doc", PATHS["1025_doc"], ["SV1025_6_verdict", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED"], "X Hessian contract sharpened not owned"),
    ("SRC2309_16_1026_doc", "1026_doc", PATHS["1026_doc"], ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"], "X parent metric/eigenvalue route failed"),
    ("SRC2309_17_1027_doc", "1027_doc", PATHS["1027_doc"], ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"], "X/source-zero route remains conditional"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2309_SOURCE_REGISTER.csv",
    "trichotomy": OUT / "P8_Y5_PARENT_QLOC_2309_QX_TRICHOTOMY_THEOREM.csv",
    "bridge": OUT / "P8_Y5_PARENT_QLOC_2309_QX_BRIDGE_SIGNATURE_ATTEMPT.csv",
    "pullback": OUT / "P8_Y5_PARENT_QLOC_2309_OPERATOR_PULLBACK_LAWS.csv",
    "independent": OUT / "P8_Y5_PARENT_QLOC_2309_INDEPENDENT_Q_HESSIAN_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2309_DECISION_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2309_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2309_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2309_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2309_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2309_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2309_0_trichotomy", OUTPUTS["trichotomy"], QUEUE / "JR2309_QX_TRICHOTOMY_THEOREM_NONCLAIM.csv"),
    ("COPY2309_1_bridge", OUTPUTS["bridge"], QUEUE / "JR2309_QX_BRIDGE_SIGNATURE_ATTEMPT_NONCLAIM.csv"),
    ("COPY2309_2_independent", OUTPUTS["independent"], MICROSCOPE / "q_independent_hessian_row_nonclaim_2309.csv"),
    ("COPY2309_3_pullback", OUTPUTS["pullback"], BETA_DOCS / "QX_OPERATOR_PULLBACK_LAWS_2309_NONCLAIM.csv"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def b(value: bool) -> str:
    return "true" if value else "false"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(clean(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    )


def make_sources() -> list[dict[str, Any]]:
    rows = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def make_trichotomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TRI2309_0_quotient_vertical_case",
            "case": "q is quotient/readout; X is vertical/null",
            "condition": "q=q(Phi) is a parent quotient map and Dq[v_X]=0 for the actual local X direction",
            "operator_consequence": "there is no q Green operator along X; the correct route is q/X removal, not borrowing L_X for q",
            "status": "EXACT_IF_PARENT_SIGNED_NOT_CURRENT",
            "missing_piece": "q object, actual v_X identification, action factorization, first-class/boundary/source silence",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TRI2309_1_physical_identity_case",
            "case": "q is a physical scalar proportional to X",
            "condition": "q=a X + O(X^2) with parent-owned scale a, same branch, same boundary domain, and same source/readout convention",
            "operator_consequence": "L_q is the pullback of L_X; Z_q=Z_X/a^2, M_q^2=M_X^2/a^2, D_qWeyl2=D_XWeyl2/a at linear order",
            "status": "BRIDGE_FORMULA_EXACT_IF_SIGNED",
            "missing_piece": "scale a, q-X identity, parent Hessian ownership, D_XWeyl2 source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TRI2309_2_independent_q_case",
            "case": "q is an independent physical scalar/local residual",
            "condition": "q is not removed by quotient and not parent-identified with X",
            "operator_consequence": "q needs its own Hessian block Z_q,M_q^2,D_qWeyl2,J_q and cannot inherit X values",
            "status": "RETAIN_INDEPENDENT_Q_HESSIAN_ROW",
            "missing_piece": "parent second variation in q direction and source/readout maps",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TRI2309_3_auxiliary_case",
            "case": "q is algebraic/auxiliary or a Schur-complement variable",
            "condition": "q has no independent gradient kinetic term but appears in a Hessian/source block",
            "operator_consequence": "integrating out q generates local/nonlocal higher-curvature operators; use Schur complement, not a naive propagator",
            "status": "LIVE_COUNTERMODEL_OR_BOUND_ROUTE",
            "missing_piece": "algebraic Hessian, source vector, no-tower theorem, and boundary/readout ownership",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TRI2309_4_verdict",
            "case": "q-X operator bridge decision",
            "condition": "choose one of TRI2309_0 through TRI2309_3 from current corpus",
            "operator_consequence": "current corpus does not choose a claim-grade branch; no q operator value can be promoted",
            "status": "BRANCH_SELECTION_NOT_PARENT_SIGNED",
            "missing_piece": "q-X identity/removal or independent q Hessian",
            "valid_for_claim": "false",
        },
    ]


def make_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2309_0_identity_map",
            "gate": "q=aX identity or projection",
            "required_evidence": "parent map q(Phi), local coordinate X(Phi), and derivative Dq[e_X]=a with nonzero owned a",
            "current_evidence": "637/1023/1157 mostly support Dq[v_X]=0 conditional for vertical directions, not q=aX",
            "status": "NOT_SIGNED",
            "blocks": "cannot pull back L_X to L_q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2309_1_same_branch",
            "gate": "same local branch/domain/boundary",
            "required_evidence": "q and X live on the same compact local branch with identical boundary terms and source/readout convention",
            "current_evidence": "1023/1157 keep boundary/action descent and local domain conditions unsigned",
            "status": "NOT_SIGNED",
            "blocks": "operator/domain copying would be unsafe",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2309_2_X_operator_owned",
            "gate": "X operator values are parent-owned",
            "required_evidence": "Z_X, M_X^2, lambda_X, K_X, source charges sourced in one parent normalization",
            "current_evidence": "669, 1025, and 1026 keep Z_X/M_X^2/beta/K_X missing or conditional",
            "status": "NOT_SIGNED",
            "blocks": "even a signed q=aX bridge would not yet give numbers",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2309_3_source_coupling_bridge",
            "gate": "q source/readout equals X source/readout under bridge",
            "required_evidence": "J_q, qbar, Qbar, boundary tails transform consistently under q=aX",
            "current_evidence": "1027 source-zero and bounded qbar rows remain conditional/missing",
            "status": "NOT_SIGNED",
            "blocks": "observable projection and no-cancellation envelope cannot be scored",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BR2309_4_verdict",
            "gate": "activate q-X bridge",
            "required_evidence": "BR2309_0 through BR2309_3 pass",
            "current_evidence": "all bridge gates are unsigned",
            "status": "QX_BRIDGE_NOT_ACTIVATED",
            "blocks": "must use independent q Hessian row or quotient/no-pole route",
            "valid_for_claim": "false",
        },
    ]


def make_pullback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB2309_0_linear_scale",
            "assumption": "q=aX near the local branch",
            "law": "X=q/a; delta X=delta q/a",
            "result": "all pullbacks require nonzero parent-owned scale a with units",
            "status": "EXACT_FORMULA_IF_BRIDGE_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB2309_1_kinetic_mass",
            "assumption": "S_X has 1/2 Z_X |grad X|^2 + 1/2 M_X^2 X^2",
            "law": "S_q has 1/2 (Z_X/a^2)|grad q|^2 + 1/2 (M_X^2/a^2)q^2",
            "result": "Z_q=Z_X/a^2 and M_q^2=M_X^2/a^2; lambda_q=lambda_X if the same operator branch is used",
            "status": "EXACT_FORMULA_IF_BRIDGE_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB2309_2_weyl_coefficient",
            "assumption": "S contains D_XWeyl2 X C^2 and q=aX",
            "law": "D_XWeyl2 X C^2 = (D_XWeyl2/a) q C^2",
            "result": "D_qWeyl2=D_XWeyl2/a; if the source is defined in the q equation rather than action, sign/convention must be rechecked",
            "status": "EXACT_FORMULA_WITH_CONVENTION_GUARD",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB2309_3_source_charge",
            "assumption": "source term is X J_X or q J_q",
            "law": "X J_X=(q/a)J_X, so J_q=J_X/a in the same action convention",
            "result": "qbar/Qbar/K products must transform with the same a; no-cancellation guard remains",
            "status": "EXACT_FORMULA_WITH_SOURCE_GUARD",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PB2309_4_claim_status",
            "assumption": "use pullback laws in current branch",
            "law": "requires signed q=aX, signed X operator/coefficient, and signed source convention",
            "result": "not executable in current corpus",
            "status": "PULLBACK_LAWS_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def make_independent_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQH2309_0_Zq",
            "input": "Z_q",
            "meaning": "q kinetic Hessian/sign/units in the local branch",
            "status": "MISSING_PARENT_INPUT",
            "needed_source": "delta_q^2 S_parent gradient block or no-pole theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQH2309_1_Mq2",
            "input": "M_q^2",
            "meaning": "q mass/Hessian gap and lambda_q=sqrt(Z_q/M_q^2)",
            "status": "MISSING_PARENT_INPUT",
            "needed_source": "parent Hessian curvature in q direction or massless/no-pole branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQH2309_2_DqWeyl2",
            "input": "D_qWeyl2",
            "meaning": "q Weyl-squared source coefficient in the same action convention",
            "status": "MISSING_PARENT_COEFFICIENT",
            "needed_source": "parent action coefficient or higher-curvature zero theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQH2309_3_Jq",
            "input": "J_q and boundary/source tail",
            "meaning": "non-Weyl q source, matter/readout and boundary tail",
            "status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "needed_source": "matter/coframe descent or bounded source rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IQH2309_4_claim_gate",
            "input": "independent q Hessian branch",
            "meaning": "claim-grade branch only if all rows above become source-backed or theorem-zero",
            "status": "CLAIM_BLOCKED",
            "needed_source": "IQH2309_0 through IQH2309_3",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2309_0",
            "decision": "QX_TRICHOTOMY_WRITTEN",
            "reason": "q quotient, q=aX, independent q, and auxiliary q lead to different operator logic",
            "next_action": "do not mix these branches in future runners",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2309_1",
            "decision": "QX_BRIDGE_NOT_ACTIVATED",
            "reason": "current corpus supports conditional vertical-kernel fragments, not a q=aX identity or source/operator pullback",
            "next_action": "retain independent q Hessian row unless a new q-X identity source appears",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2309_2",
            "decision": "PULLBACK_LAWS_READY_BUT_NONCLAIM",
            "reason": "if q=aX is later signed, Z/M/D/J transformations are now explicit",
            "next_action": "use pullback table only after bridge gates pass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2309_3_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "the cleanest next move is selecting q branch/removal versus independent q Hessian, not another blind coefficient hunt",
            "next_action": "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md",
            "valid_for_claim": "false",
        },
    ]


def make_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2309_0_sources", "gate": "all source paths and needles valid", "passed": "true", "claim_effect": "ledger is checkable", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2309_1_trichotomy", "gate": "q-X branch trichotomy written", "passed": "true", "claim_effect": "prevents category error in future runners", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2309_2_bridge", "gate": "q=aX bridge signed", "passed": "false", "claim_effect": "cannot copy L_X to L_q", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2309_3_X_values", "gate": "X operator values source-backed", "passed": "false", "claim_effect": "even bridge route has no numeric operator", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2309_4_independent_q", "gate": "independent q Hessian sourced", "passed": "false", "claim_effect": "independent q route remains blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2309_5_local_claim", "gate": "local GR/Newton/Weyl2 branch claim allowed", "passed": "false", "claim_effect": "all public claims remain blocked", "valid_for_claim": "false"},
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2309_0_copy_operator", "claim": "copy L_X to L_q", "allowed": "false", "reason": "q=aX bridge is not signed and X values are missing", "blocking_rows": "BR2309_4_verdict;BR2309_2_X_operator_owned", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2309_1_treat_vertical_as_physical", "claim": "use q Green operator while also claiming X is vertical quotient", "allowed": "false", "reason": "if X is vertical to q, the q/X branch is no-pole/removal, not a physical q propagator", "blocking_rows": "TRI2309_0_quotient_vertical_case", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2309_2_score_runner", "claim": "score D_qWeyl2 projection runner", "allowed": "false", "reason": "branch selection, q operator, D_qWeyl2, and source/readout maps are missing", "blocking_rows": "TRI2309_4_verdict;IQH2309_4_claim_gate", "valid_for_claim": "false"},
    ]


def make_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2309_0",
            "next_target": "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md",
            "why": "2309 blocks q-X copying; next must select no-pole/quotient removal or build independent q Hessian source rows",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    trichotomy_rows: list[dict[str, Any]],
    bridge_rows: list[dict[str, Any]],
    pullback_rows: list[dict[str, Any]],
    independent_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, trichotomy_rows, bridge_rows, pullback_rows, independent_rows, decision_rows, claim_rows, refusal_rows, copy_rows]
    formalization_output_markers = (
        "2309-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2309",
        "P8_Y5_BRR545_2309",
        "JR2309_",
        "QX_OPERATOR_PULLBACK_LAWS_2309",
        "q_independent_hessian_row_nonclaim_2309",
        "Y5_R2FR_q_X_operator_identity_bridge_or_independent_q_Hessian_2309",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2309_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2309_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2309_02_trichotomy", any(row["row_id"] == "TRI2309_4_verdict" and row["status"] == "BRANCH_SELECTION_NOT_PARENT_SIGNED" for row in trichotomy_rows), "q-X trichotomy verdict is recorded"))
    checks.append(("VAL2309_03_bridge_blocked", any(row["row_id"] == "BR2309_4_verdict" and row["status"] == "QX_BRIDGE_NOT_ACTIVATED" for row in bridge_rows), "q-X bridge remains blocked"))
    checks.append(("VAL2309_04_pullback_laws", {"PB2309_1_kinetic_mass", "PB2309_2_weyl_coefficient", "PB2309_3_source_charge"}.issubset({row["row_id"] for row in pullback_rows}), "operator/coefficient/source pullback laws are written"))
    checks.append(("VAL2309_05_independent_q_rows", {"IQH2309_0_Zq", "IQH2309_1_Mq2", "IQH2309_2_DqWeyl2", "IQH2309_3_Jq"}.issubset({row["row_id"] for row in independent_rows}), "independent q Hessian row is complete"))
    checks.append(("VAL2309_06_claim_gates", any(row["row_id"] == "CG2309_5_local_claim" and row["passed"] == "false" for row in claim_rows), "local claim gate false"))
    checks.append(("VAL2309_07_refusal_runner", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks claims"))
    checks.append(("VAL2309_08_next_target", any(row["row_id"] == "DEC2309_3_next" and "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2309_09_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2309_10_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2309_11_formalization_untouched_by_2309", len(formalization_hits) == 0, "no 2309 checkpoint output appears in formalization-workbench"))
    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2309_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2309 writes the q-X trichotomy, blocks copying X/L_X into q without a signed bridge, records exact pullback laws if q=aX is later signed, and stages the independent q Hessian row.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    trichotomy_rows: list[dict[str, Any]],
    bridge_rows: list[dict[str, Any]],
    pullback_rows: list[dict[str, Any]],
    independent_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2309 — q-X Operator Identity Bridge Or Independent q Hessian",
        "",
        "## Summary",
        "",
        "2309 resolves the category mistake risk. If `q` is the quotient/readout and `X` is vertical, then `X` is killed by `q`; it is not the same as a propagating `q` scalar. If `q=aX`, the `X` operator can only be pulled across with a signed scale `a` and a shared parent action branch. If neither is true, `q` needs its own Hessian.",
        "",
        "Current evidence does not sign the bridge. The old `X/L_X` work is useful scaffolding, but it cannot be copied into `q`; even the X-side numbers are still missing. The useful output is a trichotomy, exact pullback laws for a future signed bridge, and an independent `q` Hessian row.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## q-X Trichotomy Theorem",
        "",
        md_table(trichotomy_rows, ["row_id", "case", "condition", "operator_consequence", "status", "missing_piece", "valid_for_claim"]),
        "",
        "## q-X Bridge Signature Attempt",
        "",
        md_table(bridge_rows, ["row_id", "gate", "required_evidence", "current_evidence", "status", "blocks", "valid_for_claim"]),
        "",
        "## Operator Pullback Laws",
        "",
        md_table(pullback_rows, ["row_id", "assumption", "law", "result", "status", "valid_for_claim"]),
        "",
        "## Independent q Hessian Row",
        "",
        md_table(independent_rows, ["row_id", "input", "meaning", "status", "needed_source", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = make_sources()
    trichotomy_rows = make_trichotomy_rows()
    bridge_rows = make_bridge_rows()
    pullback_rows = make_pullback_rows()
    independent_rows = make_independent_rows()
    decision_rows = make_decision_rows()
    claim_rows = make_claim_gate_rows()
    refusal_rows = make_refusal_rows()
    next_rows = make_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["trichotomy"], trichotomy_rows)
    write_csv(OUTPUTS["bridge"], bridge_rows)
    write_csv(OUTPUTS["pullback"], pullback_rows)
    write_csv(OUTPUTS["independent"], independent_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claim_gates"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        trichotomy_rows,
        bridge_rows,
        pullback_rows,
        independent_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        trichotomy_rows,
        bridge_rows,
        pullback_rows,
        independent_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2309_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
