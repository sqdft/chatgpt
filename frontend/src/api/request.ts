// eslint-disable-next-line simple-import-sort/imports
import { MessagePlugin } from 'tdesign-vue-next';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store';

const BASE_URL = 'https://chatgpt-backend-wbu0.onrender.com/0x/'; // 后端基础路径

const RequestApi = async (url: string, method = 'GET', body: any = undefined) => {
  const userStore = useUserStore();
  const { token } = userStore;
  const router = useRouter();

  // 拼接基础 URL，确保路径以 /0x/ 开头
  const fullUrl = url.startsWith('http') ? url : `${BASE_URL}${url.replace(/^\//, '')}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `token ${token}` }), // 仅在 token 存在时添加
  };

  try {
    const response = await fetch(fullUrl, {
      method,
      headers: defaultHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    // 调试日志
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