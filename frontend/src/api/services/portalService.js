import api from "../client";

export const portalService = {
  async getStudentPortal(studentId) {
    const response = await api.get(`/portal/student/${studentId}`);
    return response.data;
  },
};

export default portalService;
