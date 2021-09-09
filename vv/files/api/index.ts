import Api from "./model";

const api = new Api({
  serverUrl: "http://localhost:8000",
  verbose: true
});

export default api;