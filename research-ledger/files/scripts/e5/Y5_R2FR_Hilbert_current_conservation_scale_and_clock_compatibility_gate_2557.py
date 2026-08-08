from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2557"
BRANCH_ID = "MTS_R2FR_HILBERT_CURRENT_CONSERVATION_SCALE_AND_CLOCK_COMPATIBILITY_GATE_2557"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2557_SOURCE_REGISTER.csv",
    "divergence_identity": OUT / "P8_Y5_NO_SHADOW_2557_DIVERGENCE_IDENTITY.csv",
    "clock_gate": OUT / "P8_Y5_NO_SHADOW_2557_CLOCK_COMPATIBILITY_GATE.csv",
    "scale_gate": OUT / "P8_Y5_NO_SHADOW_2557_PARENT_SCALE_OPTIONS.csv",
    "exchange_identity": OUT / "P8_Y5_NO_SHADOW_2557_EXCHANGE_CURRENT_IDENTITY.csv",
    "worldtube_gate": OUT / "P8_Y5_NO_SHADOW_2557_WORLDTUBE_SURFACE_GATE.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2557_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2557_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2557_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2557_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2557_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2557_VALIDATION.csv",
}

COPY_TARGETS = {
    "clock_gate_contract": QUEUE / "JR2557_CLOCK_COMPATIBILITY_GATE_NONCLAIM.csv",
    "scale_gate_contract": QUEUE / "JR2557_PARENT_SCALE_OPTIONS_NONCLAIM.csv",
    "worldtube_gate_contract": LOCAL_BOUNDS / "Worldtube_surface_gate_2557_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2557_00_2556_doc",
        "source_path": ROOT / "2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["HIL2556_2_parent_scale", "CON2556_2_exact_identity_needed", "NEXT2556_0_selected", "VAL2556_OVERALL"],
        "role": "active handoff selecting exact Hilbert-current conservation and scale gate",
    },
    {
        "source_id": "SRC2557_01_2556_hilbert_descent",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT.csv",
        "needles": ["HIL2556_1_define_current", "HIL2556_2_parent_scale", "MISSING_PARENT_SCALE"],
        "role": "machine-readable Hilbert current and parent-scale blocker",
    },
    {
        "source_id": "SRC2557_02_2556_conservation",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2556_CONSERVATION_AUDIT.csv",
        "needles": ["CON2556_0_matter_shell", "CON2556_2_exact_identity_needed", "MISSING_EXACT_IDENTITY"],
        "role": "machine-readable conservation identity gap",
    },
    {
        "source_id": "SRC2557_03_2556_worldtube",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE.csv",
        "needles": ["WT2556_2_surface_independence", "WT2556_4_no_orbital_GM", "PASS_GUARDRAIL"],
        "role": "worldtube surface-independence and anti-circularity guardrail",
    },
    {
        "source_id": "SRC2557_04_2556_wep",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL.csv",
        "needles": ["WEP2556_0_hilbert_universal", "WEP2556_3_composition_bound", "BLOCKS_CLAIM"],
        "role": "universality support and residual composition blocker",
    },
    {
        "source_id": "SRC2557_05_2556_vacuum",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2556_EXTERNAL_VACUUM_SUPPORT.csv",
        "needles": ["VAC2556_0_exact_vacuum", "VAC2556_2_clock_leak", "MISSING_CLOCK_BOUND"],
        "role": "external vacuum conditional and clock-leak blocker",
    },
    {
        "source_id": "SRC2557_06_2467_precedent",
        "source_path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": ["DIV2467_1_full_divergence", "DIV2467_5_generic_clock", "SCL2467_5_current_status", "VAL2467_OVERALL"],
        "role": "earlier same-gate derivation precedent, now re-run against sharper 2556 bridge",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in SOURCE_SPECS:
        path = Path(spec["source_path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        exists = path.exists()
        rows.append(
            {
                **base_row(),
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "missing_needles": ";".join(missing),
                "source_pass": bool_text(exists and not missing),
                "role": spec["role"],
            }
        )
    return rows


def divergence_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DIV2557_0_define_current",
            "J_M^mu := ell_J T_matter^{mu nu} tau_nu",
            "2556 Hilbert-current source bridge",
            "source current is universal if matter action is metric-coupled and tau is parent-owned",
            "PASS_AS_INPUT",
        ),
        (
            "DIV2557_1_full_product_rule",
            "nabla_mu J_M^mu = (nabla_mu ell_J) T^{mu nu} tau_nu + ell_J (nabla_mu T^{mu nu}) tau_nu + ell_J T^{mu nu} nabla_mu tau_nu",
            "Leibniz rule for a scalar ell_J, symmetric Hilbert stress, and clock one-form tau",
            "exact algebraic identity before using matter equations",
            "PASS_DERIVED",
        ),
        (
            "DIV2557_2_matter_shell_constant_scale",
            "if nabla_mu T^{mu nu}=0 and nabla_mu ell_J=0, then nabla_mu J_M^mu = ell_J T^{mu nu} nabla_mu tau_nu",
            "matter equations plus fixed parent scale",
            "clock strain is the only remaining leakage",
            "PASS_DERIVED_CONDITIONAL",
        ),
        (
            "DIV2557_3_symmetric_clock_strain",
            "for symmetric T, T^{mu nu} nabla_mu tau_nu = T^{mu nu} nabla_(mu tau_nu)",
            "Hilbert stress symmetry",
            "antisymmetric clock vorticity cannot source the divergence",
            "PASS_DERIVED",
        ),
        (
            "DIV2557_4_Killing_or_covariantly_constant_clock",
            "if nabla_(mu tau_nu)=0 in the collar, nabla_mu J_M^mu=0 on shell with fixed ell_J",
            "stationary local clock condition",
            "stationary compact-source route can close conditionally",
            "CONDITIONAL_CLOSES",
        ),
        (
            "DIV2557_5_generic_clock_obstruction",
            "for generic tau, nabla_mu J_M^mu is nonzero unless a parent exchange term cancels the clock-strain leak",
            "dynamic MTS/time sector",
            "Hilbert current alone does not prove exact conservation",
            "BLOCKED_CURRENT_THEOREM",
        ),
        (
            "DIV2557_6_variable_scale_obstruction",
            "if nabla_mu ell_J != 0, the term (nabla_mu ell_J)T^{mu nu}tau_nu is an extra source leak",
            "scale as field or local fitted normalisation",
            "ell_J must be parent-fixed, constant in the local collar, or supplied with its own exchange identity",
            "BLOCKED_IF_SCALE_FLOATS",
        ),
    ]
    return [
        {**base_row(), "divergence_id": item, "identity_or_condition": identity, "basis": basis, "result": result, "status": status}
        for item, identity, basis, result, status in rows
    ]


def clock_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CLK2557_0_stationary_gate",
            "stationary/Killing collar",
            "nabla_(mu tau_nu)=0 across the local source collar",
            "kills the Hilbert-current leakage term exactly on matter shell",
            "CONDITIONAL_PASS",
        ),
        (
            "CLK2557_1_local_inertial_point_gate",
            "pointwise local inertial frame",
            "nabla_(mu tau_nu)=0 only at one event or to finite-order approximation",
            "good for local expansion bookkeeping, not enough for finite worldtube conservation",
            "APPROXIMATION_NOT_THEOREM",
        ),
        (
            "CLK2557_2_dynamic_clock_gate",
            "generic evolving MTS clock",
            "nabla_(mu tau_nu) generally nonzero",
            "requires parent-derived exchange current or a dynamical clock equation with signed cancellation",
            "BLOCKED",
        ),
        (
            "CLK2557_3_FLRW_split",
            "cosmology/time activation",
            "cosmological memory may deliberately have nonzero clock strain",
            "local GR route must split local stationary collars from cosmological activation",
            "REQUIRED_SPLIT",
        ),
        (
            "CLK2557_4_parent_clock_origin",
            "tau parent-owned",
            "tau must descend from the parent action/coframe rather than be chosen to fit a source",
            "clock compatibility cannot be imposed as an after-the-fact gauge patch",
            "MISSING_PARENT_CLOCK_EQUATION",
        ),
        (
            "CLK2557_5_clock_leak_bound",
            "finite local bound",
            "epsilon_tau(W)=int_W |ell_J T^{mu nu}nabla_(mu tau_nu)| dV",
            "if exact closure fails, this becomes the residual PPN/local-GR bound to source",
            "BOUND_FORM_ONLY",
        ),
    ]
    return [
        {**base_row(), "clock_id": item, "gate": gate, "condition": condition, "effect": effect, "status": status}
        for item, gate, condition, effect, status in rows
    ]


