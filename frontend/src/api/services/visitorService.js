import api from "../client";

export const visitorService = {
  async getVisitors() {
    const response = await api.get("/visitors");
    return response.data;
  },

  async createVisitor(data) {
    const response = await api.post("/visitors", data);
    return response.data;
  },

  async getVisits(params = {}) {
    const response = await api.get("/visits", { params });
    return response.data;
  },

  async createVisit(data) {
    const response = await api.post("/visits", data);
    return response.data;
  },
};

export default visitorService;
