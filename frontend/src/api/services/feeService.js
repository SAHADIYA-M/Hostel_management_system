import api from "../client";

export const feeService = {
  // Fees
  async getFees(params = {}) {
    const response = await api.get("/fees", { params });
    return response.data;
  },

  async createFee(data) {
    const response = await api.post("/fees", data);
    return response.data;
  },

  async updateFeeStatus(feeId, status) {
    const response = await api.put(`/fees/${feeId}/status`, { status });
    return response.data;
  },

  async deleteFee(feeId) {
    const response = await api.delete(`/fees/${feeId}`);
    return response.data;
  },

  // Fines
  async getFines(params = {}) {
    const response = await api.get("/fines", { params });
    return response.data;
  },

  async createFine(data) {
    const response = await api.post("/fines", data);
    return response.data;
  },

  async updateFineStatus(fid, status) {
    const response = await api.put(`/fines/${fid}/status`, { status });
    return response.data;
  },

  async deleteFine(fid) {
    const response = await api.delete(`/fines/${fid}`);
    return response.data;
  },
};

export default feeService;
