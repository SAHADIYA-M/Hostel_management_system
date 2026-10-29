import api from "../client";

export const studentService = {
  async getAll(params = {}) {
    const response = await api.get("/students", { params });
    return response.data;
  },

  async getById(studentId) {
    const response = await api.get(`/students/${studentId}`);
    return response.data;
  },

  async create(studentData) {
    const response = await api.post("/students", studentData);
    return response.data;
  },

  async allotRoom(studentId, allotData) {
    const response = await api.put(`/students/${studentId}/allot`, allotData);
    return response.data;
  },

  async delete(studentId) {
    const response = await api.delete(`/students/${studentId}`);
    return response.data;
  },

  async updateMessPlan(studentId, messId) {
    // messId = null means unenroll (cancel mess plan)
    const response = await api.patch(`/students/${studentId}/mess`, { mess_id: messId });
    return response.data;
  },
};

export default studentService;
