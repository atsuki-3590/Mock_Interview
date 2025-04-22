// 吹き出し用の再利用可能なコンポーネント

function ChatBubble({ type, text }) {
    const styles = {
      question: "bg-blue-100 text-left self-start",
      answer: "bg-green-100 text-right self-end",
      feedback: "bg-yellow-100 text-left self-start text-sm italic"
    };
  
    return (
      <div className={`rounded-xl px-4 py-2 my-1 max-w-[75%] ${styles[type]}`}>
        {text}
      </div>
    );
  }
  
  export default ChatBubble;
  