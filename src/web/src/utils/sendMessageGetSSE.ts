import { useCallback } from 'react';
import qs from 'qs';
type T_NODE_NAME = "role_classifier_agent_node" | "init_state_node" | "end_generate_msg_node" | "product_to_dev_node" | "dev_to_product_node" | "output_node"

interface SSEMessage {
    node_name: T_NODE_NAME
    snapshot: {
        role_inferred: string,
        role_confidence: number,
        transction_content: string,
        result: string,
        reason: string,
    }
}

interface UseSSEOptions {
    onMessage: (data: SSEMessage) => void;
    onError?: (error: string) => void;
    onComplete?: () => void;
    url?: string;
    queryParams?: Record<"user_input" | "thread_id", string>;
}

export const end_node = "output_node"
export const nodeNameTextMap: Record<T_NODE_NAME, string> = {
    "init_state_node": "正在初始化...",
    "role_classifier_agent_node": "正在区分角色.",
    "end_generate_msg_node": "wow! 可能没有区分出来呢...",
    "product_to_dev_node": "正在生成内容...",
    "dev_to_product_node": "正在生成内容...",
    "output_node": "",
}

// 畸形使用的sse，不值得参考哦
export const sendMessageGetSSE = ({
    onMessage,
    onError,
    onComplete,
    queryParams,
    url = 'http://localhost:8000/stream',
}: UseSSEOptions) => {
    let eventSourceRef: EventSource | null = null;

    const connect = async () => {
        if (eventSourceRef) {
            return;
        }

        try {
            const query = qs.stringify(queryParams);
            const eventSource = new EventSource(url + '?' + query);

            eventSource.onerror = (error) => {
                console.error('SSE Error:', error);
                if (onError) {
                    onError('连接失败');
                }
                disconnect();
            };

            eventSource.addEventListener('send', (event) => {
                try {
                    const data = JSON.parse(event.data);
                    onMessage(data);
                } catch (error: Error | any) {
                    console.error('SSE Error:', error);
                    if (onError && error) {
                        onError(error)
                    }
                }
            });

            eventSource.addEventListener('end', () => {
                disconnect();
                if (onComplete) {
                    onComplete();
                }
            });

            eventSourceRef = eventSource;
        } catch (error) {
            console.error('Failed to connect:', error);
            if (onError) {
                onError('连接失败');
            }
        }
    };

    const disconnect = () => {
        if (eventSourceRef) {
            eventSourceRef.close();
            eventSourceRef = null;
        }
    };


    return {
        connect,
        disconnect,
    };
};