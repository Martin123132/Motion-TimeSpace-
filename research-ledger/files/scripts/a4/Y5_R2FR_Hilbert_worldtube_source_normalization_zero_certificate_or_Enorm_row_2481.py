from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_HILBERT_WORLDTUBE_SOURCE_NORMALIZATION_2481"
CHECKPOINT_ID = "2481"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_NORM_2481_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_SOURCE_NORM_2481_THEOREM_ATTEMPT.csv",
    "normalization_chain": OUT / "P8_Y5_SOURCE_NORM_2481_NORMALIZATION_CHAIN.csv",
    "worldtube_gate": OUT / "P8_Y5_SOURCE_NORM_2481_WORLDTUBE_GAUSS_GATE.csv",
    "enorm_row": OUT / "P8_Y5_SOURCE_NORM_2481_ENORM_ROW.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_NORM_2481_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_NORM_2481_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_NORM_2481_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_NORM_2481_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2481_VALIDATION.csv",
}

COPY_TARGETS = {
    "theorem_attempt": LOCAL_BOUNDS / "Hilbert_worldtube_source_normalization_2481_THEOREM_NONCLAIM.csv",
    "enorm_row": LOCAL_BOUNDS / "E_norm_source_normalization_gap_2481_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2481_KAPPA_GREF_CALIBRATION_OR_DYNAMIC_WORLDTUBE_CLOSURE.csv",
}

