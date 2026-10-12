import api from "../client";

export const authService = {
  async studentLogin(regNo, phone) {
    const response = await api.post("/auth/student-login", {
      reg_no: regNo,
      phone: phone,
    });
    return response.data;
  },

  async wardenLogin(wardenId, phone) {
    const response = await api.post("/auth/warden-login", {
      warden_id: Number(wardenId),
      phone: phone,
    });
    return response.data;
  },

  async logout() {
    try {
      const response = await api.post("/auth/logout");
      return response.data;
    } catch {
      // In case backend is offline, logout continues client-side
      return { status: "logged_out" };
    }
  },
};

export default authService;
