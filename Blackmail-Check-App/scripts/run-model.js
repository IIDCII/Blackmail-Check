import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

export async function main() {
  const chatCompletion = await getGroqChatCompletion();
  // Print the completion returned by the LLM.
  console.log(chatCompletion.choices[0]?.message?.content || "");
}

export async function getGroqChatCompletion() {
    const output = await groq.chat.completions.create({
    messages: [
      {
        role: "user",
        content: [
            {
                type:"text",
                text:""
            }

        ]  

      },
    ],
    model: "openai/gpt-oss-20b",
  });
  return output
}
