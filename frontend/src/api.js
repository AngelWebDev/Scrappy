import { API_URL, headers } from "./config";

export const inviteUser = async (data) => {
  return await fetch(`${API_URL}/office/user/invite`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
};

export const updateUser = async (uid, data) => {
  return await fetch(`${API_URL}/office/user`, {
    method: "PUT",
    headers,
    body: JSON.stringify(data),
  });
};

export const deleteUser = async (uid) => {
  return await fetch(`${API_URL}/office/user`, {
    method: "DELETE",
    headers,
    body: JSON.stringify({ id: uid }),
  });
};

export const deactiveUser = async (uid) => {
  return await fetch(`${API_URL}/office/user/${uid}/deactive`, {
    method: "PUT",
    headers,
  });
};

export const createCustomer = async (data) => {
  return await fetch(`${API_URL}/office/customer`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
};

export const updateCustomer = async (cid, data) => {
  return await fetch(`${API_URL}/office/customer/${cid}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(data),
  });
};

export const deactiveCustomer = async (cid) => {
  return await fetch(`${API_URL}/office/customer/${cid}/deactive`, {
    method: "PUT",
    headers,
  });
};
