import AsyncStorage from '@react-native-async-storage/async-storage';

export const setAuth = async (auth: string | undefined) => {
    try {
        if (!auth) {
            return;
        }
        await AsyncStorage.setItem('auth', auth);
    } catch (error) {
        console.log(`Error while setting auth: ${error}`);
    }
};

export const getAuth = async () => {
    try {
        return (await AsyncStorage.getItem('auth')) || '';
    } catch (error) {
        console.log(`Error while getting auth: ${error}`);
        return '';
    }
};
