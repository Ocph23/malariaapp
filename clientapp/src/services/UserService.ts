
import axios from 'axios';
import type { User } from '@/models';
const url = "/user";

const UserService = {
  get: async (): Promise<User[]> => {
    try {
      const result = await axios.get(url);
      return result.data as unknown as User[];
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  post: async (user: User): Promise<User> => {
    try {
      const result = await axios.post(url, user);
      return result.data as unknown as User;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  delete: async (id: number): Promise<User> => {
    try {
      const result = await axios.delete(`${url}/${id}`);
      return result.data as unknown as User;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
}

export default UserService;
