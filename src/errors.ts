// One place that turns backend and CLI errors into plain sentences with the fix (M7).
// Skeleton: the mapping table is filled in by its issue.

export interface PlainError {
  message: string;
  fix: string;
}

export function plainError(_raw: unknown): PlainError {
  throw new Error("not implemented");
}
