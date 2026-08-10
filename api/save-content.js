/**
 * POST /api/save-content
 * Commits the updated content.json to GitHub, which triggers a Vercel auto-redeploy.
 * Requires GITHUB_TOKEN environment variable (set in Vercel project settings).
 */

const OWNER = 'Vaibhavmani';
const REPO  = 'DPOG';
const FILE_PATH = 'content/content.json';
const BRANCH = 'main';
const GH_API = `https://api.github.com/repos/${OWNER}/${REPO}/contents/${FILE_PATH}`;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ status: 'error', message: 'Method not allowed' });
  }

  const token = req.headers['x-github-token'] || process.env.GITHUB_TOKEN;
  if (!token) {
    return res.status(500).json({
      status: 'error',
      message: 'GitHub Access Token is missing. Please set GITHUB_TOKEN in Vercel environment variables OR enter your GitHub Personal Access Token in the Admin Settings field.'
    });
  }

  let newContent;
  try {
    newContent = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  } catch (e) {
    return res.status(400).json({ status: 'error', message: 'Invalid JSON body' });
  }

  if (!newContent || typeof newContent !== 'object' || !newContent.meta || !Array.isArray(newContent.posts)) {
    return res.status(400).json({ status: 'error', message: 'Invalid content structure: missing meta or posts array' });
  }

  // Validate: every post must have equal en/hi instruction counts
  if (newContent.posts && Array.isArray(newContent.posts)) {
    for (const post of newContent.posts) {
      if (!post.en || !post.hi) {
        return res.status(400).json({ status: 'error', message: `Post "${post.slug || post.id}" is missing en or hi object` });
      }
      const enLen = (post.en?.instructions || []).length;
      const hiLen = (post.hi?.instructions || []).length;
      if (enLen !== hiLen) {
        return res.status(400).json({
          status: 'error',
          message: `Instruction count mismatch in post "${post.en?.name}": EN has ${enLen} lines, HI has ${hiLen} lines. They must match.`
        });
      }
    }
  }

  const authHeader = { 
    'Authorization': (token.startsWith('github_pat_') || token.startsWith('ghp_')) ? `Bearer ${token}` : `token ${token}`, 
    'User-Agent': 'DPOG-Admin-Portal' 
  };

  try {
    // Step 1: Get current file SHA (required for the PUT request)
    const shaRes = await fetch(GH_API, { headers: authHeader });
    if (!shaRes.ok) {
      const errData = await shaRes.json().catch(() => ({}));
      throw new Error(`GitHub SHA fetch failed (${shaRes.status}): ${errData.message || shaRes.statusText}`);
    }
    const shaData = await shaRes.json();
    const currentSha = shaData.sha;

    // Step 2: Encode new content as Base64
    const contentJson = JSON.stringify(newContent, null, 2);
    const contentBase64 = Buffer.from(contentJson, 'utf-8').toString('base64');

    // Step 3: Commit the updated file to GitHub
    const commitRes = await fetch(GH_API, {
      method: 'PUT',
      headers: { ...authHeader, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: `Admin update: content.json [${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC]`,
        content: contentBase64,
        sha: currentSha,
        branch: BRANCH
      })
    });

    if (!commitRes.ok) {
      const errData = await commitRes.json().catch(() => ({}));
      throw new Error(`GitHub commit failed (${commitRes.status}): ${errData.message || commitRes.statusText}`);
    }

    const commitData = await commitRes.json();
    const commitSha = commitData.commit?.sha?.slice(0, 7) || 'unknown';

    return res.status(200).json({
      status: 'ok',
      message: `Content committed to GitHub (${commitSha}). Vercel will rebuild the site in ~60 seconds.`,
      gzipped_kb: '~91',
      commit: commitSha
    });

  } catch (err) {
    return res.status(500).json({
      status: 'error',
      message: String(err)
    });
  }
}
