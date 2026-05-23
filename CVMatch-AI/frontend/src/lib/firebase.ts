// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDNiJM0i7D5ln-Ss072aUncB5bS1gHXb0k",
  authDomain: "cv-scoring-8aae1.firebaseapp.com",
  projectId: "cv-scoring-8aae1",
  storageBucket: "cv-scoring-8aae1.firebasestorage.app",
  messagingSenderId: "155063609392",
  appId: "1:155063609392:web:a591996eeb0b2bc1a925f5",
  measurementId: "G-VLWS7F3JPX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const analytics = typeof window !== "undefined" ? getAnalytics(app) : null;
export default app;
