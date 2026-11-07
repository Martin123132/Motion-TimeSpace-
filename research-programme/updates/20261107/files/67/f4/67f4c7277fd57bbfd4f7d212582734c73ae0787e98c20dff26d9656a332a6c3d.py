from join_common import *


def main():
    modest()
    folder=ROOT/'results/identities'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for upper in UPPERS:
        window=lambda frequency:matching_weight(frequency,upper)
        base_edges=[2e-5,4e-5,.01,upper]
        for ratio in [.87,1.,1.13]:
            full_edges=sorted(set(base_edges+[value/ratio for value in base_edges]))
            frequency,measure=log_rule(full_edges,64)
            central,weights=log_rule(base_edges,64)
            for h_degree in [0,1,2]:
                history=lambda points:(points/upper)**h_degree
                for degree in [1,2,3]:
                    potential=lambda points:(points/upper)**degree
                    delta_potential=potential(ratio*frequency)-potential(frequency)
                    delta_history=history(ratio*frequency)-history(frequency)
                    delta_window=window(ratio*frequency)-window(frequency)
                    average_history=(history(ratio*frequency)+history(frequency))/2
                    average_window=(window(ratio*frequency)+window(frequency))/2
                    bulk=-np.sum(measure*delta_potential*average_window*delta_history)/(2*I3*ratio)
                    joining=-np.sum(measure*delta_potential*average_history*delta_window)/(2*I3*ratio)
                    total=-np.sum(measure*delta_potential*(window(ratio*frequency)*history(ratio*frequency)-window(frequency)*history(frequency)))/(2*I3*ratio)
                    forward=potential(ratio*central)-potential(central)
                    backward=potential(central/ratio)-potential(central)
                    compact_bulk=-np.sum(weights*window(central)*(forward*(history(ratio*central)-history(central))+backward*(history(central/ratio)-history(central))/ratio))/(4*I3*ratio)
                    compact_join=np.sum(weights*window(central)*(forward*(history(ratio*central)+history(central))+backward*(history(central/ratio)+history(central))/ratio))/(4*I3*ratio)
                    scale=max(abs(bulk)+abs(joining)+abs(total),1e-300)
                    label=f'm{upper}r{ratio}h{h_degree}A{degree}'
                    checks.extend([check('Weak product:'+label,abs(bulk+joining-total)/scale,1e-8),
                        check('Independent compact bulk:'+label,abs(bulk-compact_bulk)/scale,1e-8),
                        check('Independent compact joining:'+label,abs(joining-compact_join)/scale,1e-8)])
                    if h_degree==0:
                        checks.append(check('Constant h has zero bulk:'+label,abs(bulk),1e-14))
                    rows.append(dict(upper=upper,ratio=ratio,h_degree=h_degree,test_degree=degree,
                        bulk=bulk,joining=joining,total=total,compact_bulk=compact_bulk,compact_join=compact_join))
    finish(folder,dict(checks=checks,rows=rows,window_fitted=False,join_term_discarded=False),__file__)
    print(json.dumps(dict(checks=len(checks),failures=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