def scale_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCL2557_0_dimension",
            "[ell_J]=M^-1=L if [J_M]=M^3, [T]=M^4, and tau is dimensionless",
            "fits the 2555 viable branch where A has mass dimension one and Gamma_eff has mass dimension two",
            "PASS_DERIVED_DIMENSION",
        ),
        (
            "SCL2557_1_parent_length_candidate",
            "ell_J could be a universal parent length ell_*",
            "acceptable only if fixed by the parent action before any local/cosmology fits",
            "CANDIDATE_ONLY",
        ),
        (
            "SCL2557_2_gap_candidate",
            "ell_J could be inverse parent gap 1/m_*",
            "acceptable only if m_* is an independently derived spectrum/action scale",
            "CANDIDATE_ONLY",
        ),
        (
            "SCL2557_3_clock_normalisation_candidate",
            "ell_J could be absorbed into parent normalisation of tau",
            "acceptable only if tau normalisation is universal and not source-fitted",
            "CANDIDATE_ONLY",
        ),
        (
            "SCL2557_4_forbidden_fit",
            "ell_J cannot be chosen from observed GM, orbital acceleration, H0 pressure, or M_H_ref denominator reuse",
            "would make the Newton/local-GR bridge circular",
            "REJECTED_GUARDRAIL",
        ),
        (
            "SCL2557_5_current_status",
            "current corpus has no signed parent derivation of ell_J",
            "source-current normalisation remains blocked for theorem claims",
            "MISSING_PARENT_SCALE",
        ),
        (
            "SCL2557_6_variable_scale_warning",
            "if ell_J is dynamical, nabla_mu ell_J must be included in the exchange identity",
            "otherwise the scale field injects an untracked source leak",
            "MISSING_SCALE_EXCHANGE_CLAUSE",
        ),
    ]
    return [
        {**base_row(), "scale_id": item, "scale_clause": clause, "reason": reason, "status": status}
        for item, clause, reason, status in rows
    ]


