import { create } from 'zustand';
import { persist, devtools, createJSONStorage } from 'zustand/middleware';
import { getAuth, setAuth } from '../storage';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const URL = 'http://192.168.100.9:5000/';

interface AuthStore {
    isLoggedIn: boolean;
    login: () => void;
    logout: () => void;
}
const useAuthStore = create(
    devtools(
        persist<AuthStore>(
            (set) => ({
                isLoggedIn: false,
                login: async () => {
                    const userLocalStorage = await getAuth();
                    if (userLocalStorage) {
                        set({ isLoggedIn: true });
                    }
                },
                logout: async () => {
                    set({ isLoggedIn: false });
                    await setAuth('');
                },
            }),
            {
                name: 'userLoginStatus',
                storage: createJSONStorage(() => AsyncStorage),
            }
        )
    )
);

export default useAuthStore;
