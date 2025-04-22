import { useState } from "react";
import { uploadPdf, sendAnswer, getNextQuestion } from "./services/api";
import ChatBubble from "./components/ChatBubble";

function App() {
  const [file, setFile] = useState(null);
  const [qaList, setQaList] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState("");

  const handleUpload = async () => {
    const question = await uploadPdf(file);
    setQaList([{ question, answer: "", feedback: "" }]);
  };

  const handleSendAnswer = async () => {
    const lastQA = qaList[qaList.length - 1];
    const fb = await sendAnswer(lastQA.question, currentAnswer);

    const updated = [...qaList];
    updated[updated.length - 1].answer = currentAnswer;
    updated[updated.length - 1].feedback = fb;

    setQaList(updated);
    setCurrentAnswer("");
  };

  const handleNextQuestion = async () => {
    const question = await getNextQuestion(qaList);
    setQaList([...qaList, { question, answer: "", feedback: "" }]);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">面接練習サイト</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="mt-2 px-4 py-1 bg-blue-500 text-white rounded">
        質問を生成
      </button>

      <div className="mt-6 flex flex-col space-y-2">
        {qaList.map((qa, idx) => (
          <div key={idx}>
            <ChatBubble type="question" text={`Q${idx + 1}: ${qa.question}`} />
            {qa.answer && (
              <ChatBubble type="answer" text={qa.answer} />
            )}
            {qa.feedback && (
              <ChatBubble type="feedback" text={qa.feedback} />
            )}
          </div>
        ))}
      </div>

      {qaList.length > 0 && !qaList[qaList.length - 1].answer && (
        <div className="mt-4">
          <textarea
            value={currentAnswer}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            rows={3}
            className="w-full p-2 border rounded"
            placeholder="回答を入力してください"
          />
          <button
            onClick={handleSendAnswer}
            className="mt-2 px-4 py-1 bg-green-500 text-white rounded"
          >
            回答を送信
          </button>
        </div>
      )}

      {qaList.length > 0 && qaList[qaList.length - 1].answer && (
        <button
          onClick={handleNextQuestion}
          className="mt-4 px-4 py-1 bg-purple-500 text-white rounded"
        >
          次の質問へ
        </button>
      )}
    </div>
  );
}

export default App;
