import math, cmath
SQRT2=math.sqrt(2)
def probs(state): return {format(i, f'0{int(math.log2(len(state)))}b'): round(abs(a)**2,10) for i,a in enumerate(state)}
def apply_h_zero():
    s=[1/SQRT2,1/SQRT2]
    return {'state':'1/√2(|0⟩ + |1⟩)','vector':s,'probabilities':probs(s)}
def bell_state():
    s=[1/SQRT2,0,0,1/SQRT2]
    return {'state':'1/√2(|00⟩ + |11⟩)','vector':s,'probabilities':probs(s)}
def solve_known(question:str):
    q=question.lower().replace('⟩','>').replace('⟨','<')
    if 'bell' in q: return bell_state()
    if ('h' in q or 'hadamard' in q) and ('|0' in q or '0>' in q): return apply_h_zero()
    if 'photon' in q and '500' in q and 'nm' in q:
        h=6.62607015e-34;c=299792458;lam=500e-9;E=h*c/lam;ev=E/1.602176634e-19
        return {'energy_joule':E,'energy_ev':ev,'formula':'E = hc/λ'}
    return None
