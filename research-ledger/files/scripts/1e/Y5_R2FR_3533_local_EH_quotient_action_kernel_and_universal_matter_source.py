from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3533-Y5-R2FR-local-EH-quotient-action-kernel-and-universal-matter-source.md"
CANONICAL_STATUS = OUT / "P8_local_GR_EH_quotient_action_kernel_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3533": {"path": Path(__file__).resolve(), "role": "3533 generator"},
    "doc_3532": {
        "path": ROOT / "3532-Y5-R2FR-PiM-Htau-commutator-integrability-zero-or-denominator-bound.md",
        "role": "3532 PiM/Htau zero mechanism handoff",
    },
    "status_3532": {
        "path": OUT / "P8_local_GR_PiM_Htau_zero_mechanism_status.csv",
        "role": "3532 canonical PiM/Htau status",
    },
    "next_3532": {
        "path": OUT / "P8_Y5_R2FR_3532_NEXT_TARGET.csv",
        "role": "3532-selected local EH quotient target",
    },
    "zero_contract_3532": {
        "path": OUT / "P8_Y5_R2FR_3532_ZERO_CONTRACT.csv",
        "role": "3532 zero contract rows",
    },
    "zero_proof_3532": {
        "path": OUT / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "role": "3532 PiM/Htau zero proof attempt",
    },
    "min_local_gr_blocks": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "minimal parent local-GR action blocks",
    },
    "min_local_gr_chain": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "role": "minimal parent local-GR derived chain",
    },
    "symbol_to_gr_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "MTS symbol to local-GR action map",
    },
    "constant_kappa_contract": {
        "path": OUT / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "same-frame kappa/G contract",
    },
    "constant_sector_contract": {
        "path": OUT / "P8_constant_sector_universality_CONTRACT.csv",
        "role": "universal constant-sector contract",
    },
    "hilbert_worldtube_contract": {
        "path": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "role": "Hilbert/worldtube parent action contract",
    },
    "charge_current_direct": {
        "path": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "charge-current equality direct attempt",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical residual bounds",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def action_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "LAK3533_0_quotient_fields",
            "block": "observed quotient fields",
            "action_clause": "Define a parent quotient q(Phi)=(g_obs,tau_obs,orientation,units) plus a local-silent multiplet Y^A for motion/time/domain/memory/range/source-selector deviations.",
            "mathematical_form": "Phi -> (g_obs,Y^A); g_readout=g_obs+O(Y^2); tau_readout=tau_obs+O(Y^2)",
            "purpose": "separate the GR readout from extra MTS structure without allowing first-order local leakage",
            "not_smuggled_guard": "requires an actual MTS variable map in 3534; this row is only the kernel shape",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_1_EH_core",
            "block": "EH local spin-2 core",
            "action_clause": "Use the Einstein-Hilbert operator as the compact local low-energy metric branch with calibrated kappa0/G_ref.",
            "mathematical_form": "S_EH=(2 kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "purpose": "inherit the standard Hamiltonian constraint and Poisson source coefficient",
            "not_smuggled_guard": "G_ref is calibrated/integration-constant level; this does not derive G from pure MTS",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_2_universal_matter",
            "block": "universal matter source",
            "action_clause": "Matter couples to g_obs only at leading local order; no species-dependent direct coupling to Y^A.",
            "mathematical_form": "S_matter=S_matter[g_obs,psi]; partial S_matter/partial Y^A|_{g_obs,psi,Y=0}=0",
            "purpose": "derive same Hilbert source for WEP, clocks, orbital readout and Poisson",
            "not_smuggled_guard": "must be derived from parent quotient/matter rule, not imposed separately per species",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_3_silent_Y_fixed_point",
            "block": "extra-sector fixed point",
            "action_clause": "The local compact branch has Y^A=0 as a stable stationary point with positive quadratic operator and no source-linear forcing.",
            "mathematical_form": "S_Y=int sqrt(-g)[-1/2 G_AB(Y) grad Y^A grad Y^B - 1/2 M^2_AB Y^A Y^B + O(Y^3)]",
            "purpose": "make motion/time/domain/memory/range fields silent locally without deleting them cosmologically",
            "not_smuggled_guard": "3534 must show actual MTS fields enter this Y^A multiplet with M^2_AB positive or bounded",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_4_double_zero_couplings",
            "block": "double-zero non-EH/source couplings",
            "action_clause": "Every local non-EH/source-normalization operator has coefficient that starts at quadratic order in Y.",
            "mathematical_form": "C_i(Y)=1/2 C_i,AB Y^A Y^B+O(Y^3); C_i(0)=0; partial_A C_i(0)=0",
            "purpose": "prevents fifth-force, PPN, source-charge and clock residuals at linear local order",
            "not_smuggled_guard": "must come from symmetry/topological/norm-square origin, not hand-set coefficients",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_5_boundary_no_flux",
            "block": "boundary/reference/no-flux",
            "action_clause": "Use GHY/EH boundary terms plus fixed reference subtraction; impose local no-flux for Y on compact exterior boundaries.",
            "mathematical_form": "S_boundary=S_GHY[g_obs]+B_ref+O(Y^2); integral_boundary i_tau omega_Y=0 at Y=delta Y=0",
            "purpose": "make H_tau integrable and stop hidden boundary mass leakage",
            "not_smuggled_guard": "requires parent-owned worldtube/reference selector, not a fitted surface choice",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "LAK3533_6_charge_identified_source",
            "block": "charge-identified source denominator",
            "action_clause": "Define M_H_ref from the same EH/Hilbert Hamiltonian charge and Hilbert source integral before orbital fitting.",
            "mathematical_form": "M_H_ref=c^-2(H_tau-H_ref)=int_W rho_H dV_H; mu_obs=G_ref M_H_ref(1+epsilon_mu)",
            "purpose": "kills the fitted-GM loophole and gives R_PiM an actual owner",
            "not_smuggled_guard": "epsilon_mu remains a residual unless charge equality is derived",
            "valid_for_claim": "False",
        },
    ]


