import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';

export class Task {
    id: string | undefined;
    title: string | undefined;
    description: string | undefined;
    done: boolean | undefined;
    imageUrl: string | undefined;

    constructor(json: Partial<Task>) {
        this.id = json.id || uuidv4();
        this.title = json.title;
        this.description = json.description;
        this.done = json.done || false;
        this.imageUrl = json.imageUrl;
    }
}

export const resetTask = (task: Task) => {
    task.id = uuidv4();
    task.title = '';
    task.description = '';
    task.done = false;
    task.imageUrl = '';
};

export class DBTask {
    id: string | undefined;
    title: string | undefined;
    description: string | undefined;
    done: boolean | undefined;
    imageUrl: string | undefined;
    createdAt: string | undefined;

    constructor(json: Partial<any>) {
        this.id = json.id;
        this.title = json.title;
        this.description = json.description;
        this.done = json.done || false;
        this.imageUrl = json.image_url;
        this.createdAt = json.created_at ?? new Date().toISOString();
    }
}

export class User {
    id: string | undefined;
    name: string | undefined;
    email: string | undefined;
    password: string | undefined;
    confirmPassword: string | undefined;

    constructor(json: Partial<User>) {
        this.id = json.id || uuidv4();
        this.name = json.name;
        this.email = json.email;
        this.password = json.password;
        this.confirmPassword = json.confirmPassword;
    }
}

export const resetUser = (user: User) => {
    user.id = uuidv4();
    user.name = '';
    user.email = '';
    user.password = '';
    user.confirmPassword = '';
};

export class DBUser {
    id: string | undefined;
    name: string | undefined;
    email: string | undefined;
    imageUrl: string | undefined;
    password: string | undefined;
    createdAt: string | undefined;

    constructor(json: Partial<any>) {
        this.id = json.id;
        this.name = json.name;
        this.email = json.email;
        this.password = json.password;
        this.imageUrl = json.image_url;
        this.createdAt = json.created_at ?? new Date().toISOString();
    }
}

export const formatTime = (time: string) => {
    const date = new Date(time);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        timeZone: 'UTC',
    };

    // Format the date
    const formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);
    return formattedDate;
};

export const getFormattedDate = (date: Date, offset: number) => {
    const d = new Date(date);
    const utc = d.getTime() + d.getTimezoneOffset() * 60000;
    const nd = new Date(utc + 3600000 * offset);
    return nd;
};

export const getFormattedTime = (date: Date, offset: number) => {
    const d = new Date(date);
    const utc = d.getTime() + d.getTimezoneOffset() * 60000;
    const nd = new Date(utc + 3600000 * offset);
    return nd;
};
