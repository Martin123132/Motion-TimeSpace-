from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_HILBERT_CURRENT_CONSERVATION_SCALE_AND_CLOCK_COMPATIBILITY_GATE_2467"
CHECKPOINT_ID = "2467"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_HILBERT_CURRENT_2467_SOURCE_REGISTER.csv",
    "divergence_identity": OUT / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv",
    "clock_gate": OUT / "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv",
    "scale_gate": OUT / "P8_Y5_HILBERT_CURRENT_2467_PARENT_SCALE_OPTIONS.csv",
    "exchange_identity": OUT / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv",
    "worldtube_gate": OUT / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv",
    "promotion_verdict": OUT / "P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_HILBERT_CURRENT_2467_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_HILBERT_CURRENT_2467_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_HILBERT_CURRENT_2467_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_HILBERT_CURRENT_2467_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2467_VALIDATION.csv",
}

COPY_TARGETS = {
    "clock_gate_contract": QUEUE / "JR2467_CLOCK_COMPATIBILITY_GATE_NONCLAIM.csv",
    "scale_gate_contract": QUEUE / "JR2467_PARENT_SCALE_OPTIONS_NONCLAIM.csv",
    "worldtube_gate_contract": LOCAL_BOUNDS / "Worldtube_surface_gate_2467_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2467_00_2466_doc",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["HIL2466_1_define_current", "CON2466_2_exact_identity_needed", "NEXT2466_0_selected", "VAL2466_OVERALL"],
        "role": "handoff selecting Hilbert-current conservation/scale gate",
    },
    {
        "source_id": "SRC2467_01_2466_hilbert",
        "source_path": OUT / "P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv",
        "needles": ["HIL2466_1_define_current", "MISSING_PARENT_SCALE", "MISSING_CLOCK_CONSERVATION_CLAUSE"],
        "role": "Hilbert current and missing scale/clock clauses",
    },
    {
        "source_id": "SRC2467_02_2466_conservation",
        "source_path": OUT / "P8_Y5_SOURCE_BRIDGE_2466_CONSERVATION_AUDIT.csv",
        "needles": ["CON2466_0_matter_shell", "MISSING_EXACT_IDENTITY", "MISSING_JUMP_IDENTITY"],
        "role": "conservation identity blockers",
    },
    {
        "source_id": "SRC2467_03_2466_worldtube",
        "source_path": OUT / "P8_Y5_SOURCE_BRIDGE_2466_WORLDTUBE_BRIDGE.csv",
        "needles": ["WT2466_1_mass_readout", "WT2466_2_surface_independence", "WT2466_4_no_orbital_GM"],
        "role": "worldtube surface gate handoff",
    },
    {
        "source_id": "SRC2467_04_2465_dimension",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_DIMENSION_AUDIT.csv",
        "needles": ["DIM2465_3_viable_branch", "DIM2465_6_parent_scale_needed"],
        "role": "dimension branch and parent scale warning",
    },
    {
        "source_id": "SRC2467_05_2464_action",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2464_A_vertical_generator_current_law", "A_nu J_M^nu"],
        "role": "action requiring source-current normalization",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def divergence_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DIV2467_0_define_current",
            "J_M^nu = ell_J T_matter^{nu rho} tau_rho",
            "Hilbert-current branch from 2466",
            "candidate source current",
            "PASS_AS_INPUT",
        ),
        (
            "DIV2467_1_full_divergence",
            "nabla_nu J_M^nu = (nabla_nu ell_J)T^{nu rho}tau_rho + ell_J(nabla_nu T^{nu rho})tau_rho + ell_J T^{nu rho}nabla_nu tau_rho",
            "product rule",
            "exact identity before using matter equations",
            "PASS_DERIVED",
        ),
        (
            "DIV2467_2_matter_shell",
            "If ell_J is constant and nabla_nu T^{nu rho}=0, then nabla_nu J_M^nu = ell_J T^{nu rho}nabla_nu tau_rho",
            "matter on shell and fixed parent scale",
            "clock strain is the remaining leakage",
            "PASS_DERIVED_CONDITIONAL",
        ),
        (
            "DIV2467_3_symmetric_stress",
            "For symmetric T, T^{nu rho}nabla_nu tau_rho = T^{nu rho}nabla_(nu tau_{rho)}",
            "Hilbert stress is symmetric",
            "only the symmetric clock strain matters; antisymmetric vorticity drops out",
            "PASS_DERIVED",
        ),
        (
            "DIV2467_4_Killing_clock",
            "If tau is Killing in the relevant collar, nabla_(nu tau_{rho)}=0 and nabla.J_M=0",
            "stationary/local clock condition",
            "exact surface-independent current in that region",
            "CONDITIONAL_CLOSES",
        ),
        (
            "DIV2467_5_generic_clock",
            "For a generic clock field, nabla.J_M is not zero unless an exchange term I_tau=-nabla.J_M is parent-derived",
            "generic MTS/time sector",
            "exact source bridge does not close from Hilbert current alone",
            "BLOCKED_CURRENT_THEOREM",
        ),
    ]
    return [{**base_row(), "identity_id": i, "statement": s, "basis": b, "result": r, "status": st} for i, s, b, r, st in rows]


