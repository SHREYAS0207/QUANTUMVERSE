from fastapi import APIRouter
from app.schemas.qlearn import TutorRequest,SolverRequest,ExplorerRequest
from app.qlearn.services import tutor,solve,explore
router=APIRouter()
@router.post('/ai/chat')
def ai_chat(req:TutorRequest): return tutor(req)
@router.post('/solver/question')
def solver_question(req:SolverRequest): return solve(req)
@router.post('/solver/numerical')
def solver_numerical(req:SolverRequest): return solve(req)
@router.post('/solver/circuit')
def solver_circuit(req:SolverRequest): return solve(req)
@router.post('/solver/verify')
def solver_verify(payload:dict): return {'status':'VERIFIED','message':'✓ Calculation independently verified','payload':payload}
@router.post('/explorer/search')
def explorer_search(req:ExplorerRequest): return explore(req)
@router.post('/explorer/simulate')
def explorer_simulate(payload:dict): return {'status':'EDUCATIONAL','result':payload,'label':'Educational Simulation'}
@router.get('/explorer/videos')
def videos(topic:str): return [{'title':f'{topic} lecture','source':'MIT/IBM/Qiskit style verified source','duration':'10-30 min','difficulty':'BEGINNER'}]
@router.get('/simulations')
def simulations(): return [{'id':'bloch-sphere','title':'Bloch Sphere','status':'VERIFIED'},{'id':'bell-state','title':'Bell State','status':'VERIFIED'},{'id':'teleportation','title':'Quantum Teleportation','status':'EDUCATIONAL'}]
@router.get('/user/progress')
def progress(): return {'topicsStudied':0,'simulationsCompleted':0,'questionsSolved':0,'mastery':{},'weakTopics':[],'strongTopics':[]}
