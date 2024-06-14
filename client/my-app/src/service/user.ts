import ky from 'ky';
import { getAuth } from '../storage';
import { URL } from '../store/auth';

const CREATE_REQ = {
    INPUT: {
        NAME: 'name',
        EMAIL: 'email',
        PASSWORD: 'password',
    },
};

export const signUp = (data: any) => {
    try {
        const input = {
            name: data[CREATE_REQ.INPUT.NAME],
            email: data[CREATE_REQ.INPUT.EMAIL],
            password: data[CREATE_REQ.INPUT.PASSWORD],
        };
        return ky
            .post(`${URL}/register`, {
                json: input,
            })
            .json();
    } catch (error) {
        console.log(`Failed to create user: ${error}`);
    }
};
export const signIn = (data: any) => {
    const input = {
        email: data[CREATE_REQ.INPUT.EMAIL],
        password: data[CREATE_REQ.INPUT.PASSWORD],
    };
    return ky
        .post(`${URL}/login`, {
            json: input,
        })
        .json();
};

export const checkToken = (token: string) => {
    try {
        return ky
            .post(`${URL}/check`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .json();
    } catch (error) {
        console.log(`Failed to check token: ${error}`);
    }
};
export const refreshToken = (token: string) => {
    try {
        return ky
            .post(`${URL}/refresh`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .json();
    } catch (error) {
        console.log(`Failed to refresh token: ${error}`);
    }
};

export const getUser = async () => {
    try {
        const token = await getAuth();
        return ky
            .get(`${URL}/user`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .json();
    } catch (error) {
        console.log(`Failed to fetch users: ${error}`);
    }
};

export const updateUser = async (image_url: string) => {
    try {
        const token = await getAuth();
        return ky
            .put(`${URL}/update_user`, {
                json: {
                    image_url: image_url,
                },
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .json();
    } catch (error) {
        console.log(`Failed to update user: ${error}`);
    }
};
