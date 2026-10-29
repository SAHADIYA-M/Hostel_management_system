import api from "../client";

export const messService = {
  async getMessPlans() {
    const response = await api.get("/mess");
    return response.data;
  },

  async createMessPlan(data) {
    const response = await api.post("/mess", data);
    return response.data;
  },

  async deleteMessPlan(id) {
    const response = await api.delete(`/mess/${id}`);
    return response.data;
  },
};

export default messService;
