// Configuración base de la API
const API_URL = "http://localhost:8000";

// Helpers de almacenamiento
const Auth = {
  setToken: (token) => localStorage.setItem("token", token),
  getToken: () => localStorage.getItem("token"),
  setUser: (user) => localStorage.setItem("user", JSON.stringify(user)),
  getUser: () => JSON.parse(localStorage.getItem("user") || "null"),
  setRole: (role) => localStorage.setItem("role", role),
  getRole: () => localStorage.getItem("role") || "comprador",
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");
    window.location.href = "login.html";
  },
  isLoggedIn: () => !!localStorage.getItem("token"),
  requireLogin: () => {
    if (!localStorage.getItem("token")) {
      window.location.href = "login.html";
    }
  }
};

// Cliente API
const api = {
  async request(endpoint, options = {}) {
    const headers = options.headers || {};
    const token = Auth.getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
    if (!options.body || !(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      Auth.logout();
      return null;
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Error desconocido" }));
      throw new Error(error.detail || "Error en la solicitud");
    }

    if (response.status === 204) return null;
    return response.json();
  },

  get(endpoint) { return this.request(endpoint, { method: "GET" }); },
  post(endpoint, data) { return this.request(endpoint, { method: "POST", body: JSON.stringify(data) }); },
  put(endpoint, data) { return this.request(endpoint, { method: "PUT", body: JSON.stringify(data) }); },
  delete(endpoint) { return this.request(endpoint, { method: "DELETE" }); },
  postForm(endpoint, formData) { return this.request(endpoint, { method: "POST", body: formData }); },

  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error al iniciar sesión");
    }
    return response.json();
  }
};