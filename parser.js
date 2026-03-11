
export const getUrlParams = (url) => {
  const params = {};
  new URLSearchParams(new URL(url).search).forEach((value, key) => {
    params[key] = value;
  });
  return params;
};

