import type { Diagnosa, DiagnosaResponse, RiwayatDiagnosa } from '@/models'
import type { DiagnosaRequest } from '@/models/request'
import axios from 'axios'

const url = '/pasien'

const PasienService = {
  diagnosa: async (gejalas: { kode: string, jawaban: string }[]): Promise<DiagnosaResponse[]> => {
    try {
      const result = await axios.post(`${url}/diagnosa`, gejalas)
      return result.data as unknown as DiagnosaResponse[]
    } catch (err: unknown | Error) {
      return Promise.reject(err)
    }
  },

  saveDiagnosa: async (diagnosa: DiagnosaRequest): Promise<Diagnosa> => {
    try {
      const result = await axios.post(`${url}/savediagnosa`, diagnosa)
      return result.data as unknown as Diagnosa
    } catch (err: unknown | Error) {
      return Promise.reject(err)
    }
  },
  riwayat: async (): Promise<RiwayatDiagnosa[]> => {
    try {
      const result = await axios.get(`${url}/riwayat`)
      return result.data as unknown as RiwayatDiagnosa[]
    } catch (err: unknown | Error) {
      return Promise.reject(err)
    }
  },



}

export default PasienService
