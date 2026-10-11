import api from "../client";

export const attendanceService = {
  async getAttendance(params = {}) {
    const response = await api.get("/attendance", { params });
    return response.data;
  },

  async mark(data) {
    const response = await api.post("/attendance", data);
    return response.data;
  },

  async markBulk(data) {
    const response = await api.post("/attendance/bulk", data);
    return response.data;
  },
};

export default attendanceService;
