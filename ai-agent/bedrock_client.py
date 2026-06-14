import boto3
import json

REGION = "us-east-1"

client = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

def invoke_claude(prompt):

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(
        response["body"].read()
    )

    return result["content"][0]["text"]