module MTSTwoField
use DarkEnergyInterface
use classes
use Interpolation
implicit none
private
type, extends(TDarkEnergyModel) :: TMTSTwoField
    real(dl) :: slow_mass_mpc = 0._dl
    real(dl) :: heavy_mass_mpc = 0._dl
    real(dl) :: heavy_fraction = 0._dl
    real(dl) :: heavy_exact_limit = 0.00028_dl
    real(dl) :: seed_scale = 1._dl
    real(dl) :: initial_time_factor = 1._dl
    real(dl) :: matching_scale = 0._dl
    real(dl) :: matching_density = 0._dl
    real(dl) :: matching_raw = 0._dl
    type(TCubicSpline) :: slow_phi, slow_phidot, heavy_phi, heavy_phidot
    type(TCubicSpline) :: heavy_logrho, heavy_w
    type(TCubicSpline) :: matching_delta, matching_momentum
contains
    procedure :: Init => MTS_Init
    procedure :: SetSlowTable => TMTSTwoField_SetSlowTable
    procedure :: SetHeavyTable => TMTSTwoField_SetHeavyTable
    procedure :: SetHeavyBackground => TMTSTwoField_SetHeavyBackground
    procedure :: FieldValues => MTS_FieldValues
    procedure :: BackgroundDensityAndPressure => MTS_Background
    procedure :: PerturbedStressEnergy => MTS_Stress
    procedure :: PerturbationEvolve => MTS_Evolve
    procedure :: SeedFromCold => MTS_Seed
    procedure :: Diagnostics => MTS_Diagnostics
    procedure :: SetMatching => TMTSTwoField_SetMatching
    procedure :: ApplyMatching => MTS_ApplyMatching
    procedure :: AveragedPressure => MTS_AveragedPressure
    procedure, nopass :: PythonClass => TMTSTwoField_PythonClass
    procedure, nopass :: SelfPointer => TMTSTwoField_SelfPointer
end type
public TMTSTwoField
contains

subroutine MTS_Init(this, State)
class(TMTSTwoField), intent(inout) :: this
class(TCAMBdata), intent(in), target :: State
this%is_cosmological_constant = .false.
this%num_perturb_equations = 2
if (this%heavy_fraction > 0) this%num_perturb_equations = 5
if (this%matching_scale > 0 .and. this%matching_density <= 0) error stop 'MTS matching requires positive density'
end subroutine

subroutine TMTSTwoField_SetMatching(this, modes, density, momentum, count)
class(TMTSTwoField) :: this
integer, intent(in) :: count
real(dl), intent(in) :: modes(count), density(count), momentum(count)
call this%matching_delta%Init(modes, density)
call this%matching_momentum%Init(modes, momentum)
end subroutine

subroutine MTS_ApplyMatching(this, y, a, k)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(inout) :: y(:)
real(dl), intent(in) :: a, k
real(dl) :: field, velocity, density, old_field, old_velocity
integer :: mode_index
if (y(5) /= 0) error stop 'MTS matching called more than once'
density = this%matching_density/a
if (this%matching_raw > 0.5_dl) then
    old_field = y(3)
    old_velocity = y(4)
    call this%FieldValues(a, field, velocity, .true.)
    y(3) = (velocity*old_velocity+(a*this%heavy_mass_mpc)**2*field*old_field)/density
    y(4) = k*velocity*old_field/density
else
    do mode_index = 1, size(this%matching_delta%X)
        if (abs(k/this%matching_delta%X(mode_index)-1) < 1.e-12_dl) then
            y(3) = this%matching_delta%F(mode_index)
            y(4) = this%matching_momentum%F(mode_index)
            y(5) = 1
            return
        end if
    end do
    error stop 'MTS mode has no sourced phase projection; interpolation not permitted'
end if
y(5) = 1
end subroutine

function MTS_AveragedPressure(this, a, k, hubble, density, momentum) result(pressure)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(in) :: a, k, hubble, density, momentum
real(dl) :: pressure, ratio, sound2
ratio = (k/(a*this%heavy_mass_mpc))**2
sound2 = ratio/(sqrt(1+ratio)+1)**2
pressure = sound2*(density+3*hubble*momentum/k)
end function

