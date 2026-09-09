import type { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({ icon: Icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="glass rounded-xl border border-white/5 flex flex-col items-center justify-center py-16 px-8 text-center">
      <Icon className="w-12 h-12 text-muted-foreground/20 mb-4" />
      <p className="text-white font-medium mb-1">{title}</p>
      {description && <p className="text-xs text-muted-foreground">{description}</p>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
