export function SkeletonCard({ lines = 3, className = "" }: { lines?: number; className?: string }) {
  return (
    <div className={`glass rounded-xl border border-white/5 p-5 animate-pulse ${className}`}>
      <div className="h-4 bg-white/5 rounded-full w-3/4 mb-3" />
      {[...Array(lines - 1)].map((_, i) => (
        <div key={i} className={`h-3 bg-white/5 rounded-full mb-2 ${ i === lines - 2 ? "w-1/2" : "w-full" }`} />
      ))}
    </div>
  );
}

export function SkeletonGrid({ count = 6, className = "" }: { count?: number; className?: string }) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 ${className}`}>
      {[...Array(count)].map((_, i) => <SkeletonCard key={i} />)}
    </div>
  );
}
