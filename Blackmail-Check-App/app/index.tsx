import { Text, View } from "react-native";
import { useState, useEffect } from "react";
import { getGroqChatCompletion } from "../scripts/run-model";

export default function Index() {
  // 1. Create a state to hold the model's response
  const [responseText, setResponseText] = useState("Loading response...");

  // 2. Use an effect to fetch the data when the component mounts
  useEffect(() => {
    const fetchResponse = async () => {
      const model_output = await getGroqChatCompletion();
      setResponseText(model_output); // Update the state with the response
    };

    fetchResponse();
  }, []); // The empty array [] means this effect runs only once

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 3. Display the text from the state */}
      <Text>{responseText}</Text>
    </View>
  );
}