def euler_zero_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "EZT3533_0_metric_variation",
            "target": "metric equation",
            "derivation": "Vary g_obs at Y=0 with C_i(0)=partial_A C_i(0)=0 and no linear readout coupling.",
            "result": "G_mn+Lambda0 g_mn = kappa0 T_mn^matter + O(Y^2)+boundary_residuals",
            "if_passes": "local Einstein equation is inherited at leading order",
            "current_status": "KERNEL_SUFFICIENT_NOT_MTS_MAPPED",
            "valid_for_claim": "False",
        },
        {
            "test_id": "EZT3533_1_Y_variation",
            "target": "extra-field equation",
            "derivation": "Vary Y^A around the compact local branch.",
            "result": "(Box delta^A_B - M^2_AB)Y^B = source_i partial_A C_i(0) + O(Y^2); source term vanishes if partial_A C_i(0)=0",
            "if_passes": "Y=0 is a consistent local solution rather than an imposed plateau",
            "current_status": "KERNEL_SUFFICIENT_NEEDS_DOUBLE_ZERO_ORIGIN",
            "valid_for_claim": "False",
        },
        {
            "test_id": "EZT3533_2_matter_variation",
            "target": "Hilbert source and WEP",
            "derivation": "Vary matter fields with S_matter[g_obs,psi] and no Y species vertices.",
            "result": "T_H is the single matter source; nabla_mu T^{mu nu}=0 follows from diffeo invariance on the g_obs branch",
            "if_passes": "R_md and source-charge WEP are routed to zero",
            "current_status": "KERNEL_SUFFICIENT_NEEDS_PARENT_MATTER_RULE",
            "valid_for_claim": "False",
        },
        {
            "test_id": "EZT3533_3_PiM_commutator",
            "target": "R_PiM",
            "derivation": "At Y=0, Pi_M is the charge-identified Hilbert mass functional of g_obs, tau_obs and J_H.",
            "result": "[D_Y,Pi_M^H]J_H=0 because D_Y g_obs=D_Y tau_obs=D_Y J_H=0 at fixed quotient",
            "if_passes": "3532 R_PiM zero mechanism becomes live",
            "current_status": "CONDITIONAL_ZERO_IF_KERNEL_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "test_id": "EZT3533_4_Htau_integrability",
            "target": "R_Htau",
            "derivation": "At Y=0, extra symplectic flux is quadratic/zero and EH time generator has the usual integrability conditions.",
            "result": "curl(delta H_tau)=integral_boundary i_tau omega_EH + O(Y delta Y)=0 under stationary/asymptotic/local no-flux conditions",
            "if_passes": "3532 R_Htau zero mechanism becomes live",
            "current_status": "CONDITIONAL_ZERO_IF_BOUNDARY_SELECTOR_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "test_id": "EZT3533_5_second_order_warning",
            "target": "PPN/local GR",
            "derivation": "Even after first-order zero, expand g_00, g_ij and g_0i through O(c^-4).",
            "result": "gamma-1, beta-1, alpha_i, zeta_i, xi remain explicit rows until second-order kernel is computed",
            "if_passes": "local GR can be promoted only after PPN residual vector is zero/bounded",
            "current_status": "NOT_REACHED",
            "valid_for_claim": "False",
        },
    ]


