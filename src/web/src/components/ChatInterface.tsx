import React, { useState, useRef, useEffect } from 'react';
import { Button, Input, Card, Space, Spin, message } from 'antd';
import { SendOutlined, UserOutlined, RobotOutlined } from '@ant-design/icons';
import styled from 'styled-components';
import { end_node, nodeNameTextMap, sendMessageGetSSE } from '../utils/sendMessageGetSSE';
import { v7 } from 'uuid';

const { TextArea } = Input;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 20px;
`;

const MessageBubble = styled.div<{ isUser: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  margin: 8px 0;
  border-radius: 16px;
  background: ${props => props.isUser ? '#1890ff' : '#f0f0f0'};
  color: ${props => props.isUser ? 'white' : 'black'};
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  word-wrap: break-word;
`;

const InputContainer = styled.div`
  display: flex;
  gap: 10px;
  align-items: flex-end;
`;

const StyledTextArea = styled(TextArea)`
  flex: 1;
  resize: none;
`;

interface Message {
    id: string;
    content: string;
    isUser: boolean;
    timestamp: Date;
}

const ChatInterface: React.FC = () => {
    const [threadId, setThreadId] = useState(localStorage.getItem('threadId') || v7());
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);


    useEffect(() => {
        // 自动滚动到底部
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isLoading) return;
        const id = Date.now().toString();
        const userMessage: Message = {
            id: id + "USER",
            content: inputValue,
            isUser: true,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {

            const { connect, disconnect } = sendMessageGetSSE({
                onMessage: (data) => {
                    setMessages(prev => {
                        const id_ai = id + "AI";
                        let currentMsg = prev.find(item => item.id === id_ai)
                        if (!currentMsg) {
                            currentMsg = {
                                id: id_ai,
                                content: "",
                                isUser: false,
                                timestamp: new Date()
                            }
                            prev.push(currentMsg);
                        }

                        if (data.node_name === end_node) {
                            const state = data.snapshot;
                            currentMsg.content = `
                            生成结束：
                            您的角色是：${state.role_inferred}
                            角色评分是（0-1分，数值越大越好）：${state.role_confidence}
                            评判角色的理由是：${state.reason}
                            您想要转换的内容是：${state.transction_content}
                    

                            结果：
                            ${state.result}
                            `
                        } else {
                            currentMsg.content = nodeNameTextMap[data.node_name] || "未知流程"
                        }

                        return [...prev];
                    });
                    console.log(data);
                },
                onError: (error: string) => {
                    setIsLoading(false);
                },
                onComplete: () => {
                    setIsLoading(false);
                    disconnect();
                },
                queryParams: {
                    user_input: inputValue,
                    thread_id: threadId
                },
            })
            connect()
            //   if (!isConnected) {
            //     await connect();
            //   }
            //   await sendMessage(inputValue);
        } catch (error) {
            message.error('发送消息失败');
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <ChatContainer>
            <h1 style={{ textAlign: 'center', marginBottom: 20 }}>AI 对话助手</h1>

            <MessagesContainer>
                {messages.map((message) => (
                    <MessageBubble key={message.id} isUser={message.isUser}>
                        <Space>
                            {message.isUser ? <UserOutlined /> : <RobotOutlined />}
                            <span style={{ whiteSpace: 'pre-line' }}>{message.content}</span>
                        </Space>
                    </MessageBubble>
                ))}
                {/* {isLoading && (
                    <MessageBubble isUser={false}>
                        <Spin size="small" />
                        <span style={{ marginLeft: 8 }}>AI 正在思考...</span>
                    </MessageBubble>
                )} */}
                <div ref={messagesEndRef} />
            </MessagesContainer>

            <InputContainer>
                <StyledTextArea
                    rows={2}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="输入您的问题..."
                    disabled={isLoading}
                />
                <Button
                    type="primary"
                    icon={<SendOutlined />}
                    onClick={handleSendMessage}
                    loading={isLoading}
                    disabled={!inputValue.trim()}
                >
                    发送
                </Button>
            </InputContainer>
        </ChatContainer>
    );
};

export default ChatInterface;