import Groq from "groq-sdk";

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

export async function getGroqChatCompletion() {
    const imageurl = "none";
    const output = await groq.chat.completions.create({
    messages: [
      {
        role: "user",
        content: [
            {
                type:"text",
                text:"You are a cyber security expert. You need to look at images and identify all of the images that are vulnerable to blackmail attacks. So images like passwords, nudity, nsfw, confidential/personal data and more. You have to respond with the first token being the vulnerability rating {NONE,LOW,MEDIUM,HIGH} then following up with an explanation (max 400 tokens)"
            },
            // {
            //   type:"",
            //   image_url:{
            //     url: imageurl
            //   }
            // },
        ]  
      },
    ],
    model: "meta-llama/llama-4-scout-17b-16e-instruct",
    temperature: 1,
    max_completion_tokens:500,
  });
  return chatCompletion.choices[0].message.content;
}
