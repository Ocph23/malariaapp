import type { LoginRequest } from "@/models/request";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";

export const MockAuthService = {
  login: async (url: string, data: LoginRequest) => {
    const mock = new MockAdapter(axios);
    mock.onPost(url, data)
      .reply(200,
        {
          "message": "User authenticated successfully",
          "user": {
            "id": 1,
            "username": "admin@app.com",
            "email": "admin@app.com",
            "role": "admin",
          },
          "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJJc3N1ZXIgb2YgdGhlIEpXVCIsImF1ZCI6IkF1ZGllbmNlIHRoYXQgdGhlIEpXVCIsInN1YiI6IlN1YmplY3Qgb2YgdGhlIEpXVCIsIm5iZiI6MTcxODE3MjU1MCwiaWF0IjoxNzE4MTcyNTQwLCJleHAiOjE3MTgyMDg1NDAsImRhdGEiOnsidWlkIjoxLCJ1c2VybmFtZSI6ImFkbWluQGFwcC5jb20iLCJlbWFpbCI6ImFkbWluQGFwcC5jb20iLCJzdGF0dXMiOm51bGx9fQ.VSttc9gDP29K26KwQWCPktKdKd3qUPZBT-TJNJbb3A2_ng16ofstcL6O7PiwHXYLYXs9TOeKwyiSIQJS8-mj8QtcsjZmWstC8gqHJqNdj9ubVxxNp2a8D_PBA43NCKHCPguT_v8ygTQrwRr9WtQcW273MU2sAlcy_SBUSzaBp3A",
        }
      );
  }

}
