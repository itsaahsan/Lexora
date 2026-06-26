import type { HTMLAttributes } from "react";
import { cn } from "../../lib/utils";

interface CardProps extends HTMLAttributes<HTMLDivElement> {}

export default function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "glass rounded-xl p-6 transition-all duration-200",
        className
      )}
      {...props}
    />
  );
}
