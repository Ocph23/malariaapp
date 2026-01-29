
import axios, { AxiosError } from 'axios';
import type { Gejala, MessageError } from '@/models';
const url = "/gejala";

const GejalaService = {
  get: async (): Promise<Gejala[]> => {
    try {
      const result = await axios.get(url);
      return result.data as unknown as Gejala[];
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  post: async (Gejala: Gejala): Promise<Gejala> => {
    try {
      const result = await axios.post(url, Gejala);
      return result.data as unknown as Gejala;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  put: async (id: number, Gejala: Gejala): Promise<Gejala> => {
    try {
      const result = await axios.put(`${url}/${id}`, Gejala);
      return result.data as unknown as Gejala;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  delete: async (id: number): Promise<Gejala> => {
    try {
      const result = await axios.delete(`${url}/${id}`);
      return result.data as unknown as Gejala;
    } catch (err: unknown) {
      const axiosError = err as AxiosError;
      const message = axiosError.response?.data as MessageError
      console.log(message);
      return Promise.reject(err);
    }
  },
}

export default GejalaService;