def exchange_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EXC2557_0_required_identity",
            "nabla_mu J_M^mu + I_GK = 0",
            "integrability of the A/current equation and surface independence of Q_M",
            "required for a general dynamic source theorem",
            "REQUIRED_NOT_DERIVED",
        ),
        (
            "EXC2557_1_minimal_on_shell_form",
            "I_GK = -ell_J T^{mu nu}nabla_(mu tau_nu)",
            "after nabla_mu T^{mu nu}=0 and fixed ell_J",
            "exact form of the needed clock-exchange cancellation is identified",
            "FORM_DERIVED_SOURCE_MISSING",
        ),
        (
            "EXC2557_2_full_scale_form",
            "I_GK = -[(nabla_mu ell_J)T^{mu nu}tau_nu + ell_J(nabla_mu T^{mu nu})tau_nu + ell_J T^{mu nu}nabla_mu tau_nu]",
            "before matter-shell and fixed-scale reductions",
            "full cancellation target known, but not yet produced by parent variation",
            "FORM_DERIVED_SOURCE_MISSING",
        ),
        (
            "EXC2557_3_parent_source_requirement",
            "I_GK must be obtained from Gamma/Khat/tau equations or a Noether identity",
            "parent action consistency",
            "cannot be manually appended without losing the derivation route",
            "MISSING_PARENT_DERIVATION",
        ),
        (
            "EXC2557_4_stationary_silence",
            "in stationary collars I_GK=0 because the clock-strain source is zero",
            "Killing/covariantly constant tau branch",
            "gives a narrow local theorem path without dynamic exchange machinery",
            "CONDITIONAL_CLOSES",
        ),
        (
            "EXC2557_5_boundary_silence",
            "boundary/local projection terms must vanish or be included in I_GK",
            "worldtube and local projection consistency",
            "uncontrolled boundary leakage blocks promotion",
            "MISSING_BOUNDARY_IDENTITY",
        ),
    ]
    return [
        {**base_row(), "exchange_id": item, "identity": identity, "basis": basis, "result": result, "status": status}
        for item, identity, basis, result, status in rows
    ]