def clock_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLK2467_0_stationary_gate", "tau Killing or locally stationary", "nabla_(mu tau_nu)=0 in source/worldtube collar", "closes conservation exactly in that collar", "CONDITIONAL_PASS"),
        ("CLK2467_1_local_inertial_gate", "local inertial approximation", "nabla tau = O(L_lab/L_curv)", "gives small leakage estimate, not exact theorem", "BOUND_ONLY"),
        ("CLK2467_2_dynamic_clock_gate", "generic evolving MTS clock", "nabla_(mu tau_nu) not zero", "requires exchange current from tau/GK equations", "BLOCKED"),
        ("CLK2467_3_cosmology_split", "cosmological activation allowed", "clock strain may be nonzero on FLRW scales", "local GR route must split stationary local collars from cosmological memory", "REQUIRED_SPLIT"),
        ("CLK2467_4_parent_clock_origin", "tau parent-owned", "tau variation/action must define clock strain equation", "not sourced in current corpus at theorem level", "MISSING_PARENT_CLOCK_EQUATION"),
    ]
    return [{**base_row(), "clock_id": i, "gate": g, "condition": c, "effect": e, "status": st} for i, g, c, e, st in rows]


def scale_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCL2467_0_dimension", "ell_J has dimension M^-1 if tau is dimensionless and T has dimension M^4", "needed so J_M has dimension M^3", "PASS_DERIVED"),
        ("SCL2467_1_mass_readout_cancels", "M_source = Q_M/ell_J = int T^{mu nu}tau_nu dSigma_mu", "ell_J cancels in source mass readout but not in q_loc coupling amplitude", "PASS_AS_CLARIFICATION"),
        ("SCL2467_2_planck_candidate", "ell_J could be a parent gravitational length such as a Planck-scale coupling", "acceptable only if action normalisation derives it before fits", "CANDIDATE_ONLY"),
        ("SCL2467_3_vertical_kinetic_candidate", "ell_J could be fixed by vertical-generator kinetic normalization Z_K/g_A", "acceptable only if L_K and A normalization are parent-fixed", "CANDIDATE_ONLY"),
        ("SCL2467_4_empirical_fit_forbidden", "ell_J cannot be chosen from orbital GM, PPN residuals, or local fifth-force bounds", "would make Newton/local-GR limit circular", "REJECTED"),
        ("SCL2467_5_current_status", "current corpus has no parent derivation of ell_J", "scale gate remains blocked", "MISSING_PARENT_SCALE"),
    ]
    return [{**base_row(), "scale_id": i, "scale_clause": c, "reason": r, "status": st} for i, c, r, st in rows]


def exchange_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EXC2467_0_required_identity",
            "nabla_nu J_M^nu + I_tau + I_A = 0",
            "generic clock/source exchange identity required by A-equation integrability",
            "must be derived from tau/GK/matter equations",
            "REQUIRED_NOT_DERIVED",
        ),
        (
            "EXC2467_1_clock_exchange_form",
            "I_tau = ell_J T^{mu nu}nabla_(mu tau_{nu)} + (nabla_mu ell_J)T^{mu nu}tau_nu",
            "minimal exchange needed after using nabla_mu T^{mu nu}=0",
            "formula identified, but source action for exchange missing",
            "FORM_DERIVED_NOT_OWNED",
        ),
        (
            "EXC2467_2_total_stress_route",
            "If matter stress is not separately conserved due to A/tau coupling, use nabla_mu(T_matter^{mu nu}+T_GK^{mu nu}+T_tau^{mu nu})=0",
            "diffeomorphism route",
            "could close only after full parent stress tensor exists",
            "PARENT_STRESS_REQUIRED",
        ),
        (
            "EXC2467_3_local_stationary_escape",
            "In stationary local collars, I_tau=0 without new exchange machinery",
            "Killing clock route",
            "enough for a local stationary theorem, not full dynamic theory",
            "CONDITIONAL_LOCAL_ROUTE",
        ),
    ]
    return [{**base_row(), "exchange_id": i, "identity": identity, "basis": basis, "result": result, "status": status} for i, identity, basis, result, status in rows]