def implication_rows() -> list[dict[str, Any]]:
    return [
        {
            "implication_id": "IMP3533_0_3532_double_zero",
            "input_kernel_rows": "LAK3533_0;LAK3533_2;LAK3533_3;LAK3533_4;LAK3533_5;LAK3533_6",
            "derived_if_signed": "R_PiM=0 and R_Htau=0 on compact local branches",
            "observable_effect": "source denominator stops being a free local-GR closure",
            "current_status": "SUFFICIENT_ROUTE_ONLY",
            "valid_for_claim": "False",
        },
        {
            "implication_id": "IMP3533_1_Newton_first_order",
            "input_kernel_rows": "LAK3533_1;LAK3533_2;LAK3533_6 plus EZT3533_0",
            "derived_if_signed": "nabla^2 Phi=4*pi*G_ref rho_H + O(Y^2,boundary,PPN_residual)",
            "observable_effect": "Newtonian limit is inherited with calibrated G_ref and independently defined M_H_ref",
            "current_status": "CONDITIONAL_FIRST_ORDER",
            "valid_for_claim": "False",
        },
        {
            "implication_id": "IMP3533_2_no_direct_fifth_force",
            "input_kernel_rows": "LAK3533_3;LAK3533_4",
            "derived_if_signed": "no linear Y-mediated local fifth force or species-dependent source charge",
            "observable_effect": "R10/WEP/clock/PPN rows start at O(Y^2) or sourced coefficient rows",
            "current_status": "CONDITIONAL_DOUBLE_ZERO",
            "valid_for_claim": "False",
        },
        {
            "implication_id": "IMP3533_3_cosmology_not_deleted",
            "input_kernel_rows": "LAK3533_3",
            "derived_if_signed": "Y can be locally silent while still active on cosmological/galaxy domains if boundary/source conditions differ",
            "observable_effect": "keeps MTS from becoming merely GR everywhere by fiat",
            "current_status": "ROUTE_COMPATIBLE_BUT_UNPROVEN",
            "valid_for_claim": "False",
        },
    ]