def worldtube_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WTG2557_0_surface_difference",
            "Q_M[Sigma_2]-Q_M[Sigma_1]=int_V nabla_mu J_M^mu dV + side_flux",
            "Gauss theorem for the worldtube slab",
            "surface independence needs exact conservation and controlled side flux",
            "PASS_DERIVED",
        ),
        (
            "WTG2557_1_stationary_surface",
            "if T has compact support, ell_J is fixed, tau is Killing, and side flux vanishes, Q_M is surface-independent",
            "DIV2557_4 plus compact-support collar",
            "stationary local source theorem can be attempted",
            "CONDITIONAL_CLOSES",
        ),
        (
            "WTG2557_2_dynamic_surface",
            "if tau is dynamic, surface drift equals int_V[-I_GK]dV plus side flux once exchange identity is known",
            "EXC2557_0 dynamic branch",
            "blocked until parent exchange current is derived",
            "BLOCKED",
        ),
        (
            "WTG2557_3_distributional_surface",
            "surface layers need jump terms in J_M or an explicit boundary flux ledger",
            "compact source with boundary",
            "prevents hiding source at the matter boundary",
            "MISSING_JUMP_IDENTITY",
        ),
        (
            "WTG2557_4_no_orbital_GM",
            "do not force Q_M/ell_J to equal observed GM",
            "anti-circularity guardrail from 2556",
            "Newton limit remains derivation-first",
            "PASS_GUARDRAIL",
        ),
        (
            "WTG2557_5_external_q_zero",
            "outside compact matter support J_M=0, so q_loc=P_loc J_M=0 only after projection/support/boundary clauses are signed",
            "source-free exterior",
            "useful local-vacuum route, but still conditional",
            "CONDITIONAL_NOT_CLAIM",
        ),
    ]
    return [
        {**base_row(), "worldtube_id": item, "clause": clause, "basis": basis, "result": result, "status": status}
        for item, clause, basis, result, status in rows
    ]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PV2557_0_conservation_identity",
            "Is the Hilbert current exactly conserved?",
            "ONLY_IF_STATIONARY_OR_PARENT_EXCHANGE_DERIVED",
            "product-rule divergence leaves clock strain and possible scale-gradient leakage",
            "not a general theorem yet",
        ),
        (
            "PV2557_1_parent_scale",
            "Is ell_J parent-derived?",
            "NO",
            "dimension and candidate routes are identified, but no action-normalised source exists",
            "scale gate remains blocked",
        ),
        (
            "PV2557_2_clock_compatibility",
            "Does local clock compatibility close?",
            "CONDITIONALLY",
            "Killing/stationary local collar closes; generic MTS time requires exchange current",
            "split local and cosmological/dynamic branches",
        ),
        (
            "PV2557_3_worldtube",
            "Is worldtube source mass surface-independent?",
            "CONDITIONAL_NOT_GENERAL",
            "surface independence follows only under conservation plus no side/boundary leakage",
            "need jump/support theorem",
        ),
        (
            "PV2557_4_Newton_local_GR",
            "Does 2557 prove Newton/local GR?",
            "NO",
            "source normalisation, dynamic exchange, and boundary support remain unsigned",
            "no local-GR claim",
        ),
        (
            "PV2557_5_overall",
            "Overall 2557 verdict",
            "DERIVATION_SHARPENED_NOT_PROMOTED",
            "exact leakage terms are now explicit; branch survives as a narrow stationary theorem plus dynamic exchange target",
            "next target should derive I_GK or prove the stationary theorem cleanly",
        ),
    ]
    return [
        {**base_row(), "verdict_id": item, "question": question, "result": result, "evidence": evidence, "effect": effect}
        for item, question, result, evidence, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GATE2557_0_product_rule",
            "Full divergence identity is derived.",
            "PASS",
            "DIV2557_1 records exact product rule",
            "true",
            "false",
        ),
        (
            "GATE2557_1_stationary_contract",
            "Stationary compact-source Hilbert current is conserved.",
            "PASS_AS_CONDITIONAL_CONTRACT",
            "requires fixed ell_J, conserved T, Killing tau, compact support, and no side flux",
            "true",
            "false",
        ),
        (
            "GATE2557_2_dynamic_exchange",
            "Generic dynamic MTS source current is conserved.",
            "BLOCKED",
            "I_GK form is known but not parent-derived",
            "false",
            "false",
        ),
        (
            "GATE2557_3_parent_scale",
            "ell_J is parent-derived and not fitted.",
            "BLOCKED",
            "no signed parent scale in corpus",
            "false",
            "false",
        ),
        (
            "GATE2557_4_worldtube",
            "Q_M is surface-independent for physical bounded sources.",
            "BLOCKED",
            "dynamic exchange, jump terms, and side flux ledger missing",
            "false",
            "false",
        ),
        (
            "GATE2557_5_local_GR_Newton",
            "Local GR/Newton branch passes.",
            "BLOCKED",
            "2557 is a source-bridge gate, not a full metric-limit theorem",
            "false",
            "false",
        ),
    ]
    return [
        {**base_row(), "gate_id": item, "claim": claim, "gate_status": status, "reason": reason, "gate_pass": gate_pass, "claim_promoted": promoted}
        for item, claim, status, reason, gate_pass, promoted in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2557_0_keep_hilbert",
            "Keep Hilbert/energy current as the primary matter source route.",
            "it matches GR source structure and avoids species-tuned charges",
            "continue this branch",
        ),
        (
            "DEC2557_1_no_fake_scale",
            "Do not promote ell_J or derive it from observed GM.",
            "that would make the Newton bridge circular",
            "parent scale remains a blocker",
        ),
        (
            "DEC2557_2_split_clock_routes",
            "Split stationary local collars from dynamic/cosmological clock activation.",
            "stationary collars can close conditionally; dynamic clocks need I_GK",
            "prevents local GR and cosmology from fighting each other",
        ),
        (
            "DEC2557_3_next_target",
            "Next attempt parent derivation of the exchange current or prove the stationary source theorem.",
            "the exact obstruction is now I_GK plus ell_J and boundary support",
            "2558 selected",
        ),
    ]
    return [
        {**base_row(), "decision_id": item, "decision": decision, "reason": reason, "effect": effect}
        for item, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2557_0_selected",
            "selection_status": "selected",
            "target_file": "2558-Y5-R2FR-parent-clock-exchange-current-or-stationary-source-theorem.md",
            "target_script": "scripts/Y5_R2FR_parent_clock_exchange_current_or_stationary_source_theorem_2558.py",
            "task": "try to derive I_GK from the parent tau/Gamma/Khat equations; if that fails, prove the narrower stationary compact-source theorem and demote dynamic closure",
            "acceptance_target": "parent exchange-current derivation attempt, stationary theorem hypotheses, ell_J status, boundary/jump ledger, and no local-GR claim unless all gates close",
            "guardrails": "no fitted GM; no M_H_ref reuse; no plateau axiom; no local-GR claim from conditional stationary contract; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    copy_sources = {
        "clock_gate_contract": OUTPUTS["clock_gate"],
        "scale_gate_contract": OUTPUTS["scale_gate"],
        "worldtube_gate_contract": OUTPUTS["worldtube_gate"],
    }
    rows = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        shutil.copyfile(source, target)
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": bool_text(source.exists()),
                "target_exists": bool_text(target.exists()),
            }
        )
    return rows


