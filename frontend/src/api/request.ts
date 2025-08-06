// frontend/src/api/request.ts
import { MessagePlugin } from 'tdesign-vue-next';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store';

const BASE_URL = 'https://chatgpt-backend-wbu0.onrender.com/0x/';

const RequestApi = async (url: string, method = 'GET', body: any = undefined) => {
  const userStore = useUserStore();
  const { token } = userStore;
  const router = useRouter();

  const fullUrl = url.startsWith('http') ? url : `${BASE_URL}${url.replace(/^\//, '')}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `token ${token}` }),
  };

  try {
    const response = await fetch(fullUrl, {
      method,
      headers: defaultHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    console.log(`Request to ${fullUrl} returned status: ${response.status}`);

    if (response.status === 401 || response.status === 403) {
      MessagePlugin.warning('请先登录');
      router.push({ name: 'login' });
      return new Response();
    }

    if (response.status === 500) {
      MessagePlugin.error('系统异常');
      return new Response();
    }

    if (response.status === 502) {
      MessagePlugin.error('服务未正常启动');
      return new Response();
    }

    return response;
  } catch (error) {
    MessagePlugin.error('网络请求失败');
    console.error('RequestApi error:', error, 'URL:', fullUrl);
    return new Response();
  }
};

export default RequestApi;