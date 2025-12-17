import React from 'react';
import ChatInterface from './components/ChatInterface';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <div className="App">
        <ChatInterface />
      </div>
    </ConfigProvider>
  );
}

export default App;
