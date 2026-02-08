import type { ZodError } from "zod";

const HelperService = {
  isUseMockMode(): boolean {
    return true;
  },

  greet(name: string): string {
    return `Hello, ${name}!`;
  },

  hitungUmur: (tanggalLahir: Date | undefined): string => {
    if (!tanggalLahir) return '';
    const today = new Date();
    const birthDate = new Date(tanggalLahir);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();

    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return `${age} tahun`;
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



