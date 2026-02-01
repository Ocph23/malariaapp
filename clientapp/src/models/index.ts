export interface User {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
}

export interface Gejala {
  id: number
  kode: string
  nama: string
  is_active: boolean
}

export interface Aturan {
  id: number
  kode: string
  nama: string
  gejala_id: number
  is_active: boolean
}

export interface Penyakit {
  id: number
  kode: string
  nama: string
  bobot: number
  solusi: string
  aturan: Aturan[]
}

export interface Aturan {
  id: number
  penyakit_id: number
  gejala_id: number
  is_active: boolean
  penyakit: Penyakit
  gejala: Gejala
}

export interface Pasien {
  id: number
  nama: string
  tanggal_lahir: Date
  jenis_kelamin: string
  nomor_telepon: string
  alamat: string
  is_active: boolean
  user_id: number
  user: User
}

export interface Diagnosa {
  id: number
  pasien_id: number
  tanggal_diagnosa: Date
  pasien: Pasien
}

export interface DiagnosaGejala {
  id: number
  diagnosa_id: number
  gejala_id: number
  gejala: Gejala
}

export interface MessageError {
  error: string
  message: string
  detail: string
}