def csv_row_count(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in csv.DictReader(handle)), 0)


def formalization_status_detail() -> tuple[bool, str]:
    touched_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC, Path(__file__).resolve()]
    outside_formalization = [path for path in touched_paths if not is_relative_to(path, FORMALIZATION)]
    return len(outside_formalization) == len(touched_paths), f"declared_2557_paths_outside_formalization={len(outside_formalization)}/{len(touched_paths)}"


def validation_rows(
    sources: list[dict[str, Any]],
    divergence: list[dict[str, Any]],
    clock: list[dict[str, Any]],
    scale: list[dict[str, Any]],
    exchange: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail})

    all_sources_pass = all(row["source_pass"] == "true" for row in sources)
    add("VAL2557_00_sources_exist", all_sources_pass, "all cited source paths exist and needles are present")
    add("VAL2557_01_full_product_rule", any(row["divergence_id"] == "DIV2557_1_full_product_rule" and row["status"] == "PASS_DERIVED" for row in divergence), "full divergence identity derived")
    add("VAL2557_02_symmetric_clock_strain", any(row["divergence_id"] == "DIV2557_3_symmetric_clock_strain" and row["status"] == "PASS_DERIVED" for row in divergence), "antisymmetric clock vorticity drops out for symmetric stress")
    add("VAL2557_03_generic_clock_block", any(row["divergence_id"] == "DIV2557_5_generic_clock_obstruction" and row["status"] == "BLOCKED_CURRENT_THEOREM" for row in divergence), "generic dynamic clock obstruction retained")
    add("VAL2557_04_stationary_gate", any(row["clock_id"] == "CLK2557_0_stationary_gate" and row["status"] == "CONDITIONAL_PASS" for row in clock), "stationary/Killing clock gate recorded")
    add("VAL2557_05_clock_bound_form", any(row["clock_id"] == "CLK2557_5_clock_leak_bound" and row["status"] == "BOUND_FORM_ONLY" for row in clock), "clock-leak residual bound form recorded")
    add("VAL2557_06_parent_scale_blocked", any(row["scale_id"] == "SCL2557_5_current_status" and row["status"] == "MISSING_PARENT_SCALE" for row in scale), "parent scale remains blocked")
    add("VAL2557_07_no_forbidden_scale_fit", any(row["scale_id"] == "SCL2557_4_forbidden_fit" and row["status"] == "REJECTED_GUARDRAIL" for row in scale), "GM/H0/M_H_ref fitted scale routes rejected")
    add("VAL2557_08_exchange_identity_required", any(row["exchange_id"] == "EXC2557_0_required_identity" and row["status"] == "REQUIRED_NOT_DERIVED" for row in exchange), "dynamic exchange identity remains required and unsigned")
    add("VAL2557_09_exchange_form_derived", any(row["exchange_id"] == "EXC2557_1_minimal_on_shell_form" and row["status"] == "FORM_DERIVED_SOURCE_MISSING" for row in exchange), "minimal on-shell exchange form derived but not parent-sourced")
    add("VAL2557_10_worldtube_guardrail", any(row["worldtube_id"] == "WTG2557_4_no_orbital_GM" and row["status"] == "PASS_GUARDRAIL" for row in worldtube), "orbital-GM source definition remains forbidden")
    add("VAL2557_11_no_local_gr_claim", any(row["gate_id"] == "GATE2557_5_local_GR_Newton" and row["gate_status"] == "BLOCKED" and row["claim_promoted"] == "false" for row in gates), "local GR/Newton claim remains blocked")
    add("VAL2557_12_overall_verdict_nonclaim", any(row["verdict_id"] == "PV2557_5_overall" and row["result"] == "DERIVATION_SHARPENED_NOT_PROMOTED" for row in verdicts), "overall verdict is sharpened nonclaim")
    add("VAL2557_13_next_target_selected", any(row["route_id"] == "NEXT2557_0_selected" and row["selection_status"] == "selected" for row in next_rows), "2558 next target selected")
    add("VAL2557_14_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_copies), "nonclaim branch copies exist")

    output_paths = list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]
    add("VAL2557_15_all_outputs_inside_post_checkpoint", all(is_relative_to(path, ROOT) for path in output_paths), "all 2557 outputs stay inside post-checkpoint-work")
    formalization_ok, formalization_detail = formalization_status_detail()
    add("VAL2557_16_formalization_workbench_not_targeted", formalization_ok, "declared 2557 outputs do not target formalization-workbench", formalization_detail)

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        add(f"VAL2557_OUTPUT_{key}", path.exists() and csv_row_count(path) > 0, f"{key} output exists and has rows", str(path))

    for copy_id, path in COPY_TARGETS.items():
        add(f"VAL2557_COPY_{copy_id}", path.exists() and csv_row_count(path) > 0, f"{copy_id} copy exists and has rows", str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2557_OVERALL", overall, "2557 derives the Hilbert-current leakage identity, blocks theorem claims on parent scale/exchange/boundary support, and selects 2558")
    return rows


def escape_md(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(escape_md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    divergence: list[dict[str, Any]],
    clock: list[dict[str, Any]],
    scale: list[dict[str, Any]],
    exchange: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2557 Y5 R2FR Hilbert-current Conservation Scale And Clock Compatibility Gate",
                "**Status:** derivation sharpened, theorem not promoted. The exact divergence of `J_M^mu=ell_J T_matter^{mu nu}tau_nu` is now explicit: it is controlled by parent-scale gradients, matter stress conservation, and symmetric clock strain. A stationary/Killing local collar can close conditionally, but the generic dynamic branch still needs a parent-derived exchange current.",
                "**Main result:** the Hilbert route survives, but only honestly. The stationary compact-source route is a real theorem target; the full dynamic MTS/time route is blocked until `I_GK` and `ell_J` come from the parent action rather than being patched in. No Newton, local-GR, PPN, WEP, or R10 pass is claimed here.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
                "## Divergence Identity",
                markdown_table(divergence, ["divergence_id", "identity_or_condition", "basis", "result", "status"]),
                "## Clock Compatibility Gate",
                markdown_table(clock, ["clock_id", "gate", "condition", "effect", "status"]),
                "## Parent Scale Options",
                markdown_table(scale, ["scale_id", "scale_clause", "reason", "status"]),
                "## Exchange Current Identity",
                markdown_table(exchange, ["exchange_id", "identity", "basis", "result", "status"]),
                "## Worldtube Surface Gate",
                markdown_table(worldtube, ["worldtube_id", "clause", "basis", "result", "status"]),
                "## Promotion Verdict",
                markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
                "## Claim Gates",
                markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_promoted"]),
                "## Decision Ledger",
                markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
                "## Next Target",
                markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
                "## Branch Copies",
                markdown_table(branch_copies, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
                "## Validation",
                markdown_table(validations, ["check_id", "status", "notes", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    divergence = divergence_identity_rows()
    clock = clock_gate_rows()
    scale = scale_gate_rows()
    exchange = exchange_identity_rows()
    worldtube = worldtube_gate_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["divergence_identity"], divergence)
    write_csv(OUTPUTS["clock_gate"], clock)
    write_csv(OUTPUTS["scale_gate"], scale)
    write_csv(OUTPUTS["exchange_identity"], exchange)
    write_csv(OUTPUTS["worldtube_gate"], worldtube)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_copies = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validations = validation_rows(sources, divergence, clock, scale, exchange, worldtube, verdicts, gates, decisions, next_rows, branch_copies)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, divergence, clock, scale, exchange, worldtube, verdicts, gates, decisions, next_rows, branch_copies, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
