import localforage from "localforage";
import { v7 } from "uuid";
import { Message } from "../types";

const current_thread_id_name = "current_thread_id"
const current_thread_id_history_name = "current_thread_id_history"
const thread_id_message_history_name = "thread_id_message_history"
export async function newThreadId() {
    const tid = v7()
    await localforage.setItem(current_thread_id_name, tid)
    return tid;
}

export async function selectThreadId(tid: string) {
    return localforage.setItem(current_thread_id_name, tid)
}

export async function saveThreadIdHistory(tid: string) {
    const id_history = await localforage.getItem<Array<string>>(current_thread_id_history_name) || []
    const next = new Set([...id_history, tid])
    await localforage.setItem(current_thread_id_history_name, Array.from(next))
}
export async function getThreadIdHistory() {
    return await localforage.getItem<Array<string>>(current_thread_id_history_name) || []
}

export function savaMessages(thread_id: string, messages: Array<Message>) {
    return localforage.setItem(
        thread_id_message_history_name + thread_id,
        messages
    );
}

export async function getMessages(thread_id: string) {
    return await localforage.getItem(thread_id_message_history_name + thread_id) || []
}