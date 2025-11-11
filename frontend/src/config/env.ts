import Constants from 'expo-constants';

type AnyMap = Record<string, unknown>;

const DEFAULT_PORT = process.env.EXPO_PUBLIC_API_PORT ?? '5000';

// Allow explicit override from app.json/app.config via "extra.apiBaseUrl"
const configApiBase =
  ((Constants.expoConfig as unknown as AnyMap)?.['extra'] as AnyMap | undefined)?.[
    'apiBaseUrl'
  ] as string | undefined;

const coerceToUrl = (raw: string) => {
  let candidate = raw.trim();
  if (!candidate) {
    return null;
  }

  if (!/^https?:\/\//i.test(candidate)) {
    candidate = candidate.replace(/^exp:\/\//i, 'http://');
    if (!/^https?:\/\//i.test(candidate)) {
      candidate = `http://${candidate}`;
    }
  }

  try {
    return new URL(candidate);
  } catch {
    return null;
  }
};

const extractHost = (value: unknown) => {
  if (typeof value !== 'string') {
    return null;
  }

  const url = coerceToUrl(value);
  if (!url) {
    return null;
  }

  const host = url.hostname;
  if (!host || host === 'localhost' || host === '127.0.0.1') {
    return null;
  }

  return host;
};

const resolvePotentialHosts = () => {
  const constants = Constants as unknown as AnyMap;
  const expoGoConfig = (constants['expoGoConfig'] ?? {}) as AnyMap;
  const manifest = (constants['manifest'] ?? {}) as AnyMap;
  const manifest2 = (constants['manifest2'] ?? {}) as AnyMap;
  const manifest2Extra = (manifest2['extra'] ?? {}) as AnyMap;
  const manifest2Client = (manifest2Extra['expoClient'] ?? {}) as AnyMap;
  const expoConfig = (Constants.expoConfig ?? {}) as AnyMap;

  return [
    constants['expoGoHostUri'],
    expoGoConfig['hostUri'],
    expoGoConfig['debuggerHost'],
    manifest['hostUri'],
    manifest['debuggerHost'],
    manifest2Client['hostUri'],
    manifest2Client['debuggerHost'],
    expoConfig['hostUri'],
    expoConfig['debuggerHost']
  ];
};

const resolveDefaultHost = () => {
  const resolved = resolvePotentialHosts()
    .map(extractHost)
    .find((value): value is string => Boolean(value));

  if (resolved) {
    return resolved;
  }

  if (Constants.platform?.android) {
    return '10.0.2.2';
  }

  return '127.0.0.1';
};

const resolveDefaultApiBaseUrl = () => `http://${resolveDefaultHost()}:${DEFAULT_PORT}`;

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? configApiBase ?? resolveDefaultApiBaseUrl();

export const env = {
  apiBaseUrl: API_BASE_URL
};

