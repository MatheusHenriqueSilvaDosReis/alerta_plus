import { Platform } from "react-native";

const DEFAULT_NATIVE_API_URL = "http://192.168.1.82:8000";

// No navegador (build unificado / Render), usa a mesma origem ("").
// Em apps nativos, usa EXPO_PUBLIC_API_URL se definida ou o IP local padrão.
export const API_URL =
  process.env.EXPO_PUBLIC_API_URL ??
  (Platform.OS === "web" ? "" : DEFAULT_NATIVE_API_URL);
