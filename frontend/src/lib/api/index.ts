import axios from 'axios';
import type { AxiosResponse, AxiosError } from 'axios';

// const API_URL = import.meta.env.VITE_API_URL;
const API_URL = 'https://ecsite-api-ikkihkmqma-an.a.run.app/api';
const axiosInstance = axios.create({ baseURL: API_URL });

/**
 * Performs a GET request to the specified URL and returns the response.
 *
 * @template T - The type of the response data expected.
 * @param url - The URL to which the request is made.
 * @param params - An optional object containing URL parameters.
 * @returns - A promise that resolves to the response of the GET request.
 */
const get = async <T>(url: string, { params }: { params?: object } = {}): Promise<AxiosResponse<T>> => {
  const config = {
    params: params,
    withCredentials: true,
    headers: {
      accept: 'application/json',
    },
  };
  const resp = await axiosInstance.get<T>(url, config);
  return resp;
};

/**
 * Performs a POST request to the specified URL with the given data and returns the response.
 *
 * @template T - The type of the response data expected.
 * @param url - The URL to which the request is made.
 * @param data - The data to be sent as the request body.
 * @param params - An optional object containing URL parameters.
 * @param contentType - An optional content type for the request header. Defaults to 'application/json;charset=utf-8' if not provided.
 * @returns - A promise that resolves to the response of the POST request.
 */
const post = async <T>(
  url: string,
  data: object = {},
  { params, contentType }: { params?: object; contentType?: string } = {},
): Promise<AxiosResponse<T>> => {
  const config = {
    params: params,
    withCredentials: true,
    headers: {
      accept: 'application/json',
      'Content-Type': contentType ? contentType : 'application/json;charset=utf-8',
    },
  };
  const resp = await axiosInstance.post<T>(url, data, config);
  return resp;
};

/**
 * Performs a PUT request to the specified URL with the given data and configuration, and returns the response.
 *
 * @template T - The expected type of the response data.
 * @param url - The URL where the PUT request is sent.
 * @param data - The data to be updated, sent in the request body.
 * @param params - Optional parameters to be included in the URL query string.
 * @param contentType - Optional specification for the content type of the request. Defaults to 'application/json;charset=utf-8' if not provided.
 * @returns - A promise that resolves with the response of the PUT request.
 */
const put = async <T>(
  url: string,
  data: object = {},
  { params, contentType }: { params?: object; contentType?: string } = {},
): Promise<AxiosResponse<T>> => {
  const config = {
    params: params,
    withCredentials: true,
    headers: {
      accept: 'application/json',
      'Content-Type': contentType ? contentType : 'application/json;charset=utf-8',
    },
  };
  const resp = await axiosInstance.put<T>(url, data, config);
  return resp;
};

/**
 * Performs a DELETE request to the specified URL and returns the response.
 *
 * @template T - The expected type of the response data.
 * @param url - The URL where the DELETE request is sent.
 * @returns - A promise that resolves with the response of the DELETE request.
 */
const deleteReqest = async <T>(url: string): Promise<AxiosResponse<T>> => {
  const config = {
    withCredentials: true,
    headers: {
      accept: 'application/json',
    },
  };
  const resp = await axiosInstance.delete<T>(url, config);
  return resp;
};

/**
 * Verify if the given error is an Axios error.
 *
 * @param error - The error object to be verified.
 * @returns - A boolean indicating if the error is an Axios error.
 */
const verifyAxiosError = (error: unknown): error is AxiosError => {
  return (error as AxiosError).isAxiosError;
};

const Api = {
  get,
  post,
  put,
  delete: deleteReqest,
  verifyAxiosError,
};

export default Api;