def no_smuggling_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NSA3533_0_EH_core_admitted",
            "risk": "This kernel includes an EH core rather than deriving the spin-2 operator from first principles.",
            "why_not_fatal": "A fundamental framework may have GR as a derived/effective local quotient; the honest claim is local reduction, not derivation of EH from nothing.",
            "required_next": "map MTS variables to q(Phi)=g_obs and show the quotient action actually has this EH branch",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NSA3533_1_G_not_derived",
            "risk": "G_ref/kappa0 remains calibrated or integration-constant level.",
            "why_not_fatal": "GR also treats G as an empirical constant; MTS can still be competitive if it derives the residual structure and known limits.",
            "required_next": "keep G_ref separate from M_H_ref and never define mass from fitted GM",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NSA3533_2_matter_universality_strong",
            "risk": "Universal matter coupling can be an assumption disguised as a theorem.",
            "why_not_fatal": "It becomes a theorem if the quotient rule makes all local matter clocks and rods couple to g_obs only.",
            "required_next": "derive the matter quotient rule or keep WEP/source charge residual rows",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NSA3533_3_double_zero_must_have_origin",
            "risk": "Setting C_i(0)=partial_A C_i(0)=0 by hand is just closure language.",
            "why_not_fatal": "A norm-square, parity, topological, or quotient-invariance origin can force double zeros naturally.",
            "required_next": "test actual MTS variables for symmetry/topological/norm-square double-zero origin",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NSA3533_4_local_silence_not_global_silence",
            "risk": "Making Y silent locally could accidentally kill galaxy/cosmology mechanisms.",
            "why_not_fatal": "The kernel only requires compact local branch silence; Y can activate under cosmological boundary/source conditions.",
            "required_next": "state branch conditions separating compact local tests from cosmology/galaxies",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3533_0_kernel_viable",
            "decision": "The local EH quotient kernel is a viable derivation route.",
            "rationale": "It gives algebraic reasons for Pi_M/H_tau zeros and keeps G/GM calibration honest.",
            "effect": "move from pure bound ledgers to parent-action variable mapping",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3533_1_not_claim_ready",
            "decision": "Do not claim local GR/Newton pass from the kernel alone.",
            "rationale": "MTS variables are not yet mapped into Y^A and double-zero origins are not derived.",
            "effect": "status remains conditional despite stronger mechanism",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3533_2_next_map_variables",
            "decision": "Map actual MTS symbols into the quotient/fixed-point multiplet next.",
            "rationale": "The kernel only becomes MTS physics when q, Gamma, chi, psi/motion-time-space variables own the clauses.",
            "effect": "3534 should attack the true derivation rather than add more placeholders",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3533_0_kernel",
            "quantity": "local_EH_quotient_action_kernel",
            "value": "sufficient_route_constructed_not_parent_mapped",
            "meaning": "a compact local action structure that would derive the 3532 double zero has been written",
            "claim_effect": "no local-GR claim until MTS variables and double-zero origins are supplied",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3533_1_matter",
            "quantity": "universal_matter_source",
            "value": "required_clause_identified",
            "meaning": "matter universality is the hinge for WEP/source charge and Hilbert source normalization",
            "claim_effect": "WEP/source residuals remain live",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3533_2_next",
            "quantity": "next_best_target",
            "value": "MTS_variable_to_Y_multiplet_map_and_double_zero_origin",
            "meaning": "the next derivation must tie the kernel to actual MTS symbols instead of abstract Y fields",
            "claim_effect": "routes toward derived local GR",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3534-Y5-R2FR-MTS-variable-to-local-EH-quotient-map-and-double-zero-origin.md",
            "next_script": "scripts/Y5_R2FR_3534_MTS_variable_to_local_EH_quotient_map_and_double_zero_origin.py",
            "objective": "Map actual MTS variables into g_obs and the silent Y^A multiplet, then test whether double-zero couplings follow from quotient invariance, norm-square structure, parity, topology, or branch support.",
            "success_gate": "Every local residual channel gets either a parent-derived double zero C_i(0)=dC_i(0)=0 or an explicit fallback coefficient row with bounds.",
            "why_next": "3533 supplies the action kernel; now the kernel must be owned by MTS variables rather than abstract placeholders.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    implications: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3533_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    kernel_ids = {row["kernel_id"] for row in kernel}
    checks.append({"check_id": "VAL3533_1_kernel_blocks_present", "passed": bool_text({"LAK3533_1_EH_core", "LAK3533_2_universal_matter", "LAK3533_3_silent_Y_fixed_point", "LAK3533_4_double_zero_couplings"} <= kernel_ids), "detail": "EH, matter, silent-Y and double-zero kernel blocks present", "valid_for_claim": "False"})
    test_ids = {row["test_id"] for row in tests}
    checks.append({"check_id": "VAL3533_2_euler_tests_present", "passed": bool_text({"EZT3533_0_metric_variation", "EZT3533_1_Y_variation", "EZT3533_3_PiM_commutator", "EZT3533_4_Htau_integrability"} <= test_ids), "detail": "metric, Y, PiM and Htau derivation tests present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_3_3532_implication_present", "passed": bool_text(any(row["implication_id"] == "IMP3533_0_3532_double_zero" for row in implications)), "detail": "kernel explicitly implies 3532 double-zero if signed", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_4_no_smuggling_audit_present", "passed": bool_text({"NSA3533_0_EH_core_admitted", "NSA3533_1_G_not_derived", "NSA3533_3_double_zero_must_have_origin"} <= {row["audit_id"] for row in audit}), "detail": "EH/G/double-zero honesty audit present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_5_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + kernel + tests + implications + status) and all(row["claim_allowed"] == "False" for row in audit + decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3534-Y5-R2FR-MTS-variable")), "detail": "3534 MTS variable-to-quotient map target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3533_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3533_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3533_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    implications: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3533 - Local EH Quotient Action Kernel And Universal Matter Source

## Summary
- **Leap taken:** wrote the minimal local action kernel that would make the 3532 `R_PiM/R_Htau` double zero happen for a reason.
- **Kernel:** `S_parent -> S_EH[g_obs] + S_matter[g_obs,psi] + S_Y[Y] + sum_i C_i(Y) O_i[g_obs,psi] + dB`.
- **Critical condition:** `C_i(0)=0` and `partial_A C_i(0)=0`; local non-GR couplings must be double-zero, not merely small.
- **Current verdict:** viable route, not a claim. The kernel is sufficient but not yet mapped to actual MTS variables.
- **Best next move:** map `q/Gamma/chi/psi` or the motion-time-space variables into `g_obs` and `Y^A`, then hunt the double-zero origin.

## Action Kernel In One Line
`S_parent = S_EH[g_obs;kappa0] + S_matter[g_obs,psi] + S_Y[Y] + sum_i C_i(Y) O_i[g_obs,psi] + S_boundary`

with

`Y=0`, `C_i(0)=0`, `partial_A C_i(0)=0`, `g_readout=g_obs+O(Y^2)`, and `delta H_tau^Y=0`.

Then local GR/Newton is not inserted as a plateau axiom; it is the quotient/fixed-point branch of the parent action. That is the good path, provided MTS can own the quotient and the double zeros.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Action Kernel
{markdown_table(kernel, ["kernel_id", "block", "action_clause", "mathematical_form", "purpose", "not_smuggled_guard", "valid_for_claim"])}

## Euler Zero Tests
{markdown_table(tests, ["test_id", "target", "derivation", "result", "if_passes", "current_status", "valid_for_claim"])}

## Implications
{markdown_table(implications, ["implication_id", "input_kernel_rows", "derived_if_signed", "observable_effect", "current_status", "valid_for_claim"])}

## No-Smuggling Audit
{markdown_table(audit, ["audit_id", "risk", "why_not_fatal", "required_next", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    kernel = action_kernel_rows()
    tests = euler_zero_test_rows()
    implications = implication_rows()
    audit = no_smuggling_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3533_SOURCE_REGISTER.csv",
        "action_kernel": OUT / "P8_Y5_R2FR_3533_ACTION_KERNEL.csv",
        "euler_zero_tests": OUT / "P8_Y5_R2FR_3533_EULER_ZERO_TESTS.csv",
        "implications": OUT / "P8_Y5_R2FR_3533_PIM_HTAU_IMPLICATIONS.csv",
        "no_smuggling_audit": OUT / "P8_Y5_R2FR_3533_NO_SMUGGLING_AUDIT.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3533_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3533_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3533_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3533_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["action_kernel"], kernel, ["kernel_id", "block", "action_clause", "mathematical_form", "purpose", "not_smuggled_guard", "valid_for_claim"])
    write_csv(outputs["euler_zero_tests"], tests, ["test_id", "target", "derivation", "result", "if_passes", "current_status", "valid_for_claim"])
    write_csv(outputs["implications"], implications, ["implication_id", "input_kernel_rows", "derived_if_signed", "observable_effect", "current_status", "valid_for_claim"])
    write_csv(outputs["no_smuggling_audit"], audit, ["audit_id", "risk", "why_not_fatal", "required_next", "claim_allowed"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, kernel, tests, implications, audit, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, kernel, tests, implications, audit, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
