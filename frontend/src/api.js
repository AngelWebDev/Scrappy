import { API_URL, headers } from "./config";

export const inviteUser = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/user/invite`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const cancelInviteUser = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/user/cancel-invite`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const updateUser = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/user`, {
    method: "PUT",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const deleteUser = async (uid, csrftoken) => {
  return await fetch(`${API_URL}/office/user`, {
    method: "DELETE",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
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

export const getCustomer = (id, csrftoken) => {
  return fetch(`${API_URL}/office/customer?id=${id}`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  }).then((res) => res.json());
};

export const updateCustomer = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/customer`, {
    method: "PUT",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const deleteCustomer = async (id, csrftoken) => {
  return await fetch(`${API_URL}/office/customer`, {
    method: "DELETE",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify({ id: id }),
  });
};

export const deactiveCustomer = async (cid) => {
  return await fetch(`${API_URL}/office/customer/${cid}/deactive`, {
    method: "PUT",
    headers,
  });
};
