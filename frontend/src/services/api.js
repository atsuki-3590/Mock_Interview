import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const uploadPdf = async (file) => {
  const formData = new FormData();
  formData.append("pdf", file);

  const res = await axios.post(`${API_BASE}/upload_pdf/`, formData);
  return res.data.question;
};

export const sendAnswer = async (question, answer) => {
  const res = await axios.post(`${API_BASE}/send_answer/`, {
    question,
    answer,
  });
  return res.data.feedback;
};

export const getNextQuestion = async (history) => {
  const res = await axios.post(`${API_BASE}/next_question/`, { history });
  return res.data.question;
};
