import type { ZodError } from "zod";

const HelperService = {
  isUseMockMode(): boolean {
    return true;
  },

  greet(name: string): string {
    return `Hello, ${name}!`;
  },


  mapZodErrors(error: ZodError) {
    const errors: Record<string, string> = {}
    error.issues.forEach((e) => {
      const key = e.path[0] as string
      errors[key] = e.message
    })
    return errors
  }
};

export default HelperService;



