class ActionProvider {
  constructor(createChatBotMessage, setStateFunc) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  // new method
  greet() {
    const greetingMessage = this.createChatBotMessage("Hi, friend.");
    this.updateChatbotState(greetingMessage);
  }
	callAPI(message) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    };
    return fetch("http://localhost:8008/api", requestOptions)
      .then((response) => response.json())
      .then((data) => ({
        text: data.text,
        buttons: data.buttons_text.map((buttonText) => ({
          label: buttonText,
        }))
      }));
  }
	
	
  handleSendRequest = (message) => {
    // send a request to the API with the user's message in the request body
    this.callAPI(message).then((data) => {
		console.log(data.buttons);
      // create a new chatbot message with the text and buttons from the API response
      const chatbotMessage = this.createChatBotMessage(data.text, {
		  widget: 'myButton',
		  buttons: data.buttons, // add buttons prop here
		});
      // pass the chatbot message to the ActionProvider's triggerEvent() method
      this.updateChatbotState(chatbotMessage);
    });
  };


	
	
  handleJavascriptList = () => {
    const message = this.createChatBotMessage(
      "Fantastic, I've got the following resources for you on Javascript:",
      {
        widget: "javascriptLinks",
      }
    );

    this.updateChatbotState(message);
  };

  updateChatbotState(message) {
    // NOTICE: This function is set in the constructor, and is passed in from the top level Chatbot component. The setState function here actually manipulates the top level state of the Chatbot, so it's important that we make sure that we preserve the previous state.

    this.setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message],
    }));
  }
	addMessageToState = (message) => {
		this.setState((state) => ({
		  ...state,
		  messages: [...state.messages, message]
		}));
	};
}

export default ActionProvider;
