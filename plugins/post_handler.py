import json
import requests

def process_message(message):
    """
    Processes an incoming message from the user.
    
    Args:
        message (dict): The message payload.
        
    Returns:
        dict: A response payload to send back.
    """
    try:
        user_id = message.get("user_id")
        text = message.get("text", "").strip().lower()

        # Example response logic
        if text == "hello":
            response_text = "Hi there! How can I assist you today?"
        elif text == "bye":
            response_text = "Goodbye! Have a great day!"
        else:
            response_text = f"I'm sorry, I didn't understand: {text}"
        
        return {
            "user_id": user_id,
            "response": response_text
        }
    except Exception as e:
        print(f"Error processing message: {e}")
        return {"error": "Failed to process message"}

def handle_event(event_type, data):
    """
    Handles different types of bot events.
    
    Args:
        event_type (str): The type of event.
        data (dict): The event payload.
        
    Returns:
        str: A status message about the event.
    """
    try:
        if event_type == "message":
            return f"Message received: {data.get('text')}"
        elif event_type == "join":
            return f"User joined: {data.get('user_id')}"
        elif event_type == "leave":
            return f"User left: {data.get('user_id')}"
        else:
            return "Unknown event type"
    except Exception as e:
        print(f"Error handling event: {e}")
        return "Failed to handle event"

def send_to_api(data, api_url):
    """
    Sends data to an external API.
    
    Args:
        data (dict): The payload to send.
        api_url (str): The API endpoint URL.
        
    Returns:
        dict: The API response.
    """
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to API: {e}")
        return {"error": "Failed to send data"}

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Simulate processing a user message
    test_message = {"user_id": "12345", "text": "hello"}
    print(process_message(test_message))

    # Simulate handling a bot event
    test_event = {"type": "message", "text": "This is a test event"}
    print(handle_event(test_event["type"], test_event))

    # Simulate sending data to an API
    test_data = {"message": "Test API call"}
    api_endpoint = "https://example.com/api"
    print(send_to_api(test_data, api_endpoint))
  