subroutine TMTSTwoField_SetSlowTable(this, loga, field, velocity, count)
class(TMTSTwoField) :: this
integer, intent(in) :: count
real(dl), intent(in) :: loga(count), field(count), velocity(count)
call this%slow_phi%Init(loga, field)
call this%slow_phidot%Init(loga, velocity)
end subroutine

subroutine TMTSTwoField_SetHeavyTable(this, loga, field, velocity, count)
class(TMTSTwoField) :: this
integer, intent(in) :: count
real(dl), intent(in) :: loga(count), field(count), velocity(count)
call this%heavy_phi%Init(loga, field)
call this%heavy_phidot%Init(loga, velocity)
end subroutine

subroutine TMTSTwoField_SetHeavyBackground(this, loga, logrho, pressure_ratio, count)
class(TMTSTwoField) :: this
integer, intent(in) :: count
real(dl), intent(in) :: loga(count), logrho(count), pressure_ratio(count)
call this%heavy_logrho%Init(loga, logrho)
call this%heavy_w%Init(loga, pressure_ratio)
end subroutine

subroutine MTS_FieldValues(this, a, field, velocity, heavy)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(in) :: a
real(dl), intent(out) :: field, velocity
logical, intent(in) :: heavy
real(dl) :: loga, first
loga = log(max(a, 1.e-40_dl))
if (heavy) then
    first = this%heavy_phi%X(1)
    if (loga < first) then
        field = this%heavy_phi%F(1)
        velocity = this%heavy_phidot%F(1)*exp(3*(loga-first))
    else
        field = this%heavy_phi%Value(loga)
        velocity = this%heavy_phidot%Value(loga)
    end if
else
    first = this%slow_phi%X(1)
    if (loga < first) then
        field = this%slow_phi%F(1)
        velocity = this%slow_phidot%F(1)*exp(3*(loga-first))
    else
        field = this%slow_phi%Value(min(loga, 0._dl))
        velocity = this%slow_phidot%Value(min(loga, 0._dl))
    end if
end if
end subroutine

subroutine MTS_Background(this, grhov, a, grhov_t, w)
class(TMTSTwoField), intent(inout) :: this
real(dl), intent(in) :: grhov, a
real(dl), intent(out) :: grhov_t
real(dl), optional, intent(out) :: w
real(dl) :: field, velocity, density, pressure, loga
call this%FieldValues(a, field, velocity, .false.)
grhov_t = (velocity**2+(a*this%slow_mass_mpc*field)**2)/2
pressure = (velocity**2-(a*this%slow_mass_mpc*field)**2)/2
if (this%heavy_fraction > 0) then
    if (this%matching_scale > 0 .and. a >= this%matching_scale) then
        density = this%matching_density/a
    else if (a <= this%heavy_exact_limit) then
        call this%FieldValues(a, field, velocity, .true.)
        density = (velocity**2+(a*this%heavy_mass_mpc*field)**2)/2
        pressure = pressure+(velocity**2-(a*this%heavy_mass_mpc*field)**2)/2
    else
        loga = min(log(a), 0._dl)
        density = a**2*exp(this%heavy_logrho%Value(loga))
        pressure = pressure+density*this%heavy_w%Value(loga)
    end if
    grhov_t = grhov_t+density
end if
if (present(w)) w = pressure/grhov_t
end subroutine

subroutine MTS_Stress(this, dgrhoe, dgqe, a, dgq, dgrho, grho, grhov_t, w, &
    gpres_noDE, etak, adotoa, k, kf1, ay, ayprime, w_ix)
class(TMTSTwoField), intent(inout) :: this
real(dl), intent(out) :: dgrhoe, dgqe
real(dl), intent(in) :: a, dgq, dgrho, grho, grhov_t, w, gpres_noDE, etak, adotoa, k, kf1
real(dl), intent(in) :: ay(*)
real(dl), intent(inout) :: ayprime(*)
integer, intent(in) :: w_ix
real(dl) :: field, velocity
call this%FieldValues(a, field, velocity, .false.)
dgrhoe = velocity*ay(w_ix+1)+a**2*this%slow_mass_mpc**2*field*ay(w_ix)
dgqe = k*velocity*ay(w_ix)
if (this%heavy_fraction > 0) then
    if (ay(w_ix+4) > 0.5_dl) then
        dgrhoe = dgrhoe+this%matching_density/a*ay(w_ix+2)
        dgqe = dgqe+this%matching_density/a*ay(w_ix+3)
    else
        if (a > this%heavy_exact_limit) error stop 'MTS exact domain exceeded before matching'
        call this%FieldValues(a, field, velocity, .true.)
        dgrhoe = dgrhoe+velocity*ay(w_ix+3)+a**2*this%heavy_mass_mpc**2*field*ay(w_ix+2)
        dgqe = dgqe+k*velocity*ay(w_ix+2)
    end if
