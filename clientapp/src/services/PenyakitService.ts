
import axios, { AxiosError } from 'axios';
import type { Penyakit, MessageError } from '@/models';
const url = "/penyakit";

const PenyakitService = {
  get: async (): Promise<Penyakit[]> => {
    try {
      const result = await axios.get(url);
      return result.data as unknown as Penyakit[];
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  getById: async (id: number): Promise<Penyakit> => {
    try {
      const result = await axios.get(`${url}/${id}`);
      return result.data as unknown as Penyakit;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  post: async (Penyakit: Penyakit): Promise<Penyakit> => {
    try {
      const result = await axios.post(url, Penyakit);
      return result.data as unknown as Penyakit;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  put: async (id: number, Penyakit: Penyakit): Promise<Penyakit> => {
    try {
      const result = await axios.put(`${url}/${id}`, Penyakit);
      return result.data as unknown as Penyakit;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  delete: async (id: number): Promise<Penyakit> => {
    try {
      const result = await axios.delete(`${url}/${id}`);
      return result.data as unknown as Penyakit;
    } catch (err: unknown) {
      const axiosError = err as AxiosError;
      const message = axiosError.response?.data as MessageError
      console.log(message);
      return Promise.reject(err);
    }
  },
}

export default PenyakitService;
