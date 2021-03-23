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

export const getUsers = async (csrftoken) => {
  return await fetch(`${API_URL}/office/user`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const updateUser = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/user/`, {
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

export const activeUser = async (uid) => {
  return await fetch(`${API_URL}/office/user/${uid}/active`, {
    method: "PUT",
    headers,
  });
};

export const createCustomer = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/customer`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const verifyIdentification = async (data, csrftoken) => {
  return await fetch(`${API_URL}/office/identification`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
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

export const getCustomers = async (csrftoken) => {
  return await fetch(`${API_URL}/office/customer`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
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

export const getMaterial = (id, csrftoken) => {
  return fetch(`${API_URL}/arrival/material?id=${id}`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  }).then((res) => res.json());
};

export const getMaterials = async (csrftoken) => {
  return await fetch(`${API_URL}/arrival/material`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const updateMaterial = async (data, csrftoken) => {
  return await fetch(`${API_URL}/arrival/material`, {
    method: "PUT",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const deleteMaterial = async (id, csrftoken) => {
  return await fetch(`${API_URL}/arrival/material`, {
    method: "DELETE",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify({ id: id }),
  });
};

export const createMaterial = async (data, csrftoken) => {
  return await fetch(`${API_URL}/arrival/material`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const createArrival = async (data, csrftoken) => {
  return await fetch(`${API_URL}/arrival/shipment/`, {
    method: "POST",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify(data),
  });
};

export const getArrivalPosList = async (id, csrftoken) => {
  return await fetch(`${API_URL}/arrival/shipment/?customer_id=${id}`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const deleteArrivalPos = async (id, csrftoken) => {
  return await fetch(`${API_URL}/arrival/arrival_pos/${id}`, {
    method: "DELETE",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const getOpenList = async (csrftoken) => {
  return await fetch(`${API_URL}/payout/open`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const getOpen = (id, csrftoken) => {
  return fetch(`${API_URL}/payout/open/${id}`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  }).then((res) => res.json());
};

export const createPaid = (id, csrftoken) => {
  return fetch(`${API_URL}/payout/open/${id}/`, {
    method: "PUT",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
    body: null,
  }).then((res) => res.json());
};

export const getPaidList = async (csrftoken) => {
  return await fetch(`${API_URL}/payout/paid`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};

export const getPaid = (id, csrftoken) => {
  return fetch(`${API_URL}/payout/paid/${id}/`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  }).then((res) => res.json());
};

export const getReportsData = async (date, csrftoken) => {
  return await fetch(`${API_URL}/payout/report/?date=${date}`, {
    method: "GET",
    headers: {
      ...headers,
      "X-CSRFTOKEN": csrftoken,
    },
  });
};
