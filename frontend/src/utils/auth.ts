export const getCsrfToken = async () => {
  const response = await fetch('/api/csrf/', {
    method: 'GET',
    credentials: 'include',
  });
  const data = await response.json();
  return data.csrfToken;
};