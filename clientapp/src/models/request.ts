export interface ResponseRequest {
  success: boolean;
  message: string;
  data: unknown;
  error: unknown;
}

export interface LoginRequest {
  username: string;
  password: string;
}
export interface RegisterRequest {
  nama: string;
  email: string;
  tanggal_lahir: string;
  jenis_kelamin: string;
  nomor_telepon: string;
  alamat: string;
  username: string;
  password: string;
}

export interface HeaderRequest {
  headers: {
    Authorization: string;
  };
}


export interface DiagnosaRequest {
  id: number
  penyakit_id: number
  pasien_id: number
  tanggal_diagnosa: Date
  gejalas: number[]
}