SOURCES = [
    {
        "source_id": "SRC2481_00_2480_doc",
        "source_path": ROOT / "2480-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-norm-vector.md",
        "needles": ["NEXT2480_0_selected", "e_source_norm_gap", "VAL2480_OVERALL"],
        "role": "handoff selecting source-normalization zero certificate",
    },
    {
        "source_id": "SRC2481_01_2466_source_bridge",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["J_M^nu = ell_J T_matter", "WT2466_2_surface_independence", "Do not define M_source by observed GM"],
        "role": "Hilbert current, worldtube charge and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2481_02_2467_conservation",
        "source_path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["DIV2467_1_full_divergence", "SCL2467_1_mass_readout_cancels", "WTG2467_1_stationary_surface"],
        "role": "conservation identity, ell_J cancellation and stationary surface theorem",
    },
    {
        "source_id": "SRC2481_03_2468_stationary",
        "source_path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": ["EXT2468_3_surface_mass", "SCP2468_0_parent_scale", "No full Newton/PPN/local-GR pass"],
        "role": "stationary compact-source theorem and claim limit",
    },
    {
        "source_id": "SRC2481_04_2404_poisson",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["kappa0=8 pi G_ref/c^4", "WF2404_1_00_equation", "REF2404_2_orbital_G_laundering"],
        "role": "conditional Poisson normalization and no orbital-G laundering",
    },
    {
        "source_id": "SRC2481_05_2480_validation",
        "source_path": OUT / "P8_Y5_BRR545_2480_VALIDATION.csv",
        "needles": ["VAL2480_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic path
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "THM2481_0_define_current",
            "statement": "Use J_M^nu=ell_J T_matter^{nu rho} tau_rho as the Hilbert source current.",
            "result": "least-circular source object because the same Hilbert stress appears in the metric field equation",
            "status": "PASS_AS_CONTRACT",
            "blocker": "ell_J and tau/current exchange still parent-owned but unsigned",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2481_1_mass_readout_cancels_ellJ",
            "statement": "Q_M[Sigma]=int J_M.dSigma and M_H[Sigma]=Q_M/ell_J=int T^{mu nu}tau_nu dSigma_mu.",
            "result": "ell_J cancels from Hilbert mass readout when ell_J is constant and nonzero",
            "status": "PASS_CONDITIONAL_DERIVATION",
            "blocker": "ell_J still affects q_loc coupling amplitude and is not parent-derived",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2481_2_stationary_surface_independence",
            "statement": "If nabla_(mu tau_nu)=0, nabla_mu T^{mu nu}=0, compact support holds, and side flux vanishes, then Q_M[Sigma] is surface-independent.",
            "result": "stationary compact-source Hilbert mass is a valid internal source charge",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "blocker": "dynamic clock exchange, jump identities and support theorem are not fully derived",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2481_3_poisson_source_match",
            "statement": "With residuals silent and kappa0=8*pi*G_ref/c^4, the weak-field 00 equation gives nabla^2 U=4*pi*G_ref*rho_H.",
            "result": "source normalization is internally consistent in the candidate branch",
            "status": "PASS_CONDITIONAL_POISSON",
            "blocker": "kappa0/G_ref is not deeper-MTS-derived and residual silence is not proved",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2481_4_no_fitted_GM",
            "statement": "Do not choose J_M, ell_J, G_ref or M_source from observed orbital GM.",
            "result": "anti-circularity guardrail passes",
            "status": "PASS_GUARDRAIL",
            "blocker": "empirical G must later be a measurement of the parent coupling, not an input used to prove Newton",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2481_5_zero_certificate_verdict",
            "statement": "e_source_norm_gap=0 requires parent coupling calibration plus stationary/dynamic worldtube closure plus Hilbert source equivalence.",
            "result": "stationary branch is conditionally strong, but the full zero certificate does not close",
            "status": "ZERO_NOT_PROMOTED_RETAIN_E_NORM",
            "blocker": "parent kappa0/G_ref origin, dynamic exchange, jump/support and source-shadow equivalence remain unsigned",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def normalization_chain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "chain_id": "CHAIN2481_0_T_H",
            "object": "T_H^{mu nu}",
            "normalization_role": "Hilbert stress from matter action",
            "formula": "T_H^{mu nu}=-(2/sqrt(-g))*delta S_matter/delta g_mu_nu",
            "status": "PASS_AS_CONTRACT",
            "gap": "matter coupling descent/source-shadow zero remains unsigned",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2481_1_JM",
            "object": "J_M^nu",
            "normalization_role": "source current for q_loc/GK sector",
            "formula": "J_M^nu=ell_J T_H^{nu rho} tau_rho",
            "status": "PASS_CONDITIONAL",
            "gap": "ell_J and tau exchange not parent-derived",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2481_2_QM",
            "object": "Q_M[Sigma]",
            "normalization_role": "worldtube source charge",
            "formula": "Q_M=int_{Sigma cap W} J_M^mu dSigma_mu",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "gap": "surface independence blocked dynamically",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2481_3_MH",
            "object": "M_H[Sigma]",
            "normalization_role": "Hilbert mass/energy source before orbital fitting",
            "formula": "M_H=Q_M/ell_J=int T_H^{mu nu}tau_nu dSigma_mu",
            "status": "PASS_CONDITIONAL_ELLJ_CANCELS",
            "gap": "requires normalized tau and fixed ell_J convention",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2481_4_kappa_G",
            "object": "kappa0/G_ref",
            "normalization_role": "metric source coupling in Poisson equation",
            "formula": "kappa0=8*pi*G_ref/c^4",
            "status": "CONDITIONAL_DEFINITION_NOT_PARENT_PROOF",
            "gap": "parent EH-leading-operator/coupling origin not signed",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2481_5_deltaG",
            "object": "delta_G_source",
            "normalization_role": "residual mismatch between parent source and Newton source",
            "formula": "delta_G_source -> E_norm until CHAIN2481_0..4 and worldtube dynamics close",
            "status": "RETAIN_AS_E_NORM",
            "gap": "full zero certificate missing",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def worldtube_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "WT2481_0_gauss_identity",
            "condition": "Q[Sigma_2]-Q[Sigma_1]=int_V nabla_mu J_M^mu dV + side_flux",
            "result": "formal Gauss gate exists",
            "status": "PASS_DERIVED",
            "residual_if_failed": "E_norm_surface",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2481_1_stationary_collar",
            "condition": "ell_J constant, tau Killing/stationary, matter shell conservation, compact support, side flux zero",
            "result": "Q_M and M_H are surface-independent in stationary branch",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "residual_if_failed": "E_norm_clock_or_side_flux",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2481_2_dynamic_exchange",
            "condition": "nabla_mu J_M^mu + I_tau + I_A = 0 from parent tau/GK/matter equations",
            "result": "not derived in current corpus",
            "status": "BLOCKED_DYNAMIC",
            "residual_if_failed": "E_norm_dynamic_exchange",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2481_3_jump_support",
            "condition": "distributional worldtube jump conditions and matter support theorem",
            "result": "needed to prevent hidden source on the boundary",
            "status": "BLOCKED_JUMP_SUPPORT",
            "residual_if_failed": "E_norm_jump_tail",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2481_4_no_orbital_shortcut",
            "condition": "M_source is never defined by observed orbital GM",
            "result": "guardrail active",
            "status": "PASS_GUARDRAIL",
            "residual_if_failed": "INVALID_CIRCULAR_PROOF",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def enorm_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "enorm_id": "ENORM2481_0_E_norm",
            "norm_symbol": "E_norm",
            "definition": "E_norm = e_kappaG + e_surface_drift + e_clock_exchange + e_jump_support + e_hilbert_shadow",
            "why_retained": "source-normalization zero certificate closes only in a stationary conditional branch, not dynamically or parent-calibrated",
            "zero_condition": "parent kappa0/G_ref calibration, ell_J/tau convention, conserved Hilbert worldtube charge, jump/support theorem, and source-shadow zero",
            "status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "enorm_id": "ENORM2481_1_stationary_zero_subbranch",
            "norm_symbol": "E_norm_stationary",
            "definition": "E_norm_stationary=0 if kappa0/G_ref is parent-declared and stationary compact-source hypotheses hold",
            "why_retained": "useful local theorem target, but not full MTS dynamic/Newton proof",
            "zero_condition": "must also keep DeltaE_MTS, DeltaE_boundary and J_shadow silent",
            "status": "CONDITIONAL_CONTROL_BRANCH_ONLY",
            "valid_for_claim": False,
        },
        {
            "enorm_id": "ENORM2481_2_source_gap_vector",
            "norm_symbol": "source_norm_gap_vector",
            "definition": "(e_kappaG,e_surface_drift,e_clock_exchange,e_jump_support,e_hilbert_shadow)",
            "why_retained": "keeps source errors separated instead of hiding all under one scalar",
            "zero_condition": "each component must be zeroed or bounded before local tests",
            "status": "VECTOR_FOR_NEXT_RUNNER",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2481_0_hilbert_mass_chain",
            "claim": "Hilbert mass readout chain is written.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "M_H=Q_M/ell_J=int T tau dSigma is explicit under fixed ell_J.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2481_1_stationary_worldtube",
            "claim": "Stationary compact-source worldtube surface independence closes conditionally.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "Gauss theorem plus stationary Hilbert-current conservation gives a control branch.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2481_2_e_norm_zero",
            "claim": "e_source_norm_gap is zero in the full theory.",
            "gate_status": "BLOCKED",
            "reason": "parent kappa/G calibration, dynamic exchange, jump/support and source-shadow zero are unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2481_3_kappaG",
            "claim": "kappa0/G_ref is parent-derived rather than candidate-declared.",
            "gate_status": "BLOCKED",
            "reason": "2404 gives the conditional Poisson normalization but not the deeper MTS coupling origin.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2481_4_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "source normalization has a stationary control branch but not a full zero theorem; residual sectors also remain.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2481_5_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, or plateau axiom is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "orbital-GM laundering remains explicitly forbidden.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2481_0_gain",
            "decision": "Accept stationary Hilbert/worldtube source normalization as a control branch.",
            "reason": "It gives an honest non-fitted source mass under explicit stationary hypotheses.",
            "effect": "Useful for local theorem scaffolding, not a full Newton claim.",
        },
        {
            "decision_id": "DEC2481_1_retain_Enorm",
            "decision": "Retain E_norm in E_local_res.",
            "reason": "The full dynamic/parent-calibrated zero certificate is not proved.",
            "effect": "Future C_res_ext must include source-normalization components unless zeroed.",
        },
        {
            "decision_id": "DEC2481_2_next",
            "decision": "Attack kappa0/G_ref parent calibration or dynamic worldtube closure next.",
            "reason": "Those are the remaining pieces preventing e_source_norm_gap=0.",
            "effect": "2482 selected.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2481_0_selected",
            "selection_status": "selected",
            "target_file": "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
            "target_script": "scripts/Y5_R2FR_kappaG_parent_calibration_or_dynamic_worldtube_closure_2482.py",
            "task": "try to close e_kappaG or dynamic worldtube source drift: derive parent kappa0/G_ref from the action normalization, or derive the exchange/jump/support identity needed for dynamic surface independence",
            "acceptance_target": "kappa/G calibration theorem attempt, dynamic exchange-current identity, jump/support ledger, E_norm component retained if unsigned",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "theorem_attempt": OUTPUTS["theorem_attempt"],
        "enorm_row": OUTPUTS["enorm_row"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2481_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2481_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2481_01_hilbert_chain_written",
        any(row["theorem_id"] == "THM2481_1_mass_readout_cancels_ellJ" for row in data["theorems"]),
        "ell_J cancellation in mass readout is recorded",
    )
    add(
        "VAL2481_02_stationary_gate",
        any(row["gate_id"] == "WT2481_1_stationary_collar" and row["status"] == "PASS_STATIONARY_CONDITIONAL" for row in data["worldtube"]),
        "stationary worldtube surface gate is conditional pass",
    )
    add(
        "VAL2481_03_Enorm_retained",
        any(row["norm_symbol"] == "E_norm" and row["status"] == "RETAIN_NONCLAIM" for row in data["enorm"]),
        "E_norm is retained as nonclaim",
    )
    add("VAL2481_04_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add(
        "VAL2481_05_next_target_written",
        any(row["route_id"] == "NEXT2481_0_selected" for row in data["next"]),
        "2482 kappa/G or dynamic worldtube target selected",
    )
    add("VAL2481_06_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2481*", "*P8_Y5_SOURCE_NORM_2481*", "*JR2481*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2481_07_no_formalization_artifacts", not formalization_artifacts, "no 2481 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2481_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2481_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2481_OVERALL",
        overall,
        "2481 closes a stationary Hilbert/worldtube source-normalization control branch, retains E_norm for full theory, and selects kappa/G or dynamic worldtube closure next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2481 Y5 R2FR Hilbert-worldtube Source-normalization Zero Certificate Or Enorm Row",
        "",
        "**Status:** stationary source-normalization control branch sharpened, but full `e_source_norm_gap=0` is not promoted. The Hilbert mass readout is internally clean under fixed `ell_J`, stationary `tau`, compact support and no side flux; dynamic exchange, jump/support and parent `kappa0/G_ref` calibration remain unsigned.",
        "",
        "**Main result:** `M_H=Q_M/ell_J=int T^{mu nu}tau_nu dSigma_mu` removes `ell_J` from the mass readout in the stationary branch, so fitted orbital `GM` is not needed there. But `E_norm` remains in `E_local_res` because the full parent-coupled, dynamic, source-shadow-free zero certificate has not closed.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Theorem Attempt",
        markdown_table(data["theorems"], ["theorem_id", "statement", "result", "status", "blocker", "valid_for_claim"]),
        "",
        "## Normalization Chain",
        markdown_table(data["chain"], ["chain_id", "object", "normalization_role", "formula", "status", "gap", "valid_for_claim"]),
        "",
        "## Worldtube Gauss Gate",
        markdown_table(data["worldtube"], ["gate_id", "condition", "result", "status", "residual_if_failed", "valid_for_claim"]),
        "",
        "## E_norm Row",
        markdown_table(data["enorm"], ["enorm_id", "norm_symbol", "definition", "why_retained", "zero_condition", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "theorems": theorem_attempt_rows(),
        "chain": normalization_chain_rows(),
        "worldtube": worldtube_gate_rows(),
        "enorm": enorm_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorems"])
    write_csv(OUTPUTS["normalization_chain"], data["chain"])
    write_csv(OUTPUTS["worldtube_gate"], data["worldtube"])
    write_csv(OUTPUTS["enorm_row"], data["enorm"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
