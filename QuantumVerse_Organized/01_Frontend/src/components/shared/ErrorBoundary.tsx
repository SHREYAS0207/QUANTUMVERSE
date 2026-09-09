"use client";
import React, { Component, ReactNode } from "react";

interface Props { children: ReactNode; fallback?: ReactNode; }
interface State { hasError: boolean; error?: Error; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="p-6 text-center text-muted-foreground">
          <p className="text-2xl mb-2">⚠️</p>
          <p className="text-sm">{this.state.error?.message ?? "Something went wrong."}</p>
          <button onClick={() => this.setState({ hasError: false })}
            className="mt-3 text-xs text-quantum-blue hover:underline">Try again</button>
        </div>
      );
    }
    return this.props.children;
  }
}
