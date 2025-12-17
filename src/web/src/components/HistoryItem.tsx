import { useQuery } from "@tanstack/react-query"
import { getThreadIdHistory } from "../utils/cache"
import styled from "styled-components"

export default function HistoryItem(props: {
    current_thread_id: string,
    updateThreadId: (tid: string) => void
}) {

    const { data: history, isPending, error } = useQuery({
        queryKey: ['thread_id_history' + props.current_thread_id],
        queryFn: getThreadIdHistory,
    })

    const is_exists = history && history.includes(props.current_thread_id)
    const history_clone = history || []
    if (!is_exists) {
        history_clone.unshift(props.current_thread_id)
    }
    if (error) {
        return <div>Error: {error.message}</div>
    }
    if (isPending) {
        return <div>Loading...</div>
    }
    return <Box>
        {
            history && history.map((tid) => {
                return <HistoryItemTitle
                    key={tid}
                    className={tid === props.current_thread_id ? 'active' : ''}
                    onClick={() => props.updateThreadId(tid)}>
                    {tid}
                </HistoryItemTitle >
            })
        }

    </Box>
}

const Box = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 20vw;
    background-color: #e7e7e7;
    overflow-y: auto;
`

const HistoryItemTitle = styled.div`
    padding: 10px;
    cursor: pointer;
    &:hover {
        background-color: #d7d7d7;
    }
    &.active {
        background-color: #a8b38f;
    }
`