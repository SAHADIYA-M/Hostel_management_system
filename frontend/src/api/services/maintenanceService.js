import api from "../client";

export const maintenanceService = {
  // Maintenance work orders
  async getAll(params = {}) {
    const response = await api.get("/maintenance", { params });
    return response.data;
  },

  async create(data) {
    const response = await api.post("/maintenance", data);
    return response.data;
  },

  async updateStatus(requestId, status) {
    const response = await api.put(`/maintenance/${requestId}/status`, { status });
    return response.data;
  },

  // Student grievances & complaints
  async getAllComplaints(params = {}) {
    const response = await api.get("/complaints", { params });
    return response.data;
  },

  async createComplaint(data) {
    const response = await api.post("/complaints", data);
    return response.data;
  },

  async updateComplaintStatus(complaintId, status) {
    const response = await api.put(`/complaints/${complaintId}/status`, { status });
    return response.data;
  },
};

export default maintenanceService;
