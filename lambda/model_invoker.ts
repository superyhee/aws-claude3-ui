import {
  BedrockRuntimeClient,
  InvokeModelCommand,
  InvokeModelCommandInput,
} from "@aws-sdk/client-bedrock-runtime";
import { Handler } from "aws-lambda";

function convertImageUrls(messages) {
  messages.forEach((message) => {
    if (message.content && typeof message.content !== "string") {
      message.content.forEach((item) => {
        if (item.type === "image_url") {
          const imageUrl = item.image_url.url;
          const base64Image = imageUrl.substring(
            imageUrl.indexOf("{") + 1,
            imageUrl.indexOf("}")
          );
          item.type = "image";
          item.source = {
            type: "base64",
            media_type: "image/jpeg",
            data: base64Image,
          };
          delete item.image_url;
        }
      });
    }
  });
  return messages;
}

export const handler: Handler = async (event, context) => {
  const badResponse = {
    statusCode: 400,
    body: JSON.stringify("Invalid request!"),
  };

  if (event.body && event.body !== "") {
    let body = JSON.parse(event.body);
    if (body.model && body.messages && body.messages.length > 0) {
      const convertedMessages = convertImageUrls(body.messages);
      let max_tokens = body.max_tokens || 1000;
      let top_p = body.top_p || 1;
      let top_k = body.top_k || 250;
      let system = body.system;
      let temperature = body.temperature || 0.5;
      const modelId = "anthropic.claude-3-sonnet-20240229-v1:0";
      const contentType = "application/json";
      const rockerRuntimeClient = new BedrockRuntimeClient({
        region: process.env.REGION,
      });

      const inputCommand: InvokeModelCommandInput = {
        modelId,
        contentType,
        accept: contentType,
        body: system
          ? JSON.stringify({
              anthropic_version: "bedrock-2023-05-31",
              max_tokens: max_tokens,
              temperature: temperature,
              top_k: top_k,
              top_p: top_p,
              system: system,
              messages: convertedMessages,
            })
          : JSON.stringify({
              anthropic_version: "bedrock-2023-05-31",
              max_tokens: max_tokens,
              temperature: temperature,
              top_k: top_k,
              top_p: top_p,
              messages: convertedMessages,
            }),
      };

      const command = new InvokeModelCommand(inputCommand);
      const response = await rockerRuntimeClient.send(command);

      return {
        statusCode: 200,
        headers: {
          "Content-Type": `${contentType}`,
        },
        body: JSON.stringify(
          JSON.parse(new TextDecoder().decode(response.body)),
          null,
          2
        ),
      };
    } else {
      return badResponse;
    }
  } else {
    return badResponse;
  }
};
