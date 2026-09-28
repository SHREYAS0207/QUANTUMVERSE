from app.qlearn.quantum_math import apply_h_zero, bell_state
def test_h_zero_probs():
    r=apply_h_zero(); assert r['probabilities']['0']==0.5 and r['probabilities']['1']==0.5
def test_bell_probs():
    r=bell_state(); assert r['probabilities']['00']==0.5 and r['probabilities']['11']==0.5
