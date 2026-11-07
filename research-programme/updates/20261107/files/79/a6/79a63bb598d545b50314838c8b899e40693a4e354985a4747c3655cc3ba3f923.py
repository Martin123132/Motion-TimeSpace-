import sympy as sp


def verify():
    diagonal1,offdiag1,offdiag2,diagonal2=sp.symbols("m11 m12 m21 m22")
    matrix=sp.Matrix([[diagonal1,offdiag1],[offdiag2,diagonal2]])
    determinant=diagonal1*diagonal2-offdiag1*offdiag2
    inverse=sp.Matrix([[diagonal2,-offdiag1],[-offdiag2,diagonal1]])/determinant
    inverse_error=sp.simplify(matrix*inverse-sp.eye(2))
    change1,change2=sp.symbols("dc1 dc2")
    change=sp.Matrix([change1,change2])
    defect=sp.simplify(matrix*(inverse*change)-change)
    clock=sp.symbols("N",real=True)
    row=[sp.Function("q"+str(index))(clock) for index in range(3)]
    state=[sp.Function("Y"+str(index))(clock) for index in range(3)]
    primitive=sum(coefficient*value for coefficient,value in zip(row,state))
    chain=sp.simplify(sp.diff(primitive,clock)-sum(sp.diff(coefficient,clock)*value+coefficient*sp.diff(value,clock) for coefficient,value in zip(row,state)))
    slow,mean,rapid,representation,qrate=sp.symbols("S R0 Rosc DeltaR QN")
    full=slow+mean+rapid+representation-qrate
    remainder=rapid-qrate
    reduced=slow+mean+representation
    retained=sp.simplify(full-reduced-remainder)
    hubble,velocity,frequency,field,delta_field,delta_velocity,wave=sp.symbols("H v omega phi dd du k")
    field_rate,velocity_rate=sp.symbols("dN uN")
    density_actual=hubble*(velocity*(velocity_rate+delta_velocity)+frequency**2*field*(field_rate+delta_field))
    density_native=hubble*(velocity*velocity_rate+frequency**2*field*field_rate)
    density=sp.simplify(density_actual-density_native-hubble*(velocity*delta_velocity+frequency**2*field*delta_field))
    flux=sp.simplify(hubble*wave*velocity*(field_rate+delta_field)-hubble*wave*velocity*field_rate-hubble*wave*velocity*delta_field)
    identities=dict(inverse=str(inverse_error),defect=str(defect),row_chain=str(chain),retained_remainder=str(retained),
                    physical_density_rate=str(density),physical_current_rate=str(flux))
    passed=inverse_error==sp.zeros(2) and defect==sp.zeros(2,1) and all(value==0 for value in (chain,retained,density,flux))
    if not passed:
        raise ValueError("second transformation identities")
    return dict(passed=True,identities=identities,assumptions=["nonzero determinant of joint scalar block",
                "spectator derivatives unchanged when comparing full and reduced current-state systems",
                "declared differentiable background-only coefficient row"],
                scope="algebraic identities; numerical bounds and physical qualification tested separately")

