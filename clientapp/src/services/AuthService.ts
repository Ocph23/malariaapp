import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import type { HeaderRequest, LoginRequest } from '@/models/request';
import type { User } from '@/models';
import HelperService from './HelperService';
import { MockAuthService } from './mocks/MockAuthService';

const AuthService = {
  login: async (loginRequest: LoginRequest): Promise<User> => {
    try {
      const url = "/api/login";
      if (HelperService.isUseMockMode()) {
        await MockAuthService.login(url, loginRequest);
      }
      const result = await axios.post(url, loginRequest);
      if (result) {
        const auth = useAuthStore();
        await auth.setAuthResponse(result.data);
      }
      return result as unknown as User;
    } catch (err: unknown | Error) {
      return Promise.reject(err);
    }
  },
  getHeader: (): HeaderRequest => {
    const auth = useAuthStore();
    const token = auth.getToken();
    return {
      headers: {
        'Authorization': 'bearer ' + token
      }
    } as HeaderRequest
  },

  isLogin: async (): Promise<boolean> => {
    const auth = useAuthStore();
    return auth.isLogin();
  },

  logout: async (): Promise<void> => {
    const auth = useAuthStore();
    auth.logout();
  },

}


export default AuthService;
