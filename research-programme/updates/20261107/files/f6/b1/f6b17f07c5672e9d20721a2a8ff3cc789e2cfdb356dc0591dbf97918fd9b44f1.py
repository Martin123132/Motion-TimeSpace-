from matched_feedback_common import *


def main():
    modest()
    folder=ROOT/'results/transport-attribution'
    folder.mkdir(parents=True,exist_ok=False)
    checks,inputs,models=[],[],{}
    for model in ['heavy','cold']:
        folders={'fine':'response-fine-q32-m40-n1024','coarse':'response-space-q32-m40-n1024',
            'profile_only':'response-space-fine-transport-n1024','transport_only':'response-fine-space-transport-n1024'}
        data={}
        for label,name in folders.items():
            path=ROOT/'results'/name/(model+'.npz')
            inputs.extend([path,path.parent/'status.json'])
            with np.load(path) as saved:
                data[label]={key:saved[key].copy() for key in ['physical_change','saved_potential','measure']}
        norm=lambda value:np.sqrt(np.sum(data['fine']['measure'][:,None]*value**2,axis=0))
        original=norm(data['fine']['saved_potential'])
        reference=norm(data['fine']['physical_change'])
        profile=data['profile_only']['physical_change']-data['fine']['physical_change']
        transport=data['transport_only']['physical_change']-data['fine']['physical_change']
        interaction=data['coarse']['physical_change']-data['profile_only']['physical_change']-data['transport_only']['physical_change']+data['fine']['physical_change']
        combined=data['coarse']['physical_change']-data['fine']['physical_change']
        pieces=[profile,transport,interaction]
        defect=float(np.max(norm(combined-sum(pieces))/original))
        bound=float(np.max((norm(combined)-sum(norm(value) for value in pieces))/original))
        checks.extend([dict(name='Two-factor transport/profile decomposition:'+model,value=defect,limit=1e-12,passed=defect<=1e-12),
            dict(name='No cancellation credit in uncertainty budget:'+model,value=bound,limit=1e-12,passed=bound<=1e-12)])
        models[model]={name:dict(over_saved_norm=(norm(value)/original).tolist(),over_fine_response=(norm(value)/reference).tolist())
            for name,value in [('profile_only',profile),('transport_only',transport),('interaction',interaction),('combined',combined)]}
    finish(folder,dict(checks=checks,models=models,no_new_parent_history=True,
        four_corner_operator_profile_swap=True,
        conclusion='The propagated net response must not be assigned continuum physical precision while parent-tail and compact Compton transport discretizations dominate it.'),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=models)),flush=True)


if __name__=='__main__':
    main()
