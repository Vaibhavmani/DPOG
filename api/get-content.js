/**
 * GET /api/get-content
 * Returns the current content.json from the GitHub repository.
 * The repo is public so no auth token is needed for reading.
 */
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const response = await fetch(
      'https://raw.githubusercontent.com/Vaibhavmani/DPOG/main/content/content.json',
      { headers: { 'Cache-Control': 'no-cache' } }
    );

    if (!response.ok) {
      throw new Error(`GitHub raw fetch failed: ${response.status}`);
    }

    const data = await response.json();

    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json(data);
  } catch (err) {
    return res.status(500).json({ error: 'Failed to load content', detail: String(err) });
  }
}
