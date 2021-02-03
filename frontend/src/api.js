import { API_URL, headers } from "./config";

export const inviteUser = async (data) => {
  return await fetch(`${API_URL}/office/user/invite`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
};

export const updateUser = async (uid, data) => {
  return await fetch(`${API_URL}/office/user/${uid}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(data),
  });
};

export const deleteUser = async (uid) => {
  return await fetch(`${API_URL}/office/user/${uid}`, {
    method: "DELETE",
    headers,
  });
};

export const deactiveUser = async (uid) => {
  return await fetch(`${API_URL}/office/user/${uid}/deactive`, {
    method: "PUT",
    headers,
  });
};
