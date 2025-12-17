import ChatInterface from './components/ChatInterface';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import localforage from 'localforage';
import { useQuery } from '@tanstack/react-query';
import { newThreadId, selectThreadId } from './utils/cache';
import HistoryItem from './components/HistoryItem';

function App() {
  const { data: tid, isPending, error, refetch } = useQuery({
    queryKey: ['current_thread_id'],
    queryFn: async () => {
      let tid: string | null = await localforage.getItem('current_thread_id')
      if (!tid) tid = await newThreadId();
      return tid;
    },
  });
  async function updateThreadId() {
    await newThreadId();
    refetch();
  }

  async function updateHistory(tid: string) {
    await selectThreadId(tid);
    refetch();
  }

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <ConfigProvider locale={zhCN}>
      <div className="App">
        <HistoryItem updateThreadId={updateHistory} current_thread_id={tid} />
        <ChatInterface current_thread_id={tid} updateThreadId={updateThreadId} />
      </div>
    </ConfigProvider>
  );
}

export default App;
