
const HelperService = {
  isUseMockMode(): boolean {
    return true;
  },

  greet(name: string): string {
    return `Hello, ${name}!`;
  },
};

export default HelperService;



