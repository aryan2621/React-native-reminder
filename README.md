
# Todo App

A mobile application to create Todo List with Image support.


[![Todo Demo](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fyoutu.be%2FFFQYnk6LRko)](https://youtu.be/FFQYnk6LRko)



## Tech Stack

**Client:** React Native, Zustand, JWt Styled components, Firebase and NativeWinds.

**Server:** Flask, Sql Alchemy and Mysql.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FIRE_BASE_API_S`

`MY_SQL_SERVER`


## Features

- Sign up and Login
- Todos based on individual User
- Crud operation of Todos
- Camera support with Todos
- User Profile


## API Reference

#### Todo

```http
  GET /todos
  POST /todos
  DELETE /deleteTodoById
  PUT /updateTodoById
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `TOKEN` | `string` | **Required** Auth JWT TOKEN |

#### User

```http
  GET /User
  PUT /updateUser
  POST /register
  POST /login
```



## Contributing

Currently I am the sole author of this code, hence if anyone want to contribute contact me at risha2621@gmail.com

