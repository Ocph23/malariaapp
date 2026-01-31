import type { User } from ".";

export interface AuthResponse { token: string | null, user: User }
