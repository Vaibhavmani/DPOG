/**
 * Vercel Edge Middleware — HTTP Basic Auth gate for internal-only routes.
 *
 * Protected routes:
 *   /dp-c9f7e2/   (duty shift compliance tool)
 *   /dp-q3b8a1/   (QR card reference)
 *
 * Set DP_INTERNAL_PASSWORD in Vercel project environment variables.
 * Never hardcode a password here.
 *
 * Usage at the door:
 *   curl -u "dp:YOUR_PASSWORD" https://your-domain.vercel.app/dp-c9f7e2/
 */

export const config = {
  matcher: [
    '/dp-c9f7e2/:path*',
    '/dp-q3b8a1/:path*',
    '/admin/:path*',
    '/api/save-content'
  ],
};

function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

export default function middleware(request) {
  const authHeader = request.headers.get('authorization') || '';
  const [scheme, encoded] = authHeader.split(' ');

  if (scheme && scheme.toLowerCase() === 'basic' && encoded) {
    let decoded = '';
    try {
      decoded = atob(encoded);
    } catch {
      // invalid base64 encoding
    }
    const colonIdx = decoded.indexOf(':');
    const user = decoded.substring(0, colonIdx);
    const pass = decoded.substring(colonIdx + 1);

    const envPass = process.env.DP_INTERNAL_PASSWORD;
    if (envPass) {
      const validUser = (user === 'admin' || user === 'dp');
      const validPass = timingSafeEqual(pass, envPass);

      if (validUser && validPass) {
        // Authenticated — proceed cleanly
        return;
      }
    }
  }

  // Not authenticated — return 401 with WWW-Authenticate challenge
  return new Response(
    '<!DOCTYPE html><html><head><title>401 Unauthorized</title></head>' +
    '<body style="font-family:sans-serif;text-align:center;padding:60px">' +
    '<h1>401 Unauthorized</h1>' +
    '<p>Authentication required. Contact the duty officer for access credentials.</p>' +
    '</body></html>',
    {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Delhi Police Internal"',
        'Content-Type': 'text/html; charset=utf-8',
      },
    }
  );
}

