require('dotenv').config();
const express = require('express');
const crypto = require('crypto');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// PostgreSQL Connection
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

// Test DB Connection
pool.query('SELECT NOW()', (err, res) => {
    if (err) {
        console.error('Error connecting to the database:', err);
    } else {
        console.log('Connected to PostgreSQL successfully');
    }
});

// API Routes

/**
 * Extracts the client IP address from request headers or connection info.
 */
function getClientIp(req) {
    // Check X-Forwarded-For header (common for reverse proxies)
    const forwardedFor = req.headers['x-forwarded-for'];
    if (forwardedFor) {
        // Can be a comma-separated list; the first one is the original client
        return forwardedFor.split(',')[0].trim();
    }

    // Check X-Real-IP header
    const realIp = req.headers['x-real-ip'];
    if (realIp) {
        return realIp;
    }

    // Fallback to Express req.ip or socket address
    return req.ip || req.socket.remoteAddress;
}

/**
 * Hashes the IP address with a salt, matching the behavior in the cert system.
 */
function hashIp(ip, salt = '') {
    if (!ip) return null;
    return crypto.createHash('sha256').update(salt + ip).digest('hex');
}
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok' });
});

// Register a visit
app.post('/api/stats/visit', async (req, res) => {
    try {
        const { path, userAgent } = req.body;
        const referrer = req.headers.referer || '';

        // Extract client IP and generate hash
        const clientIp = getClientIp(req);
        const ipHash = hashIp(clientIp, process.env.ACCESS_LOGGING_IP_SALT || '');

        await pool.query(
            'INSERT INTO logging.access_log (path, method, status, ip_hash, user_agent, referrer, ts) VALUES ($1, $2, $3, $4, $5, $6, NOW())',
            [path || '/', 'PAGEVIEW', 200, ipHash, userAgent, referrer]
        );
        res.status(201).json({ message: 'Visit logged successfully' });
    } catch (err) {
        console.error('Error logging visit:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get total visit count (filtered by current site if requested)
app.get('/api/stats/count', async (req, res) => {
    try {
        const { site } = req.query;
        let query = 'SELECT COUNT(*) FROM logging.access_log';
        let params = [];

        if (site) {
            query += ' WHERE referrer LIKE $1';
            params.push(`%${site}%`);
        }

        const result = await pool.query(query, params);
        res.json({ count: parseInt(result.rows[0].count) });
    } catch (err) {
        console.error('Error fetching count:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
