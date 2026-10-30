// Chat view of the session: messages, input, on-screen keyboard, controller focus (M2, M4).
// Skeleton: not mounted anywhere yet.
import { FC } from "react";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "tool";
  text: string;
}

export const ChatView: FC<{ messages: ChatMessage[]; onSend: (text: string) => void }> = () => {
  return null;
};
