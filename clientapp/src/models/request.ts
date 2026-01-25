export interface ResponseRequest {
  success: boolean;
  message: string;
  data: unknown;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface HeaderRequest {
  headers: {
    Authorization: string;
  };
}
