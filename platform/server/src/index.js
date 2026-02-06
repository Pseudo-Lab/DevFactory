require('dotenv').config();
const express = require('express');
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
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok' });
});

// Register a visit
app.post('/api/stats/visit', async (req, res) => {
    try {
        const { path, userAgent } = req.body;
        // 기존 로그 포맷에 맞춰 method는 'PAGEVIEW'로, referrer는 현재 호스트로 기록
        const referrer = req.headers.referer || '';

        await pool.query(
            'INSERT INTO logging.access_log (path, method, status, user_agent, referrer, ts) VALUES ($1, $2, $3, $4, $5, NOW())',
            [path || '/', 'PAGEVIEW', 200, userAgent, referrer]
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
