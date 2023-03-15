const chatBody = document.querySelector(".chat-body");


const renderUserMessage = () => {
    const userInput = txtInput.value;
    renderMessageEle(userInput, "user");
    txtInput.value = '';
    renderChatbotResponse(userInput);
    secScrollPosition();
}

const renderChatbotResponse = (userInput) => {
    const res = getChatbotResponse(userInput);
    renderMessageEle(res);
}

const renderMessageEle = (txt, type) => {
    let className = "user-message";
    if (type != 'user') {
        if(type == 'acceptability')
            className = "acceptability-agent";
        if(type == 'justification')
            className = "justification-agent";
        if(type == 'debias')
            className = "debias-agent";
    }
    const messageEle = document.createElement("div");
    const txtNode = document.createTextNode(txt);
    messageEle.classList.add(className);
    messageEle.append(txtNode);
    chatBody.append(messageEle);
    chatBody.scrollTop = chatBody.scrollHeight;
}

const getChatbotResponse = (userInput) => {
    return responseObj[userInput] == undefined ? "Please try something else" : responseObj[userInput];
}

const secScrollPosition = () => {
    if (chatBody.scrollHeight > 0) {
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}