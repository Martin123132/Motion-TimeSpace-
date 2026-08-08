from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_HILBERT_WORLDTUBE_SOURCE_NORMALIZATION_2568"
CHECKPOINT_ID = "2568"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_NORM_2568_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv",
    "normalization_chain": OUT / "P8_Y5_SOURCE_NORM_2568_NORMALIZATION_CHAIN.csv",
    "worldtube_gate": OUT / "P8_Y5_SOURCE_NORM_2568_WORLDTUBE_GAUSS_GATE.csv",
    "enorm_components": OUT / "P8_Y5_SOURCE_NORM_2568_ENORM_COMPONENTS.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_NORM_2568_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_NORM_2568_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_NORM_2568_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_NORM_2568_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2568_VALIDATION.csv",
}

COPY_TARGETS = {
    "theorem_attempt": LOCAL_BOUNDS / "Hilbert_worldtube_source_normalization_2568_THEOREM_NONCLAIM.csv",
    "enorm_components": LOCAL_BOUNDS / "E_norm_source_normalization_gap_2568_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2568_PARENT_EH_COUPLING_OR_DYNAMIC_EXCHANGE_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2568_00_2567_doc",
        "source_path": ROOT / "2567-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-local-norm.md",
        "needles": ["NEXT2567_0_selected", "ZERO2567_e_norm", "VAL2567_OVERALL"],
        "role": "active handoff selecting source-normalization closure for E_norm",
    },
    {
        "source_id": "SRC2568_01_2556_source_bridge",
        "source_path": ROOT / "2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["CUR2556_A_Hilbert_energy_current", "WT2556_2_surface_independence", "Do not define M_source"],
        "role": "modern Hilbert current, worldtube source and no fitted-GM guardrail",
    },
    {
        "source_id": "SRC2568_02_2557_conservation",
        "source_path": ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["DIV2557_1_full_product_rule", "SCL2557_5_current_status", "WTG2557_1_stationary_surface"],
        "role": "exact divergence identity, parent-scale blocker and stationary surface gate",
    },
    {
        "source_id": "SRC2568_03_2468_stationary_theorem",
        "source_path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": ["EXT2468_3_surface_mass", "SCP2468_0_parent_scale", "VAL2468_OVERALL"],
        "role": "stationary q_loc/source theorem precedent and remaining stress/scale limits",
    },
    {
        "source_id": "SRC2568_04_2481_source_norm",
        "source_path": ROOT / "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["THM2481_1_mass_readout_cancels_ellJ", "GATE2481_2_e_norm_zero", "VAL2481_OVERALL"],
        "role": "earlier Hilbert/worldtube source-normalization branch",
    },
    {
        "source_id": "SRC2568_05_2482_kappag_dynamic",
        "source_path": ROOT / "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
        "needles": ["KAP2482_1_parent_origin", "DYN2482_1_exchange_identity", "VAL2482_OVERALL"],
        "role": "kappa/G parent calibration and dynamic worldtube closure blockers",
    },
    {
        "source_id": "SRC2568_06_2404_poisson",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["kappa0=8 pi G_ref/c^4", "WF2404_1_00_equation", "REF2404_2_orbital_G_laundering"],
        "role": "conditional Poisson normalization and anti-circularity rule",
    },
    {
        "source_id": "SRC2568_07_2567_validation",
        "source_path": OUT / "P8_Y5_BRR545_2567_VALIDATION.csv",
        "needles": ["VAL2567_OVERALL", "PASS"],
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
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
            "theorem_id": "THM2568_0_hilbert_current_contract",
            "statement": "Use J_M^nu=ell_J T_H^{nu rho} tau_rho as the source current for q_loc/GK sector.",
            "result": "This is the least-circular source object because the same Hilbert stress appears in the metric field equation.",
            "status": "PASS_AS_CONTRACT",
            "blocker": "ell_J, tau ownership and any A-sector source supplement are not yet parent-signed.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_1_mass_readout_cancels_ellJ",
            "statement": "Q_M[Sigma]=int_{Sigma cap W} J_M^mu dSigma_mu and M_H[Sigma]=Q_M/ell_J=int T_H^{mu nu}tau_nu dSigma_mu.",
            "result": "ell_J cancels out of the Hilbert mass readout if ell_J is fixed, nonzero and not chosen from orbital data.",
            "status": "PASS_CONDITIONAL_DERIVATION",
            "blocker": "ell_J still affects q_loc/current amplitude and must come from the parent action or universal convention.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_2_exact_divergence_identity",
            "statement": "nabla_mu J_M^mu=(nabla_mu ell_J)T^{mu nu}tau_nu + ell_J(nabla_mu T^{mu nu})tau_nu + ell_J T^{mu nu}nabla_mu tau_nu.",
            "result": "The source leak is exactly localized in parent-scale gradients, matter-shell failure and clock strain.",
            "status": "PASS_DERIVED",
            "blocker": "generic dynamic MTS time needs a parent exchange current to cancel the clock/scale leak.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_3_stationary_surface_independence",
            "statement": "If ell_J is fixed, nabla_mu T^{mu nu}=0, tau is Killing/stationary, support is compact and side flux vanishes, then Q_M is surface-independent.",
            "result": "The stationary compact-source Hilbert branch gives an honest non-fitted source-mass control theorem.",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "blocker": "jump/support terms and dynamic exchange remain unsigned outside the stationary collar.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_4_poisson_source_match",
            "statement": "With residuals silent and kappa0=8*pi*G_ref/c^4, the weak-field 00 equation gives nabla^2 U=4*pi*G_ref rho_H.",
            "result": "The source-normalized Newton lane is internally consistent as a candidate branch.",
            "status": "PASS_CONDITIONAL_POISSON",
            "blocker": "kappa0/G_ref is not derived from the MTS parent action and residual silence is not proved.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_5_no_fitted_GM",
            "statement": "Do not choose J_M, ell_J, G_ref, kappa0 or M_source from observed orbital GM.",
            "result": "Anti-circularity guardrail passes and prevents Newton from being proved by smuggling Newton in.",
            "status": "PASS_GUARDRAIL",
            "blocker": "empirical G can be a later measurement of the parent coupling, not the proof source.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "THM2568_6_zero_certificate_verdict",
            "statement": "e_source_norm_gap=0 requires parent coupling calibration, fixed parent source scale, dynamic/stationary worldtube closure and source-shadow silence.",
            "result": "The stationary branch is strong, but full source-normalization zero is not promoted.",
            "status": "ZERO_NOT_PROMOTED_RETAIN_E_NORM",
            "blocker": "e_kappaG, dynamic exchange, jump/support, ell_J ownership and source-shadow equivalence remain unsigned.",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def normalization_chain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "chain_id": "CHAIN2568_0_TH",
            "object": "T_H^{mu nu}",
            "normalization_role": "Hilbert stress from the matter action",
            "formula": "T_H^{mu nu}=-(2/sqrt(-g))*delta S_matter/delta g_mu_nu",
            "status": "PASS_AS_CONTRACT",
            "gap": "universal matter coupling/source-shadow zero remains unsigned",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2568_1_JM",
            "object": "J_M^nu",
            "normalization_role": "source current for q_loc/GK sector",
            "formula": "J_M^nu=ell_J T_H^{nu rho} tau_rho",
            "status": "PASS_CONDITIONAL",
            "gap": "ell_J, tau ownership and dynamic exchange not parent-derived",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2568_2_QM",
            "object": "Q_M[Sigma]",
            "normalization_role": "worldtube source charge",
            "formula": "Q_M=int_{Sigma cap W} J_M^mu dSigma_mu",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "gap": "surface independence blocked generically by clock/scale/jump leakage",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2568_3_MH",
            "object": "M_H[Sigma]",
            "normalization_role": "Hilbert mass/energy source before orbital fitting",
            "formula": "M_H=Q_M/ell_J=int_{Sigma cap W} T_H^{mu nu}tau_nu dSigma_mu",
            "status": "PASS_CONDITIONAL_ELLJ_CANCELS",
            "gap": "requires fixed ell_J and normalized tau convention",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2568_4_kappaG",
            "object": "kappa0/G_ref",
            "normalization_role": "metric source coupling in the weak-field Poisson equation",
            "formula": "kappa0=8*pi*G_ref/c^4",
            "status": "CONDITIONAL_DEFINITION_NOT_PARENT_PROOF",
            "gap": "parent EH-leading operator/coupling origin not signed",
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN2568_5_deltaG_source",
            "object": "delta_G_source",
            "normalization_role": "residual mismatch between parent source and Newton source",
            "formula": "delta_G_source -> E_norm until CHAIN2568_0..4 and worldtube dynamics close",
            "status": "RETAIN_AS_E_NORM",
            "gap": "full source-normalization zero certificate missing",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def worldtube_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "WT2568_0_gauss_identity",
            "condition": "Q_M[Sigma_2]-Q_M[Sigma_1]=int_V nabla_mu J_M^mu dV + side_flux + jump_terms",
            "result": "formal worldtube Gauss gate exists",
            "status": "PASS_DERIVED",
            "residual_if_failed": "E_norm_surface_drift",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2568_1_stationary_collar",
            "condition": "ell_J fixed, tau Killing/stationary, matter shell conservation, compact support, no side flux and no hidden jump source",
            "result": "Q_M and M_H are surface-independent in the stationary local control branch",
            "status": "PASS_STATIONARY_CONDITIONAL",
            "residual_if_failed": "E_norm_clock_or_side_flux",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2568_2_dynamic_exchange",
            "condition": "nabla_mu J_M^mu + I_GK + I_tau + I_A = 0 from parent equations",
            "result": "required identity is known in shape but not derived from the parent action",
            "status": "BLOCKED_PARENT_EXCHANGE",
            "residual_if_failed": "E_norm_clock_exchange",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2568_3_jump_support",
            "condition": "distributional worldtube jump conditions and compact support/falloff theorem include all boundary layers",
            "result": "not derived; stationary branch assumes no hidden boundary source",
            "status": "BLOCKED_JUMP_SUPPORT",
            "residual_if_failed": "E_norm_jump_support",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WT2568_4_no_orbital_GM",
            "condition": "do not force Q_M/ell_J or G_ref to equal observed orbital GM as a proof input",
            "result": "anti-circularity guardrail passes",
            "status": "PASS_GUARDRAIL",
            "residual_if_failed": "circular_Newton_proof",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def enorm_component_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "ENORM2568_0_E_norm",
            "component": "E_norm",
            "definition": "E_norm=e_kappaG+e_ellJ_owner+e_surface_drift+e_clock_exchange+e_jump_support+e_hilbert_shadow",
            "status": "RETAIN_NONCLAIM",
            "zero_condition": "all source-normalization chain components are parent-signed and worldtube charge is conserved without fitted GM",
            "next_action": "split retained components and attack the parent coupling/source scale first",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_1_e_kappaG",
            "component": "e_kappaG",
            "definition": "gap between candidate kappa0=8*pi*G_ref/c^4 and a parent-derived MTS coupling",
            "status": "RETAIN",
            "zero_condition": "MTS parent action derives EH-leading coefficient and G_ref is only a later measurement",
            "next_action": "derive parent EH/coupling normalization or keep explicit coupling residual",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_2_e_ellJ_owner",
            "component": "e_ellJ_owner",
            "definition": "gap between the source-current scale ell_J and a parent-owned universal normalization",
            "status": "RETAIN",
            "zero_condition": "ell_J is fixed by parent scale, parent gap or tau normalization before local/cosmology fits",
            "next_action": "tie ell_J to the same parent action normalization as kappa0 if possible",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_3_e_surface_drift",
            "component": "e_surface_drift",
            "definition": "worldtube source-charge drift between hypersurfaces",
            "status": "RETAIN",
            "zero_condition": "Gauss law closes with no side flux for the physical source class",
            "next_action": "derive fixed worldtube surface class and side-flux silence",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_4_e_clock_exchange",
            "component": "e_clock_exchange",
            "definition": "dynamic tau/clock strain leakage in nabla_mu J_M^mu",
            "status": "RETAIN",
            "zero_condition": "parent tau/GK/A equations derive the exchange current cancelling clock strain",
            "next_action": "derive I_GK/I_tau/I_A or restrict to stationary control branch",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_5_e_jump_support",
            "component": "e_jump_support",
            "definition": "distributional worldtube boundary/source support leakage",
            "status": "RETAIN",
            "zero_condition": "source support theorem and jump conditions include all boundary layers",
            "next_action": "write distributional source ledger for compact matter bodies",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_6_e_hilbert_shadow",
            "component": "e_hilbert_shadow",
            "definition": "difference between Hilbert stress source and any non-Hilbert/source-shadow coupling",
            "status": "RETAIN",
            "zero_condition": "matter coupling descent proves no independent source-shadow survives",
            "next_action": "return to source-shadow/universal coupling after parent stress route",
            "valid_for_claim": False,
        },
        {
            "component_id": "ENORM2568_7_stationary_control",
            "component": "E_norm_stationary_control",
            "definition": "zero source-normalization drift under stationary compact-source hypotheses and declared kappa/G relation",
            "status": "CONTROL_ONLY",
            "zero_condition": "valid only inside stationary local theorem branch, not the full dynamic theory",
            "next_action": "use as benchmark branch, not as a local-GR claim",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2568_0_hilbert_mass_chain",
            "claim": "Hilbert mass readout chain is written.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "M_H=Q_M/ell_J=int T_H tau dSigma is explicit under fixed ell_J and normalized tau.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_1_stationary_worldtube",
            "claim": "Stationary compact-source worldtube surface independence closes conditionally.",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "Gauss theorem plus stationary Hilbert-current conservation gives a control branch.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_2_e_norm_zero",
            "claim": "e_source_norm_gap is zero in the full theory.",
            "gate_status": "BLOCKED",
            "reason": "parent kappa/G calibration, ell_J ownership, dynamic exchange, jump/support and source-shadow zero are unsigned.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_3_kappaG",
            "claim": "kappa0/G_ref is parent-derived rather than candidate-declared.",
            "gate_status": "BLOCKED",
            "reason": "2404/2482 give the conditional weak-field relation but not the deeper MTS coupling origin.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_4_dynamic_worldtube",
            "claim": "The physical dynamic worldtube source charge is surface-independent.",
            "gate_status": "BLOCKED",
            "reason": "exchange current, total stress route and jump/support theorem are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_5_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "source normalization has a stationary control branch, not a full zero theorem; residual sectors also remain.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2568_6_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref reuse, plateau axiom or GitHub/public step is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "orbital-GM laundering and EH-import proof remain explicitly forbidden.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2568_0_gain",
            "decision": "Accept stationary Hilbert/worldtube source normalization as a control branch.",
            "reason": "It gives an honest non-fitted source mass under explicit stationary hypotheses.",
            "effect": "Useful for local theorem scaffolding, not a full Newton/local-GR claim.",
        },
        {
            "decision_id": "DEC2568_1_retain_Enorm",
            "decision": "Retain E_norm in E_local_res.",
            "reason": "The full dynamic and parent-calibrated zero certificate is not proved.",
            "effect": "C_res_ext must include source-normalization components unless they are later zeroed.",
        },
        {
            "decision_id": "DEC2568_2_next",
            "decision": "Attack the parent EH/coupling origin before arena kernels.",
            "reason": "The coupling normalization is upstream of R10/PPN observables and controls e_kappaG plus possibly ell_J ownership.",
            "effect": "2569 selected.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2568_0_selected",
            "selection_status": "selected",
            "target_file": "2569-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
            "target_script": "scripts/Y5_R2FR_parent_EH_coupling_origin_or_coupling_residual_row_2569.py",
            "task": "attempt to derive the EH-leading operator and kappa0 coupling from the MTS parent action; if not possible, retain e_kappaG/e_ellJ_owner as explicit coupling residual rows",
            "acceptance_target": "parent action normalization audit, EH import rejection, kappa/G and ell_J residual rows, no fitted-GM guardrail, nonclaim validation",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "theorem_attempt": OUTPUTS["theorem_attempt"],
        "enorm_components": OUTPUTS["enorm_components"],
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
                    "copy_id": f"COPY2568_{key}",
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

    all_output_paths = [DOC, *OUTPUTS.values(), *COPY_TARGETS.values()]
    add("VAL2568_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add("VAL2568_01_hilbert_chain_written", any(row["theorem_id"] == "THM2568_1_mass_readout_cancels_ellJ" for row in data["theorems"]), "ell_J cancellation in mass readout is recorded")
    add("VAL2568_02_divergence_identity_written", any(row["theorem_id"] == "THM2568_2_exact_divergence_identity" for row in data["theorems"]), "exact product-rule divergence is recorded")
    add("VAL2568_03_stationary_gate", any(row["gate_id"] == "WT2568_1_stationary_collar" and row["status"] == "PASS_STATIONARY_CONDITIONAL" for row in data["worldtube"]), "stationary worldtube surface gate is conditional pass")
    add("VAL2568_04_Enorm_retained", any(row["component"] == "E_norm" and row["status"] == "RETAIN_NONCLAIM" for row in data["enorm"]), "E_norm is retained as nonclaim")
    add("VAL2568_05_kappa_and_dynamic_blocked", any(row["component"] == "e_kappaG" and row["status"] == "RETAIN" for row in data["enorm"]) and any(row["component"] == "e_clock_exchange" and row["status"] == "RETAIN" for row in data["enorm"]), "kappa/G and dynamic clock exchange components remain retained")
    add("VAL2568_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10 claim")
    add("VAL2568_07_no_fitted_GM_shortcut", any("fitted GM" in row.get("reason", "") or "fitted GM" in row.get("statement", "") or "fitted GM" in row.get("guardrails", "") for row in [*data["gates"], *data["theorems"], *data["next"]]), "no-fitted-GM guardrail is explicitly carried forward")
    add("VAL2568_08_next_target_written", any(row["route_id"] == "NEXT2568_0_selected" for row in data["next"]), "2569 parent EH/coupling origin target selected")
    add("VAL2568_09_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2568_10_no_formalization_targets", all(FORMALIZATION not in path.parents and path != FORMALIZATION for path in all_output_paths), "all generated target paths are outside formalization-workbench")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2568_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2568_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2568_OVERALL",
        overall,
        "2568 closes a stationary Hilbert/worldtube source-normalization control branch, retains E_norm for the full theory, and selects parent EH/coupling origin next",
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
        "# 2568 Y5 R2FR Hilbert-worldtube Source-normalization Zero Certificate Or Enorm Row",
        "",
        "**Status:** source-normalization control branch sharpened, but full `e_source_norm_gap=0` is not promoted. The Hilbert mass readout is internally clean under fixed `ell_J`, stationary `tau`, compact support and no side/jump flux; dynamic exchange, parent `kappa0/G_ref`, `ell_J` ownership and source-shadow silence remain unsigned.",
        "",
        "**Main result:** `M_H=Q_M/ell_J=int T_H^{mu nu}tau_nu dSigma_mu` removes `ell_J` from the stationary mass readout, so fitted orbital `GM` is not needed there. But `E_norm` remains in `E_local_res` because the full parent-coupled, dynamic and source-shadow-free zero certificate has not closed.",
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
        "## E Norm Components",
        markdown_table(data["enorm"], ["component_id", "component", "definition", "status", "zero_condition", "next_action", "valid_for_claim"]),
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
        "enorm": enorm_component_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorems"])
    write_csv(OUTPUTS["normalization_chain"], data["chain"])
    write_csv(OUTPUTS["worldtube_gate"], data["worldtube"])
    write_csv(OUTPUTS["enorm_components"], data["enorm"])
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
