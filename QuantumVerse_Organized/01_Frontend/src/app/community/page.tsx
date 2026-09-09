"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Heart, Share2, FlaskConical, Users } from "lucide-react";
import { PageHeader } from "@/components/shared/PageHeader";
import { api } from "@/lib/api";

interface PublicCircuit {
  id: string; name: string; description: string;
  qubits: number; like_count: number; created_at: string;
}

const SORT_OPTS = ["Recent", "Popular"] as const;

export default function CommunityPage() {
  const [circuits, setCircuits] = useState<PublicCircuit[]>([]);
  const [sort, setSort]     = useState<"Recent" | "Popular">("Recent");
  const [liked, setLiked]   = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get(`/community/circuits?sort=${sort.toLowerCase()}`)
      .then(r => {
        const data = r.data;
        setCircuits(data.circuits ?? []);
      })
      .finally(() => setLoading(false));
  }, [sort]);

  async function toggleLike(id: string) {
    if (liked.has(id)) {
      await api.delete(`/community/circuits/${id}/like`);
      setLiked(p => { const n = new Set(p); n.delete(id); return n; });
      setCircuits(cs => cs.map(c => c.id === id ? { ...c, like_count: c.like_count - 1 } : c));
    } else {
      await api.post(`/community/circuits/${id}/like`);
      setLiked(p => new Set([...p, id]));
      setCircuits(cs => cs.map(c => c.id === id ? { ...c, like_count: c.like_count + 1 } : c));
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-8">
        <PageHeader icon={<Users className="w-6 h-6 text-quantum-blue" />}
          title="Community Circuits" subtitle="Explore and remix circuits shared by the community" />
        <div className="flex gap-1 p-1 glass rounded-xl border border-white/5">
          {SORT_OPTS.map(o => (
            <button key={o} onClick={() => setSort(o)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                sort === o ? "bg-quantum-blue/10 text-quantum-blue border border-quantum-blue/20" : "text-muted-foreground hover:text-white"
              }`}>{o}</button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 glass rounded-xl border border-white/5 animate-pulse" />
          ))}
        </div>
      ) : circuits.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          <FlaskConical className="w-12 h-12 mx-auto mb-4 opacity-20" />
          <p>No circuits shared yet. Be the first!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {circuits.map((c, i) => (
            <motion.div key={c.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass rounded-xl border border-white/5 p-5 flex flex-col hover:border-quantum-blue/20 transition-all">
              <div className="flex items-start justify-between mb-3">
                <FlaskConical className="w-5 h-5 text-quantum-blue" />
                <span className="text-xs text-muted-foreground">{c.qubits}q</span>
              </div>
              <h3 className="font-semibold text-white text-sm mb-1 truncate">{c.name}</h3>
              <p className="text-xs text-muted-foreground line-clamp-2 flex-1">{c.description || "No description"}</p>
              <div className="flex items-center justify-between mt-4">
                <button onClick={() => toggleLike(c.id)}
                  className={`flex items-center gap-1.5 text-xs transition-colors ${ liked.has(c.id) ? "text-red-400" : "text-muted-foreground hover:text-red-400" }`}>
                  <Heart className={`w-3.5 h-3.5 ${ liked.has(c.id) ? "fill-current" : "" }`} />
                  {c.like_count}
                </button>
                <button className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-white transition-colors">
                  <Share2 className="w-3.5 h-3.5" /> Open
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
