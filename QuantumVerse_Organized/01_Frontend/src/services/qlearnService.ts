import {TutorRequest,TutorResponse,SolverRequest,SolverResponse,ExplorerRequest,ExplorerResponse} from '@/types/qlearn';
const API=process.env.NEXT_PUBLIC_API_URL || '/api/v1';
const authHeaders = (): HeadersInit => {
	const token = typeof window !== 'undefined' ? localStorage.getItem('qv_token') : null;
	return token ? { Authorization: `Bearer ${token}` } : {};
};
async function post<T>(path:string,body:any):Promise<T>{const r=await fetch(`${API}/qlearn${path}`,{method:'POST',headers:{'Content-Type':'application/json',...authHeaders()},credentials:'include',body:JSON.stringify(body)});if(!r.ok)throw new Error(await r.text());return r.json();}
async function get<T>(path:string):Promise<T>{const r=await fetch(`${API}/qlearn${path}`,{headers:authHeaders(),credentials:'include'});if(!r.ok)throw new Error(await r.text());return r.json();}
export const qlearnService={chat:(body:TutorRequest)=>post<TutorResponse>('/ai/chat',body),solve:(body:SolverRequest)=>post<SolverResponse>('/solver/question',body),solveCircuit:(body:any)=>post<SolverResponse>('/solver/circuit',body),verify:(body:any)=>post('/solver/verify',body),explore:(body:ExplorerRequest)=>post<ExplorerResponse>('/explorer/search',body),simulate:(body:any)=>post('/explorer/simulate',body),videos:(topic:string)=>get(`/explorer/videos?topic=${encodeURIComponent(topic)}`),simulations:()=>get('/simulations'),progress:()=>get('/user/progress')};
