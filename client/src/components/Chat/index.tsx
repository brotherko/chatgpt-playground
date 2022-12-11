import './styles.scss';
import {
  MainContainer,
  ChatContainer,
  ConversationHeader,
  MessageList,
  MessageSeparator,
  Message,
  TypingIndicator,
  MessageInput,
  Button,
} from '@chatscope/chat-ui-kit-react';
import { useApi } from '../../hooks/useApi';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowsRotate } from '@fortawesome/free-solid-svg-icons';

const MessageLoading = () => (
  <Message
  model={{
    direction: 'incoming',
    position: 'single',
    type: 'custom',
    payload: <TypingIndicator style={{ position: 'relative' }} />,
  }}
/>
);

export const Chat = () => {
  const { data, post, loading, reset } = useApi(
    process.env.REACT_APP_API_BASE_URL as string
  );

  const messages =
    data &&
    data.map((conversation: any, i: any) => (
      <Message
        key={i}
        model={{
          message: conversation.message,
          direction: conversation.sender === 'human' ? 'outgoing' : 'incoming',
          position: 'single',
        }}
      />
    ));

  return (
    <div style={{ position: 'absolute', height: '100%', width: '100%' }}>
      <MainContainer>
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Content userName="ChatGPT" />
            <ConversationHeader.Actions>
              <Button
                disabled={loading}
                icon={<FontAwesomeIcon icon={faArrowsRotate} />}
                onClick={reset}
              />
            </ConversationHeader.Actions>
          </ConversationHeader>
          <MessageList>
            <MessageSeparator as="h2">
              {/* ⚡ Conversations are logged anonymously for analytical purpose ⚡ */}
              ⚡ Your messages are directly proxied to the OpenAI Server. We don't store any of your conversation in our server ⚡
            </MessageSeparator>
            {messages}
            {loading && <MessageLoading />}
          </MessageList>
          <MessageInput
            placeholder="Type message here"
            onSend={(v) => post(v)}
            attachButton={false}
            onPaste={(e) => e.preventDefault()}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};
