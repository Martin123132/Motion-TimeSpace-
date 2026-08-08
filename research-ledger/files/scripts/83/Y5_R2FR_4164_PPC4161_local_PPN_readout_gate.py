from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4164"
BRANCH_ID = "MTS_R2FR_Y5_PPC4161_LOCAL_PPN_READOUT_GATE_4164"
DECISION = "PPC4161_LOCAL_PPN_RESIDUAL_VECTOR_DERIVED_PUBLIC_LOCAL_GR_CLAIM_STILL_BLOCKED"
DOC_PATH = POST / "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md"
NEXT_TARGET = "4165-Y5-R2FR-kappa-G-normalization-superselection-or-coupling-derivation.md"

SOURCES = {
    "SRC4164_00_4161_packet": (
        POST / "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md",
        "S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+S_GK+B_proper+S_top+S_vertical+S_reset",
        "4161 private packet adoption.",
    ),
    "SRC4164_01_formal_180": (
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        "local PPN readout gate for `gamma`, `beta`, `alpha_i`, `xi`, `zeta_i`, and `Gdot/G`",
        "Formal bridge says PPN gate is still required.",
    ),
    "SRC4164_02_claims": (
        FORMAL / "02-claims-register.csv",
        "L-005,local_gravity,PPC4161",
        "Claims register has PPC4161 nonclaim row.",
    ),
    "SRC4164_03_spine": (
        FORMAL / "07-unification-spine.md",
        "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md",
        "Main spine names 4164 as next local-GR gate.",
    ),
    "SRC4164_04_handoff": (
        SOURCE_DIR / "P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF.csv",
        "gamma=1 under PPC4161",
        "4163 PPN handoff rows.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def clause_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "clause_id": "C4164_0_EH_operator",
            "clause": "The 2PN bulk metric operator is the Einstein-Hilbert operator for g_obs.",
            "source_basis": "S_EH[g_obs;kappa_*] in PPC4161",
            "private_packet_status": "signed_inside_PPC4161",
            "if_rejected": "activate epsilon_EH and do not infer gamma=beta=1",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_1_kappa_normalization",
            "clause": "kappa_* is fixed and locally read as 8*pi*G_N/c^4, not drifting through time or environment.",
            "source_basis": "fixed local G_ref/kappa branch in PPC4161",
            "private_packet_status": "conditional_private_normalization_not_G_prediction",
            "if_rejected": "activate epsilon_kappa and Gdot/G residual",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_2_matter_minimal_same_source",
            "clause": "Matter follows one Hilbert stress tensor from S_matter[psi,g_obs,theta] and the same source charge used in the Newton kernel.",
            "source_basis": "same-source matter Hilbert current in 4161",
            "private_packet_status": "signed_inside_PPC4161",
            "if_rejected": "activate epsilon_matter, zeta_i and WEP/source-mismatch residuals",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_3_EM_stress_owner",
            "clause": "S_EM[A,g_obs] is the unique Maxwell-Hodge EM stress owner and bound/radiative EM stress is counted once.",
            "source_basis": "unique minimal EM owner in 4161",
            "private_packet_status": "signed_inside_PPC4161_for_local_packet",
            "if_rejected": "activate epsilon_EM and possible stress-nonconservation residuals",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_4_extra_modes_silent",
            "clause": "S_GK, S_top, S_vertical, S_reset and B_proper have zero 2PN bulk projection or are pure boundary/topological/gauge terms.",
            "source_basis": "q-basic fixed domain/projector and hidden-charge silence from 4160-4161",
            "private_packet_status": "conditional_zero_inside_compact_local_branch",
            "if_rejected": "activate epsilon_extra and preferred-frame/location residuals",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_5_readout_gauge",
            "clause": "The observer readout uses one PPN gauge/frame/clock convention and does not hide unit or clock drift.",
            "source_basis": "same S/tau/frame/units clause from 4160 and 4161",
            "private_packet_status": "conditional_private_readout_clause",
            "if_rejected": "activate epsilon_tau and apparent gamma/beta/Gdot drift",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "C4164_6_local_collar_no_leak",
            "clause": "Cosmology/galaxy/open-memory gradients do not enter the compact local collar at 2PN order.",
            "source_basis": "formal 180 explicitly does not erase nonlocal sectors",
            "private_packet_status": "not_yet_global_only_local_collar_assumption",
            "if_rejected": "activate epsilon_cosmo_leak and preferred-location residual xi",
            "public_claim_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def derivation_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "gate_id": "PPN4164_0_field_equation",
            "step": "Vary the private packet with respect to g_obs.",
            "result": "G_mu_nu(g_obs)=kappa_* T_total_mu_nu + R_GK_mu_nu + R_top_mu_nu + R_vertical_mu_nu + R_reset_mu_nu + R_boundary_mu_nu",
            "needed_zero": "R_GK+R_top+R_vertical+R_reset+R_boundary vanish through 2PN bulk projection",
            "private_status": "conditional_derived_gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "PPN4164_1_normalize_GR",
            "step": "Normalize the coupling and total stress against the measured local Newton source.",
            "result": "E_mu_nu := G_mu_nu - 8*pi*G_N*T_total_mu_nu/c^4 = residual_tensor_mu_nu",
            "needed_zero": "epsilon_kappa=0 and same-source Hilbert/Hamiltonian charge",
            "private_status": "conditional_private_normalization",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "PPN4164_2_project_PPN",
            "step": "Project residual_tensor_mu_nu onto the standard PPN coefficient basis.",
            "result": "Delta p_A = <W_A,residual_tensor> + O(residual_tensor^2), A in {gamma,beta,alpha_i,xi,zeta_i,Gdot/G}",
            "needed_zero": "each projected residual coefficient vanishes or is source-bounded",
            "private_status": "new_residual_vector_defined",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "PPN4164_3_private_zero_theorem",
            "step": "Apply PPC4161 clauses to the projected residuals.",
            "result": "PPC4161 plus 2PN/readout/no-leak clauses implies R_PPN_private=(0,0,0,0,0,0,0,0,0,0,0)",
            "needed_zero": "all clause rows remain signed in the adopted parent packet",
            "private_status": "conditional_symbolic_zero_not_public_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[Dict[str, str]]:
    data = [
        (
            "gamma",
            "1",
            "Delta_gamma = gamma - 1",
            "spatial curvature per unit Newton potential",
            "epsilon_EH + epsilon_matter + epsilon_extra + epsilon_tau",
            "EH operator, same source charge, no scalar/disformal/vertical 2PN bulk residual",
        ),
        (
            "beta",
            "1",
            "Delta_beta = beta - 1",
            "nonlinear U^2 self-interaction",
            "epsilon_EH + epsilon_binding + epsilon_extra + epsilon_kappa",
            "EH self-interaction coefficient, binding stress counted once, fixed kappa_*",
        ),
        (
            "alpha1",
            "0",
            "Delta_alpha1 = alpha1",
            "preferred-frame velocity coupling",
            "epsilon_frame + epsilon_projector + epsilon_extra",
            "no local frame/projector drift and no independent vector mode",
        ),
        (
            "alpha2",
            "0",
            "Delta_alpha2 = alpha2",
            "preferred-frame spin/velocity anisotropy",
            "epsilon_frame + epsilon_projector + epsilon_extra",
            "same observer frame and no anisotropic q-basic residual",
        ),
        (
            "alpha3",
            "0",
            "Delta_alpha3 = alpha3",
            "momentum nonconservation/preferred-frame self acceleration",
            "epsilon_matter + epsilon_hidden_flux + epsilon_extra",
            "conserved total Hilbert stress and hidden flux silence",
        ),
        (
            "xi",
            "0",
            "Delta_xi = xi",
            "preferred-location or external-field coupling",
            "epsilon_cosmo_leak + epsilon_boundary + epsilon_extra",
            "compact local collar decouples from FLRW/galaxy/open-memory gradients at 2PN",
        ),
        (
            "zeta1",
            "0",
            "Delta_zeta1 = zeta1",
            "stress-energy conservation residual 1",
            "epsilon_matter + epsilon_hidden_flux",
            "same Hilbert stress source and no unbalanced pressure/current term",
        ),
        (
            "zeta2",
            "0",
            "Delta_zeta2 = zeta2",
            "stress-energy conservation residual 2",
            "epsilon_matter + epsilon_binding + epsilon_hidden_flux",
            "binding and matter stress are included once in T_total",
        ),
        (
            "zeta3",
            "0",
            "Delta_zeta3 = zeta3",
            "stress-energy conservation residual 3",
            "epsilon_EM + epsilon_hidden_flux",
            "EM stress owner is Maxwell-Hodge and counted once",
        ),
        (
            "zeta4",
            "0",
            "Delta_zeta4 = zeta4",
            "stress-energy conservation residual 4",
            "epsilon_pressure + epsilon_binding + epsilon_hidden_flux",
            "pressure/internal energy bookkeeping descends to the same g_obs stress tensor",
        ),
        (
            "Gdot_over_G",
            "0",
            "Delta_Gdot = dot(G_eff)/G_eff",
            "time drift of local gravitational coupling",
            "epsilon_kappa + epsilon_tau + epsilon_cosmo_leak",
            "kappa_* is locally superselected and clock/readout drift is absent",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for parameter, gr_value, residual_symbol, meaning, active_epsilons, zero_condition in data:
        rows.append(
            {
                **common(),
                "parameter": parameter,
                "gr_ppn_value": gr_value,
                "residual_symbol": residual_symbol,
                "meaning": meaning,
                "readout_law": f"{residual_symbol} = L_{parameter}[E_mu_nu_residual] + O(epsilon_PPN^2)",
                "active_epsilons_if_not_zero": active_epsilons,
                "PPC4161_zero_condition": zero_condition,
                "private_packet_result": "zero_if_all_clause_rows_pass",
                "public_claim_result": "not_claimed",
                "needs_empirical_bound": "True",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "theorem_id": "THM4164_0_private_PPN_zero",
            "statement": "If PPC4161 is adopted and its 2PN/readout/no-leak clauses hold, then the local PPN residual vector is zero relative to GR.",
            "formula": "R_PPN=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G)=0",
            "proof_status": "conditional_private_symbolic_derivation",
            "not_claim": "not a public local-GR theorem, not a numerical prediction of G, not an empirical PPN pass",
            "fallback": "epsilon_PPN <= C_kappa*epsilon_kappa + C_EH*epsilon_EH + C_m*epsilon_matter + C_EM*epsilon_EM + C_extra*epsilon_extra + C_B*epsilon_boundary + C_tau*epsilon_tau + C_cosmo*epsilon_cosmo_leak",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4164_0_private_only",
            "rule": "PPN zero is conditional on private PPC4161 adoption and cannot be advertised as a public local-GR pass.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4164_1_G_not_predicted",
            "rule": "kappa_* normalization to measured G_N is not a derivation of the numerical value of Newton's constant.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4164_2_empirical_pending",
            "rule": "PPN, clock, orbital, R10 and EM tests remain downstream until bound/source rows are real.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "private_PPN_residual_vector_derived": "True",
            "private_symbolic_R_PPN_zero_if_clauses_pass": "True",
            "public_local_gr_claimed": "False",
            "numerical_G_predicted": "False",
            "empirical_PPN_pass_claimed": "False",
            "fallback_epsilon_bound_defined": "True",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why_next": "The PPN vector now reduces to GR under PPC4161, but kappa_*/G_N is still a measured normalization rather than a parent-derived coupling.",
            "route_A": "derive kappa_* as a superselected coupling from the parent action or flow measure",
            "route_B": "if not derivable, mark G_N as an empirical calibration constant exactly as GR does",
            "must_not_do": "do not pretend the numerical value of G has been predicted",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4164 - PPC4161 Local PPN Readout Gate

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4163 synced the private PPC4161 local packet into the formal spine without making a public claim. 4164 now does the next real mathematical job: translate the packet into a local PPN residual vector.

This is not another target list. The derivation gate is:

```text
S_loc^{{<=2PN}} =
S_EH[g_obs;kappa_*]
+ S_matter[psi,g_obs,theta]
+ S_EM[A,g_obs]
+ S_binding
+ S_GK
+ B_proper
+ S_top
+ S_vertical
+ S_reset
```

Varying with respect to `g_obs` gives the effective local equation:

```text
G_mu_nu(g_obs)
= kappa_* T_total_mu_nu
+ R_GK_mu_nu
+ R_top_mu_nu
+ R_vertical_mu_nu
+ R_reset_mu_nu
+ R_boundary_mu_nu.
```

Normalize against the measured local Newton source:

```text
E_mu_nu := G_mu_nu - 8*pi*G_N*T_total_mu_nu/c^4.
```

Then the PPN deviations are projections of the residual tensor:

```text
Delta p_A = <W_A, E_mu_nu> + O(E^2),
A in {{gamma,beta,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G}}.
```

## Private PPN Theorem
If PPC4161 is adopted and its `<=2PN` readout clauses hold, then:

```text
R_PPN =
(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G)
= 0.
```

That is the actual leap: the local packet is now mapped onto the full standard local-GR PPN vector, not only the first-order Newton kernel.

## Fallback Bound
If any clause fails, the result demotes immediately to:

```text
epsilon_PPN
<= C_kappa epsilon_kappa
+ C_EH epsilon_EH
+ C_m epsilon_matter
+ C_EM epsilon_EM
+ C_extra epsilon_extra
+ C_B epsilon_boundary
+ C_tau epsilon_tau
+ C_cosmo epsilon_cosmo_leak.
```

So the branch no longer falls into vague failure. It either gives the GR PPN vector privately, or it gives a named residual vector to bound.

## Claim Firewall
- This is not a public local-GR theorem.
- This is not a prediction of the numerical value of `G`.
- This is not an empirical PPN pass.
- It is a private symbolic readout gate from PPC4161 to the standard PPN vector.

## Next Target
`{NEXT_TARGET}`

Reason: the next exposed coupling issue is `kappa_*`. Either MTS derives/superselects it from the parent action, or we explicitly treat `G_N` as a measured calibration constant in the same practical sense GR does.

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4164_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4164_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4164_CLAUSE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4164_CLAUSE_AUDIT.csv",
        "P8_Y5_R2FR_4164_DERIVATION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4164_DERIVATION_GATE.csv",
        "P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR.csv",
        "P8_Y5_R2FR_4164_THEOREM_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4164_THEOREM_STATUS.csv",
        "P8_Y5_R2FR_4164_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4164_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4164_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4164_STATUS.csv",
        "P8_Y5_R2FR_4164_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4164_NEXT_TARGET.csv",
    }


def validate(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    checks: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, details: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(passed),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = parse_csv(outputs["P8_Y5_R2FR_4164_SOURCE_REGISTER"])
    add(
        "VAL4164_0_sources",
        "all required source paths exist and contain required tokens",
        all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources),
        str(sources),
    )

    clauses = parse_csv(outputs["P8_Y5_R2FR_4164_CLAUSE_AUDIT"])
    add(
        "VAL4164_1_clauses",
        "clause audit covers EH, kappa, matter, EM, extra modes, readout and local collar",
        len(clauses) == 7 and all(row["valid_for_claim"] == "False" for row in clauses),
        str([row["clause_id"] for row in clauses]),
    )

    derivation = parse_csv(outputs["P8_Y5_R2FR_4164_DERIVATION_GATE"])
    derivation_text = "\n".join(",".join(row.values()) for row in derivation)
    add(
        "VAL4164_2_derivation",
        "derivation gate includes field equation, GR normalization, PPN projection and private zero theorem",
        all(token in derivation_text for token in ["G_mu_nu", "E_mu_nu", "Delta p_A", "R_PPN_private"]),
        derivation_text,
    )

    residuals = parse_csv(outputs["P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR"])
    expected = {"gamma", "beta", "alpha1", "alpha2", "alpha3", "xi", "zeta1", "zeta2", "zeta3", "zeta4", "Gdot_over_G"}
    add(
        "VAL4164_3_residual_vector",
        "PPN residual vector has all 11 local-GR entries and remains nonclaim",
        {row["parameter"] for row in residuals} == expected and all(row["valid_for_claim"] == "False" for row in residuals),
        str([row["parameter"] for row in residuals]),
    )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4164_THEOREM_STATUS"])
    add(
        "VAL4164_4_theorem",
        "theorem row states conditional private R_PPN zero and fallback epsilon bound",
        len(theorem) == 1 and "R_PPN" in theorem[0]["formula"] and "epsilon_PPN" in theorem[0]["fallback"] and theorem[0]["valid_for_claim"] == "False",
        str(theorem),
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4164_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add(
        "VAL4164_5_firewall",
        "firewall blocks public local-GR, G prediction and empirical PPN pass claims",
        all(token in firewall_text for token in ["public local-GR pass", "Newton's constant", "downstream"]),
        firewall_text,
    )

    status = parse_csv(outputs["P8_Y5_R2FR_4164_STATUS"])
    add(
        "VAL4164_6_status",
        "status records private residual vector and no public/local/empirical/G claim",
        len(status) == 1
        and status[0]["result"] == DECISION
        and status[0]["private_PPN_residual_vector_derived"] == "True"
        and status[0]["public_local_gr_claimed"] == "False"
        and status[0]["numerical_G_predicted"] == "False"
        and status[0]["empirical_PPN_pass_claimed"] == "False",
        str(status),
    )

    next_rows_loaded = parse_csv(outputs["P8_Y5_R2FR_4164_NEXT_TARGET"])
    add(
        "VAL4164_7_next",
        "next target moves to kappa/G normalization or coupling derivation",
        len(next_rows_loaded) == 1 and next_rows_loaded[0]["next_target"] == NEXT_TARGET and "G_N" in next_rows_loaded[0]["why_next"],
        str(next_rows_loaded),
    )

    doc_text = read_text(DOC_PATH)
    doc_tokens = [DECISION, "R_PPN", "epsilon_PPN", NEXT_TARGET, "not a prediction of the numerical value of `G`"]
    add(
        "VAL4164_8_doc",
        "checkpoint doc records theorem, fallback, firewall and next target",
        all(token in doc_text for token in doc_tokens),
        "doc tokens checked",
    )

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add(
        "VAL4164_9_no_claim_rows",
        "all generated evidence rows keep claim_allowed/valid_for_claim false",
        not claim_failures,
        str(claim_failures),
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_details = "compiled"
    except Exception as exc:
        compile_ok = False
        compile_details = repr(exc)
    finally:
        cache = SCRIPT_PATH.parent / "__pycache__"
        if cache.exists():
            shutil.rmtree(cache)
    add("VAL4164_10_compile", "generator script compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    add(
        "VAL4164_11_scope",
        "checkpoint writes only post-checkpoint outputs and reads formal sources",
        all(str(path).startswith(str(SOURCE_DIR)) for path in outputs.values()) and str(DOC_PATH).startswith(str(POST)),
        "output scope checked",
    )

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4164_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_CLAUSE_AUDIT"], clause_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_DERIVATION_GATE"], derivation_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_THEOREM_STATUS"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4164_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4164_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['details']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
