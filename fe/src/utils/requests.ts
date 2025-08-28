import { API_ENDPOINTS, DEV_OPTIONS } from '@/constants'
import type { Service, ServiceOverview } from '@/stores/serviceStore'

const fetchWithAuth = async (
  url: string,
  payload: RequestInit = {},
) => {
  const headers = {
    'Content-Type': 'application/json',
    ...payload.headers,
  };

  const res = await fetch(url, {
    ...payload,
    headers,
    credentials: "include"
  });
  return res;
}

const requestListOfServices = async (): Promise<ServiceOverview[]> => {

  if (DEV_OPTIONS.stubModeOn) {
    const res = await fetch(DEV_OPTIONS.stubServicesPath);
    const servicesList = await res.json();
    return servicesList;
  }

  const res = await fetchWithAuth(
    API_ENDPOINTS.services,
    {
      method: 'GET',
    }
  )
  if (!res.ok) {
    throw new Error(`Failed to fetch services: ${res.statusText}`);
  }
  const obj = await res.json()
  return obj.data
};

const requestRandomPictureUrl = async () => {
  
  const thumbnailRes = await fetch('https://picsum.photos/400/200');

  if(!thumbnailRes.ok) {
    throw Error("Could not obtain an url for a random picture")
  }
  return thumbnailRes.url;
}

const requestServiceInfoById = async (serviceId: string): Promise<Service> => {

  if (DEV_OPTIONS.stubModeOn) {
    const response = await fetch(DEV_OPTIONS.stubServicesPath);
    const servicesList = await response.json();

    const candidate = servicesList.find((item: Service) => item.id.toString() == serviceId)

    if (candidate) {
      return candidate
    }
    throw new Error(`Service with id '${serviceId}' not found in stub data`);
  }

  const res = await fetchWithAuth(
    `${API_ENDPOINTS.services}/${serviceId}`,
    {
      method: 'GET',
    }
  )
  if (!res.ok) {
    throw new Error(`Failed to fetch service with id '${serviceId}': ${res.statusText}`);
  }
  const obj = await res.json()
  return obj.data;
};

const requestOperationByServiceId = async (
  serviceId: string,
  payload: JSON) => {

  if (DEV_OPTIONS.stubModeOn) {
    const response = await fetch(DEV_OPTIONS.stubServicesPath);
    const servicesList = await response.json();
    const candidate = servicesList.find((item: Service) => item.id.toString() == serviceId)
    if (candidate) {
      return {
        'message': 'Success!',
      }
    }
    throw new Error(`Service with id '${serviceId}' not found in stub data`);
  }

  const res = await fetchWithAuth(
    `${API_ENDPOINTS.services}/${serviceId}`,
    {
      method: 'POST',
      body: JSON.stringify(payload),
    },
  )
  if (!res.ok) {
    throw Error(`Request to service ${serviceId} was unsuccesful: ${res.statusText}`)
  }
  const obj = await res.json()
  return obj.data;
};

const requestThisUser = async () => {
  const res = await fetchWithAuth(API_ENDPOINTS.thisUser)
  if (!res.ok) {
    throw Error(`Cannot fetch this user ${res.statusText}`)
  }
  const user = await res.json();
  return user
}

const login = () => {
  if (DEV_OPTIONS.stubModeOn) {
    return;
  }
  window.location.href = `${API_ENDPOINTS.loginWithGitHub}?next_url=http://localhost:3000/login/callback`;
}

const logout = () => {
  localStorage.setItem("expAPI_isLoggedIn", 'false');

  if (DEV_OPTIONS.stubModeOn) {
    return;
  }
  window.location.href = `${API_ENDPOINTS.logout}?next_url=http://localhost:3000/`;
}

const isAuthenticated = () => {
  if (DEV_OPTIONS.stubModeOn) {
    return true
  }
  const storedVar = localStorage.getItem("expAPI_isLoggedIn") === 'true'
  return storedVar
}

export const requests = {
  requestListOfServices,
  requestRandomPictureUrl,
  requestServiceInfoById,
  requestOperationByServiceId,
  requestThisUser,
  login,
  logout,
  isAuthenticated
};