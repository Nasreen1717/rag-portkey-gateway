import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

from retriever import retrieve_docs, rerank_docs, client as qdrant_client

load_dotenv()

llm = ChatOpenAI(
    model="placeholder",
    api_key="portkey",
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        api_key=os.getenv("PORTKEY_API_KEY"),
        config=os.getenv("PORTKEY_PROD_CONFIG"),
        metadata={"_user": "user_001", "feature": "langgraph", "env": "dev"},
    ),
    max_tokens=1500,
)


class State(TypedDict):
    question: str
    plan: str
    context: str
    sources: list
    answer: str


def planner(state: State) -> dict:
    msg = f"Break this question into one short search query (max 10 words): {state['question']}"
    plan = llm.invoke(msg).content
    print(f"[Planner] {plan}")
    return {"plan": plan}


def retriever(state: State) -> dict:
    query = state["plan"].strip() or state["question"]
    docs = retrieve_docs(query, k=15)
    print(f"[Retriever] Qdrant se {len(docs)} chunks mile")
    top = rerank_docs(state["question"], docs, top_n=5)
    print("[Reranker] top 5:")
    for d in top:
        print(f"  {d['score']} | {d['source']} #{d['chunk']}")
    return {
        "context": "\n".join(d["text"] for d in top),
        "sources": [
            {"source": d["source"], "chunk": d["chunk"], "score": d["score"]}
            for d in top
        ],
    }


def responder(state: State) -> dict:
    msg = (
        f"Context:\n{state['context']}\n\n"
        f"Question: {state['question']}\n\n"
        "Answer in 2 sentences using only the context."
    )
    answer = llm.invoke(msg).content
    print(f"[Responder] {answer}")
    return {"answer": answer}


graph = StateGraph(State)
graph.add_node("planner", planner)
graph.add_node("retriever", retriever)
graph.add_node("responder", responder)
graph.add_edge(START, "planner")
graph.add_edge("planner", "retriever")
graph.add_edge("retriever", "responder")
graph.add_edge("responder", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"question": "What is Portkey used for?"})
    print("\nFINAL ANSWER:", result["answer"])
    print("SOURCES:", result["sources"])
    qdrant_client.close()