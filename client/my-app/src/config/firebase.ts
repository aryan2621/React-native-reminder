import { initializeApp, getApp, getApps } from 'firebase/app';
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage';
import ky from 'ky';
import Config from 'react-native-config';

const firebaseConfig = {
    apiKey: Config.API_KEY,
    authDomain: Config.AUTH_DOMAIN,
    projectId: Config.PROJECT_ID,
    storageBucket: Config.STORAGE_BUCKET,
    messagingSenderId: Config.MESSAGING_SENDER_ID,
    appId: Config.APP_ID,
};

let firebaseApp;
if (getApps().length === 0) {
    initializeApp(firebaseConfig);
} else {
    firebaseApp = getApp();
}
const fireStorage = getStorage(firebaseApp);

export const uploadImage = async (fileUri: string) => {
    try {
        const response = await fetch(fileUri);
        const blob = await response.blob();

        const r = storageRef(fireStorage, `images/${blob.size}_${new Date().getTime()}`);
        await uploadBytes(r, blob);
        const downloadURL = await getDownloadURL(r);
        return downloadURL;
    } catch (error) {
        console.log(`Failed to upload image: ${error}`);
        throw error;
    }
};

export const uploadProfile = async (fileUri: string) => {
    try {
        const response = await fetch(fileUri);
        const blob = await response.blob();
        const r = storageRef(fireStorage, `profile/${blob.size}_${new Date().getTime()}`);
        await uploadBytes(r, blob);
        const downloadURL = await getDownloadURL(r);
        return downloadURL;
    } catch (error) {
        console.log(`Failed to upload image: ${error}`);
        throw error;
    }
};

export const fetchImage = async (url: string) => {
    try {
        const blob = await ky.get(url).blob();
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        return new Promise<string>((resolve, reject) => {
            reader.onloadend = () => {
                resolve(reader.result as string);
            };
        });
    } catch (error) {
        console.log(`Failed to fetch image: ${error}`);
        throw error;
    }
};