end if
end subroutine

subroutine MTS_Evolve(this, ayprime, w, w_ix, a, adotoa, k, z, y)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(inout) :: ayprime(:)
real(dl), intent(in) :: a, adotoa, k, z, y(:), w
integer, intent(in) :: w_ix
real(dl) :: field, velocity, pressure
call this%FieldValues(a, field, velocity, .false.)
ayprime(w_ix) = y(w_ix+1)
ayprime(w_ix+1) = -2*adotoa*y(w_ix+1)-k*z*velocity &
    -(k**2+(a*this%slow_mass_mpc)**2)*y(w_ix)
if (this%heavy_fraction > 0) then
    ayprime(w_ix+4) = 0
    if (y(w_ix+4) > 0.5_dl) then
        pressure = this%AveragedPressure(a, k, adotoa, y(w_ix+2), y(w_ix+3))
        ayprime(w_ix+2) = -3*adotoa*pressure-k*y(w_ix+3)-k*z
        ayprime(w_ix+3) = -adotoa*y(w_ix+3)+k*pressure
    else
        if (a > this%heavy_exact_limit) error stop 'MTS exact domain exceeded before matching'
        call this%FieldValues(a, field, velocity, .true.)
        ayprime(w_ix+2) = y(w_ix+3)
        ayprime(w_ix+3) = -2*adotoa*y(w_ix+3)-k*z*velocity &
            -(k**2+(a*this%heavy_mass_mpc)**2)*y(w_ix+2)
    end if
end if
end subroutine

subroutine MTS_Seed(this, y, a, tau, cold)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(out) :: y(:)
real(dl), intent(in) :: a, tau, cold
real(dl) :: field, velocity
call this%FieldValues(a, field, velocity, .false.)
y(1) = -this%seed_scale*field*(a*this%slow_mass_mpc*tau)**2*cold/105
y(2) = 6*y(1)/tau
if (this%heavy_fraction > 0) then
    call this%FieldValues(a, field, velocity, .true.)
    y(3) = -this%seed_scale*field*(a*this%heavy_mass_mpc*tau)**2*cold/105
    y(4) = 6*y(3)/tau
    y(5) = 0
end if
end subroutine

subroutine MTS_Diagnostics(this, a, k, hubble, y, output)
class(TMTSTwoField), intent(in) :: this
real(dl), intent(in) :: a, k, hubble, y(:)
real(dl), intent(out) :: output(10)
real(dl) :: field, velocity, kinetic, potential
output = 0
call this%FieldValues(a, field, velocity, .false.)
kinetic = velocity*y(2)
potential = (a*this%slow_mass_mpc)**2*field*y(1)
output(1:5) = [y(1), y(2), kinetic+potential, kinetic-potential, k*velocity*y(1)]
if (this%heavy_fraction > 0) then
    if (y(5) > 0.5_dl) then
        output(8) = this%matching_density/a*y(3)
        output(9) = this%matching_density/a*this%AveragedPressure(a, k, hubble, y(3), y(4))
        output(10) = this%matching_density/a*y(4)
    else
        call this%FieldValues(a, field, velocity, .true.)
        kinetic = velocity*y(4)
        potential = (a*this%heavy_mass_mpc)**2*field*y(3)
        output(6:10) = [y(3), y(4), kinetic+potential, kinetic-potential, k*velocity*y(3)]
    end if
end if
end subroutine

function TMTSTwoField_PythonClass() result(name)
character(len=:), allocatable :: name
name = 'MTSTwoField'
end function

subroutine TMTSTwoField_SelfPointer(cptr, P)
use iso_c_binding
type(c_ptr) :: cptr
type(TMTSTwoField), pointer :: native
class(TPythonInterfacedClass), pointer :: P
call c_f_pointer(cptr, native)
P => native
end subroutine
end module MTSTwoField
