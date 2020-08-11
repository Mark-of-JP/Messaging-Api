
# Everglade Messaging Back-end
Code for the React back-end of the messaging web app. Api Url can be found here [https://everglade-messaging-api.herokuapp.com/](https://everglade-messaging-api.herokuapp.com/). Since it is hosted on Heroku it may take a few seconds to load when you initially attempt to go on the website.

## Websocket Events

### Accepting Events
- join_chats
```
{ chats: [chat uids] }
Puts the user into the rooms associated with the chats
```
- connect_user
```
{ uid: user_uid }
Puts the user into the room associated with the user
```
### Outgoing Events
- confirm
```
{ data: "Connection Made" }
Is called right after the connection has been made
```
- chat_updated
```
{ chat: chat_uid, message: "Summary of what happened", payload: (DICT) "Info associated with event" }
Is called whenever a chat experiences a change
```
- user_updated
```
{ user: user_uid, message: "Summary of what happened", payload: (DICT) "Info associated with event" }
Is called whenever a user experiences a change
```

## RESTful Api Endpoints
Most endpoints requires the **EVERGLADE-USER-TOKEN** header which should contain the JToken received from the login and signup endpoints

### Auth Endpoints

- /login - **POST**
``` 
body: { email, password }
Logs in the user 
```
- /signup - **POST**
```
body: { email, password, display_name }
Signs up a user with the given display_name
```

### User Endpoints

- /users - **POST**
```
body: { users }
Gets the info of all users with the desired uids
users: Should be a list of user uids
```
- /users/me - **GET**
```
Gets the user info of the sign in user
```
- /users/me - **PATCH**
```
body: { new_display_name, description, picture }
Updates the user info
picture: refers to the pictureKey
```
- /users/{user_uid} - **GET**
```
Gets the user info of the user with the uid
```
- /users/{user_uid}/invite - **PUT**
```
Sends a friend request invite to the user
```
- /users/{user_uid}/request - **PUT**
```
Accepts the friend request from the uid user
```
- /users/{user_uid}/request - **DELETE**
```
Declines the friend request from the uid user
```
- /users/{user_uid}/friends - **DELETE**
```
Removes the user from the friends list
```
- /users/{display_name}/name - **GET**
```
Gets the user info of the user with the display name
```

### Chat Endpoints
- /create/chat - **POST**
```
body: { chat_name }
Create a new chat with the chat name and adds the signed in user
```
- /chat/{chat_uid} - **GET**
```
parameters: "message_limit" - max num of messages
Gets the chat info of the desired chat. Info contains formatted messages
```
- /chat/{chat_uid} - **POST**
```
body: { message }
Sends a message to the chat from the signed in user
message: refers to the actual message string
```
- /chat/{chat_uid} - **DELETE**
```
Deletes the chat
```
- /chat/{chat_uid}/simple - **GET**
```
Gets the chat info of the desired chat. Does not contain any message info
```
- /chat/{chat_uid}/invite - **PUT**
```
body: { receiver }
Sends a chat invite to the receiver
receiver: refers to the uid of the user
```
- /chat/{chat_uid}/request - **PUT**
```
The signed in user accepts the chat invite
```
- /chat/{chat_uid}/request - **DELETE**
```
The signed in user declines the chat invite
```
- /chat/{chat_uid}/leave - **DELETE**
```
The signed in user leaves the chat
```

### Message Endpoints
- /message/{message_uid} - **PATCH**
```
body: { edit }
Edits a message's content
edit: refers to the new message string
```
- /message/{message_uid} - **DELETE**
```
Deletes the message
```