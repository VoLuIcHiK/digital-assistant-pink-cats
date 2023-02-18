import React from "react";
import { createChatBotMessage } from "react-chatbot-kit";

import LearningOptions from "./components/LearningOptions/LearningOptions";
import LinkList from "./components/LinkList/LinkList";
import MyButton from "./components/MyButton/MyButton";
import NButton from "./components/NButton/NButton";

const config = {
  botName: "LearningBot",
  initialMessages: [
    createChatBotMessage("Hi, I'm here to help. What do you want to learn?", {
      widget: "learningOptions",
    }),
  ],
  customStyles: {
    botMessageBox: {
      backgroundColor: "#376B7E",
    },
    chatButton: {
      backgroundColor: "#376B7E",
    },
  },
  widgets: [
    {
      widgetName: 'myButton',
      widgetFunc: (props) => <MyButton {...props} />,
      mapStateToProps: ['buttons']
    },
    {
      widgetName: 'nButton',
      widgetFunc: (props) => <NButton {...props} />,
    },
  ],
};

export default config;
