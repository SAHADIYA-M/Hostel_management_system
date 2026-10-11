import api from "../client";

export const hostelService = {
  async getAll() {
    const response = await api.get("/hostels");
    return response.data;
  },

  async getStaff(hostelId) {
    const response = await api.get(`/hostels/${hostelId}/staff`);
    return response.data;
  },

  async getRooms(params = {}) {
    const response = await api.get("/rooms", { params });
    return response.data;
  },

  async createRoom(roomData) {
    const response = await api.post("/rooms", roomData);
    return response.data;
  },
};

export default hostelService;