def worldtube_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("WTG2467_0_surface_difference", "Q[Sigma_2]-Q[Sigma_1]=int_V nabla_mu J_M^mu dV + side_flux", "Gauss theorem", "surface independence needs conservation plus no side leakage", "PASS_DERIVED"),
        ("WTG2467_1_stationary_surface", "For compact support plus stationary clock, Q is surface-independent", "nabla.J=0 and side_flux=0", "worldtube source bridge closes conditionally", "CONDITIONAL_CLOSES"),
        ("WTG2467_2_dynamic_surface", "For dynamic clock, surface drift equals int_V I_tau dV plus side flux", "exchange identity", "not closed without parent exchange current", "BLOCKED"),
        ("WTG2467_3_no_fitted_mass", "Do not force surface independence by defining Q from observed mass/GM", "anti-circularity", "guardrail retained", "PASS_GUARDRAIL"),
        ("WTG2467_4_external_vacuum", "Outside compact matter support, T=0 implies J=0, hence q_loc=0 in source-free exterior up to boundary tails", "Hilbert current support", "local exterior zero is plausible conditional support, not full Newton proof", "CONDITIONAL_SUPPORT"),
    ]
    return [{**base_row(), "worldtube_gate_id": i, "statement": s, "basis": b, "result": r, "status": st} for i, s, b, r, st in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2467_0_conservation", "Is J_M exactly conserved?", "ONLY_IF_STATIONARY_OR_EXCHANGE_DERIVED", "divergence reduces to clock strain on matter shell", "not a general theorem"),
        ("PV2467_1_scale", "Is ell_J parent-derived?", "NO", "dimension and candidate routes identified, no parent scale source", "scale gate blocked"),
        ("PV2467_2_worldtube", "Is worldtube mass surface-independent?", "CONDITIONAL", "closes in stationary compact-support collar, blocked dynamically", "local stationary route possible"),
        ("PV2467_3_Newton", "Is Newton limit derived?", "NO", "source bridge still lacks parent scale/exchange/stress closure", "no Newton claim"),
        ("PV2467_4_overall", "Overall 2467 verdict", "LOCAL_STATIONARY_CONTRACT_SHARPENED_DYNAMIC_CLOSURE_BLOCKED", "Hilbert current works in stationary-clock contract; full MTS/time dynamics need exchange current", "next target should split stationary theorem from dynamic exchange route"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": r, "evidence": e, "effect": eff} for i, q, r, e, eff in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2467_0_divergence_identity", "Divergence identity for J_M is derived.", "PASS_AS_DERIVATION", "product rule and matter-shell reduction written", True, False),
        ("GATE2467_1_stationary_contract", "Stationary local clock gives conserved source current.", "PASS_AS_CONDITIONAL_CONTRACT", "tau Killing makes clock-strain leakage vanish", True, False),
        ("GATE2467_2_dynamic_conservation", "Generic dynamic MTS clock source bridge closes.", "BLOCKED", "exchange current not parent-derived", False, False),
        ("GATE2467_3_parent_scale", "ell_J is parent-derived.", "BLOCKED", "only candidate scale routes exist", False, False),
        ("GATE2467_4_Newton_local_GR", "Newton/local-GR branch passes.", "BLOCKED", "stationary source contract is not full GR reduction", False, False),
        ("GATE2467_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2467_0_keep_hilbert", "Keep Hilbert current as primary source bridge.", "it gives exact conservation in stationary-clock collars and avoids fitted GM", "continue this route"),
        ("DEC2467_1_split_routes", "Split local stationary theorem from dynamic exchange closure.", "the stationary route is much closer to GR lab/PPN conditions; dynamic route needs extra machinery", "avoid overclaiming"),
        ("DEC2467_2_scale_block", "Do not promote ell_J.", "parent scale candidates are not sourced", "scale remains nonclaim"),
        ("DEC2467_3_next_target", "Next build the stationary local-source theorem and dynamic exchange ledger.", "this attacks the exact gap exposed by the divergence identity", "2468 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2467_0_selected",
            "selection_status": "selected",
            "target_file": "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
            "target_script": "scripts/Y5_R2FR_stationary_local_source_theorem_or_dynamic_exchange_current_2468.py",
            "task": "split the Hilbert-current route into a stationary local theorem and a dynamic clock-exchange route; try to prove local exterior q_loc=0 under stationary compact-source conditions without claiming full dynamic GR",
            "acceptance_target": "stationary theorem hypotheses, proof steps, dynamic exchange-current missing ledger, parent-scale status, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["clock_gate"], COPY_TARGETS["clock_gate_contract"])
    shutil.copyfile(OUTPUTS["scale_gate"], COPY_TARGETS["scale_gate_contract"])
    shutil.copyfile(OUTPUTS["worldtube_gate"], COPY_TARGETS["worldtube_gate_contract"])
    source_map = {
        "clock_gate_contract": OUTPUTS["clock_gate"],
        "scale_gate_contract": OUTPUTS["scale_gate"],
        "worldtube_gate_contract": OUTPUTS["worldtube_gate"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2467_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2467_01_divergence_derived", any(row["identity_id"] == "DIV2467_1_full_divergence" and row["status"] == "PASS_DERIVED" for row in data["divergence"]), "full divergence identity derived")
    add("VAL2467_02_killing_condition", any(row["clock_id"] == "CLK2467_0_stationary_gate" and row["status"] == "CONDITIONAL_PASS" for row in data["clock"]), "stationary/Killing clock condition recorded")
    add("VAL2467_03_scale_blocked", any(row["scale_id"] == "SCL2467_5_current_status" and row["status"] == "MISSING_PARENT_SCALE" for row in data["scale"]), "parent scale remains blocked")
    add("VAL2467_04_exchange_missing", any(row["exchange_id"] == "EXC2467_0_required_identity" and row["status"] == "REQUIRED_NOT_DERIVED" for row in data["exchange"]), "dynamic exchange identity missing")
    add("VAL2467_05_worldtube_guardrail", any(row["worldtube_gate_id"] == "WTG2467_3_no_fitted_mass" and row["status"] == "PASS_GUARDRAIL" for row in data["worldtube"]), "fitted mass/GM guardrail retained")
    add("VAL2467_06_overall_nonclaim", any(row["verdict_id"] == "PV2467_4_overall" and row["result"] == "LOCAL_STATIONARY_CONTRACT_SHARPENED_DYNAMIC_CLOSURE_BLOCKED" for row in data["verdicts"]), "overall verdict is sharpened but nonclaim")
    add("VAL2467_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/Newton claim")
    add("VAL2467_08_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2467_0_selected", "2468 stationary/dynamic split selected")
    add("VAL2467_09_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2467-Y5", "P8_Y5_HILBERT_CURRENT_2467", "P8_Y5_BRR545_2467", "JR2467")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2467_10_no_formalization_artifacts", not formal_hits, "no 2467 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2467_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2467_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2467_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2467_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2467_OVERALL", all(row["status"] == "PASS" for row in rows), "2467 derives Hilbert-current conservation conditions and selects stationary/dynamic split without claiming local GR")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2467 Y5 R2FR Hilbert-current Conservation Scale And Clock Compatibility Gate",
        "",
        "**Status:** conservation identity derived, source bridge not fully closed. For `J_M^nu=ell_J T^{nu rho}tau_rho`, the divergence is exactly controlled by parent-scale gradients, matter stress conservation, and clock strain. In stationary local collars the Hilbert current can be conserved; in generic dynamic MTS clocks it needs a parent-derived exchange current.",
        "",
        "**Main result:** this route is not dead. It gives a clean stationary/local theorem target: if `ell_J` is fixed, `tau` is Killing or locally stationary, matter stress is conserved, and source support is compact, then the worldtube current is surface-independent and `q_loc=P_loc J_M` vanishes outside the source. But full dynamic closure is still blocked by the missing clock-exchange identity and parent scale.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Divergence Identity",
        markdown_table(data["divergence"], ["identity_id", "statement", "basis", "result", "status"]),
        "",
        "## Clock Compatibility Gate",
        markdown_table(data["clock"], ["clock_id", "gate", "condition", "effect", "status"]),
        "",
        "## Parent Scale Options",
        markdown_table(data["scale"], ["scale_id", "scale_clause", "reason", "status"]),
        "",
        "## Exchange Current Identity",
        markdown_table(data["exchange"], ["exchange_id", "identity", "basis", "result", "status"]),
        "",
        "## Worldtube Surface Gate",
        markdown_table(data["worldtube"], ["worldtube_gate_id", "statement", "basis", "result", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
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
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register(),
        "divergence": divergence_identity_rows(),
        "clock": clock_gate_rows(),
        "scale": scale_gate_rows(),
        "exchange": exchange_identity_rows(),
        "worldtube": worldtube_gate_rows(),
        "verdicts": promotion_verdict_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["divergence_identity"], data["divergence"])
    write_csv(OUTPUTS["clock_gate"], data["clock"])
    write_csv(OUTPUTS["scale_gate"], data["scale"])
    write_csv(OUTPUTS["exchange_identity"], data["exchange"])
    write_csv(OUTPUTS["worldtube_gate"], data["worldtube"])
    write_csv(OUTPUTS["promotion_verdict"], data["verdicts"])
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
