import type { Diagnosa } from '@/models'
import axios from 'axios'

const url = '/pasien/diagnosa'

const PasienService = {
  diagnosa: async (gejalas: string[]): Promise<Diagnosa> => {
    try {
      const result = await axios.post(url, gejalas)
      return result.data as unknown as Diagnosa
    } catch (err: unknown | Error) {
      return Promise.reject(err)
    }
  },
}

export default PasienService
