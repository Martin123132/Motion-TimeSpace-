from soft_population import *


def main():
    modest()
    for theta in [1e-6,1e-5,.00014534465573404461,.00045962015785263325]:
        value,gaunt=coefficient(theta,4,4,8)
        print(json.dumps(dict(theta=theta,coefficient=value,gaunt=gaunt,first_order_slope=(1-gaunt)/theta,
                              inherited_approximation=1/(1+14.16*theta))),flush=True)


if __name__=='__main__':
    main()
