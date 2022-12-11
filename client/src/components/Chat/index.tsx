import './styles.scss'
import { MainContainer, ChatContainer, ConversationHeader, MessageList, MessageSeparator, Message, TypingIndicator, MessageInput, Button } from '@chatscope/chat-ui-kit-react';
import {  useApi } from '../../hooks/useApi';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowsRotate } from '@fortawesome/free-solid-svg-icons';


export const Chat = () => {
  const { data, post, loading, reset } = useApi(process.env.REACT_APP_API_BASE_URL as string)

  return (
    <div style={{ position: 'relative', height: '100vh' }}>
      <MainContainer>
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Content userName="ChatGPT Playground" />
            <ConversationHeader.Actions>
              <Button disabled={loading} icon={<FontAwesomeIcon icon={faArrowsRotate} />} onClick={reset} />
            </ConversationHeader.Actions>
          </ConversationHeader>
          <MessageList typingIndicator={loading && <TypingIndicator content='ChatGPT is typing'/>}>
          <MessageSeparator as="h2">⚡ Chat history will be gone after refresh</MessageSeparator>
            {data &&
              data.map((conversation: any, i: any) => (
                <Message
                  key={i}
                  model={{
                    message: conversation.message,
                    direction: conversation.sender === 'human' ? "outgoing" : "incoming",
                    position: 'single',
                  }}
                />
              ))}
              
          </MessageList>
          <MessageInput placeholder="Type message here" onSend={(v) => post(v)} attachButton={false} />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};