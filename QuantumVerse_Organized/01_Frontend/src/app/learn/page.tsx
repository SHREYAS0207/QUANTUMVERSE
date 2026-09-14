"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LearnPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/qlearn");
  }, [router]);

  return null;
}
